import logging
import os.path

from infra.core.ansi import Ansi
from infra.run.common import *
from rgbmatrix import RGBMatrixOptions

# LOGOR_LEVEL = logging.DEBUG

RGB_MATRIX_SIZE = RGB_MATRIX_WIDTH, RGB_MATRIX_HEIGHT = (32, 32)

RGB_MATRIX_OPTIONS = RGBMatrixOptions()
RGB_MATRIX_OPTIONS.brightness = 50
RGB_MATRIX_OPTIONS.rows = 16
RGB_MATRIX_OPTIONS.cols = 32
RGB_MATRIX_OPTIONS.chain_length = 2
RGB_MATRIX_OPTIONS.pixel_mapper_config = 'U-mapper'
RGB_MATRIX_OPTIONS.drop_privileges = False
RGB_MATRIX_OPTIONS.led_rgb_sequence = 'RGB'
RGB_MATRIX_OPTIONS.pwm_bits = 8
RGB_MATRIX_OPTIONS.parallel = 1
RGB_MATRIX_OPTIONS.multiplexing = 0
RGB_MATRIX_OPTIONS.row_address_type = 0
RGB_MATRIX_OPTIONS.pwm_lsb_nanoseconds = 130

ELECTRODES_SIZE = ELECTRODES_WIDTH, ELECTRODES_HEIGHT = (4, 4)
ELECTRODES_COUNT = ELECTRODES_WIDTH * ELECTRODES_HEIGHT

MPR121_MAP = [
    (0, 1, [6, 5, 7, 4, 3, 0, 2, 1]),
    (0, 0, [14, 13, 15, 12, 11, 8, 10, 9]),
]
