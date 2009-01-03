import os
import re

from mei import dirlist, config, plugin
from mei.gui import filebrowser, mplayer, mplayerembedded

class VideoBrowser(plugin.Plugin, filebrowser.FileBrowser):
    def __init__(self, config, app):
        title = config['title']
        top_path = config['path']

        super(VideoBrowser, self).__init__(title, top_path, app)
        self._app = app
        self._listview.hilight_callback = self._shouldHilight
        self._player = mplayer.Mplayer
        if not config.get('mplayer/separate_window'):
            self._player = mplayerembedded.MplayerEmbedded

    def _shouldHilight(self, i, entry):
        return os.path.exists(self._playedPath(os.path.join(self._path, self._get(i))))
       
    def _playedPath(self, entry):
        return config.get('videobrowser/played_dir') + '/' + entry + '/' + '.played'

    def _markPlayed(self, selected):
        path = self._playedPath(selected)
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        open(path, 'w').close()

    def execute(self, selected):
        is_video = re.compile(r'\.(avi|mpe?g|mp[234]|mkv|wmv|mov|asf|ogm|ogg|divx|flv)$', re.IGNORECASE)
        if os.path.isdir(selected):
            files = filter(is_video.search, dirlist.get(selected)[1])
            if files:
                self._markPlayed(selected)
                self._app.open_window(self._player(self._app, selected, files))
        elif is_video.search(selected):
            self._app.open_window(self._player(self._app, os.path.dirname(selected), [os.path.basename(selected)]))
