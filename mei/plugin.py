import re
import sys
import operator
import os
import logging

import config, keybinds

class Plugin(object):
    pass

class MissingDependency(Exception):
    pass

def load_plugins(plugin_path):
    if not os.path.isdir(plugin_path):
        return

    plugre = re.compile(r'^[^_][A-Za-z_]*\.py$')
    files = filter(lambda x: os.path.isfile(os.path.join(plugin_path, x)), os.listdir(plugin_path))
    plugins = filter(plugre.search, files)
    plugins = [p[:-3] for p in plugins]

    sys.path.insert(0, plugin_path)
    for plugin in plugins:
        try:
            logging.debug("Loading plugin '%s' from '%s'", plugin, plugin_path)
            __import__(plugin, fromlist=[''])
        except MissingDependency, (dependency):
            logging.info("Could not load '%s', required dependency '%s' is missing.", plugin, dependency)
        except:
            logging.warn("Could not load plugin file '%s' from '%s'", plugin, plugin_path, exc_info=1)
    sys.path = sys.path[1:]

# Get default settings for plugin by given name.
def get_defaults(name):
    plugin = get_plugin(name)
    if hasattr(plugin, 'DEFAULT_CONFIG'):
        return plugin.DEFAULT_CONFIG
    else:
        return {}

# Get default keybinds for plugin by given name.
def get_default_keys(name):
    plugin = get_plugin(name)
    if hasattr(plugin, 'DEFAULT_KEYS'):
        return plugin.DEFAULT_KEYS
    else:
        return {}


def get_plugins():
    return ((p, p.__name__) for p in Plugin.__subclasses__())

def get_plugin(name):
    for (plugin, plugname) in get_plugins():
        if plugname == name:
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

    def update_config(self, names):
        plugin_config = config.get('application/plugins')
        for plugname in names:
            if not plugname in plugin_config:
                plugin_config[plugname] = {}

            default_config = get_defaults(plugname)
            new_config = config.merge(default_config, plugin_config[plugname])

            plugin_config[plugname] = new_config

    def apply_default_keybinds(self, names):
        for plugname in names:
            default_keybinds = get_default_keys(plugname)
            keybinds.load_bindings(plugname, default_keybinds, ignore_dupes=True)

singletons = _SingletonPlugins()
