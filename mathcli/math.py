from sympy import Eq
from sympy import solveset

from .expression import Expression
from .results import Result
from .errors import ArgumentsNumberError, CouldNotSolveError
from ._utils import parse_solveset
from mathcli import theme


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
            the expression's value (either a number or an expression, 
                    depending on if the expression could be solved)
        
        Raises:
            ArgumentsNumberError if the expression has variables and the
                number of values passed does not match the number of  
                variables in the expression.
    """
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
    return expression.value


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
            wrt: str, optional. Variable number of strings with variables names names
    """
    expression = Expression(expression)
    expression.strip_result()

    ttl = "Derivative"
    if not wrt and expression.n_variables == 1:
        wrt = [str(expression.variables[0])]
    if wrt:
        ttl += f" w.r.t.[b {theme.variable}] " + ",".join(wrt) + "[/]"

    res = Result(expression, footer="derivative")
    res.add_expression(expression.derivative(*wrt), ttl)
    res.print()


def solve(equation, solve_for=None, **given):
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
            solve_for: str, optional. Name of the variable to solve for.
            given: kwargs, optional. Dictionary of values for variables not solving for (e.g. 'x=1')
    """
    # Compute  solution
    try:
        lhs, rhs = equation.split("=")
        eq = Eq(Expression(lhs).expression, Expression(rhs).expression)
    except ValueError:
        lhs = equation
        eq = Eq(Expression(equation).expression, 0)

    # if solve_for is not passed and only one variable is there solve for that
    if Expression(lhs).n_variables == 1:
        solve_for = str(Expression(lhs).variables[0])

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

    # solve given variables values
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
