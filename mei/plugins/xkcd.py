import os
import urllib2
import re
import shutil

import pygame

from mei import plugin, theme, datafiles
from mei.gui import widgets, util

# To use it:
## Backspace - previous comic
## Space - next comic
## Arrow keys - scroll around (big) comics
## Pgup/Pgdn - scroll quickly up & down

# This whole thing is a big hack.
# It desperately needs to be restructured!
# Currently, XkcdBrowser takes care of displaying and browsing (keyboard).
# XkcdDownloader takes care of fetching stuff.
# It's not very robust, and not very intuitive (no input info). 
# Doesn't even look very good. :-P

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    raise plugin.MissingDependency("BeautifulSoup")

class XkcdBrowser(plugin.Plugin, widgets.Window):
    DEFAULT_CONFIG = {
        'cache_dir': '/tmp/pymei/xkcd_cache'
    }
    DEFAULT_KEYS = {
        'space': 'next_comic',
        'backspace': 'prev_comic',
        'up': 'scroll_up',
        'down': 'scroll_down',
        'left': 'scroll_left',
        'right': 'scroll_right',
        'q': 'quit'
    }

    def __init__(self, config, app):
        super(XkcdBrowser, self).__init__()

        self._app = app

        self._current_comic = None
        self._current_data = None

        self._downloader = XkcdDownloader(config['cache_dir'])

        self._theme = mytheme = theme.get('plugins/xkcd')
        self._heading = pygame.font.Font(datafiles.get(mytheme['font']), mytheme['heading_size'])

        self._padding = mytheme.get('padding', 5)
        self._frame_y = self._padding * 2 + self._heading.get_linesize()
        self._frame_x = self._padding

        screen_w, screen_h = app.screen.get_size()

        frame_height = screen_h - self._frame_y - self._padding * 2 - self._heading.get_linesize() 
        font = pygame.font.Font(datafiles.get(mytheme['font']), mytheme['font_size'])
        frame_height -= 3 * font.get_linesize() + self._padding

        self._scrollable_frame = widgets.ScrollableImage((screen_w - 2 * self._frame_x, frame_height))

        self._caption_y = self._frame_y + frame_height + self._padding
        self._caption_x = self._padding
        self._caption_frame = widgets.TextBox((screen_w - 2 * self._padding,
                                               screen_h - (self._frame_y + frame_height + self._padding * 2)),
                                              theme_path='/plugins/xkcd')

    def draw(self, screen):
        super(XkcdBrowser, self).draw(screen)

        self._downloader.download(self._current_comic)
        if not self._current_comic:
            self._current_comic = self._downloader.newest

        if not self._current_data:
            self._loadData()
            self._scrollable_frame.setImage(self._current_data[0])
            self._caption_frame.setText(self._current_data[1][1])

        w, h = self._heading.size(self._current_data[1][0])

        util.drawText(screen, self._heading, ((self._app.screen.get_size()[0] - w) / 2, 0), self._current_data[1][0], self._theme['heading_color'])
        self._scrollable_frame.draw(screen, (self._frame_x, self._frame_y))
        self._caption_frame.draw(screen, (self._caption_x, self._caption_y))

    def _loadData(self):
        imagefile, textfile = self._downloader.getCache(self._current_comic)
        if not imagefile or not textfile:
            return

        image = pygame.image.load(imagefile)
        fobj = open(textfile)
        text = map(str.strip, fobj.readlines())
        fobj.close()

        self._current_data = (image, text)

    # Key actions!
    def next_comic(self, key):
        last_comic = self._downloader.getCachedComics()[-1]

        self._current_data = None
        if not self._current_comic:
            self._current_comic = 1
        else:
            self._current_comic = (self._current_comic % last_comic) + 1

    def prev_comic(self, key):
        last_comic = self._downloader.getCachedComics()[-1]

        self._current_data = None
        if not self._current_comic:
            self._current_comic = last_comic
        elif self._current_comic == 1:
            self._current_comic = self._downloader.newest_comic
        else:
            self._current_comic -= 1

    def quit(self, key):
        self._app.close_window()

    def scroll_up(self, key):
        self._scrollable_frame.scrollY(-50)

    def scroll_down(self, key):
        self._scrollable_frame.scrollY(50)

    def scroll_left(self, key):
        self._scrollable_frame.scrollX(-50)

    def scroll_right(self, key):
        self._scrollable_frame.scrollX(50)

#        elif event.key == pygame.K_PAGEUP:
#            self._scrollable_frame.scrollY(-200)
#        elif event.key == pygame.K_PAGEDOWN:
#            self._scrollable_frame.scrollY(200)

class XkcdDownloader(object):
    def __init__(self, cache_dir):
        self._newest_comic = None
        self._index = None
        self._cache = cache_dir
        if not os.path.isdir(self._cache):
            os.makedirs(self._cache)

    @property
    def newest(self):
        return self._newest_comic

    def _parse(self, path=''):
        data = urllib2.urlopen('http://xkcd.com/%s' % path)
        page = BeautifulSoup(data)
        data.close()

        return page

    def getCache(self, comic_num):
        path = os.path.join(self._cache, str(comic_num))
        img = None

        for ext in ['png', 'jpg', 'jpeg', 'gif']:
            fn = "%s.%s" % (path, ext)
            if os.path.isfile(fn):
                img = fn
                break

        fn = "%s.txt" % path
        if os.path.isfile(fn):
            return (img, fn)

        return (img, None)

    def getCachedComics(self):
        files = []
        for v in os.listdir(self._cache):
            if not v.endswith('.txt'):
                continue

            fname = v.rsplit('.', 1)[0]
            if fname.isdigit() and not None in self.getCache(int(fname)):
                files.append(int(fname))

        files.sort()

        return files

    @property
    def newest_comic(self):
        if self._newest_comic:
            return self._newest_comic

        if not self._index:
            self._index = self._parse()

        matcher = re.compile('^Permanent link to this comic: http://(?:www.)?xkcd.com/(\d+)/?$')
        for h3 in self._index.findAll('h3'):
            match = matcher.search(h3.string)
            if match:
                self._newest_comic = int(match.group(1))
                return self._newest_comic

        return None

    def download(self, comic=None):
        if not comic:
            comic = self.newest_comic

        image, text = self.getCache(comic)

        if not image or not text:
            if comic == self.newest_comic:
                page = self._index
            else:
                page = self._parse(str(comic))

            img = None
            for i in page.findAll('img'):
                if i['src'].startswith('http://imgs.xkcd.com/comics/'):
                    img = i

            if not img:
                return

        if not image:
            self._downloadComic(page, comic, img)

        if not text:
            self._saveText(page, comic, img)

    def _downloadComic(self, page, comic, img):
        ext = img['src'].rsplit('.', 1)[-1]
        data = urllib2.urlopen(img['src'])
        dest = open("%s.%s" % (os.path.join(self._cache, str(comic)), ext), 'w')
        shutil.copyfileobj(data, dest)
        data.close()
        dest.close()

    def _saveText(self, page, comic, img):
        img_title = None
        if img.has_key('title'):
            img_title = img['title']

        comic_title = None
        h1s = page.findAll('h1')
        if h1s:
            comic_title = h1s[0].string

        if not comic_title or not img_title:
            return

        dest = open("%s.txt" % os.path.join(self._cache, str(comic)), 'w')
        print >>dest, comic_title
        print >>dest, img_title
        dest.close()
