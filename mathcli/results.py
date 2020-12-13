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

        Arguments:
            values: dict of variables and their values

        Return:
            rich.table.Table with variables
    """
    # Create a table
    tb = Table(box=None, show_lines=False, show_header=False)
    tb.add_column(justify="right", width=10)
    for c in range(len(values)):
        tb.add_column(justify="right")

    # sort variables alphabetically and add to table
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
    width = 300

    def __init__(self, expression=None, footer=None):
        """
            pyinspect.panels.Report subclass showing
            the results of an operation from mathcli.math

            Arguments:
                expression: instance of Expression.
                footre: str, name to add to the panel's footer
        """
        Report.__init__(
            self,
            dim=theme.result_panel_footer,
            color=theme.result_panel,
            accent=theme.result_panel,
            show_info=True,
        )
        self._type = f"[b]{footer}[/b]"

        self.expression = expression

        if expression:
            self.add_expression()

    def add_expression(
        self, expression=None, message="Expression", prepend=""
    ):
        """
            Add an expression to the report, ideally highlighted
            to show variables symbols etc.

            Arguments: 
                expression: str, expression, number, optional.
                    If not passed, self.expression is used.
                    If an expression is passed then expression.highlighted is passed,
                    if a number then the number is used otherwise a string version 
                    of any other object.
                message: str. Message to prepent to expression in the report.
        """
        expression = expression or self.expression

        if is_number(expression):
            expression = fmt_number(expression)
        elif isinstance(expression, str):
            expression = Expression(expression).highlighted
        elif isinstance(expression, Expression):
            expression = expression.highlighted
        else:
            expression = str(expression)

        self.add(f"[{theme.text_accent}]{message}:")
        self.add(space + prepend + f"[{theme.text}]" + expression, "rich")
        self.spacer()

    def add_variables(self, message="Values", **values):
        """
            Adds a table listing an expression variables.

            Arguments:
                message: str. Message to prepent to expression in the report.
                values: dict, optional. Keyword arguments listing variables values.
        """
        self.add(f"[{theme.text_accent}]{message}:")
        self.add(values_table(values), "rich")
        self.spacer()
