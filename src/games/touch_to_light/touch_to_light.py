import os
import time
import random
import pygame
import logging
import functools
from queue import Queue
from threading import Thread
from PIL import Image, ImageDraw

from infra.app import app
from infra.run import app_client
from interactive_leds.src.games.touch_to_light import constants


class TouchToLight(app.App):
    _logger = logging.getLogger('touch_to_light')


    def __init__(self, globals):
        app.App.__init__(self, constants)

        self.game = app_client._App()
        self.game.reconnect()

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

            self.game.electrodes.update()

            for i in self.game.electrodes.get_newly_touched():
                x, y = i.mid_pixel
                pygame.draw.ellipse(s, (random.randrange(256), random.randrange(256), random.randrange(256)), (x - 4, y - 4, 8, 8), random.randrange(4))
            for i in self.game.electrodes.get_newly_released():
                x, y = i.mid_pixel
                pygame.draw.ellipse(s, (0, 0, 0), (x - 4, y - 4, 8, 8))

            self.game.draw_pil_string(pygame.image.tostring(s, 'RGB', False))

    def __exit__(self):
        app.App.__exit__(self)
