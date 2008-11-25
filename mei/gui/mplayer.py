from mei import theme
import processrunner

class Mplayer(processrunner.ProcessRunner):
    def __init__(self, app, path, files):
        if app.configfile.get('mplayer').get('separate_window'):
            cmd = ['mplayer', '-fs'] + files
        else:
            wminfo = pygame.display.get_wm_info()
            wid = wminfo['window']
            cmd = ['mplayer', '-fs', '-wid', str(wid)] + files
        super(Mplayer, self).__init__(app, cmd, path, theme.get('processrunner/mplayer'))
