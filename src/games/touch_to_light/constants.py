import logging
import os.path

from infra.core.ansi import Ansi
from infra.run.common import *

# LOGOR_LEVEL = logging.DEBUG

RGB_MATRIX_SIZE = RGB_MATRIX_WIDTH, RGB_MATRIX_HEIGHT = (32, 32)
ELECTRODES_SIZE = ELECTRODES_WIDTH, ELECTRODES_HEIGHT = (4, 4)
ELECTRODES_COUNT = ELECTRODES_WIDTH * ELECTRODES_HEIGHT
