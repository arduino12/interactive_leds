import sys
import time
import pygame
import logging
import importlib
from PIL import Image
from queue import Queue
from threading import Thread
from rgbmatrix import RGBMatrix, graphics

from . import constants
from infra.app import app
from infra.core import utils
from infra.modules.sensors.mpr121 import electrodes


class GameServer(app.App):
    _logger = logging.getLogger('game_server')

    def __init__(self, globals):
        app.App.__init__(self, constants)
        self._modules.extend((
            electrodes.mpr121.registers_tree, electrodes.mpr121,
            electrodes.i2c_mux, electrodes))

        if not hasattr(globals, 'matrix'):
            globals.matrix = RGBMatrix(options=constants.RGB_MATRIX_OPTIONS)
        self.matrix = globals.matrix

        self.electrodes = electrodes.Mpr121ElectrodesGrid(
            constants.MPR121_MAP, constants.ELECTRODES_SIZE,
            constants.RGB_MATRIX_SIZE)
        self.electrodes.init()

        self._runner = None
        self._last_pil_string = ''
        self.constants = constants
        self.canvas = self.matrix.CreateFrameCanvas()

        if len(sys.argv) <= 5:
            font = graphics.Font()
            font.LoadFont('/home/pi/Public/rpi-rgb-led-matrix/fonts/5x7.bdf')

            for i, t in enumerate(constants.LOCAL_IP.split('.')):
                graphics.DrawText(
                    self.canvas, font, 1, i * (font.height + 1) + font.height,
                    graphics.Color(255, 255, 0), t)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
        else:
            game_path = sys.argv[-1]
            game_module = importlib.import_module(game_path)
            game_class = getattr(
                game_module,
                utils.module_to_class_name(game_path.rsplit('.', 1)[1]))
            self.game = game_class(self)
            self._modules.append(game_module)

            self._runner_q = Queue()
            self._runner = Thread(target=self._run, daemon=True)
            self._runner.start()
            self.set_run(True)

    def _run(self):
        status = 1
        try:
            while status:
                time.sleep(0.001)
                if not self._runner_q.empty():
                    status = self._runner_q.get()
                if status == 1:
                    continue

                self.electrodes.update()
                self.game.loop(True)
        except Exception:
            self._logger.exception('runner error:')
            self.__exit__()
        else:
            self._logger.info('runner exited')

    def _set_runner(self, status):
        if self._runner is not None:
            self._runner_q.put(status)
            if not status:
                self._runner.join(1)
                if self._runner.is_alive():
                    self._logger.error('runner is still alive')

    def set_run(self, is_run):
        self._set_runner(2 if is_run else 1)

    def draw_pil_string(self, s):
        pil_image = Image.frombytes('RGB', constants.RGB_MATRIX_SIZE, s)
        # self.matrix.SetImage(pil_image)
        self.canvas.SetImage(pil_image)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def draw_surface(self, surface):
        pil_string = pygame.image.tostring(surface, 'RGB', False)
        if self._last_pil_string != pil_string:
            self._last_pil_string = pil_string
            self.draw_pil_string(pil_string)

    def __exit__(self):
        self._set_runner(0)
        app.App.__exit__(self)
