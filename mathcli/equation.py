from .expression import to_sympy


def make_eq(expression):
    if "=" not in expression:
        expression += " = 0"

    return to_sympy(expression)
