from pygame import surface

def drawText(surf, font, position, text, color):
    text = font.render(text, True, color)
    surf.blit(text, position)

def alphaSurface(width, height, *args, **kwargs):
    surf = surface.Surface((width, height), *args, **kwargs).convert_alpha()
    surf.fill((0, 0, 0, 0))

    return surf


def center(surface_area, center_area, center_width=None, center_height=None):
    if center_height is not None:
        surface_width = surface_area
        surface_height = center_area
    else:
        (surface_width, surface_height) = surface_area
        (center_width, center_height) = center_area

    x = int((surface_width - center_width)/2.0 + 0.5)
    y = int((surface_height - center_height)/2.0 + 0.5)

    return (x, y)

