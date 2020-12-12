from mathcli import math
import typer
from typing import List, Optional

app = typer.Typer()


def parse_kwargs(val):
    kwargs = {}
    for pair in val[0].split(" "):
        k, v = pair.split("=")
        kwargs[k] = float(v)
    return kwargs


@app.command()
def calc(expression: str, v: Optional[List[str]] = typer.Option(None)):

    math.calc(expression, **parse_kwargs(v))


@app.command()
def calc2(expression: str):
    expression = " ".join(expression)
    typer.echo(f"Calc {expression}")


#  TODO finish the other methods and tests

if __name__ == "__main__":
    app()
