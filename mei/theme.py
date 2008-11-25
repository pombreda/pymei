import os, logging
import yaml

_theme = None
_cache = {}
_searchpath = ['.']

class ThemeError(Exception):
    pass

class ThemeNotLoaded(Exception):
    pass

def set_searchpath(search):
    global _searchpath
    _searchpath = search

def load(theme):
    global _theme
    _theme = None

    for dir in _searchpath:
        path = os.path.join(dir, 'themes', theme)
        if os.path.isfile(path):
            _theme = yaml.load(open(path))
            logging.info("Loading theme from '%s'", path)
            break
    
    if not _theme:
        raise ThemeError("Could not find theme '%s'" % theme)

# Strips out subdicts.
def _strip(theme):
    d = {}
    for (k, v) in theme.iteritems():
        if not isinstance(v, dict): 
            d[k] = v
    return d

def _get(path, theme, current):
    current.update(_strip(theme))

    if path and path[0] in theme and isinstance(theme[path[0]], dict):
        return _get(path[1:], theme[path[0]], current)
    else:
        return current

def get(theme):
    if not _theme:
        raise ThemeNotLoaded()

    path = filter(len, theme.split("/"))

    theme = "/".join(path)
    if not theme in _cache:
        _cache[theme] = _get(path, _theme, {})
    return _cache[theme]
