from mei import theme
import processrunner

class Vlc(processrunner.ProcessRunner):
    def __init__(self, app, path, files):
        cmd = ['cvlc', '-f'] + files
        super(Vlc, self).__init__(app, cmd, path, theme.get('processrunner/vlc'))
