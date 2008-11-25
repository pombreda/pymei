import math
import pygame

from mei.gui import util
import widget

class ScrollBar(widget.Widget):
    def __init__(self, theme, height):
        self._height = height
        self._theme = theme

    def size(self):
        return (self._theme['width'], self._height)

    def draw(self, shown, top, total, surf=None, pos=None):
        sb_w = self._theme['width']
        if not surf:
            surf = util.alphaSurface(sb_w, self._height)
        if not pos:
            pos = (0, 0)

        # Draw the scrollbar background
        surf.fill(self._theme['background'] + [128], (pos[0], pos[1], sb_w, self._height))

        # Draw the scrollbar indicator
        ## Pixels per entry
        pixel_per_entry = self._height / float(total)
        ## Pixel position of top of indicator
        indicator_top = int(top * pixel_per_entry)
        ## Pixel height of indicator
        indicator_size = int(math.ceil(shown * pixel_per_entry))

        surf.fill(self._theme['color'] + [160], (pos[0], pos[1] + indicator_top, sb_w, indicator_size))

        return surf
