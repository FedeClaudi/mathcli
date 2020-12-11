from mathcli import derivative


def test_derivative():
    derivative("1")
    derivative("x")
    derivative("2x + 1/x - log(x)")
    derivative("exp(x)")
    derivative("sin(x)")
    derivative("cos 2x")

    derivative("3x + y", "y")
    derivative("3x + y - log z", "y", "z")
    derivative("3x + y - log z", "z")
