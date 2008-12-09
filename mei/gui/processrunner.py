import os
import signal
import pygame
import logging

from mei import datafiles
import util
import widgets

def get_path(bin):
    path = os.environ.get('PATH')
    if not path:
        path = os.defpath

    for dir in path.split(os.pathsep):
        file = os.path.join(dir, bin)
        if os.path.isfile(file) and os.access(file, os.X_OK):
            return file

    return None

class ProcessRunner(widgets.Window):
    DEFAULT_KEYS = {
        'q': 'quit',
        'escape': 'quit'
    }

    def __init__(self, app, cmd, path, theme):
        super(ProcessRunner, self).__init__()

        self._pid = None
        self._app = app
        self._cmd = cmd
        self._path = path

        self._theme = theme
        self._font = pygame.font.Font(datafiles.get(self._theme['font']), self._theme['font_size'])
        self._clock = pygame.time.Clock()

        self._should_fullscreen = app.getFullscreen()
        logging.debug("ProcessRunner starts, _should_fullscreen is %s" % self._should_fullscreen)

        self._process_dead = False
        self._old_sig = signal.signal(signal.SIGCHLD, self.processExit)

    def processExit(self, signum, stackframe):
        os.wait()

        self._process_dead = True
        signal.signal(signal.SIGCHLD, self._old_sig)
        self._pid = None

    def _start(self):
        if self._should_fullscreen:
            self._app.setFullscreen(False)

        self._pid = os.fork()
        if self._pid == 0:
            os.chdir(self._path)
            os.execvp(self._cmd[0], self._cmd)
            sys.exit(0)

    def _quit(self):
        if self._pid:
            os.kill(self._pid, signal.SIGKILL)

        logging.debug("ProcessRunner is quitting, _should_fullscreen is %s" % self._should_fullscreen)
        if self._should_fullscreen:
            self._app.setFullscreen(True)

        self._app.close_window()

    def draw(self, screen):
        super(ProcessRunner, self).draw(screen)

        if not self._pid:
            self._start()

        text1 = '%s is currently running!' % self._cmd[0]
        text2 = 'Command: %s "%s"' % (self._cmd[0], '" "'.join(self._cmd[1:]))

        (width1, height1) = self._font.size(text1)
        (width2, height2) = self._font.size(text2)

        height = height1 + height2

        (screen_width, screen_height) = screen.get_size()
        x1 = (screen_width - width1) / 2
        x2 = (screen_width - width2) / 2
        y = (screen_height - height) / 2

        util.drawText(screen, self._font, (x1, y), text1, self._theme['font_color'])
        util.drawText(screen, self._font, (x2, y + height1), text2, self._theme['font_color'])

        self._clock.tick(1)

        if self._process_dead:
            self._quit()

    # Key bindings. ;-)
    def action_quit(self, _):
        self._quit()
