import socket
import pygame
import logging
from PIL import Image
from rgbmatrix import RGBMatrix, graphics

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

        self.canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont('/home/pi/Public/rpi-rgb-led-matrix/fonts/5x7.bdf')
        my_text = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')] or [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ['no IP found'])[0]
        for i, t in enumerate(my_text.split('.')):
            graphics.DrawText(self.canvas, font, 1, 7 + i * 8, graphics.Color(255, 255, 0), t)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def draw_pil_string(self, s):
        pil_image = Image.frombytes('RGB', constants.RGB_MATRIX_SIZE, s)
        # self.matrix.SetImage(pil_image)
        self.canvas.SetImage(pil_image)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def __exit__(self):
        app.App.__exit__(self)
