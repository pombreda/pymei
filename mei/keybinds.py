import logging
import pygame
import functools

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
        if key == '*':
            pkey = '*'
        else:
            pkey = _get_pykey(key)

        if not pkey:
            logging.error('Global keybinding invalid, keyname %s isnt known.', key)
            continue

        if pkey in _keybinds_global:
            if not ignore_dupes:
                logging.warn('Global key %s is already bound.', key)
            continue

        meth = 'action_%s' % action
        handler = _get_handler(instance, meth)
        if handler is None:
            logging.error('%s is not a valid action to bind to!', action)
        else:
            _keybinds_global[pkey] = handler

def load_bindings(name, details, ignore_dupes=False):
    if not name in _keybinds:
        _keybinds[name] = {}

    section = _keybinds[name]

    for (key, action) in details.iteritems():
        if key == '*':
            pkey = '*'
        else:
            pkey = _get_pykey(key)

        if not pkey:
            logging.error('Keybinding for %s.%s invalid, keyname %s invalid.', name, action, key)
            continue

        if pkey in section:
            if not ignore_dupes:
                logging.warn('Key %s in %s is already bound to %s.', key, name, section[pkey])
            continue

        section[pkey] = action

def _get_handler_static_arg(meth, arg):
    def wrapped_meth(*args):
        input_args = list(args)
        input_args.append(arg)
        return meth(*input_args)

    return wrapped_meth

def _get_handler(inst, act):
    meth = act
    args = None

    if ' ' in act:
        meth, args = act.split(' ', 1)

    if not hasattr(inst, meth):
        return None

    func = getattr(inst, meth)
    if not func.func_code.co_argcount in xrange(2, 4):
        logging.error('Handler for %s is broken! Report to author. :-)', meth)
        return None

    if args is None:
        return func
    else:
        if func.func_code.co_argcount != 3:
            logging.error('%s does not take a parameter. Fix your keybinds in the configuration!', meth)
            return None

        return _get_handler_static_arg(func, args)

def _call_handler(inst, meth, arg):
    meth = 'action_%s' % meth

    handler = _get_handler(inst, meth)

    if handler is None:
        return False

    handler(arg)
    return True

def handle_key(key, current_window):
    if key in _keybinds_global:
        # Allow interception?
        _keybinds_global[key](key)
    elif '*' in _keybinds_global:
        _keybinds_global['*'](key)

    if not current_window:
        logging.warn('No active window; ignoring key input.')
        return

    name = current_window.__class__.__name__
    if not name in _keybinds:
        logging.debug('No keybindings for %s, ignoring key input.', name)
        return

    section = _keybinds[name]
    if not key in section and not '*' in section:
        logging.debug('Ignoring keypress %s, not bound.', key)
    else:
        if not key in section:
            key = '*'

        if not _call_handler(current_window, section[key], key):
            logging.error('Invalid action %s for %s.', section[key], name)
