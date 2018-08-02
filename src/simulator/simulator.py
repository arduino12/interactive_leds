import sys
import pygame
import pygame.locals
import logging
import importlib

import constants
import paws
import electrodes


class InteractiveLedsSimulator(object):
    _logger = logging.getLogger('simulator')

    def __init__(self):
        pygame.init()
        # config gui window
        self.window_surface = pygame.display.set_mode(constants.WINDOW_SIZE)
        pygame.display.set_caption(constants.WINDOW_TITLE)
        # create paws, electrodes and leds objects
        self.paws = paws.Paws(self.window_surface, constants.PAWS_PATH)
        self.electrodes = electrodes.SimulatorElectrodes(
            constants.ELECTRODES_SIZE, constants.RGB_MATRIX_SIZE, self.paws,
            constants.LED_MAP, constants.LED_SEP_PIXELS // 2)
        self.leds_surface = pygame.Surface(self.window_surface.get_size())

        self.constants = constants
        self.running = True
        self._logger.info(
            'Started %s, %s paws', constants.WINDOW_TITLE, len(self.paws.paws))

    def _draw_display(self):
        self.window_surface.blit(self.leds_surface, (0, 0))
        self.paws.draw()
        pygame.display.update()

    def draw_surface(self, surface):
        for y in range(constants.RGB_MATRIX_HEIGHT):
            for x in range(constants.RGB_MATRIX_WIDTH):
                pygame.draw.rect(
                    self.leds_surface, surface.get_at((x, y)),
                    pygame.locals.Rect(
                        constants.LED_MAP[x], constants.LED_MAP[y],
                        constants.LED_SIZE_PIXELS, constants.LED_SIZE_PIXELS))
        self._draw_display()

    def handle_events(self, events):
        needs_redraw = False
        for i in events:
            if i.type == pygame.MOUSEMOTION:
                self.paws.selected_paw.set_mouse_pos(i.pos)
                needs_redraw = True
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    self.paws.selected_paw.toggle_press()
                elif i.button == 3:
                    self.paws.select_next_paw()
                    pygame.mouse.set_pos(
                        self.paws.selected_paw.get_mouse_pos())
                needs_redraw = True
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    self.running = False
            elif i.type == pygame.locals.QUIT:
                self.running = False
        if needs_redraw:
            self._draw_display()


if __name__ == '__main__':
    # config logger
    logging.root.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s: %(message)s',
            '%Y-%m-%d %H:%M:%S'))
    logging.root.addHandler(handler)
    # create simulator
    simulator = InteractiveLedsSimulator()
    # create game object using path from cli-args
    game_path = sys.argv[-1]
    game_module = importlib.import_module(game_path)
    game_class = getattr(
        game_module,
        ''.join(i.title() for i in (game_path.rsplit('.', 1)[-1]).split('_')))
    # start the game
    game = game_class(simulator)
    game.loop()
