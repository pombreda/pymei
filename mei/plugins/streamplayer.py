import pygame

from mei import plugin
from mei.gui import util, vlc

class StreamPlayer(plugin.Plugin, vlc.Vlc):
    DEFAULT_CONFIG = {
        'vlc_arguments': []
    }
    def __init__(self, config, app):
        plugin.Plugin.__init__(self)
        vlc.Vlc.__init__(self, app, '.', [config.get('stream').encode()] + config.get('vlc_arguments', []))

        self._app = app
        self._config = config
