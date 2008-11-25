import re
import sys
import operator
import os
import logging

class Plugin(object):
    pass

def load_plugins(plugin_path):
    if not os.path.isdir(plugin_path):
        return

    plugre = re.compile(r'^[A-Za-z_]+\.py$')
    files = filter(lambda x: os.path.isfile(os.path.join(plugin_path, x)), os.listdir(plugin_path))
    plugins = filter(plugre.search, files)
    plugins = [p[:-3] for p in plugins]

    sys.path.insert(0, plugin_path)
    for plugin in plugins:
        try:
            logging.debug("Loading plugin '%s' from '%s'", plugin, plugin_path)
            __import__(plugin, fromlist=[''])
        except:
            logging.warn("Could not load plugin file '%s' from '%s'", plugin, plugin_path, exc_info=1)
    sys.path = sys.path[1:]

def get_plugin(name):
    for plugin in Plugin.__subclasses__():
        if plugin.__name__ == name:
            return plugin
    return None

class _SingletonPlugins(object):
    def __init__(self):
        self._singleton_cache = {}

    def init(self, name, *args, **kwargs):
        if not name in self._singleton_cache:
            self._singleton_cache[name] = get_plugin(name)(*args, **kwargs)
        return self._singleton_cache[name]

    def get_all(self, names):
        names = set(names).intersection(set(self._singleton_cache.iterkeys()))
        return [self._singleton_cache[p] for p in names]

    def get(self, name):
        return self._singleton_cache[name]

    def call(self, names, method, *args, **kwargs):
        for plugin in self.get_all(names):
            if hasattr(plugin, method):
                getattr(plugin, method)(*args, **kwargs)

singletons = _SingletonPlugins()
