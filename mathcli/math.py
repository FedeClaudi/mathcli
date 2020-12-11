from sympy import simplify as simp
from rich import print
from myterial import orange_light

from ._utils import is_number
from .parse import clean, parse_symbolic, parse
from .results import (
    numeric_expression_result,
    symbolic_expression_result,
    simplified_expression_result,
)


def evaluate(expr):
    """
        Evaluates a string expression and 
        returns the parse expression + the result.
        The result can be either a numnber, if the
        expression was numeric, or a sympy expression
        if it was symbolic and needs to be solved.

        Argument:
            expr: str, expression string
    """
    # parse
    expr = clean(expr)

    try:
        parsed = parse(expr)
    except SyntaxError:
        raise ValueError(
            f"Got an error while trying to parse expression, perhaps something is missing: {expr}"
        )

    # evaluate
    try:
        result = parsed.evalf()
    except Exception as e:
        raise ValueError(
            f"Failed to evaluate expression: {expr} with error: {e}"
        )

    return expr, parsed, result


# ----------------------------------- solve ---------------------------------- #


def solve(expr, **values):
    # parse and evaluate
    expr, parsed, expression = evaluate(expr)

    # show results
    if is_number(expression):  # succesfully evaluated numeric expression
        numeric_expression_result(expr, parsed)
    else:
        # Solve a symbolic expression
        # Get the variables in the expression
        variables, symbolic_function = parse_symbolic(expr, expression)

        if len(values) != len(variables):
            raise ValueError(
                "Wrong number of arguments for evaluating a symbolic expression.\n"
                "Original expression:\n"
                f"      {expr}\n"
                "parsed expression:\n"
                f"      {parsed}\n"
                f"Found {len(values)} values for {len(variables)} variables: {variables}\n"
            )

        # replace variable and evaluate
        result = symbolic_function(*[values[str(var)] for var in variables])

        # print results
        symbolic_expression_result(
            expr, simp(expression), variables, values, result
        )


def simplify(expr, show_result=True):
    # parse and evaluate
    expr, parsed, expression = evaluate(expr)

    # check if numeric expression
    if is_number(expression):
        print(f"[{orange_light}]Expression was numeric, no need to siplify")
        if show_result:
            numeric_expression_result(expr, parsed)
            return expr, expression, None

    # simplify and print
    variables, symbolic_function = parse_symbolic(expr, expression)

    if show_result:
        simplified_expression_result(expr, simp(expression), variables)
    else:
        return expr, simp(expression), variables


def derivative(expr):
    expr = "diff(" + expr + ")"
    expr, derivative, variables = simplify(expr, show_result=False)

    simplified_expression_result(
        expr, derivative, variables, is_derivative=True
    )


# TODO: find X, given e.g. '3x + y = 2' and y=1, find 'x'.
