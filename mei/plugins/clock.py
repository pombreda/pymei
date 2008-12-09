import pygame
import time

from mei import theme, plugin, datafiles
from mei.gui import util

class Clock(plugin.GlobalPlugin):
    DEFAULT_CONFIG = {
        'format': '%R'
    }

    def __init__(self, app, config):
        super(Clock, self).__init__()
        self._app = app
        self._theme = theme.get('plugins/clock')
        self._font = pygame.font.Font(datafiles.get(self._theme['font']), self._theme['font_size'])

        self._format = config['format']

    def after_draw(self, screen):
        date = time.strftime(self._format)
        w = self._font.size(date)[0]

        util.drawText(screen, self._font, (screen.get_size()[0] - w - self._theme['padding'], self._theme['padding']), date, self._theme['font_color'])
