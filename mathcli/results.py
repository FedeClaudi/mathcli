from pyinspect import Report
from rich.table import Table
from sympy import init_printing
from myterial import (
    orange_lighter,
    amber,
    cyan_light,
    salmon,
    light_blue_light,
)
from rich import print

from ._utils import is_int, is_number, fmt_number
from .expression import Expression

init_printing(use_unicode=True)

space = "   "


def values_table(values):
    """
        Creates a rich Table showing variables and their value
    """
    tb = Table(box=None, show_lines=False, show_header=False)
    tb.add_column(justify="right", width=10)
    for c in range(len(values)):
        tb.add_column(justify="right")

    sorted_vals = dict(sorted(values.items()))
    tb.add_row(
        "[dim bold]variables:",
        *[f"[{light_blue_light}]" + str(v) for v in sorted_vals.keys()],
    )
    tb.add_row(
        "[dim bold]values:", *[str(round(v, 2)) for v in sorted_vals.values()]
    )
    return tb


class Result(Report):
    width = 120

    def __init__(self, expression):
        Report.__init__(self)

        self.expression = expression
        self.add_expression()

    def add_expression(self, expression=None, message="Expression"):
        expression = expression or self.expression

        if is_number(expression):
            expression = fmt_number(expression)
        elif isinstance(expression, Expression):
            expression = expression.highlighted
        else:
            expression = str(expression)

        self.add(f"[{amber}]{message}:")
        self.add(space + expression, "rich")
        self.spacer()

    def add_variables(self, **values):
        self.add(f"[{amber}]Values:")
        self.add(values_table(values), "rich")
        self.spacer()


# # ----------------------------------- utils ---------------------------------- #


# def highlight_vars(expr, variables):
#     expr = str(expr)

#     for v in variables:
#         expr = expr.replace(
#             str(v), f"[{light_blue_light}]{str(v)}[/{light_blue_light}]"
#         )
#     return expr


# # ---------------------------------- results --------------------------------- #


# def numeric_expression_result(expr, result):
#     """
#         Prints the outcome of evaluating a numerical expression
#     """
#     if is_int(result):
#         res = str(result)
#     else:
#         res = f"{round(result, 2):.2f}"

#     print(f"[{amber}]Result:")
#     print(f"    [b white]{expr} [b {salmon}]= [b {cyan_light} u]{res}\n")


# def symbolic_expression_result(expr, simplified, variables, values, result):
#     expr = highlight_vars(expr, variables)
#     simplified = highlight_vars(simplified, variables)

#     # Create a report
#     res = Report(dim=orange_lighter, show_info=False)
#     res.width = 120

#     # Add expression
#     res.add(f"[{amber}]Expression:")
#     res.add(f"      [b]{expr}", "rich")
#     res.spacer()

#     # Add simplified expression
#     res.add(f"[{amber}]Simplified:")
#     res.add(f"      [b]{simplified}", "rich")
#     res.spacer()

#     # make a variables table
#     res.add(f"[{amber}]Variables:")
#     res.add(variables_table(values), "rich")
#     res.spacer()

#     # show results
#     res.add(f"[{amber}]Result:")
#     res.add(f"      {expr} [{salmon}]= [b {cyan_light} u]{round(result, 2)}")

#     res.print()


# def simplified_expression_result(
#     expr, simplified, variables, is_derivative=False
# ):
#     expr = highlight_vars(expr, variables)
#     simplified = highlight_vars(simplified, variables)

#     # Create a report
#     res = Report(dim=orange_lighter, show_info=False)
#     res.width = 120

#     # Add expression
#     res.add(f"[{amber}]Expression:")
#     res.add(f"      [b]{expr}", "rich")
#     res.spacer()

#     # Add simplified expression
#     if not is_derivative:
#         res.add(f"[{amber}]Simplified:")
#     else:
#         res.add(f"[{amber}]Derivative wrt {variables}:")
#     res.add(f"      [b]{simplified}", "rich")
#     res.spacer()

#     res.print()
