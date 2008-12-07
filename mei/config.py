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

_values = {}

# Recursive copy-update for dicts.
# This means we perform a deep-copy. :-)
def deep_dict_update(dest, src):
    for (k, v) in src.iteritems():
        if isinstance(v, dict):
            destv = dest.get(k)
            if not destv or not isinstance(destv, dict):
                dest[k] = {}
            deep_dict_update(dest[k], v)
        else:
            dest[k] = v

def merge(first, second):
    merged = {}
    deep_dict_update(merged, first)
    deep_dict_update(merged, second)
    return merged

def load(fname):
    global _values
    _values = merge(DEFAULT_CONFIG, yaml.load(open(fname)))

def get(key):
    keys = key.split('/')

    conf = _values
    for key in keys[:-1]:
        if isinstance(conf, dict) and key in conf:
            conf = conf[key]
        else:
            return None

    return conf[keys[-1]]
