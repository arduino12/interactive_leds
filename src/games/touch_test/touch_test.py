import random
import pygame
import logging

from . import constants


class TouchTest(object):
    _logger = logging.getLogger('touch_test')

    def __init__(self, gameplay):
        self.gameplay = gameplay
        self.surface = pygame.Surface(self.gameplay.constants.RGB_MATRIX_SIZE)

    def loop(self, single=False):
        while True:
            for i in self.gameplay.electrodes.get_newly_touched():
                x, y = i.mid_pixel
                self._logger.info('elec %s,\t%s', i.index, i.grid_indexes)
                pygame.draw.ellipse(
                    self.surface,
                    tuple(random.randrange(256) for _ in range(3)),
                    (x - 4, y - 4, 8, 8), random.randrange(4))
            for i in self.gameplay.electrodes.get_newly_released():
                x, y = i.mid_pixel
                pygame.draw.ellipse(
                    self.surface, (0, 20, 0), (x - 4, y - 4, 8, 8))

            self.gameplay.draw_surface(self.surface)

            if single:
                return False
