import pygame

from mei import theme, plugin, datafiles
from mei.gui import util, widgets

class HelloWorld(plugin.Plugin, widgets.Window):
    DEFAULT_KEYS = {
        'all': 'quit'
    }

    def __init__(self, config, app):
        super(HelloWorld, self).__init__()
        self._img = pygame.image.load(datafiles.get('icon_porn.png'))
        self._app = app

    def draw(self, screen):
        super(HelloWorld, self).draw(screen)
        screen.blit(self._img, util.center(screen.get_size(), self._img.get_size()))

    def action_quit(self, _):
        self._app.close_window()
