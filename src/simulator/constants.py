import os.path

from infra.run.common import *
from infra.core import utils


HARDWARE_VERSION = 2

RGB_MATRIX_SIZE = [(32, 32), (64, 32), (96, 96)][HARDWARE_VERSION]
RGB_MATRIX_WIDTH, RGB_MATRIX_HEIGHT = RGB_MATRIX_SIZE
ELECTRODE_SIZE = 8
ELECTRODES_WIDTH, ELECTRODES_HEIGHT = ELECTRODES_SIZE = (
    RGB_MATRIX_WIDTH // ELECTRODE_SIZE,
    RGB_MATRIX_HEIGHT // ELECTRODE_SIZE)
ELECTRODES_COUNT = ELECTRODES_WIDTH * ELECTRODES_HEIGHT

LED_SEP_PIXELS = 2
LED_SIZE_PIXELS = 4
LED_MAP = [LED_SEP_PIXELS + i * (LED_SIZE_PIXELS + LED_SEP_PIXELS) for i in
    range(max(RGB_MATRIX_SIZE))]

RES_PATH = os.path.abspath(os.path.join(utils.upper_dir(os.path.realpath(
    __file__), 3), 'res', 'paws'))
PAWS_PATH = [os.path.join(RES_PATH, i) for i in (
    'leg_left.png', 'leg_right.png', 'hand_left.png', 'hand_right.png')]

WINDOW_SIZE = [LED_SEP_PIXELS * 2 + LED_MAP[i - 1] for i in RGB_MATRIX_SIZE]
WINDOW_TITLE = 'Interactive Leds Simulator %sx%s' % RGB_MATRIX_SIZE
