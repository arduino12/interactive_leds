import socket
import logging

from infra.run.common import *
from rgbmatrix import RGBMatrixOptions

# LOGOR_LEVEL = logging.DEBUG

HARDWARE_VERSION = 1

RGB_MATRIX_OPTIONS = RGBMatrixOptions()
RGB_MATRIX_OPTIONS.rows = 16
RGB_MATRIX_OPTIONS.cols = 32
RGB_MATRIX_OPTIONS.row_address_type = 0
RGB_MATRIX_OPTIONS.pwm_lsb_nanoseconds = 130
RGB_MATRIX_OPTIONS.drop_privileges = False
RGB_MATRIX_OPTIONS.led_rgb_sequence = 'RGB'
RGB_MATRIX_OPTIONS.hardware_mapping = 'free-i2c'

MPR121_MAP = []

def _update_gamepad_params(panels_width, panels_height, snake):
    GAMEPAD_PANELS_WIDTH, GAMEPAD_PANELS_HEIGHT = GAMEPAD_PANELS_SIZE = (
        panels_width, panels_height)
    RGB_MATRIX_WIDTH, RGB_MATRIX_HEIGHT = RGB_MATRIX_SIZE = (
        GAMEPAD_PANELS_WIDTH * RGB_MATRIX_OPTIONS.cols,
        GAMEPAD_PANELS_HEIGHT * RGB_MATRIX_OPTIONS.rows)
    ELECTRODE_SIZE = 8
    ELECTRODES_WIDTH, ELECTRODES_HEIGHT = ELECTRODES_SIZE = (
        RGB_MATRIX_WIDTH // ELECTRODE_SIZE,
        RGB_MATRIX_HEIGHT // ELECTRODE_SIZE)
    ELECTRODES_COUNT = ELECTRODES_WIDTH * ELECTRODES_HEIGHT
    RGB_MATRIX_OPTIONS.parallel = panels_height // snake
    RGB_MATRIX_OPTIONS.chain_length = GAMEPAD_PANELS_WIDTH * \
        GAMEPAD_PANELS_HEIGHT // RGB_MATRIX_OPTIONS.parallel
    RGB_MATRIX_OPTIONS.pixel_mapper_config = 'Snake:%s' % (snake,)
    globals().update(locals())


if HARDWARE_VERSION == 0:
    _update_gamepad_params(1, 2, 2)
    RGB_MATRIX_OPTIONS.brightness = 100
    RGB_MATRIX_OPTIONS.gpio_slowdown = 0
    RGB_MATRIX_OPTIONS.multiplexing = 0
    RGB_MATRIX_OPTIONS.pwm_bits = 6
    MPR121_MAP = [
        (None, None, 1, [6, 5, 7, 4, 3, 0, 2, 1]),
        (None, None, 0, [14, 13, 15, 12, 11, 8, 10, 9]),
    ]
elif HARDWARE_VERSION == 1:
    _update_gamepad_params(2, 3, 3)
    RGB_MATRIX_OPTIONS.brightness = 80
    RGB_MATRIX_OPTIONS.gpio_slowdown = 2
    RGB_MATRIX_OPTIONS.multiplexing = 4
    RGB_MATRIX_OPTIONS.pwm_bits = 8
    # RGB_MATRIX_OPTIONS.scan_mode = 1
    # RGB_MATRIX_OPTIONS.pwm_lsb_nanoseconds = 500
    # RGB_MATRIX_OPTIONS.disable_hardware_pulsing = True

    MPR121_ELECTRODES_MAP = [
        [2, 3, 11, 10, 9, 8, 0, 1], [9, 8, 0, 1, 2, 3, 11, 10]
    ]
    mux_sub_index = 0
    for y in range(GAMEPAD_PANELS_HEIGHT):
        i = y * ELECTRODES_COUNT // GAMEPAD_PANELS_HEIGHT
        for x in range(GAMEPAD_PANELS_WIDTH):
            MPR121_MAP.append((
                0, mux_sub_index + 2, 0,
                [i + j for j in MPR121_ELECTRODES_MAP[y % 2]]))
            mux_sub_index += 1
            i += ELECTRODES_WIDTH // GAMEPAD_PANELS_WIDTH
elif HARDWARE_VERSION == 2:
    _update_gamepad_params(3, 6, 2)
    RGB_MATRIX_OPTIONS.brightness = 70
    RGB_MATRIX_OPTIONS.gpio_slowdown = 2
    RGB_MATRIX_OPTIONS.multiplexing = 4
    RGB_MATRIX_OPTIONS.pwm_bits = 8

    MPR121_ELECTRODES_MAP = [
        [2, 3, 15, 14, 13, 12, 0, 1], [13, 12, 0, 1, 2, 3, 15, 14]
    ]
    for mux_addr_off in range(GAMEPAD_PANELS_WIDTH):
        for mux_sub_index in range(GAMEPAD_PANELS_HEIGHT):
            i = mux_addr_off * 4 + mux_sub_index * ELECTRODES_COUNT // GAMEPAD_PANELS_HEIGHT
            MPR121_MAP.append((
                mux_addr_off, mux_sub_index + 2, 0,
                [i + j for j in MPR121_ELECTRODES_MAP[mux_sub_index % 2]]))

LOCAL_IP = ((
    [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
        if not ip.startswith('127.')] or
    [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]]
        [0][1]]) + ['no IP found'])[0]
