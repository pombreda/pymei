import logging
import pygame

from mei import plugin

try:
    import pylirc
except ImportError:
    raise plugin.MissingDependency("pylirc")

class LircError(Exception):
    pass

class LircInput(plugin.GlobalPlugin):
    _KEY_LOOKUP = {
        "backspace": pygame.K_BACKSPACE,
        "tab": pygame.K_TAB,
        "return": pygame.K_RETURN,

        "clear": pygame.K_CLEAR,
        "pause": pygame.K_PAUSE,
        "escape": pygame.K_ESCAPE,
        "space": pygame.K_SPACE,

        "exclaim": pygame.K_EXCLAIM,
        "quotedbl": pygame.K_QUOTEDBL,
        "hash": pygame.K_HASH,
        "dollar": pygame.K_DOLLAR,
        "ampersand": pygame.K_AMPERSAND,
        "quote": pygame.K_QUOTE,
        "lparenthesis": pygame.K_LEFTPAREN,
        "rparenthesis": pygame.K_RIGHTPAREN,
        "asterisk": pygame.K_ASTERISK,
        "plus": pygame.K_PLUS,
        "comma": pygame.K_COMMA,
        "minus": pygame.K_MINUS,
        "period": pygame.K_PERIOD,
        "slash": pygame.K_SLASH,
        "colon": pygame.K_COLON,
        "semicolon": pygame.K_SEMICOLON,
        "less-than": pygame.K_LESS,
        "equals": pygame.K_EQUALS,
        "greater-than": pygame.K_GREATER,
        "question mark": pygame.K_QUESTION,
        "at": pygame.K_AT,
        "lbracket": pygame.K_LEFTBRACKET,
        "rbracket": pygame.K_RIGHTBRACKET,
        "backslash": pygame.K_BACKSLASH,
        "caret": pygame.K_CARET,
        "underscore": pygame.K_UNDERSCORE,
        "grave": pygame.K_BACKQUOTE,
        "euro": pygame.K_EURO,

        "a": pygame.K_a, "b": pygame.K_b,
        "c": pygame.K_c, "d": pygame.K_d,
        "e": pygame.K_e, "f": pygame.K_f,
        "g": pygame.K_g, "h": pygame.K_h,
        "i": pygame.K_i, "j": pygame.K_j,
        "k": pygame.K_k, "l": pygame.K_l,
        "m": pygame.K_m, "n": pygame.K_n,
        "o": pygame.K_o, "p": pygame.K_p,
        "q": pygame.K_q, "r": pygame.K_r,
        "s": pygame.K_s, "t": pygame.K_t,
        "u": pygame.K_u, "v": pygame.K_v,
        "w": pygame.K_w, "x": pygame.K_x,
        "y": pygame.K_y, "z": pygame.K_z,

        "0": pygame.K_0, "1": pygame.K_1,
        "2": pygame.K_2, "3": pygame.K_3,
        "4": pygame.K_4, "5": pygame.K_5,
        "6": pygame.K_6, "7": pygame.K_7,
        "8": pygame.K_8, "9": pygame.K_9,

        "kp_period": pygame.K_KP_PERIOD, "kp_divide": pygame.K_KP_DIVIDE,
        "kp_multiply": pygame.K_KP_MULTIPLY, "kp_minus": pygame.K_KP_MINUS,
        "kp_plus": pygame.K_KP_PLUS, "kp_enter": pygame.K_KP_ENTER,
        "kp_equals": pygame.K_KP_EQUALS,

        "up": pygame.K_UP, "down": pygame.K_DOWN,
        "right": pygame.K_RIGHT, "left": pygame.K_LEFT,

        "insert": pygame.K_INSERT, "delete": pygame.K_DELETE,
        "home": pygame.K_HOME, "end": pygame.K_END, 
        "pageup": pygame.K_PAGEUP, "pagedown": pygame.K_PAGEDOWN,

        "F1": pygame.K_F1, "F2": pygame.K_F2,
        "F3": pygame.K_F3, "F4": pygame.K_F4,
        "F5": pygame.K_F5, "F6": pygame.K_F6,
        "F7": pygame.K_F7, "F8": pygame.K_F8,
        "F9": pygame.K_F9, "F10": pygame.K_F10,
        "F11": pygame.K_F11, "F12": pygame.K_F12,
        "F13": pygame.K_F13, "F14": pygame.K_F14,
        "F15": pygame.K_F15, 

        "numlock": pygame.K_NUMLOCK, "capslock": pygame.K_CAPSLOCK,
        "scrollock": pygame.K_SCROLLOCK,
        "shift": pygame.K_LSHIFT,
        "lshift": pygame.K_LSHIFT,
        "rshift": pygame.K_RSHIFT,
        "ctrl": pygame.K_LCTRL,
        "lctrl": pygame.K_LCTRL,
        "rctrl": pygame.K_RCTRL,
        "alt": pygame.K_LALT,
        "lalt": pygame.K_LALT,
        "ralt": pygame.K_RALT,
        "meta": pygame.K_LMETA,
        "lmeta": pygame.K_LMETA,
        "rmeta": pygame.K_RMETA,
        "windows": pygame.K_LSUPER,
        "lwindows": pygame.K_LSUPER,
        "rwindows": pygame.K_RSUPER,
        "shift": pygame.K_MODE,
        "help": pygame.K_HELP,
        "screen": pygame.K_PRINT,
        "sysrq": pygame.K_SYSREQ,
        "break": pygame.K_BREAK,
        "menu": pygame.K_MENU,
        "power": pygame.K_POWER
    }

    DEFAULT_CONFIG = {
        'configuration': None,
        'name': 'pymei'
    }

    def __init__(self, app, config):
        conffile = config['configuration']
        name = config['name']

        if conffile:
            self._lirc = pylirc.init(name, conffile)
        else:
            self._lirc = pylirc.init(name)

        if not self._lirc:
            raise LircError('Cannot init pylirc')

    def generate_events(self):
        events = pylirc.nextcode(False)

        for event in events:
            if event in self._KEY_LOOKUP:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                  key=self._KEY_LOOKUP[event],
                                  unicode=event, # This should really be
                                                 # something that combines
                                                 # the modifiers.
                                  scancode=None))

                # Meh, is this "good enough"? We should only look
                # at KEYDOWN, so it shouldn't be too bad.
                pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                  key=self._KEY_LOOKUP[event]))

    def quit(self):
        pylirc.exit()

