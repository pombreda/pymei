import pygame

from mei import theme
import processrunner

class Mplayer(processrunner.ProcessRunner):
    def __init__(self, app, path, files):
        cmd = ['mplayer', '-fs'] + files
        wait_for_it = False

        if not app.configfile.get('mplayer').get('separate_window'):
            wminfo = pygame.display.get_wm_info()
            wid = wminfo['window']
            cmd = ['mplayer', '-fs', '-wid', str(wid)] + files
            wait_for_it = True

        super(Mplayer, self).__init__(app, cmd, path, theme.get('processrunner/mplayer'), wait_for_it)
