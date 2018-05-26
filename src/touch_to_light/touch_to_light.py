import os
import time
import logging
import functools
from PIL import Image, ImageDraw

from rgbmatrix import RGBMatrix #, graphics
from infra.app import app
from infra.modules.sensors.mpr121 import electrodes
from interactive_leds.src.touch_to_light import constants


class TouchToLight(app.App):
    _logger = logging.getLogger('touch_to_light')


    def __init__(self, globals):
        app.App.__init__(self, constants)
        self._modules.extend((electrodes.mpr121.registers_tree, electrodes.mpr121.i2c_mux, electrodes.mpr121, electrodes))

        if not hasattr(globals, 'matrix'):
            globals.matrix = RGBMatrix(options=constants.RGB_MATRIX_OPTIONS)
        self.matrix = globals.matrix

        self.image = Image.new('RGB', constants.RGB_MATRIX_SIZE)
        self.draw = ImageDraw.Draw(self.image)

        self.electrodes = electrodes.Mpr121ElectrodesGrid(
            constants.MPR121_MAP, constants.ELECTRODES_SIZE, constants.RGB_MATRIX_SIZE)
        # self.run()

    def run(self):
        SIZE = 3
        while True:
            self.electrodes.update()
            touched_electrodes = self.electrodes.get_touched()
            for i in touched_electrodes:
                x, y = i.mid_pixel
                self.draw.ellipse((x - SIZE, y - SIZE, x + SIZE, y + SIZE), fill=(0, 0, 0), outline=(0, 0, 255))
            self.matrix.SetImage(self.image, 0, 0)
            self.draw.rectangle((0, 0) + constants.RGB_MATRIX_SIZE, fill=(0, 0, 0))
            time.sleep(0.01)

    def __exit__(self):
        app.App.__exit__(self)
