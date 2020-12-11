from pyinspect.utils import _class_name

from sympy.sets import ConditionSet, FiniteSet


def parse_solveset(solution):
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
