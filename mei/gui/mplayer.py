import pygame

from mei import theme
import processrunner

class Mplayer(processrunner.ProcessRunner):
    def __init__(self, app, path, files):
        cmd = ['mplayer', '-fs'] + files

        super(Mplayer, self).__init__(app, cmd, path, theme.get('processrunner/mplayer'))
