from pyinspect import install_traceback
from rich import pretty

install_traceback()
pretty.install()

from loguru import logger
import sys

# logger.remove()
# logger.add(sys.stderr, level="INFO")

from mathcli.math import calc, solve, simplify, derivative
