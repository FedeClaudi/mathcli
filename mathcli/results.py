from pyinspect import Report
from rich.table import Table
from sympy import init_printing

from ._utils import is_number, fmt_number
from .expression import Expression
from mathcli import theme

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
        *[f"[{theme.variable}]" + str(v) for v in sorted_vals.keys()],
    )
    tb.add_row(
        "[dim bold]values:", *[str(round(v, 2)) for v in sorted_vals.values()]
    )
    return tb


class Result(Report):
    width = 120

    def __init__(self, expression, footer=None):
        Report.__init__(
            self,
            dim=theme.result_panel_footer,
            color=theme.result_panel,
            accent=theme.result_panel,
            show_info=True,
        )
        self._type = f"[b]{footer}[/b]"

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

        self.add(f"[{theme.text_accent}]{message}:")
        self.add(f"[{theme.text}]" + space + expression, "rich")
        self.spacer()

    def add_variables(self, message="Values", **values):
        self.add(f"[{theme.text_accent}]{message}:")
        self.add(values_table(values), "rich")
        self.spacer()
