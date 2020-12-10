from ._utils import is_number
from .parse import clean, parse_symbolic, parse
from .results import numeric_expression_result, symbolic_expression_result


def calc(expr, *vals):
    expr = clean(expr)
    result = parse(expr)

    if is_number(result):  # succesfully evaluated!
        numeric_expression_result(expr, parse(expr))
    else:
        variables, symbolic_function = parse_symbolic(expr)

        if len(vals) != len(variables):
            raise ValueError(
                "Wrong number of arguments for evaluating a symbolic expression,"
                f" it was {len(vals)} instead of {len(variables)}"
            )

        result = symbolic_function(*vals)
        symbolic_expression_result(expr, variables, vals, result)
