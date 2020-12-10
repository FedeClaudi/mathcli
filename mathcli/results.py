from pyinspect import Report
from rich.table import Table

from myterial import orange_lighter, amber, cyan_light, salmon
from rich import print


def numeric_expression_result(expr, result):
    """
        Prints the outcome of evaluating a numerical expression
    """
    print(f"[{amber}]Result:")
    print(
        f"    [b white]{expr} [b {salmon}]= [b {cyan_light} u]{round(result, 2)}\n"
    )


def variables_table(variables, values):
    """
        Creates a rich Table showing variables and their value
    """
    tb = Table(box=None, show_lines=False, show_header=False)
    tb.add_column(justify="right", width=10)
    for c in range(len(variables)):
        tb.add_column(justify="center", width=2)

    tb.add_row(
        "[dim bold]variables:", *[f"[{amber}]" + str(v) for v in variables]
    )
    tb.add_row("[dim bold]values:", *[str(round(v, 2)) for v in values])

    return tb


def highlight_vars(expr, variables):
    for v in variables:
        expr = expr.replace(str(v), f"[{amber}]{str(v)}[/{amber}]")
    return expr


def symbolic_expression_result(expr, variables, values, result):
    expr = highlight_vars(expr, variables)

    # Create a report
    res = Report(dim=orange_lighter, show_info=False)
    res.width = 120

    # Add expression
    res.add(f"[{amber}]Expression:")
    res.add(f"      [b]{expr}", "rich")
    res.spacer()

    # make a variables table
    res.add(f"[{amber}]Variables:")
    res.add(variables_table(variables, values), "rich")
    res.spacer()

    # show results
    res.add(f"[{amber}]Result:")
    res.add(f"      {expr} [{salmon}]= [b {cyan_light} u]{round(result, 2)}")

    res.print()
