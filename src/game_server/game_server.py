import pygame
import logging
from PIL import Image
from rgbmatrix import RGBMatrix, graphics

from . import constants
from infra.app import app
from infra.modules.sensors.mpr121 import electrodes


class GameServer(app.App):
    _logger = logging.getLogger('game_server')

    def __init__(self, globals):
        app.App.__init__(self, constants)
        self._modules.extend((
            electrodes.mpr121.registers_tree, electrodes.mpr121,
            electrodes.i2c_mux, electrodes))

        if not hasattr(globals, 'matrix'):
            globals.matrix = RGBMatrix(options=constants.RGB_MATRIX_OPTIONS)
        self.matrix = globals.matrix

        self.electrodes = electrodes.Mpr121ElectrodesGrid(
            constants.MPR121_MAP, constants.ELECTRODES_SIZE,
            constants.RGB_MATRIX_SIZE)
        self.electrodes.init()

        self.canvas = self.matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont('/home/pi/Public/rpi-rgb-led-matrix/fonts/5x7.bdf')

        for i, t in enumerate(constants.LOCAL_IP.split('.')):
            graphics.DrawText(
                self.canvas, font, 1, 7 + i * 8,
                graphics.Color(255, 255, 0), t)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def draw_pil_string(self, s):
        pil_image = Image.frombytes('RGB', constants.RGB_MATRIX_SIZE, s)
        # self.matrix.SetImage(pil_image)
        self.canvas.SetImage(pil_image)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def __exit__(self):
        app.App.__exit__(self)
