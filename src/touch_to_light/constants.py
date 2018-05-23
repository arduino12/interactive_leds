import logging
import os.path

from infra.core.ansi import Ansi
from infra.run.common import *


LOGOR_LEVEL = logging.DEBUG


MPR121_ELECTRODES_MAP = [6, 5, 7, 4, 3, 0, 2, 1]
MPR121_MAP = {
    0x5A: [i + 8 for i in MPR121_ELECTRODES_MAP],
    0x5B: MPR121_ELECTRODES_MAP,
}
