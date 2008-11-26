import pygame

from mei import theme
import processrunnerembedded

class MplayerEmbedded(processrunnerembedded.ProcessRunnerEmbedded):
    def __init__(self, app, path, files):
        wminfo = pygame.display.get_wm_info()
        wid = wminfo['window']
        cmd = ['mplayer', '-fs', '-wid', str(wid)] + files

        super(MplayerEmbedded, self).__init__(app, cmd, path, theme.get('processrunner/mplayer'))
