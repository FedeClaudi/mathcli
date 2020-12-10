from sympy.parsing.sympy_parser import parse_expr
from sympy import latex, lambdify
from sympy.parsing.sympy_parser import (
    function_exponentiation,
    standard_transformations,
    implicit_application,
    implicit_multiplication_application,
    convert_equals_signs,
)

from ._symbols import symbols


def parse(expr, evaluate=True):
    """ wraps around parse_expr to give more control """
    transformations = standard_transformations + (
        function_exponentiation,
        implicit_multiplication_application,
        implicit_application,
        convert_equals_signs,
    )

    return parse_expr(expr, transformations=transformations, evaluate=evaluate)


def clean(expr):
    """
        cleans up an expression string

        Arguments:
            expr: tring, expression
    """
    expr = expr.replace("^", "**")
    return expr


def parse_symbolic(expr):
    """
        Given an expression string for a symbolic expression
        it returns a list of the variables in the expression
        and a lambdified function to evaluate the expression
        given variable values.

        Arguments:
            expr: tring, expression
    """
    # Get variables in the expression
    variables = [symb for s, symb in symbols.items() if s in expr]

    lambda_function = lambdify(variables, parse(expr), modules="numpy")
    return variables, lambda_function


def to_latex(expr):
    latexstring = "$" + latex(parse(expr)) + "$"
    return latexstring
