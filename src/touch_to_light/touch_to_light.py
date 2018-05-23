import os
import time
import logging


from infra.app import app
from infra.modules.mpr121.mpr121 import Mpr121
from interactive_leds.src.touch_to_light import constants


class TouchToLight(app.App):
    _logger = logging.getLogger('touch_to_light')


    def __init__(self):
        app.App.__init__(self, constants)
        self._modules.extend((mpr121,))

    def __exit__(self):
        app.App.__exit__(self)
