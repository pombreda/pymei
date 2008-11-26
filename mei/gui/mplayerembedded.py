import pygame

import os, subprocess, signal

from mei.gui import widgets

class MplayerEmbedded(widgets.Widget):
    def __init__(self, app, path, files):
        super(MplayerEmbedded, self).__init__()

        self._app = app
        self._path = path
        self._files = files

        self._process = None

        self._old_sig = signal.signal(signal.SIGCHLD, self.processExit)


    def processExit(self, signum, stackframe):
        signal.signal(signal.SIGCHLD, self._old_sig)
        self._process = None

    def key(self, event):
        if not self._process:
            return

        key = event.key
        if key in _MPLAYER_LOOKUP:
            key = _MPLAYER_LOOKUP[key]

        print >>self._process.stdin, 'key_down_event %i' % key

    def draw(self, screen):
        if not self._process:
            wminfo = pygame.display.get_wm_info()
            wid = wminfo['window']
            cmd = ['mplayer', '-vo', 'x11', '-zoom', '-slave', '-quiet', '-wid', str(wid)] + self._files

            self._process = subprocess.Popen(cmd, stdin=subprocess.PIPE, cwd=self._path)

        while self._process:
            event = pygame.event.wait()
            if hasattr(event, 'key') and event.type == pygame.KEYDOWN:
                self.key(event)

        self._quit()

    def _quit(self):
        if self._process and self._process.pid is not None:
           os.kill(self._process.pid, signal.SIGKILL) 

        # This ensures a quick redraw. :)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))

        self._app.windows.pop()

from pygame.locals import *
# Based on osdep/keycodes.h, mplayer source snapshot 26/11/2008.
# KEY code definitions for GyS-TermIO v2.0 (C) 1999 A'rpi/ESP-team
_KEY_BASE = 0x100
_KEY_CRSR = _KEY_BASE + 16
_KEY_F = _KEY_BASE + 64
_KEY_KP = _KEY_BASE + 32
_MPLAYER_LOOKUP = {
    K_RETURN: 13,
    K_TAB: 9,
    K_F1: _KEY_F+1,
    K_F2: _KEY_F+2,
    K_F3: _KEY_F+3,
    K_F4: _KEY_F+4,
    K_F5: _KEY_F+5,
    K_F6: _KEY_F+6,
    K_F7: _KEY_F+7,
    K_F8: _KEY_F+8,
    K_F9: _KEY_F+9,
    K_F10: _KEY_F+10,
    K_F11: _KEY_F+11,
    K_F12: _KEY_F+12,
    K_F13: _KEY_F+13,
    K_F14: _KEY_F+14,
    K_F15: _KEY_F+15,

    K_BACKSPACE: _KEY_BASE,
    K_DELETE: _KEY_BASE+1,
    K_INSERT: _KEY_BASE+2,
    K_HOME: _KEY_BASE+3,
    K_END: _KEY_BASE+4,
    K_PAGEUP: _KEY_BASE+5,
    K_PAGEDOWN: _KEY_BASE+6,
    K_ESCAPE: _KEY_BASE+7,

    K_RIGHT: _KEY_CRSR,
    K_LEFT: _KEY_CRSR+1,
    K_DOWN: _KEY_CRSR+2,
    K_UP: _KEY_CRSR+3,

    K_KP0: _KEY_KP,
    K_KP1: _KEY_KP + 1,
    K_KP2: _KEY_KP + 2,
    K_KP3: _KEY_KP + 3,
    K_KP4: _KEY_KP + 4,
    K_KP5: _KEY_KP + 5,
    K_KP6: _KEY_KP + 6,
    K_KP7: _KEY_KP + 7,
    K_KP8: _KEY_KP + 8,
    K_KP9: _KEY_KP + 9,
    K_KP_MINUS: _KEY_KP + 10,
    # + 11: KEY_KPINS
    # + 12: KEY_KPDEL
    K_KP_ENTER: _KEY_KP + 13
}
