import os

_searchpath = ['.']

def set_searchpath(search):
    global _searchpath
    _searchpath = search

def get(fname):
    for dir in _searchpath:
        path = os.path.join(dir, 'data', fname)
        if os.path.isfile(path):
            return path

    return os.path.join(_searchpath[0], 'data', fname)
