import time
import pygame
import random
import logging

from . import constants
from ..game_base import game_base


class TouchTest(game_base.GameBase):
    _logger = logging.getLogger('touch_test')

    @staticmethod
    def _get_rand_color():
        return tuple(random.randrange(256) for _ in range(3))

    def step(self, time_diff, events):
        # update electrodes
        self.gameplay.electrodes.update()
        # randomly colorize newly touched electrodes
        for i in self.gameplay.electrodes.get_newly_touched():
            self._logger.info('elec %s,\t%s', i.index, i.grid_indexes)
            pygame.draw.ellipse(
                self.surface, self._get_rand_color(), i.rect,
                random.randrange(4))
        # colorize newly released electrodes with RELEASED_COLOR
        for i in self.gameplay.electrodes.get_newly_released():
            pygame.draw.ellipse(
                self.surface, constants.RELEASED_COLOR, i.rect)
