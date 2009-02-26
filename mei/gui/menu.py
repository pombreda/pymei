import functools
import os
import pygame

from mei import plugin, theme, datafiles, config
from mei.gui import widgets

class Menu(widgets.Window):
    DEFAULT_KEYS = {
        'escape': 'quit',
        'q': 'quit',
        'backspace': 'quit',
        'down': 'next_selection',
        'up': 'previous_selection',
        'right': 'select',
        'return': 'select'
    }

    def __init__(self, app, choices=None):
        super(Menu, self).__init__()

        self._app = app
        self._theme = theme.get('menu')
        self._config = config.get('menu')

        if not choices:
            choices = self._config['choices']

        self._choices = []

        if app.current_window:
            self._choices.append((self.makeButton('Back'), self.goBack))


        for choice in choices:
            type = choice['type'].lower()
            
            if choice['type'].lower() == 'menu':
                func = functools.partial(Menu, choices=choice['choices'])
            else:
                # Apply default config for this plugin.
                default_config = plugin.get_defaults(choice['type'])
                cfg = config.merge(default_config, choice)

                plug = plugin.get_plugin(choice['type'])
                if plug:
                    func = functools.partial(plug, cfg)
                else:
                    print >>sys.stderr, "Config contains plugin %s, but it could not be loaded." % choice['type']
                    continue


            self._choices.append((self.makeButton(choice['title']), func))

        self.selected = 0

    def goBack(self, app):
        app.close_window()
        return None

    def makeButton(self, label):
        icon = datafiles.get('icon_%s.png' % label.lower())
        if not os.path.isfile(icon):
            icon = None

        return widgets.Button(label, icon, theme.get('menu/button'))

    def calcHeight(self):
        h = 0
        for (button, _)  in self._choices:
            h += button.getDimensions()[1]

        h += (len(self._choices) - 1) * self._theme['spacing']

        return h

    def draw(self, screen):
        super(Menu, self).draw(screen)

        y = (screen.get_size()[1] - self.calcHeight())/2
        selected = self.selected
        for (button, _) in self._choices:
            (w, h) = button.getDimensions()
            x = (screen.get_size()[0] - w)/2

            (dx, dy) = button.draw(screen, (x, y), selected == 0)
            selected -= 1

            y += dy + self._theme['spacing']

    # Various key handlers!
    def action_quit(self, _):
        self._app.close_window()

    def action_next_selection(self, _):
        if not self._choices:
            return
        self.selected = (self.selected + 1) % len(self._choices)

    def action_previous_selection(self, _):
        if not self._choices:
            return
        self.selected = (self.selected - 1) % len(self._choices)

    def action_select(self, _):
        if not self._choices:
            return
        win = self._choices[self.selected][1](self._app)
        if win:
            self._app.open_window(win)
