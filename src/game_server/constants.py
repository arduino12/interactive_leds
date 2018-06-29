import logging
import os.path

from infra.core.ansi import Ansi
from infra.run.common import *
from rgbmatrix import RGBMatrixOptions

# LOGOR_LEVEL = logging.DEBUG

HARDWARE_VERSION = 0

RGB_MATRIX_OPTIONS = RGBMatrixOptions()
RGB_MATRIX_OPTIONS.rows = 16
RGB_MATRIX_OPTIONS.cols = 32
RGB_MATRIX_OPTIONS.pwm_bits = 8
RGB_MATRIX_OPTIONS.row_address_type = 0
RGB_MATRIX_OPTIONS.pwm_lsb_nanoseconds = 130
RGB_MATRIX_OPTIONS.drop_privileges = False
RGB_MATRIX_OPTIONS.led_rgb_sequence = 'RGB'
RGB_MATRIX_OPTIONS.pixel_mapper_config = 'U-mapper'

def _calc_elecs_map(index):
    BASE_MAP = [6, 5, 7, 4, 3, 0, 2, 1]
    offset = index * len(BASE_MAP)
    if index & 1:
        return [i + offset for i in BASE_MAP]
    else:
        return [i + offset for i in BASE_MAP[::-1]]

if HARDWARE_VERSION == 0:
    RGB_MATRIX_OPTIONS.brightness = 100
    RGB_MATRIX_OPTIONS.chain_length = 2
    RGB_MATRIX_OPTIONS.parallel = 1
    RGB_MATRIX_OPTIONS.multiplexing = 0
    RGB_MATRIX_SIZE = (32, 32)
    ELECTRODES_SIZE = (4, 4)
    MPR121_MAP = [
        (0, 1, [6, 5, 7, 4, 3, 0, 2, 1]),
        (0, 0, [14, 13, 15, 12, 11, 8, 10, 9]),
    ]
elif HARDWARE_VERSION == 1:
    RGB_MATRIX_OPTIONS.brightness = 50
    RGB_MATRIX_OPTIONS.chain_length = 6
    RGB_MATRIX_OPTIONS.parallel = 1
    RGB_MATRIX_OPTIONS.multiplexing = 4
    RGB_MATRIX_SIZE = (32, 96)
    ELECTRODES_SIZE = (4, 12)
    MPR121_MAP = []
    for mux_addr_off in range(3):
        for mux_sub_index in range(6):
            MPR121_MAP.append((mux_addr_off, mux_sub_index, 0, _calc_elecs_map(len(MPR121_MAP))))

RGB_MATRIX_WIDTH, RGB_MATRIX_HEIGHT = RGB_MATRIX_SIZE
ELECTRODES_WIDTH, ELECTRODES_HEIGHT = ELECTRODES_SIZE
ELECTRODES_COUNT = ELECTRODES_WIDTH * ELECTRODES_HEIGHT
