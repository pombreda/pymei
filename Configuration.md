#summary Introduction to configuration file and its options.
#labels Featured,Phase-Deploy,Documentation

# Configuration #

The configuration file is in [YAML format](http://www.yaml.org/), and should be human readable & writable. Description of what the different options mean can be found below.

You can find the global configuration file in /etc/pymei.config. If you want to change something, copy this to ~/.pymei/config by the following commands:
```
mkdir ~/.pymei
cp /etc/pymei.config ~/.pymei/config
```

These are the options in pymei.config as of ~v0.1.

| **Option name** | **Type** | **Description** | **Default value** |
|:----------------|:---------|:----------------|:------------------|
| debug | boolean | Wether or not PyMei spews debug stuff to stdout | false |

## application section ##

| **Option name** | **Type** | **Description** | **Default value** |
|:----------------|:---------|:----------------|:------------------|
| fullscreen | boolean | Should PyMei run fullscreen or windowed? | false |
| resolution | list | Two numbers, [W, H] of the window. | [800, 600] |
| theme | string | Name of theme we use, should be found in /usr/local/pymei/themes or ~/.pymei/themes | default |
| min\_fps | number | Minimum number of FPS (we draw at LEAST every 1/min\_fps seconds) | 0.25 |
| max\_fps | number | Try to keep below this FPS count | 20 |

### plugins subsection ###

| **Option name** |  **Type** | **Description** | **Default value** |
|:----------------|:----------|:----------------|:------------------|
| <name of plugin> | dictionary | This is the name of a plugin that should be loaded, and the dictionary (map) are the configuration values passed to the plugin when it's loaded. | Clock: {} |

## videobrowser section ##

| **Option name** |  **Type** | **Description** | **Default value** |
|:----------------|:----------|:----------------|:------------------|
| played\_dir | path | Directory where we store persistent information in order to hilight directories that have been already played in the videobrowser. | /tmp/played |

## mplayer section ##

| **Option name** |  **Type** | **Description** | **Default value** |
|:----------------|:----------|:----------------|:------------------|
| separate\_window | boolean | Wether or not we should get mplayer to use its own window. If this is false, we use the -wid option to mplayer to make it use our window. | false |

## menu section ##

| **Option name** |  **Type** | **Description** | **Default value** |
|:----------------|:----------|:----------------|:------------------|
| choices | list of choice-subsections | A list containing information about the choices displayed on the main menu. | a lot ;) |

### choice subsection ###

| **Option name** |  **Type** | **Description** | **Default value** |
|:----------------|:----------|:----------------|:------------------|
| title | string | Title display on main menu | none |
| type | string | What kind of menu this is; `plugin`, `browser_video` or `menu` | none |
| choices (only for `type: menu`) | list of choice-subsections | Same as for menu, except this creates a new submenu that can be browsed. | none |
| path (only for `type: browser_video`) | path | The toplevel directory that this browser should allow browsing of. | none |

For `type: plugin`, the other options are dependant on the plugin in question.