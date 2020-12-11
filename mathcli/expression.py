from sympy.parsing.sympy_parser import parse_expr
from sympy import latex, lambdify, Derivative, integrate
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
            expr: tring, expression
    """
    expr = expr.replace("^", "**")
    return expr


def parse(expr, evaluate=True):
    """ wraps around parse_expr to give more control """
    transformations = standard_transformations + (
        function_exponentiation,
        implicit_multiplication_application,
        implicit_application,
        convert_equals_signs,
    )
    return parse_expr(expr, transformations=transformations, evaluate=evaluate)


class Expression:
    def __init__(self, expression):
        self.variables = []

        self.string = clean(expression)
        self.expression = parse(self.string, evaluate=False)
        self.eval()

        if is_number(self.evalued):
            self._needs_eval = False
        else:
            self._needs_eval = True

        self.get_variables()
        self.highlight()

    def derivative(self, *wrt):
        try:
            expr = Expression(
                str(Derivative(self.expression, *wrt, evaluate=True))
            )
        except ValueError:
            raise DerivativeArgumentsNumberError(self)

        expr.strip_result()
        return expr

    def integrate(self, *wrt):
        return Expression(str(integrate(self.expression, *wrt)))

    def simplify(self):
        return Expression(str(simp(self.expression)))

    def eval(self):
        self.evalued = self.expression.evalf()

        if is_number(self.evalued):
            # numeric expression completely evalued
            self.is_solved = True
            self.add_result_to_string(self.evalued)
        else:
            # it's a symbolic expression, will need to be evalued
            self.is_solved = False

    def add_result_to_string(self, result):
        self.string += f" = [b u {theme.result}]{fmt_number(result)}"
        self.highlight()

    def strip_result(self):
        if "=" in self.string:
            self.string = self.string[: self.string.index("=")]
        self.highlight()

    def solve(self, **values):
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

    def get_variables(self):
        self.variables = [
            x for x in list(self.expression.atoms()) if not is_number(x)
        ]
        self.n_variables = len(self.variables)

    def highlight(self):
        "returns a version of self.string with variables highlighted"
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
        latexstring = "$" + latex(self.expression) + "$"
        return latexstring
