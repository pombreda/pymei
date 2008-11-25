import os
import signal
import pygame

import util
import widgets

class ProcessRunner(widgets.Window):
    def __init__(self, app, cmd, path, theme):
        super(ProcessRunner, self).__init__()

        self._pid = None
        self._app = app
        self._cmd = cmd
        self._path = path

        self._theme = theme
        self._font = pygame.font.Font(self._theme['font'], self._theme['font_size'])
        self._clock = pygame.time.Clock()

        self._process_dead = False
        self._old_sig = signal.signal(signal.SIGCHLD, self.processExit)

    def key(self, event):
        if event.key == pygame.K_LSUPER or event.key == pygame.K_RSUPER:
            if self._pid:
                os.kill(self._pid, signal.SIGKILL)
            self._app.windows.pop()

    def processExit(self, signum, stackframe):
        self._process_dead = True
        signal.signal(signal.SIGCHLD, self._old_sig)

    def draw(self, screen):
        super(ProcessRunner, self).draw(screen)

        if not self._pid:
            self._pid = os.fork()
            if self._pid == 0:
                os.chdir(self._path)
                print repr(self._cmd)
                os.execvp(self._cmd[0], self._cmd)
                sys.exit(0)

        text1 = '%s is currently running! Press Windows-button to kill it.' % self._cmd[0]
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
            self._app.windows.pop()
