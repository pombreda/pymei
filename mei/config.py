import yaml

DEFAULT_CONFIG = {
    'debug': False,
    'application': {
        'fullscreen': False,
        'resolution': (800, 600),
        'theme': 'default',
        'min_fps': 0.5,
        'max_fps': 20,
        'plugins': {}
    }, 'videobrowser': {
        'played_dir': '/tmp/played'
    }, 'mplayer': {
        'separate_window': False
    }, 'menu': {
        'choices': []
    }
}

values = {}

# Recursive copy-update for dicts.
# This means we perform a deep-copy. :-)
def _deep_dict_update(dest, src):
    print repr((dest, src))
    for (k, v) in src.iteritems():
        print repr((k, v))
        if isinstance(v, dict):
            destv = dest.get(k)
            if not destv or not isinstance(destv, dict):
                dest[k] = {}
            _deep_dict_update(dest[k], v)
        else:
            dest[k] = v

def load(fname):
    global values

    values = {}
    _deep_dict_update(values, DEFAULT_CONFIG)
    _deep_dict_update(values, yaml.load(open(fname)))

def get(key):
    return values[key]
