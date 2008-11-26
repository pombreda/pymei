import itertools

import pygame

from mei import datafiles
from mei.gui import util
import window
import widget

class ListView(widget.Widget):
    def __init__(self, theme, populator, length_calc=None):
        super(ListView, self).__init__()

        self.theme = theme
        self.font = pygame.font.Font(datafiles.get(theme['font']), theme['font_size'])

        self.top = 0
        self._selected = 0

        self._populator = populator
        self._length_calc = length_calc
        self.hilight_callback = None

    def _getLength(self):
        if self._length_calc:
            return self._length_calc()
        else:
            return len(list(self._populator()))

    def getViewEntries(self):
        return self.theme['entries']

    def getSelected(self):
        return self._selected

    def setSelected(self, value):
        self._selected = value % self._getLength()
        if self._selected < self.top:
            self.top = self._selected
        elif self._selected >= self.top + self.getViewEntries():
            self.top = self._selected - self.getViewEntries() + 1

    selected = property(getSelected, setSelected)

    def size(self):
        height = (self.font.get_linesize() + self.theme['padding']) * self.getViewEntries() + self.theme['padding']
        width = self.theme['padding'] * 2
        width += max((self.font.size(s)[0] for s in self._populator()))

        if width < self.theme['min_width']:
            width = self.theme['min_width']

        return (width, height)

    def draw(self, surf=None, pos=None):
        (width, height) = self.size()
        if not surf:
            surf = util.alphaSurf(width, height)
        if not pos:
            pos = (0, 0)

        surf.fill(self.theme['background'] + [160], (pos[0], pos[1], width, height))
        self._drawContents(surf, width, pos)

        return surf

    def _drawContents(self, surf, width, pos):
        y = self.theme['padding'] + pos[1]
        x = pos[0]
        for (i, entry) in itertools.islice(enumerate(self._populator()), self.top, self.top + self.getViewEntries()):
            if i == self._selected:
                bar = (x, y, width, self.font.get_linesize())
                surf.fill(self.theme['background_selected'], bar)

            color = self.theme['font_color']
            if self.hilight_callback and self.hilight_callback(i, entry):
                color = self.theme['hilight_color']

            util.drawText(surf, self.font, (x + self.theme['padding'], y), entry, color)

            y += self.font.get_linesize() + self.theme['padding']
