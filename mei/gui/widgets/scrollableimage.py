import pygame

from mei.gui import util
import window
import widget
    
def _clamp(i, min, max):
    if i < min:
        return min
    if i > max:
        return max

    return i

class ScrollableImage(widget.Widget):
    def __init__(self, size, image=None):
        super(ScrollableImage, self).__init__()

        self._w, self._h = size
        self._x, self._y = 0, 0

        if image:
            self.setImage(image)

    def setImage(self, image):
        self._image = image
        im_w, im_h = image.get_size()

        self._x = 0
        self._y = 0
        self._im_x = 0
        self._im_y = 0

        if im_w < self._w:
            self._x = (self._w - im_w) / 2

        if im_h < self._h:
            self._y = (self._h - im_h) / 2

    def scrollX(self, delta):
        im_w, _ = self._image.get_size()

        # If image is less than area, don't scroll.
        if im_w < self._w:
            return

        self._im_x = _clamp(self._im_x + delta, 0, im_w - self._w)

    def scrollY(self, delta):
        _, im_h = self._image.get_size()

        # If image is less than area, don't scroll.
        if im_h < self._h:
            return

        self._im_y = _clamp(self._im_y + delta, 0, im_h - self._h)

    def draw(self, screen, pos):
        pos = (pos[0] + self._x, pos[1] + self._y)
        area = (self._im_x, self._im_y, self._w, self._h)
        screen.blit(self._image, pos, area)
