from mathcli import calc, simplify, derivative, solve
from mathcli._utils import is_number
from mathcli.cli import app
import pytest
from typer.testing import CliRunner

from tests import expressions, close


@pytest.mark.parametrize("expression", expressions)
def test_calc(expression):
    if expression["numeric"]:
        res = calc(expression["string"])
    else:
        res = calc(expression["string"], **expression["values"])

    assert is_number(res), "numerics should yield a number"
    assert close(
        res, expression["calc_res"]
    ), f"exptected {expression['calc_res']} got {res}"


@pytest.mark.parametrize("expression", expressions)
def test_simplify(expression):
    simplify(expression["string"])


@pytest.mark.parametrize("expression", expressions)
def test_derivative(expression):
    if not expression["numeric"] and expression["wrt"] is not None:
        derivative(expression["string"], expression["wrt"])
    else:
        derivative(expression["string"])

    # assert der == expression["der_res"]


@pytest.mark.parametrize("expression", expressions)
def test_solve(expression):
    if expression["numeric"]:
        solve(expression["string"])
    else:
        solve(expression["string"], solve_for=expression["solve_for"])
        solve(
            expression["string"],
            solve_for=expression["solve_for"],
            **expression["given"],
        )

    #     assert is_number(res)

    # assert res == expression['solve_res']


runner = CliRunner()


@pytest.mark.parametrize("expression", expressions)
def test_cli(expression):
    runner.invoke(app, ["calc", expression["string"]])
    runner.invoke(app, ["simplify", expression["string"]])

    if not expression["numeric"]:
        runner.invoke(
            app, ["simplify", expression["string"], "--v", expression["wrt"]]
        )
    else:
        runner.invoke(app, ["simplify", expression["string"]])
    # runner.invoke(app, ['solve', expression['string'], '--solve-for', expression['solve_for'], '--give', expression['given']])

    runner.invoke(app, ["latex", expression["string"]])
    runner.invoke(app, ["unicode", expression["string"]])
