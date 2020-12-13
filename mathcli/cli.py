from mathcli import math
from mathcli.expression import Expression
import typer
from typing import List, Optional

app = typer.Typer(help="Numerical and symbolic math in your terminal")


"""
    Command line interface for mathcli, powered by Typer:
        https://typer.tiangolo.com/
    
    Once mathcli is installed (pip install mathcli or pip install .),
    using math in the command line gives acces to mathcli's functionality

            Usage: main.py [OPTIONS] COMMAND [ARGS]...

            Numerical and symbolic math in your terminal

            Options:
            --install-completion [bash|zsh|fish|powershell|pwsh]
                                            Install completion for the specified shell.
            --show-completion [bash|zsh|fish|powershell|pwsh]
                                            Show completion for the specified shell, to
                                            copy it or customize the installation.

            --help                          Show this message and exit.

            Commands:
            calc        Calculate the value of an expression.
            derivative  Compute the derivative of an expression.
            simplify    Simplify an expression.
            solve       Solve an equation.
                                        
"""


def parse_kwargs(val):
    """
        Given a string with form:
            'x=1 y=2'
        it parses it to return a dictionary of the form:
            {x:1, y:2}

        Arguments:
            val: str
        
        Returns:
            parsed kwargs: dict
    """
    kwargs = {}
    if val:
        for pair in val[0].split(" "):
            k, v = pair.split("=")
            kwargs[k] = float(v)
    return kwargs


def parse_args(val):
    """
        Given a string of the form:
            'xyz' or 'x'
        it parses it to return a list:
            ['x', 'y', 'z'] or ['x']

        Arguments:
            val: str

        Returns:
            parsed args: list of strings
    """
    if val is None or not val[0]:
        return []
    else:
        return [x for x in val[0]]


@app.command()
def calc(
    expression: str,
    v: Optional[List[str]] = typer.Option(None, help="variables values"),
):
    """
        Calculate the value of an expression. 
        If the expression is numeric (e.g. '3 + sqrt(10)') then no other arguments  are necessary.
        For symbolic expressions like '3x + 2' the value of the variables must be passed to 
        compute the expressions value. Use the '--v' options to pass variables value like 'x=1'.
        For more information: https://docs.sympy.org/latest/modules/evalf.html

        Arguments:
            expression: str. Numeric or symbolic expression.
            v: str, optional. A string with variables values like: 'x=1 y=2'
    """
    math.calc(expression, **parse_kwargs(v))


@app.command()
def simplify(expression: str):
    """
        Simplify an expression.
        Simplifies an expression, e.g. '3x + 2x -1' becomes '5x -1'
        For more information about simplification: https://docs.sympy.org/latest/tutorial/simplification.html

        Arguments:
            expression: str. Numeric or symbolic expression.
    """
    math.simplify(expression)


@app.command()
def latex(expression: str):
    """
        Format an expression as latex

        Arguments:
            expression: str. Numeric or symbolic expression.
    """
    typer.echo(Expression(expression).latex)


@app.command()
def unicode(expression: str):
    """
        Format an expression as unicode chrs

        Arguments:
            expression: str. Numeric or symbolic expression.
    """
    typer.echo(Expression(expression).unicode)


@app.command()
def derivative(expression: str, v: str = typer.Option(None)):
    """
        Compute the derivative of an expression.
        For expressions with no or single variables, no other argument is necessary:
        if a variable is present the derivative will be computed for that variable. 
        If >1 variables is present, the user must specify for which variables the
        derivative is to be computed. This is done with the --v option which should
        be used to pass a string e.g. 'x' to compute the derivate w.r.t. x.
        For more information about derivatives: https://docs.sympy.org/latest/tutorial/calculus.html


        Arguments:
            expression: str. Numeric or symbolic expression.
            v: str, optional. A string with variables names like 'x'
    """
    math.derivative(expression, *parse_args(v))


@app.command()
def solve(
    expression: str,
    solve_for: str = typer.Option(None),
    given: Optional[List[str]] = typer.Option(None),
):
    """
        Solve an equation.
        Given an expression for an equation e.g. '3x + 2y = 0` it attempts to solve the equation and 
        find  the value of the variable(s) of interest. 
        Note: `= 0` is optional and if no rhs of the equation is passed it is assumed to be '0;, 
        i.e. passing '3x = 0' is the same as passing just '3x'.

        If no variables are there in the expression, it attempts to compute the outcome of the equation.
        If only one variable is present, it solves the equation for that variable.
        If >1 variable is present, the user must specify which variable to solve for by passing the
        name to --solve-for (e.g. '--solve-for 'x''). Also when multiple variables are present, 
        the values of the other variables (not being solved for) can be passed with the 
        optional argument --given (e.g. 'solve '3x + 2y = 1' --solve-for 'x' --given 'y=1').
        For more information: https://docs.sympy.org/latest/modules/solvers/solveset.html
        
        Arguments:
            expression: str. Numeric or symbolic expression. Can be an equation. 
            solve_for: str, optional. Name of the variable to solve for.
            given: str, optional. Values of variables not solving for (e.g. 'x=1')
    """
    math.solve(expression, solve_for, **parse_kwargs(given))


if __name__ == "__main__":
    app()
