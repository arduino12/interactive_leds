import pygame

from . import constants


class GameBase(object):

    def __init__(self, gameplay):
        pygame.init()
        self.gameplay = gameplay
        self.fps_clock = pygame.time.Clock()
        self.is_simulator = 'Simulator' in str(self.gameplay.__class__)
        self.surface = pygame.Surface(self.gameplay.constants.RGB_MATRIX_SIZE)

    def step(self, time_diff, events):
        pass

    def loop(self, single=False):
        while self.gameplay.running:
            # limit framerate
            time_diff = self.fps_clock.tick(constants.FPS)
            # handle pygame events
            events = pygame.event.get()
            if self.is_simulator:
                self.gameplay.handle_events(events)
            # step game frame
            self.step(time_diff, events)
            # update surface
            self.gameplay.draw_surface(self.surface)
            # return for single loop
            if single:
                return
