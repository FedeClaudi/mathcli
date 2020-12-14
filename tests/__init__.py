from collections import namedtuple
import math


def close(x, X):
    x = round(x, 3)
    X = round(X, 3)
    return math.isclose(x, X, abs_tol=0.01)


"""
    Test expression are dictionaries of the form

  
    string = str,  # expression
    numeric = bool, # true if numeric expression
    values = dict,  # values of variables
    wrt = str,  # string with variables names
    solve_for = str,  # str with variables name
    given = dict,  # dict of variables values for solving

    and it includes result
    calc_res = float 
    solve_res = bool, float
)

"""
expressions = [
    # ---------------------------------- numeric --------------------------------- #
    dict(
        string="2 + 10/4 - sqrt(9)*2",
        numeric=True,
        calc_res=-1.5,
        der_res="0",
        solve_res=False,
    ),
    dict(
        string="log(10)/sqrt(12) + exp(12) + 2sin 10 + cos(pi - 2)",
        numeric=True,
        calc_res=162754.784,
        der_res="0",
        solve_res=False,
    ),
    dict(
        string="sin**2(3) - cos**2(3)",
        numeric=True,
        calc_res=-0.960,
        der_res="0",
        solve_res=False,
    ),
    # --------------------------------- symbolic --------------------------------- #
    dict(
        string="2x +y - cos(z)",
        numeric=False,
        values={"x": 1, "y": 2, "z": 3},
        wrt="x",
        solve_for="y",
        given={"x": 1, "z": 2},
        calc_res=4.990,
        der_res="2",
        solve_res=-2.416,
    ),
    dict(
        string="log(x) + sqrt(x)",
        numeric=False,
        values={"x": 1},
        wrt="x2",
        solve_for=None,
        given={"x": 1},
        calc_res=1,
        der_res="1/x + 1/(2*sqrt(x))",
        solve_res=1,
    ),
    dict(
        string="exp(2x) - cos y",
        numeric=False,
        values={"x": 1, "y": 2},
        wrt="xy",
        solve_for="y",
        given={"x": 1},
        calc_res=7.805,
        der_res="2*exp(2*x)",
        solve_res=0,
    ),
    dict(
        string="3x - y",
        numeric=False,
        values={"x": 1, "y": 2},
        wrt="x",
        solve_for="y",
        given={"x": 1},
        calc_res=1,
        der_res="3",
        solve_res=3,
    ),
]
