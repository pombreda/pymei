from mei import theme
import processrunner

class Vlc(processrunner.ProcessRunner):
    def __init__(self, app, path, files):
        bin = 'vlc'
        if processrunner.get_path('cvlc') is not None:
            bin = 'cvlc'

        cmd = [bin, '-f'] + files
        super(Vlc, self).__init__(app, cmd, path, theme.get('processrunner/vlc'))
