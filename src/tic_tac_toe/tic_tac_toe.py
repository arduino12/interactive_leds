import os
import time
import pygame
import random
import logging
from queue import Queue
from threading import Thread
from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix

from infra.app import app
from infra.modules.sensors.mpr121 import electrodes
from interactive_leds.src.tic_tac_toe import constants


class TicTacToe(app.App):
    _logger = logging.getLogger('tic_tac_toe')


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
        
        pygame.init()
        self.screen = pygame.Surface(constants.RGB_MATRIX_SIZE)
        
        pygame.mixer.init()

        self._runner_q = Queue()
        self._runner = Thread(target=self.run, daemon=True)
        self._runner.start()
        self.set_run(True)

    def set_run(self, is_run):
        self._runner_q.put(2 if is_run else 1)
    
    def run(self):
        status = 1
        s = pygame.Surface(constants.RGB_MATRIX_SIZE)
        
        while status:
            time.sleep(0.01)
            if not self._runner_q.empty():
                status = self._runner_q.get()
            if status == 1:
                continue

            self.electrodes.update()
            if len(self.electrodes.get_newly_touched()):
                pygame.mixer.Sound('/home/pi/Public/interactive_leds/res/sounds/takaro/005br.wav').play()

            for i in self.electrodes.get_newly_touched():
                x, y = i.mid_pixel
                pygame.draw.ellipse(s, (random.randrange(256), random.randrange(256), random.randrange(256)), (x - 4, y - 4, 8, 8), random.randrange(4))
            for i in self.electrodes.get_newly_released():
                x, y = i.mid_pixel
                pygame.draw.ellipse(s, (0, 0, 0), (x - 4, y - 4, 8, 8))

            pil_string_image = pygame.image.tostring(s, 'RGB',False)
            pil_image = Image.frombytes('RGB', s.get_size(), pil_string_image)
            self.matrix.SetImage(pil_image, 0, 0)

    def __exit__(self):
        self._runner_q.put(0)
        self._runner.join()
        app.App.__exit__(self)
