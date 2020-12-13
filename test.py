# from mathcli import solve, simplify, derivative, calc
# from mathcli.expression import Expression
# from rich import print

# import unicodeit

# # TODO tests
# # integrals

# # TODO functionality
# # solve ODEs
# # find X
# # CLI
# # tests docstrings...


# # --------------------------------- printing --------------------------------- #
# # e = Expression('y * 4*3x + Integral(2, x) - sqrt(10) - log(2) * exp(3) - 1/2 + 1/sin(3) + sqrt(2)/sqrt(3)')
# # e = Expression('gamma')
# # print('\n', e)
# # print(e.string)

# # ? ----------------------------- known limitations ---------------------------- #
# # 1. single letter variables
# # solve('x1+2', x1=2)
# # solve('my_var + your_var')

# # ------------------------------- failed tests ------------------------------- #
# # solve("x + 2y - sqrt(z)", "x", y=2)


# # ---------------------------------------------------------------------------- #
# #                                     solve                                    #
# # ---------------------------------------------------------------------------- #
# # solve('3x + sqrt(20)')
# # solve('x - y', 'x')
# # solve('x = y', 'x')
# # solve("2x + sin(y) - sqrt(3x)", "x")
# # solve("2x + sin(y) - sqrt(3x) = 2", "x")
# # solve("2x + sin(y) - sqrt(3x)", "x", y=10)
# # solve("x = y", "x", y=2)
# # solve("x + 2y - sqrt(z)", "x", y=2, z=10)
# # solve('x/0', 'x')
# # solve('sqrt(x) = -1', 'x')
# # solve('sqrt(x) = -y', 'x', y=1)

# # ---------------------------------------------------------------------------- #
# #                                   simplify                                   #
# # ---------------------------------------------------------------------------- #
# # simplify("1+1 - (5 + 3)")
# # simplify("2x + 3x - (x + 2)")
# # simplify("sin x - sin(3)")
# # simplify("sin**2( x )+ cos**2( 1) + cos(1) - cos**3(2)")
# # simplify("sqrt x + tanh 3 - sqrt(x)")
# # simplify("log(10/x) -x +log(x)")
# # simplify("x*sin(3-sqrt(x))")
# # simplify("exp(x) - exp(x) +x*log(2)")
# # simplify("x-x")

# # ---------------------------------------------------------------------------- #
# #                                  Derivative                                  #
# # ---------------------------------------------------------------------------- #
# derivative("1")
# derivative("x")
# derivative("2x + 1/x - log(x)")
# derivative("exp(x)")
# derivative("sin(x)")
# derivative("cos 2x")
# derivative("3x + log(x)", "y")

# derivative("3x + y", "y")
# derivative("3x + y - log z", "y", "z")
# derivative("3x + y - log z", "z")

# # ---------------------------------------------------------------------------- #
# #                                     calc                                     #
# # ---------------------------------------------------------------------------- #
# # calc('2 + 3**2 - 5/2')
# # calc("(1+1)*2")
# # calc("(1+1)2")
# # calc('3^3')
# # calc('1-1')
# # calc('pi * 2')
# # calc('2*2 - sqrt(10)')

# # calc('sin 1')
# # calc('sin**2( 1 )+ cos**2( 1)')
# # calc('sqrt 9 + tanh 3')
# # calc('log 10')
# # calc('2sin(3-sqrt(2))')
# # calc('exp(2)')

# # calc('3x', x=2)
# # calc('3x +2y -z +5z', z=1000, y=-2, x=2)
# # calc('exp(x)', x=1)
# # calc('x-x')

# # calc('3x + log 10', x=2)
# # calc('3x +2y -sin z', z=1000, y=-2, x=2)
# # calc('sin**2(x) + cos**2(x)', x=10)
