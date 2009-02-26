import re
import sys
import operator
import os
import logging

import config, keybinds

class GlobalPlugin(object):
    pass

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
            logging.info("Could not load plugin '%s', required dependency '%s' is missing.", plugin, dependency)
        except:
            logging.warn("Could not load plugin file '%s' from '%s'", plugin, plugin_path, exc_info=1)
    sys.path = sys.path[1:]

# Get default settings for plugin by given name.
def get_defaults(name, plugins=None):
    plugin = get_plugin(name, plugins)
    if hasattr(plugin, 'DEFAULT_CONFIG'):
        return plugin.DEFAULT_CONFIG
    else:
        return {}

# Get default keybinds for plugin by given name.
def get_default_keys(name, plugins=None):
    plugin = get_plugin(name, plugins)
    if hasattr(plugin, 'DEFAULT_KEYS'):
        return plugin.DEFAULT_KEYS
    else:
        return {}

def get_plugins():
    return ((p, p.__name__) for p in Plugin.__subclasses__())

def get_plugin(name, plugins=None):
    if plugins is None:
        plugins = get_plugins()

    for (plugin, plugname) in plugins:
        if plugname == name:
            return plugin
    return None

class _GlobalPlugins(object):
    def __init__(self):
        self._global_cache = {}

    def init(self, names, app):
        self.update_config(names)

        configs = config.get('application/plugins')
        for name in names:
            if not name in self._global_cache:
                cfg = configs.get(name, {})
                plug = get_plugin(name, self.get_all())
                if plug:
                    self._global_cache[name] = plug(app, cfg)
                else:
                    print >>sys.stderr, "Plugin '%s' is specified in config, but could not be loaded." % name

        self.load_keybinds(names, config.get('keybinds'))

    def get_all(self):
        return ((p, p.__name__) for p in GlobalPlugin.__subclasses__())

    def get_these(self, names):
        names = set(names).intersection(set(self._global_cache.iterkeys()))
        return [self._global_cache[p] for p in names]

    def get_instance(self, name):
        return self._global_cache.get(name)

    def call(self, names, method, *args, **kwargs):
        for plugin in self.get_these(names):
            if hasattr(plugin, method):
                getattr(plugin, method)(*args, **kwargs)

    def update_config(self, names):
        plugin_config = config.get('application/plugins')
        for plugname in names:
            if not plugname in plugin_config:
                plugin_config[plugname] = {}

            default_config = get_defaults(plugname, self.get_all())
            new_config = config.merge(default_config, plugin_config[plugname])

            plugin_config[plugname] = new_config

    def load_keybinds(self, names, binds):
        for plugname in names:
            # First we apply any in configuration.
            if plugname in binds:
                keybinds.load_global(binds[plugname], self.get_instance(plugname))

            # Then we apply the defaults, without overwriting the old ones.
            default_keybinds = get_default_keys(plugname, self.get_all())
            keybinds.load_global(default_keybinds, self.get_instance(plugname), ignore_dupes=True)

globals = _GlobalPlugins()
