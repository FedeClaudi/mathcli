from sympy.parsing.sympy_parser import parse_expr
from sympy import latex, lambdify
from sympy.parsing.sympy_parser import (
    function_exponentiation,
    standard_transformations,
    implicit_application,
    implicit_multiplication_application,
    convert_equals_signs,
)

from ._utils import is_number


def parse(expr, evaluate=True):
    """ wraps around parse_expr to give more control """
    transformations = standard_transformations + (
        function_exponentiation,
        implicit_multiplication_application,
        implicit_application,
        convert_equals_signs,
    )
    expr = expr.replace("^", "**")
    return parse_expr(expr, transformations=transformations, evaluate=evaluate)


def parse_symbolic(expr, result):
    """
        Given an expression for a symbolic computation
        it returns a list of the variables in the expression
        and a lambdified function to evaluate the expression
        given variable values.

        Arguments:
            expr: string, expression
            result: sympy expression with variables not yet substituted
    """
    # Get variables in the expression
    variables = [x for x in list(result.atoms()) if not is_number(x)]

    lambda_function = lambdify(variables, parse(expr), modules="numpy")
    return variables, lambda_function


def to_latex(expr):
    latexstring = "$" + latex(parse(expr)) + "$"
    return latexstring
