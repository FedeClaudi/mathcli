from pyinspect import install_traceback
from rich import pretty

install_traceback()
pretty.install()


from mathcli.math import calc, solve, simplify, derivative
