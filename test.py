from mathcli import solve, simplify, derivative

# TODO tests
# derivatives
# integrals

# TODO functionality
# simplify
# CLI

# ---------------------------------------------------------------------------- #
#                                   simplify                                   #
# ---------------------------------------------------------------------------- #
# simplify('1+1 - (5 + 3)')
# simplify('2x + 3x - (x + 2)')
simplify("sin x - sin(3)")
simplify("sin**2( x )+ cos**2( 1) + cos(1) - cos**3(2)")
simplify("sqrt x + tanh 3 - sqrt(x)")
simplify("log(10/x) -x +log(x)")
simplify("x*sin(3-sqrt(x))")
# simplify('exp(x) - exp(x) +x*log(2)')
# simplify('x-x')

# ? simplify can also compute derivatives!
derivative("x")
derivative("2x + 1/x - log(x)")

# ---------------------------------------------------------------------------- #
#                                     SOLVE                                    #
# ---------------------------------------------------------------------------- #

# # ---------------------------------- numeric --------------------------------- #
# solve('2 + 3**2 - 5/2')
solve("(1+1)*2")
solve("(1+1)2")
# solve('3^3')
# solve('1-1')


# # --------------------------------- operators -------------------------------- #
# solve('sin 1')
# solve('sin**2( 1 )+ cos**2( 1)')
# solve('sqrt 9 + tanh 3')
# solve('log 10')
# solve('2sin(3-sqrt(2))')
# solve('exp(2)')

# # --------------------------------- symbolic --------------------------------- #
# solve('3x', x=2)
# solve('3x +2y -z +5z', z=1000, y=-2, x=2)
# solve('exp(x)', x=1)
# solve('x-x')

# # --------------------------- symbolic + operators --------------------------- #
# solve('3x + log 10', x=2)
# solve('3x +2y -sin z', z=1000, y=-2, x=2)
# solve('sin**2(x) + cos**2(x)', x=10)


# ----------------------------- known limitations ---------------------------- #
# 1. single letter variables
# solve('x1+2', x1=2)
# solve('my_var + your_var')
