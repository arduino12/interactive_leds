import time
import pygame
import random
import logging

from . import constants as C
from ..game_base import game_base


class TouchCirclesTest(game_base.GameBase):
    _logger = logging.getLogger('touch_circles_test')

    def __init__(self, gameplay):
        game_base.GameBase.__init__(self, gameplay)

    def get_elecs_bounding_rects(self):
        s = pygame.Surface(self.gameplay.constants.RGB_MATRIX_SIZE)
        for i in self.gameplay.electrodes.get_touched():
            pygame.draw.circle(s, C.C.WHITE, i.mid_pixel, 6)
        s.set_colorkey((0, 0, 0))
        m = pygame.mask.from_surface(s)
        return m.get_bounding_rects()

    def step(self, time_diff, events):
        # clear screen
        self.surface.fill(C.C.BLACK)
        # update electrodes
        self.gameplay.electrodes.update()
        # update electrodes
        rects = self.get_elecs_bounding_rects()
        # self._logger.info('bounding_rects: %s', rects)
        for i in rects:
            pygame.draw.ellipse(
                self.surface, C.CIRCLE_COLOR, i, 1)

        for i in self.gameplay.electrodes.get_touched():
            pygame.draw.ellipse(
                self.surface, C.ELECTRODE_COLOR, i.rect, 3)

        mid_pixels = [i.center for i in rects]
        for i, a in enumerate(mid_pixels):
            for b in mid_pixels[i:]:
                pygame.draw.line(
                    self.surface, C.LINE_COLOR, a, b)
