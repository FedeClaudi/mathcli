from sympy.parsing.sympy_parser import parse_expr
from sympy import latex, lambdify, Derivative, preview, Eq
from sympy.parsing.sympy_parser import (
    function_exponentiation,
    standard_transformations,
    implicit_application,
    implicit_multiplication_application,
    convert_equals_signs,
)
from sympy import simplify as simp
from sympy.parsing.latex import parse_latex

from loguru import logger

from .errors import DerivativeArgumentsNumberError, ArgumentsNumberError
from ._utils import is_number
from mathcli import _unicode


def clean(expr):
    """
        cleans up an expression string

        Arguments:
            expr: string, expression
    """
    expr = expr.replace("^", "**")
    return expr


def parse(expr, evaluate=True):
    """ wraps around sympy.parse_expr to give more control and add transformations
    
        Arguments:
            expr: string, expression
            evaluate: bool. If true it evaluates the parsed expression. 
    """
    if not isinstance(expr, str):
        return expr

    transformations = standard_transformations + (
        function_exponentiation,
        implicit_multiplication_application,
        implicit_application,
        convert_equals_signs,
    )

    try:
        return parse_expr(
            expr, transformations=transformations, evaluate=evaluate
        )
    except SyntaxError as e:
        raise ValueError(f"Failed to parse expression: {expr}: {e}")


# ---------------------------------------------------------------------------- #
#                               ExpressionString                               #
# ---------------------------------------------------------------------------- #


class ExpressionString(object):
    operators = "−−+-"
    symbols = "−-+*:_|√-−"
    operator_names = ("sin", "cos", "tan", "atan", "sqrt", "log", "exp")
    parentheses = "(){}"

    def __init__(self, expression):
        """
            Handles string manipulation of expression strings (e.g. highlighting)
        """
        self.string = clean(expression)
        self.expression = None
        self.result = ""
        self.variables = []

    def __str__(self):
        return self.unicode

    def __repr__(self):
        return self.unicode

    def __rich__(self):
        return self.unicode

    # def __rich_console__(self, *args):
    #     yield self.unicode

    @classmethod
    def from_latex(cls, latex_expression):
        """
            Parses an expression given by a string with
            latex format and creates a new instance of Expression for it
        """
        return cls(parse_latex(latex_expression))

    @property
    def latex(self):
        """
            Convert expression to latex syntax
        """
        if self.expression is None:
            expr = parse(self.string, evaluate=False)
        else:
            expr = self.expression
        return "$$" + latex(expr) + "$$"

    @property
    def unicode(self):
        """
            Convert the latex form of the expression to unicode symbols,
            see: https://github.com/svenkreiss/unicodeit
        """
        if not self.is_eq:
            ltx = _unicode.clean_latex(latex(self.expression))
        else:
            ltx = (
                _unicode.clean_latex(latex(self.expression.lhs))
                + "="
                + _unicode.clean_latex(latex(self.expression.rhs))
            )

        if self.is_derivative:
            # clean up the latex for derivative expressions
            delta, expr = ltx.split("}(")
            ltx = delta + "}" + expr[:-1]

        # parse exponentials
        ltx = _unicode.parse_exponents(ltx)

        # split based on latex's \\frac and clean them up
        out = []
        for frac in ltx.split("\\frac"):
            if not frac:
                continue
            if "}{" in frac:
                out.append(_unicode.parse_frac(frac))
            else:
                out.append(_unicode.to_unicode(frac))

        if self.is_derivative:
            out[0] = _unicode.parse_derivation(
                out[0]
            )  # clean up derivation symbols

        if self.is_eq:
            l, r = "".join(out).split("=")
            out = [l + "="]

            r = _unicode.replace_in_string(r, r.find("("), "")
            r = _unicode.replace_in_string(r, r.rfind(")"), "")
            out.append(r)
        out = "".join(out).replace("  ", " ")

        logger.log(
            "EXPRESSION", "To  UNICODE: " + out,
        )

        return out

    def to_image(self, filepath, transparent_bg=False):
        """
            Save the expression as rendered latex to an image file.

            Arguments:
                filepath: str, Path. Path to where the image file will be saved
                transparent_bg: bool. If true the image will have a transparent background
        """
        options = ["-T", "tight", "-z", "0", "--truecolor", "-D 1200"]
        if transparent_bg:
            options.extend(["-bg", "Transparent"])

        preview(
            self.latex,
            viewer="file",
            filename=filepath,
            euler=False,
            dvioptions=options,
        )

        logger.log("EXPRESSION", f"saved image to file: {filepath}")
        print(f"Saved equation to image [{filepath}]")


