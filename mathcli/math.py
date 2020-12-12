from sympy import Eq
from sympy import solveset

from .expression import Expression
from .results import Result
from .errors import ArgumentsNumberError, CouldNotSolveError
from ._math import parse_solveset
from mathcli import theme


def calc(expression, **values):
    expression = Expression(expression)

    if expression.is_solved:
        # numeric expression is solved already
        Result(expression, footer="calculate").print()
    else:
        # Check that we have the correct number of variables
        if len(values) != expression.n_variables:
            raise ArgumentsNumberError(expression, **values)

        result = expression.solve(**values)
        expression.add_result_to_string(result)

        # print results
        res = Result(expression, footer="calculate")
        res.add_variables(**values)
        res.print()
    return expression.evalued


def simplify(expression, show_result=True):
    expression = Expression(expression)
    expression.strip_result()
    simplified = expression.simplify()
    simplified.strip_result()

    if show_result:
        res = Result(expression, footer="simplify")
        res.add_expression(simplified, "Simplified")
        res.print()

    return simplified.string


def derivative(expression, *wrt):
    expression = Expression(expression)
    expression.strip_result()

    ttl = "Derivative"
    if wrt:
        ttl += f" w.r.t.[b {theme.variable}] " + ",".join(wrt) + "[/]"

    res = Result(expression, footer="derivative")
    res.add_expression(expression.derivative(*wrt), ttl)
    res.print()


def solve(equation, solve_for, **given):
    # Compute  solution
    try:
        lhs, rhs = equation.split("=")
        eq = Eq(Expression(lhs).expression, Expression(rhs).expression)
    except ValueError:
        eq = Eq(Expression(equation).expression, 0)

    solution = solveset(eq, solve_for)

    # simplify and make printable
    solution_string = parse_solveset(solution)
    if solution_string:
        if isinstance(solution_string, Eq):
            solution_string = solution_string.lhs
        solution_string = str(solution_string)

        try:
            solution_string = simplify(solution_string, show_result=False)
            solution = Expression(f"{solve_for} = " + solution_string)
        except Exception as e:
            raise CouldNotSolveError(equation, solution_string, e)

    if given and solution_string:
        value = Expression(solution_string).solve(**given)
        result = Expression(solve_for)
        result.add_result_to_string(value)

    # print
    res = Result(Expression(f"{eq.lhs} = {eq.rhs}"), footer="solve")
    res.add_expression(
        solution if solution_string else "no solution",
        f"Solve for [{theme.variable}]{solve_for}[/]",
    )

    if given:
        res.add_variables(**given, message="Given")
        res.add_expression(result, f"Solution")

    res.print()
