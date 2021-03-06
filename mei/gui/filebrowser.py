import itertools
import math
import os

import pygame

from mei import dirlist, theme, datafiles, config
from mei.gui import util, widgets

class FileBrowser(widgets.Window):
    DEFAULT_KEYS = {
        'backspace': 'go_up',
        'left': 'go_up',
        'q': 'quit',
        'escape': 'quit',
        'down': 'next_entry',
        'up': 'prev_entry',
        'pagedown': 'next_page',
        'pageup': 'prev_page',
        'home': 'first_entry',
        'end': 'last_entry',
        'right': 'go_selected',
        'return': 'execute_selected'
    }

    def __init__(self, title, top_path, app):
        super(FileBrowser, self).__init__()
        self._top_path = os.path.realpath(top_path)
        self._path = os.path.realpath(top_path)

        self._title = title
        self._app = app

        self.theme = theme.get('filebrowser')
        self._font = pygame.font.Font(datafiles.get(self.theme['font']), self.theme['font_size'])
        self._font.set_bold(True)

        self._listview = widgets.ListView(theme.get('filebrowser/listview'), self._getDisplayList, self._getListLength)

        self.go('.')

        self._scrollbar = widgets.ScrollBar(theme.get('filebrowser/scrollbar'), self._listview.size()[1])

    def _getDisplayList(self):
        for entry in self._content[0]:
            yield '> %s' % entry
        for entry in self._content[1]:
            yield entry

    def _getListLength(self):
        return len(self._content[0]) + len(self._content[1])

    def _getTitle(self):
        return "%s%s" % (self._title, self._path[len(self._top_path):])

    def size(self):
        (width, height) = self._listview.size()

        height += self._font.get_linesize()
        width += self._scrollbar.size()[0]
        
        # prevent the list to go over the screen borders
        resolutionWidth = config.get('application/resolution')[0]
       
        if width > resolutionWidth:
            width = resolutionWidth

        return (width, height)

    def draw(self, screen):
        super(FileBrowser, self).draw(screen)

        (width, height) = self.size()
        (sb_width, sb_height) = self._scrollbar.size()
        browser = util.alphaSurface(width, height)

        # Draw list and render to texture.
        browser.set_clip((0, self._font.get_linesize(), width - sb_width, height))
        list = self._listview.draw(browser, (0, self._font.get_linesize()))
        browser.set_clip()

        # Draw the scrollbar
        if self._getListLength() > self._listview.getViewEntries():
            sb_pos = (width - sb_width, self._font.get_linesize())
            self._scrollbar.draw(self._listview.getViewEntries(), self._listview.top, self._getListLength(), browser, sb_pos)

            # Draw border
            pygame.draw.rect(browser, (0, 0, 0), (0, self._font.get_linesize(), width, height - self._font.get_linesize()), 1)
        else:
            # Draw border without scrollbar.
            pygame.draw.rect(browser, (0, 0, 0), (0, self._font.get_linesize(), width - sb_width, height - self._font.get_linesize()), 1)

        # Blit it all to screen
        (screen_width, screen_height) = screen.get_size()
        x = (screen_width - width) / 2
        y = (screen_height - height) / 2 + self._font.get_linesize()
        screen.blit(browser, (x, y))

        # Draw header (directly to screen)
        header_width = self._font.size(self._path)[0]
        x = (screen_width - header_width) / 2
        util.drawText(screen, self._font, (x, y), self._getTitle(), self.theme['heading_color'])

    def go(self, dir):
        dir = os.path.realpath(os.path.join(self._path, dir))
        if not dir.startswith(self._top_path):
            return

        self._content = dirlist.get(dir)
        
        old_dir = os.path.basename(self._path)
        # This checks if we're "going up a level" (or more). XXX: Breaks if we ever use ../.. etc.
        if self._path.startswith(dir) and old_dir in self._content[0]:
            self._listview.selected = self._content[0].index(old_dir)
        else:
            self._listview.selected = int(self._getListLength() > 1)

        self._path = dir

    def _getSelected(self):
        return self._get(self._listview.selected)

    def _get(self, i):
        if i < len(self._content[0]):
            return self._content[0][i]
        else:
            return self._content[1][i - len(self._content[0])]

    # Keys!
    def action_execute_selected(self, _):
        self.execute(os.path.join(self._path, self._getSelected()))

    def action_go_up(self, _):
        self.go('..')

    def action_go_selected(self, _):
        # Only go if it's a dir. :)
        if self._listview.selected < len(self._content[0]):
            self.go(self._content[0][self._listview.selected])

    def action_quit(self, _):
        self._app.close_window()

    def action_next_entry(self, _):
        self._listview.selected += 1

    def action_next_page(self, _):
        self._listview.selected += self._listview.getViewEntries() / 2

    def action_prev_entry(self, _):
        self._listview.selected -= 1

    def action_prev_page(self, _):
        self._listview.selected -= self._listview.getViewEntries()/ 2

    def action_first_entry(self, _):
        self._listview.selected = 0

    def action_last_entry(self, _):
        self._listview.selected = -1
