import pygame

from mei.gui import util
from mei import theme, datafiles
import widget
import constants

def _wordBoundary(text, index):
    while index and not text[index].isspace():
        index -= 1

    return index

class TextBox(widget.Widget):
    def __init__(self, size, align=constants.CENTER, theme_path='/', text=None):
        super(TextBox, self).__init__()

        self._w, self._h = size

        self._align = align
        self._surface = util.alphaSurface(*size)
        self._theme = theme.get(theme_path)
        self._text = None
        self._font = pygame.font.Font(datafiles.get(self._theme['font']), self._theme['font_size'])

        if text:
            self.setText(text)

    def _splitLines(self, text):
        w, h = self._w, self._h

        y = self._font.get_linesize()

        outlines = []

        lines = text.splitlines()
        lines.reverse()
        while lines and y < h:
            first_part = line = lines.pop()
            remains = ''

            t_w, t_h = self._font.size(line)
            y += t_h

            idx = _wordBoundary(line, len(line)-1)
            while t_w >= w and idx > 0:
                idx = _wordBoundary(line, idx - 1)
                first_part, remains = line[:idx], line[idx:]
                t_w, t_h = self._font.size(first_part)

            if remains:
                lines.append(remains)

            outlines.append(first_part)

        # If everything didn't fit, append some dots.
        if lines:
            outlines[-1] = outlines[-1][:-4] + '...'

        return outlines

    def setText(self, text):
        if text == self._text:
            return

        self._text = text

        self._surface.fill((0, 0, 0, 0))

        y = 0
        lines = self._splitLines(text)
        for line in lines:
            y += self._drawLine(line, y)

    def _drawLine(self, line, y):
        t_w, t_h = self._font.size(line)

        if self._align == constants.LEFT:
            x = 0
        elif self._align == constants.RIGHT:
            x = self._w - t_w
        elif self._align == constants.CENTER:
            x = (self._w - t_w) / 2

        util.drawText(self._surface, self._font, (x, y), line, self._theme['font_color'])

        return t_h

    def draw(self, screen, pos):
        #pos = (pos[0] + self._x, pos[1] + self._y)
        #area = (self._im_x, self._im_y, self._w, self._h)
        screen.blit(self._surface, pos)
