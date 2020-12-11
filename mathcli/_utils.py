from sympy.core.numbers import Float, Integer, Rational


def is_number(x):
    return isinstance(x, (Float, Integer, Rational))


def is_int(x):
    return isinstance(x, Integer)
