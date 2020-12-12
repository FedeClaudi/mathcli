from sympy.core.numbers import Float, Integer, Rational
from sympy.sets import ConditionSet, FiniteSet
from pyinspect.utils import _class_name


def parse_solveset(solution):
    """
        Given what sympy.solvest(eq) returned while
        trying to solve a sympy.Eq equation, return
        a string expression that can be parsed by Expression. 

        Arguments:
            solution: sympy.set.Set subclasses, output of sympy.solveset

        Returns:
            solutionL str. A string expression with the solution
    """
    if isinstance(solution, ConditionSet):
        return str(solution.base_set.args[0])
    elif isinstance(solution, FiniteSet):
        return str(solution.args[0])
    elif _class_name(solution) == "EmptySet":
        return None
    else:
        raise NotImplementedError(
            f"Unrecognized solution: {_class_name(solution)}"
        )


def fmt_number(num):
    """
        Given a number it returns a formatted
        string for either integers or floats

        Arguments:
            num: int, float.
        Returns:
            formatted number: str. 
    """
    if num % 1 == 0:
        return str(int(num))
    else:
        return f"{num:.3f}"


def is_number(x):
    """
        Checks if a given input is a number

        Arguments:
            x: a number class or anything else
        Return:
            is number: bool. True if x is a number
    """
    return isinstance(x, (Float, Integer, Rational, float, int))
