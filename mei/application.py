import pygame
import time

import plugin, theme

class Application(object):
    def __init__(self, entrypoint, config):
        pygame.display.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])

        self.configfile = config 
        self._config = config['application']
        theme.load(self._config['theme'])

        self._fullscreen = bool(self._config['fullscreen'])
        self._initScreen()

        self._plugins = self._config['plugins'].keys()
        for pname in self._plugins:
            plugin.singletons.init(pname, self, self._config['plugins'][pname])

        self.windows = []
        self.continue_running = True

        # Sets a recurring event that'll "wake" the loop at least every X ms, so
        # we'll have at least that many FPS. :)
        pygame.time.set_timer(pygame.USEREVENT, int(1.0/self._config['min_fps']*1000))

        self.clock = pygame.time.Clock()
        self.windows.append(entrypoint(self))

    def _initScreen(self):
        flags = pygame.DOUBLEBUF
        if self._fullscreen:
            flags |= pygame.HWSURFACE | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(self._config['resolution'], flags)

        pygame.display.set_caption('PyMei')
        return self.screen

    def setFullscreen(self, value):
        if value != self._fullscreen:
            print "New fullscreen state %s" % value
            self._fullscreen = value
        self._initScreen()

    def getFullscreen(self):
        return self._fullscreen

    fullscreen = property(getFullscreen, setFullscreen)

    def _handleEvent(self, event):
        if hasattr(event, 'key') and event.type == pygame.KEYDOWN:
            # TODO: Should this be able to "intercept" the keypress
            # so that the window doesn't receive it?
            plugin.singletons.call(self._plugins, 'key', event)
            if self.windows:
                self.windows[-1].key(event)

    def run(self):
        self.screen.fill((0, 0, 0))

        if not self.windows:
            return False

        plugin.singletons.call(self._plugins, 'before_draw', self.screen)
        self.windows[-1].draw(self.screen)
        plugin.singletons.call(self._plugins, 'after_draw', self.screen)
    
        pygame.display.flip()

        plugin.singletons.call(self._plugins, 'generate_events')

        self._handleEvent(pygame.event.wait())
        for event in pygame.event.get():
            self._handleEvent(event)

        self.clock.tick(self._config['max_fps'])
        return self.continue_running

    def quit(self):
        pygame.quit()
        plugin.singletons.call(self._plugins, 'quit')
