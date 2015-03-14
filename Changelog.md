# Changelog #

This lists changes from one release to the next, hopefully this covers everything of interest (and a bit more).

It's generated by manually skimming `svn log -vREV1:REV2`. :-)

## v0.2.0 ([r63](https://code.google.com/p/pymei/source/detail?r=63)) ##
_(from v0.1.3 (**[r42](https://code.google.com/p/pymei/source/detail?r=42)**))_

#### Major changes ####
  * The configuration system now has support for default configurations, and all plugins & windows now use it.
  * Allow keyboard to be bound by the user in config, see keybinds in pymei.config.

#### Minor changes & fixes ####
  * Make embedded mplayer relay stuff to stdout.
  * Some internal changes to clean up code.
  * Minor fixes & changes to facilitate ports package.
  * Exit properly if config isn't found.
  * Use cvlc rather than vlc, if possible.
  * Make it quit when you press the X in the window frame. ;-)
  * Other minor changes.

## v0.1.3 ([r42](https://code.google.com/p/pymei/source/detail?r=42)) ##
_(from v0.1.2 (**[r28](https://code.google.com/p/pymei/source/detail?r=28)**))_

  * Numerous fixes to embedded mplayer - this should solve all issues related to separate\_window: False
    * Make cursor be hidden properly.
    * Allow for pausing\_keep\_force in new mplayers, and just send 'pause' instead of space in old mplayers. This fixes a bug where space wouldn't unpause.
  * Reorganize a bit; put version info into mei.version, move config to example\_configuration/pymei.config
  * Make theme more YAML-y
  * Add new widgets to facilitate for new XKCD plugin (which is highly undocumented):
    * TextBox - displays text in a set area, aligning it as desired and splitting too long lines.
    * ScrollableImage - displays an image in a set area, and allows scrolling.
  * Bundle fonts, and add a LICENSE that hopefully covers this. :-)
  * Add a debug server in debug: true that gives a python console via telnet, with access to pymei.
  * Handle plugin dependencies nicer.
  * Add XKCD-plugin!