# ---------------------------------------------------------------------------- #
#                                  Expression                                  #
# ---------------------------------------------------------------------------- #


class Expression(ExpressionString):
    def __init__(self, expression):
        """
            Class representing a mathematical expression.
            It takes a string representation of an expression, like:
                '3x + log(y) - sqrt 10 + cos pi'
            and creates a sympy expression from it. 
            It can then solve the expression, take derivatives etc..
        """
        ExpressionString.__init__(self, str(expression))

        # parse and evaluate
        if isinstance(expression, str):
            self.expression = parse(self.string, evaluate=False)
        else:
            self.expression = expression

        # check if expression is derivative
        self.is_derivative = isinstance(self.expression, Derivative)
        self.is_eq = isinstance(self.expression, Eq)

        logger.log(
            "EXPRESSION",
            f"\nCreated: {self.unicode} from string {expression}.\nIs derivative: {self.is_derivative}\nIs eq: {self.is_eq}",
        )
        self.eval()

        # get variabls in the expression
        self.get_variables()

    def derivative(self, wrt):
        """
            Take the derivative of the expression.
            If 0 or 1 variables are present, no need to pass any other argument.
            If >1 variables are present the user must specify which variables to
            take the derivative for by passing a variable number of string arguments
            For more information about derivatives: https://docs.sympy.org/latest/tutorial/calculus.html

            Arguments:
                wrt: str. Variable number of variables name or ints for derivative order

            Returns:
                a new Expression representing the derivative. 

            Raises:
                DerivativeArgumentsNumberError if the number of variable >2 and wrt is not specified
        """
        logger.log("EXPRESSION", f"{self} - derivative. Wrt: {wrt}")
        wrt = wrt or ""

        try:
            expr = Expression(
                str(Derivative(self.expression, *wrt, evaluate=False))
            )
        except ValueError:
            raise DerivativeArgumentsNumberError(self, wrt)

        return expr

    def simplify(self):
        """
            Simplify the expression, returns a  new instance of Expression
            For more information about simplification: https://docs.sympy.org/latest/tutorial/simplification.html
        """
        logger.log("EXPRESSION", (f"{self} - simplify"))
        return Expression(str(simp(self.expression)))

    def eval(self):
        """
            Evaluate the expression.
            If expression is numerical it can be solved completely and
            self.value is a number, otherwise self.value is a symbolic
            expression and the expression can be fully solved only
            when the values for the variables are passed.
        """
        try:
            self.value = self.expression.evalf()
        except TypeError:
            self.value = "couldnt evalf"

        if is_number(self.value):
            # numeric expression completely evalued
            self.is_solved = True
        else:
            # it's a symbolic expression, will need to be value
            self.is_solved = False

    def calc(self, **values):
        """
            If self.eval didn't yield a number, then we have
            a symbolic expression whose value needs to be calculated given the values
            of it's variables.
            For more information: https://docs.sympy.org/latest/modules/solvers/solveset.html

            Arguments:
                values: variable number of kwargs with variables values (e.g. x=1, y=2)

            Returns:
                float: the value we got from solving the equation

            Raises:
                ArgumentsNumberError: if the number of variable values specified doesn't match
                    the number of values in the expression.
        """
        logger.log("EXPRESSION", f"{self} - solve. Values: {values}")

        # Check that we have the correct number of variables
        if len(values) != self.n_variables:
            raise ArgumentsNumberError(self, **values)

        # turn the expression into a lambda function
        # but first check if its a derivative
        if self.is_derivative:
            expression = self.expression.doit()
        else:
            expression = self.expression

        try:
            lambda_function = lambdify(
                self.variables, expression, modules="numpy"
            )
        except (SyntaxError, NameError) as e:
            logger.warn(
                f'Failed to lambdify expression "{self}" with error: {e}'
            )
            return None

        # sort the values
        try:
            vals = [values[str(var)] for var in self.variables]
        except KeyError:
            raise ArgumentsNumberError(self, **values)

        # compute
        return lambda_function(*vals)

    def get_variables(self):
        """
            Gets the name and number of variables
            in the expression.
        """
        if self.is_derivative:
            atoms = self.expression.doit().atoms()
        else:
            atoms = self.expression.atoms()

        self.variables = [x for x in list(atoms) if not is_number(x)]
        self.n_variables = len(self.variables)


def to_sympy(expression):
    return Expression(expression).expression
