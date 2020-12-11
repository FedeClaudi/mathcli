from mathcli import simplify


def test_simplify():
    simplify("1+1 - (5 + 3)")
    simplify("2x + 3x - (x + 2)")
    simplify("sin x - sin(3)")
    simplify("sin**2( x )+ cos**2( 1) + cos(1) - cos**3(2)")
    simplify("sqrt x + tanh 3 - sqrt(x)")
    simplify("log(10/x) -x +log(x)")
    simplify("x*sin(3-sqrt(x))")
    simplify("exp(x) - exp(x) +x*log(2)")
    simplify("x-x")
