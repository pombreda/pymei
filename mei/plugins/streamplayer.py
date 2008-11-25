import pygame

from mei import plugin
from mei.gui import util, vlc

class StreamPlayer(plugin.Plugin, vlc.Vlc):
    def __init__(self, options, app):
        plugin.Plugin.__init__(self)
        vlc.Vlc.__init__(self, app, '.', [options['stream'].encode()])

        self._app = app
        self._options = options

    def key(self, event):
        self._app.windows.pop()
