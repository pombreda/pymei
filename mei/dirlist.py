import os

_cache = {}

def get(path):
    path = os.path.abspath(path)
    if path in _cache:
        (mtime, cache) = _cache[path]

        if mtime != os.path.getmtime(path):
            return _refresh(path)
        else:
            return _cache[path][1]
    else:
        return _refresh(path)

def _refresh(path):
    dirs = []
    files = []

    mtime = os.path.getmtime(path)
    for entry in os.listdir(path):
        if entry.startswith('.'):
            continue

        fullpath = os.path.join(path, entry)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            dirs.append(entry)
        else:
            files.append(entry)

    dirs.sort()
    dirs.insert(0, '..')
    files.sort()

    _cache[path] = (mtime, (dirs, files))
    return (dirs, files)
