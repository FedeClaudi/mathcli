from pyinspect import install_traceback
from rich import pretty

install_traceback()
pretty.install()

from loguru import logger
import sys

# comment these two lines out to show logging info
logger.remove()
logger.add(sys.stderr, level="INFO")

logger.level("EXPRESSION", no=15, color="<yellow>", icon="🖇")
logger.level("MATH", no=15, color="<green>", icon="🖇")

from mathcli.math import calc, solve, simplify, derivative
