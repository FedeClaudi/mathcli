from sympy.parsing.sympy_parser import parse_expr
from sympy import latex, lambdify, Derivative
from sympy.parsing.sympy_parser import (
    function_exponentiation,
    standard_transformations,
    implicit_application,
    implicit_multiplication_application,
    convert_equals_signs,
)
from sympy import simplify as simp


from .errors import DerivativeArgumentsNumberError, ArgumentsNumberError
from ._utils import is_number, fmt_number
from mathcli import theme


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
    except SyntaxError:
        raise ValueError(f"Failed to parse expression: {expr}")


class Expression:
    def __init__(self, expression):
        """
            Class representing a mathematical expression.
            It takes a string representation of an expression, like:
                '3x + log(y) - sqrt 10 + cos pi'
            and creates a sympy expression from it. 
            It can then solve the expression, take derivatives etc..
        """
        self.variables = []  # variables in the expression

        # parse and evaluate
        self.string = clean(expression)
        self.expression = parse(self.string, evaluate=False)
        self.eval()

        # get variabls in the expression and create highlighted  string representation
        self.get_variables()
        self.highlight()

    def __str__(self):
        return (
            f"mathcli.expression.Expression: {self.n_variables} variables\n      "
            + self.string
        )

    def __repr__(self):
        return f"mathcli.expression.Expression: {self.n_variables} variables"

    def __rich_console__(self, *args):
        yield (
            f"[{theme.text}]mathcli.expression.Expression: "
            f"[{theme.text_accent}]{self.n_variables}[/{theme.text_accent}] variables\n       "
            + self.highlighted
        )

    def derivative(self, *wrt):
        """
            Take the derivative of the expression.
            If 0 or 1 variables are present, no need to pass any other argument.
            If >1 variables are present the user must specify which variables to
            take the derivative for by passing a variable number of string arguments
            For more information about derivatives: https://docs.sympy.org/latest/tutorial/calculus.html

            Arguments:
                wrt: str. Variable number of variables name

            Returns:
                a new Expression representing the derivative. 

            Raises:
                DerivativeArgumentsNumberError if the number of variable >2 and wrt is not specified
        """
        try:
            expr = Expression(
                str(Derivative(self.expression, *wrt, evaluate=True))
            )
        except ValueError:
            raise DerivativeArgumentsNumberError(self)

        expr.strip_result()
        return expr

    def simplify(self):
        """
            Simplify the expression, returns a  new instance of Expression
            For more information about simplification: https://docs.sympy.org/latest/tutorial/simplification.html
        """
        return Expression(str(simp(self.expression)))

    def eval(self):
        """
            Evaluate the expression.
            If expression is numerical it can be solved completely and
            self.value is a number, otherwise self.value is a symbolic
            expression and the expression can be fully solved only
            when the values for the variables are passed.
        """
        self.value = self.expression.evalf()

        if is_number(self.value):
            # numeric expression completely evalued
            self.is_solved = True
            self.add_result_to_string(self.value)
        else:
            # it's a symbolic expression, will need to be value
            self.is_solved = False

    def add_result_to_string(self, result):
        """
            Adds a result to the expression string by appending = RESULT
            to it.
        """
        self.string += f" = [b u {theme.result}]{fmt_number(result)}"
        self.highlight()

    def strip_result(self):
        """
            Remove the result from the expression string, for when it 
            needs to be removed for cleaner printing.
        """
        if "=" in self.string:
            self.string = self.string[: self.string.index("=")]
        self.highlight()

    def solve(self, **values):
        """
            If self.eval didn't yield a number, then we have
            a symbolic expression that needs to be solved given the values
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
        # turn the expression into a lambda function
        lambda_function = lambdify(
            self.variables, self.expression, modules="numpy"
        )

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
        self.variables = [
            x for x in list(self.expression.atoms()) if not is_number(x)
        ]
        self.n_variables = len(self.variables)

    def highlight(self):
        "returns a version of self.string with variables, symbols etc. highlighted"
        highlighted = self.string

        highlighted = highlighted.replace(
            "/", f"[{theme.operator}]/[/{theme.operator}]"
        )

        # highlight vars
        for v in self.variables:
            highlighted = highlighted.replace(
                str(v), f"[{theme.variable}]{str(v)}[/{theme.variable}]"
            )

        # highilight words
        names = ("sin", "cos", "tan", "atan", "sqrt", "log", "exp")
        for v in names:
            highlighted = highlighted.replace(
                str(v),
                f"[{theme.operator_dark}]{str(v)}[/{theme.operator_dark}]",
            )

        # highlight symbols
        for v in "-+*:_|":
            highlighted = highlighted.replace(
                v, f"[{theme.operator}]{v}[/{theme.operator}]"
            )
        for v in "()":
            highlighted = highlighted.replace(
                v, f"[{theme.parenthesis}]{v}[/{theme.parenthesis}]"
            )

        highlighted = highlighted.replace(
            "=", f"[{theme.operator}]=[/{theme.operator}]"
        )

        self.highlighted = f"[{theme.number}] " + highlighted

    def to_latex(self, expr):
        """
            Yields a latex representation of the expression.
        """
        latexstring = "$" + latex(self.expression) + "$"
        return latexstring
