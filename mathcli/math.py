from rich import print
from myterial import orange_light

from .expression import Expression
from ._utils import is_number
from .results import Result
from .errors import ArgumentsNumberError


# ----------------------------------- solve ---------------------------------- #


def solve(expression, **values):
    expression = Expression(expression)

    if expression.is_solved:
        # numeric expression is solved already
        Result(expression).print()
    else:
        # Check that we have the correct number of variables
        if len(values) != expression.n_variables:
            raise ArgumentsNumberError(expression, **values)

        result = expression.solve(**values)
        expression.add_result_to_string(result)

        # print results
        res = Result(expression)
        res.add_variables(**values)
        res.print()


def simplify(expression, show_result=True):
    expression = Expression(expression)
    simplified = expression.simplify()

    if show_result:
        res = Result(expression)
        res.add_expression(simplified, "Simplified")
        res.print()


def derivative(expression):
    expression = Expression(expression)

    res = Result(expression)
    res.add_expression(expression.derivative(), "Derivative")
    res.print()


# TODO: find X, given e.g. '3x + y = 2' and y=1, find 'x'.
