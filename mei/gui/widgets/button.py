import pygame

from mei import datafiles
from mei.gui import util
import widget

class Button(widget.Widget):
    def __init__(self, text, icon, theme):
        self.text = text

        if icon:
            self.icon = pygame.image.load(icon)
        else:
            self.icon = None

        self.font = pygame.font.Font(datafiles.get(theme['font']), theme['font_size'])
        self.theme = theme

    def _drawBox(self, dim, hilight):
        # Draw alpha rects.
        boxsurf = pygame.surface.Surface(dim).convert_alpha()

        if hilight:
            color = self.theme['color_hilight']
        else:
            color = self.theme['color']

        boxsurf.fill(color + [128])
        w = self.theme['border_width']
        pygame.draw.lines(boxsurf, color, True, [(0, 0), (dim[0]-1, 0), (dim[0]-1, dim[1]-1), (0, dim[1]-1)])
        return boxsurf

    def draw(self, surf, pos, hilight):
        dim = self.getDimensions()

        surf.blit(self._drawBox(dim, hilight), pos)

        (x, y) = pos
        y += self.theme['padding']

        (font_w, font_h) = self.font.size(self.text)

        if self.icon:
            x += self.theme['padding']

            (icon_w, icon_h) = self.icon.get_size()

            icon_y = y
            if icon_h < font_h:
                icon_y += (font_h - icon_h)/2
            else:
                y += (icon_h - font_h)/2

            surf.blit(self.icon, (x, icon_y))
            x += icon_w
    
        x += self.theme['padding']
        util.drawText(surf, self.font, (x, y), self.text, self.theme['font_color'])

        return dim

    def getDimensions(self):
        # Size of text
        (w, h) = self.font.size(self.text)

        if self.icon:
            # Padding between text and icon
            w += self.theme['padding']
            (icon_w, icon_h) = self.icon.get_size()

            # Icon width
            w += icon_w

            # If icon is taller than the font, we need to use the right one
            if icon_h > h:
                h = icon_h

        # Padding between edge and text (or icon), left & right, and border
        w += self.theme['padding'] * 2 + self.theme['border_width']
        # Padding between edge and text and icon, top & bottom, and border
        h += self.theme['padding'] * 2 + self.theme['border_width']

        return (w, h)
