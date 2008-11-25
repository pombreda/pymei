import pygame

from mei import datafiles
import widget

class Window(widget.Widget):
    def __init__(self, background=None):
        if not background:
            background = datafiles.get('bg-gloomy-720p.jpg')
        self._bg = pygame.image.load(background)

    def draw(self, screen):
        screen.blit(self._bg, (0, 0))
