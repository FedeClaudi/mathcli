from sympy.core.numbers import Float, Integer, Rational


def fmt_number(num):
    if num % 1 == 0:
        return str(int(num))
    else:
        return f"{num:.3f}"


def is_number(x):
    return isinstance(x, (Float, Integer, Rational))


def is_int(x):
    return isinstance(x, Integer)
