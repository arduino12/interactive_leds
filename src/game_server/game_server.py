import pygame
import logging
from PIL import Image
from rgbmatrix import RGBMatrix

from infra.app import app
from infra.modules.sensors.mpr121 import electrodes
from interactive_leds.src.game_server import constants


class GameServer(app.App):
    _logger = logging.getLogger('game_server')

    def __init__(self, globals):
        app.App.__init__(self, constants)
        self._modules.extend((electrodes.mpr121.registers_tree,
            electrodes.mpr121.i2c_mux, electrodes.mpr121, electrodes))

        if not hasattr(globals, 'matrix'):
            globals.matrix = RGBMatrix(options=constants.RGB_MATRIX_OPTIONS)
        self.matrix = globals.matrix

        self.electrodes = electrodes.Mpr121ElectrodesGrid(
            constants.MPR121_MAP, constants.ELECTRODES_SIZE, constants.RGB_MATRIX_SIZE)

    def draw_pil_string(self, s):
        pil_image = Image.frombytes('RGB', constants.RGB_MATRIX_SIZE, s)
        self.matrix.SetImage(pil_image, 0, 0)

    def __exit__(self):
        app.App.__exit__(self)
