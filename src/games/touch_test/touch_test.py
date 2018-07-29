import time
import pygame
import random
import logging

from . import constants


class TouchTest(object):
    _logger = logging.getLogger('touch_test')

    def __init__(self, gameplay):
        pygame.init()
        self.gameplay = gameplay
        self.fps_clock = pygame.time.Clock()
        self.is_simulator = 'Simulator' in str(self.gameplay.__class__)
        self.surface = pygame.Surface(self.gameplay.constants.RGB_MATRIX_SIZE)

    @staticmethod
    def _get_rand_color():
        return tuple(random.randrange(256) for _ in range(3))

    def loop(self):
        while self.gameplay.running:
            # limit framerate
            time_diff = self.fps_clock.tick(constants.FPS)
            # handle pygame events
            for event in pygame.event.get():
                if self.is_simulator:
                    self.gameplay.handle_event(event)
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
            # update display
            self.gameplay.draw_surface(self.surface)
