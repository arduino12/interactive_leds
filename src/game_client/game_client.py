import sys
import time
import pygame
import logging
import importlib
from queue import Queue
from threading import Thread

from . import constants
from infra.app import app
from infra.run import app_client
from infra.core import utils


class GameClient(app.App):
    _logger = logging.getLogger('game_client')

    def __init__(self, globals):
        app.App.__init__(self, constants)

        self.gameplay = app_client._App()
        self.gameplay.reconnect()
        self.gameplay.constants = self.gameplay._modules[0]

        self._last_pil_string = ''
        self.gameplay.draw_surface = self.draw_surface

        game_path = sys.argv[-1]
        game_module = importlib.import_module(game_path)
        game_class = getattr(
            game_module,
            utils.module_to_class_name(game_path.rsplit('.', 1)[1]))
        self.game = game_class(self.gameplay)
        self._modules.append(game_module)

        self._runner_q = Queue()
        self._runner = Thread(target=self.run, daemon=True)
        self._runner.start()
        self.set_run(True)

    def run(self):
        status = 1

        while status:
            time.sleep(0.001)
            if not self._runner_q.empty():
                status = self._runner_q.get()
            if status == 1:
                continue

            self.gameplay.electrodes.update()
            self.game.loop(True)

    def set_run(self, is_run):
        self._runner_q.put(2 if is_run else 1)

    def draw_surface(self, surface):
        pil_string = pygame.image.tostring(surface, 'RGB', False)
        if self._last_pil_string != pil_string:
            self._last_pil_string = pil_string
            self.gameplay.draw_pil_string(pil_string)

    def __exit__(self):
        self.set_run(False)
        app.App.__exit__(self)
