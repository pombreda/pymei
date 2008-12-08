import logging
import pygame

_keybinds_global = {}
_keybinds = {}

def _get_pykey(key):
    pkey = 'K_%s' % key.upper()
    if not hasattr(pygame, pkey):
        pkey = 'K_%s' % key.lower()
        if not hasattr(pygame, pkey):
            return None
    return getattr(pygame, pkey)

def load_global(details, instance, ignore_dupes=False):
    for (key, action) in details.iteritems():
        pkey = _get_pykey(key)
        if not pkey:
            logging.error('Global keybinding invalid, keyname %s isnt known.', key)
            continue

        if pkey in _keybinds_global:
            if not ignore_dupes:
                logging.warn('Global key %s is already bound.', key)
            continue

        if not hasattr(instance, action):
            logging.error('%s is not a valid action to bind to!', action)
        else:
            _keybinds_global[pkey] = getattr(instance, action)

def load_bindings(name, details, ignore_dupes=False):
    if not name in _keybinds:
        _keybinds[name] = {}

    section = _keybinds[name]

    for (key, action) in details.iteritems():
        pkey = _get_pykey(key)
        if not pkey:
            logging.error('Keybinding for %s.%s invalid, keyname %s invalid.', name, action, key)
            continue

        if pkey in section:
            if not ignore_dupes:
                logging.warn('Key %s in %s is already bound to %s.', key, name, section[pkey])
            continue

        section[pkey] = action

def _call_handler(inst, meth, arg):
    if not hasattr(inst, meth):
        return False

    getattr(inst, meth)(arg)
    return True

def handle_key(key, current_window):
    if key in _keybinds_global:
        # Allow interception?
        _keybinds_global[key](key)

    if not current_window:
        logging.warn('No active window; ignoring key input.')
        return

    name = current_window.__class__.__name__
    if not name in _keybinds:
        logging.debug('No keybindings for %s, ignoring key input.', name)
        return

    section = _keybinds[name]
    if not key in section:
        logging.debug('Ignoring keypress %s, not bound.', key)
    else:
        if not _call_handler(current_window, section[key], key):
            logging.error('Invalid action %s for %s.', section[key], name)
