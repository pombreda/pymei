#summary Introduction to the PyMei codebase, and how to contribute.
#labels Featured,Phase-Implementation,Documentation

# Introduction #

The PyMei codebase is (hopefully) extensible by the use of powerful plugins. Like PyMei, these are also written in Python. We hope people will adapt PyMei to their needs, and submit the plugins or patches that these actions create!

# Framework #

## pymei (main executable) ##
pymei finds the appropriate configuration file (either `./pymei.config`, `~/.pymei/config` or `/etc/pymei.config`), initializes the search path of the theme and datafiles modules, loads all the plugins (plugins dir in library package installation dir, e.g. `/usr/lib/python2.5/site-packages/mei/plugins/`), then runs the Application from mei/application.py with the Menu class from mei/gui/menu.py as the main screen.

## application (main event/renderloop) ##
Application is the class that takes care of the main renderloop, and initializes pygame, loads the theme and enforces max/min FPS. In addition, it dispatches key-input events and calls some plugins. (`before_draw`, `after_draw` and `generate_events`)

The Application is basically a stack-based "menu system"; when you transition from one screen to another one, the new "screen" is pushed to the window stack (`Application.windows`).

The renderloop is mostly inactive; whenever it receives an event from pygame (max wait is 1/`min_fps` seconds, where `min_fps` is defined in the Configuration) it dispatches this to the active window and any plugins that care about it, and then redraws the active window.

## theme (theme loader/accessor) ##
Theme is a module that loads a YAML file with a hierarchic structure (dict of dicts), and allows every part of PyMei to access it. Each theme entry is specified using a path, similar to the unix filesystem, for example `filebrowser/scrollbar` (or identically `/filebrowser//scrollbar`). When resolving this, theme.py will first get the theme entries in the root of the `theme`, then update these with the ones in `theme['filebrowser']` (overwriting any duplicate names), then finally update them with `theme['filebrowser']['scrollbar']` (still overwriting any duplicates).

This should in theory reduce verbosity of themes by allowing common options (like font colors) to be set in the root, and not ahve to be repeated at each stage.

See WritingThemes for more information about how they're laid out.

## datafiles (datafile path resolver) ##
datafiles is a simple module that, given a filename, finds the correct path. It does this by looking for it in the data subdirectory of three different paths: `./`, `~/.pymei` and `/usr/share/pymei`. This allows users to overwrite data files or install new themes, in their `~/.pymei` directory.

## plugin (plugin manager and base class) ##
There are two different types of plugins for PyMei: A so-called "global" (or "singleton") plugin which is instantiated once, globally, and then called for the events it "listens", or "regular plugins" which are instantiated whenever a menu-choice is made that is linked to the specific plugin in the Configuration (and then takes over as the active window).

The latter kind are just "drop-in windows", allowing new functionality to easily be added by just dropping a few files in `~/.pymei`, and they're not that interesting.

The former kind of plugins, the "global" ones, are more interesting. They're allowed to draw before or after the window does, they can react to key-presses made by the user, and they can generate events for the pygame event queue. They do each of these by implementing one or more of the following methods:
  * `key
  * `before_draw`
  * `after_draw`
  * `generate_events`

In addition, they can receive the `quit` event, which is sent when the application is quitting.

Both types of plugins are classes defined in .py-files (one file can have multiple plugins) that inherit from (at least) Plugin from mei/plugin.py.

A good source for information are the default plugins shipped with PyMei, specifically clock.py's Clock, hello\_world.py's HelloWorld and lirc\_input.py's LircInput.

Clock is a plugin that draws a clock in the upper right on all windows, HelloWorld shows a simple PNG in the middle of the screen when a menu selection is made, and lirc\_input synthesises keyboard inputs via pylirc.

For information on how to load and configure plugins, see Configuration.

## dirlist (caching directory lister) ##
dirlist is merely a module that implements a caching directory lister. It's useful for big directories on networked shares, for example. It uses the mtime of the directory to determine if the cached version is fresh.

## widget ##
Widget is an empty class that all "widgets" (individual drawable parts of a window) should inherit from. The inheritance tree is used to determine if themes should use alternate implementations of Widgets; this is achieved using the get\_widget function in widget.py, which gets a widget with the passed name that inherits from Widget (default) or a passed class (usually lower in the inheritance tree).

A more concrete example:
```
import widgets
import theme

class Button(widgets.Widget):
    pass

class TransparentButton(Button):
    def draw(self, screen, pos, hilight):
        # Do magic to draw transparent button 
        # on screen at pos.

class SparklingButton(Button):
    def draw(self, screen, pos, hilight):
        # Do magic to draw a sparkling button 
        # with ponies on screen at pos.

class SomeWindow(widgets.Window):
    def __init__(self):
        super(SomeWindow, self).__init__()
        button_type = theme.get('somewindow')['button_type']
        self._button = widgets.get_widget(button_type, Button)

    def draw(self, screen):
        super(SomeWindow, self).draw(screen)

        self._button.draw(screen, (5, 5), True)
```

The above example defines two types of button, and `SomeWindow` allows the theme to decide which one to use, via the 'button\_type' setting. This can be either `SparklingButton` or `TransparentButton`.