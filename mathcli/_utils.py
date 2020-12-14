from sympy.core.numbers import Float, Integer, Rational
from sympy.sets import ConditionSet, FiniteSet, EmptySet
from pyinspect.utils import _class_name
from loguru import logger


def parse_solveset(solution):
    """
        Given what sympy.solvest(eq) returned while
        trying to solve a sympy.Eq equation, return
        a string expression that can be parsed by Expression. 

        Arguments:
            solution: sympy.set.Set subclasses, output of sympy.solveset

        Returns:
            solution: str. A string expression with the solution
    """
    logger.debug(f"PARSE SOLVESET with solution: {solution}")
    if solution is None:
        return None

    if isinstance(solution, ConditionSet):
        try:
            return str(solution.base_set.args[0])
        except IndexError:
            raise NotImplementedError(
                f"Unrecognized solution: {_class_name(solution)}"
            )
    elif isinstance(solution, FiniteSet):
        return str(solution.args[0])
    elif _class_name(solution) == "EmptySet" or isinstance(solution, EmptySet):
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
    if isinstance(num, str):
        return num

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
