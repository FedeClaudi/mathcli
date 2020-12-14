from sympy import solveset
from loguru import logger

from .expression import Expression, to_sympy
from .results import Result
from ._utils import parse_solveset, fmt_number
from .cache import cache_expression
from mathcli import theme


def make_eq(expression):
    """
        Return a sympy expression representing an equation
    """
    if "=" not in expression:
        expression += " = 0"
    return to_sympy(expression)


@cache_expression
def calc(expression, **values):
    """
        Calculate the value of an expression. 
        If the expression is numeric (e.g. '3 + sqrt(10)') then no other arguments  are necessary.
        For symbolic expressions like '3x + 2' the value of the variables must be passed to 
        compute the expressions value. Use the **values kwargs to pass e.g. x=1, y=2.
        For more information: https://docs.sympy.org/latest/modules/evalf.html

        Arguments:
            expression: str. Numeric or symbolic expression.
            values: kwargs, dict, optional. Dictionary of values like: 'x=1 y=2'

        Returns:
            the expression's value. A float.
    """
    logger.log("MATH", f'called CALC with "{expression}" and values {values}')
    expression = Expression(expression)

    if expression.is_solved:
        # numeric expression is solved already
        Result(expression, footer="calculate").print()
        result = expression.value
    else:
        result = expression.solve(**values)
        expression.add_result_to_string(result)

        # print results
        res = Result(expression, footer="calculate")
        res.add_variables(**values)
        res.print()

    return result


@cache_expression
def simplify(expression, show_result=True):
    """
        Simplify an expression.
        Simplifies an expression, e.g. '3x + 2x -1' becomes '5x -1'
        For more information about simplification: https://docs.sympy.org/latest/tutorial/simplification.html

        Arguments:
            expression: str. Numeric or symbolic expression.
            show_result: bool. If false the result is not shown.

        Returns:
            the simplified expression as a string.
    """
    logger.log("MATH", f'called SIMPLIFY with "{expression}"')
    expression = Expression(expression)
    expression.strip_result()
    simplified = expression.simplify()
    simplified.strip_result()

    if show_result:
        res = Result(expression, footer="simplify")
        res.add_expression(simplified, "Simplified")
        res.print()

    return simplified.string


@cache_expression
def derivative(expression, wrt=None):
    """
        Compute the derivative of an expression.
        For expressions with no or single variables, no other argument is necessary:
        if a variable is present the derivative will be computed for that variable. 
        If >1 variables is present, the user must specify for which variables the
        derivative is to be computed. This is done with the `*wrt` variable number
        arguments which should be strings with variables names.
        For more information about derivatives: https://docs.sympy.org/latest/tutorial/calculus.html


        Arguments:
            expression: str. Numeric or symbolic expression.
            wrt: str, optional. String of variables names and derivative order, e.g. 'x2'

        Returns:
            derivative: str. String with the (partial) derivative of the expression
    """
    logger.log(
        "MATH", f'called DERIVATIVE with "{expression}" and wrt "{wrt}"'
    )

    expression = Expression(expression)
    expression.strip_result()
    ttl = "Derivative"

    if not wrt and expression.n_variables == 1:
        wrt = str(expression.variables[0])
    elif wrt:
        ttl += f" w.r.t.[b {theme.variable}] " + wrt + "[/]"

        # split wrt into letters/numbers
        nums = "123456789"
        wrt = [s if s not in nums else int(s) for s in wrt]

    res = Result(expression, footer="derivative")

    der = expression.derivative(wrt)
    res.add_expression(der, ttl)
    res.print()

    return der.string


@cache_expression
def solve(expression, solve_for=None, **given):
    """
        Solve an equation.
        Given an expression for an equation e.g. '3x + 2y = 0` it attempts to solve the equation and 
        find  the value of the variable(s) of interest. 
        Note: `= 0` is optional and if no rhs of the equation is passed it is assumed to be '0;, 
        i.e. passing '3x = 0' is the same as passing just '3x'.

        If no variables are there in the expression, it attempts to compute the outcome of the equation.
        If only one variable is present, it solves the equation for that variable.
        If >1 variable is present, the user must specify which variable to solve for by passing the
        name to solve_for. 
        Also when multiple variables are present, 
        the values of the other variables (not being solved for) can be passed with the 
        optional keyword arguments given (e.g. 'solve()'3x + 2y = 1' solve_for='x', y=1).
        For more information: https://docs.sympy.org/latest/modules/solvers/solveset.html
        
        Arguments:
            expression: str. Numeric or symbolic expression. Can be an equation. 
            solve_for: str, optional. Name or the variable to solve for.
            given: kwargs, optional. Dictionary of values for variables not solving for (e.g. 'x=1')

        Returns: 
            value: float, str. If no variables values are given, and the expression is
                symbolic then an expression string is return, otherwise a float.
    """
    logger.log(
        "MATH",
        f'called SOLVE with "{expression}" and solve_for "{solve_for}", given {given}',
    )

    # compute solution to expression
    eq = make_eq(expression)
    expression = Expression(expression)

    # numeric
    if expression.n_variables == 0:
        return solveset(eq)

    # symbolic
    if expression.n_variables == 1:
        solve_for = expression.variables[0]
    solution = parse_solveset(solveset(eq, solve_for))

    # Create Result
    res = Result(expression, footer="solve")

    # add solution
    if not Expression(solution).n_variables:
        sol = Expression(solution)
        solution = fmt_number(sol.value)
        value = solution
        sol.add_result_to_string(value)

        res.add_expression(
            sol,
            f"Solve for [{theme.variable}]{solve_for}[/]",
            prepend=f"{solve_for} = ",
        )

    else:
        res.add_expression(
            f"{solve_for} = {solution}" if solution else "no solution",
            f"Solve for [{theme.variable}]{solve_for}[/]",
        )

    # If values are given, we can substitute them into the solution string and compute
    if Expression(solution).n_variables:
        if given:
            value = Expression(solution).solve(**given)
            res.add_variables(**given, message="Given")
            res.add_expression(f"{solve_for} = {value}", f"Solution")
        else:
            value = solution

    res.print()
    return value
