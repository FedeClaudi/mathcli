from math import isclose

from mathcli import calc


def test_numerical():
    assert calc("2 + 3**2 - 5/2") == 8.5
    assert calc("(1+1)*2") == 4
    assert calc("(1+1)2") == 4
    assert calc("3^3") == 27
    assert isclose(calc("1-1"), 0, abs_tol=0.01)
    assert isclose(calc("pi * 2"), 6.28, abs_tol=0.01)
    assert isclose(calc("2*2 - sqrt(10)"), 0.83, abs_tol=0.01)


def test_operators():
    assert isclose(calc("sin 1"), 0.84, abs_tol=0.01)
    assert calc("sin**2( 1 )+ cos**2( 1)") == 1
    assert isclose(calc("sqrt 9 + tanh 3"), 3.995, abs_tol=0.01)
    assert isclose(calc("log 10"), 2.303, abs_tol=0.01)
    assert isclose(calc("2sin(3-sqrt(2))"), 2, abs_tol=0.01)
    assert isclose(calc("exp(2)"), 7.389, abs_tol=0.01)


def test_symbolic():
    assert isclose(calc("3x", x=2), 6, abs_tol=0.01)
    assert isclose(
        calc("3x +2y -z +5z", z=1000, y=-2, x=2), 4002, abs_tol=0.01
    )
    assert isclose(calc("exp(x)", x=1), 2.718, abs_tol=0.01)
    assert isclose(calc("x-x"), 0, abs_tol=0.01)


def test_symbolic_operators():
    assert isclose(calc("3x + log 10", x=2), 8.303, abs_tol=0.01)
    assert isclose(
        calc("3x +2y -sin z", z=1000, y=-2, x=2), 1.173, abs_tol=0.01
    )
    assert isclose(calc("sin**2(x) + cos**2(x)", x=10), 1, abs_tol=0.01)
