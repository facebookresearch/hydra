---
id: develop
title: Plugin development
sidebar_label: Plugin development
---

:::info
If you develop plugins, please join the <a href="https://hydra-framework.zulipchat.com/#narrow/stream/233935-Hydra-plugin.20dev.20announcements">Plugin developer announcement chat channel</a>.
:::


import GithubLink from "@site/src/components/GithubLink"

Hydra plugins must be registered before they can be used. There are two ways to register a plugin:
- via the automatic plugin discovery process, which discovers plugins located in the `hydra_plugins` namespace package
- by calling the `register` method on Hydra's `Plugins` singleton class

## Automatic Plugin discovery process

If you create a Plugin and want it to be discovered automatically by Hydra, keep the following things in mind:
- Hydra plugins can be either a standalone Python package, or a part of your existing Python package. 
  In both cases - They should be in the namespace module `hydra_plugins` (This is a top level module, Your plugin will __NOT__ be discovered if you place it in `mylib.hydra_plugins`).
- Do __NOT__ place an `__init__.py` file in `hydra_plugins` (doing so may break other installed Hydra plugins).
  
The plugin discovery process runs whenever Hydra starts. During plugin discovery, Hydra scans for plugins in all the submodules of `hydra_plugins`. Hydra will import each module and look for plugins defined in that module.
Any module under `hydra_plugins` that is slow to import will slow down the startup of __ALL__ Hydra applications.
Plugins with expensive imports can exclude individual files from Hydra's plugin discovery process by prefixing them with `_` (but not `__`).
For example, the file `_my_plugin_lib.py` would not be imported and scanned, while `my_plugin_lib.py` would be.

## Plugin registration via the `Plugins.register` method

Plugins can be manually registered by calling the `register` method on the instance of Hydra's `Plugins` singleton class.
```python
from hydra.core.plugins import Plugins
from hydra.plugins.plugin import Plugin

class MyPlugin(Plugin):
  ...

def register_my_plugin() -> None:
    """Hydra users should call this function before invoking @hydra.main"""
    Plugins.instance().register(MyPlugin)
```

## Getting started

The best way to get started developing a Hydra plugin is to base your new plugin on one of the example plugins:
- Copy the subtree of the relevant <GithubLink to="examples/plugins">example plugin</GithubLink> into a standalone project.
- Edit `setup.py`, rename the plugin module, for example from `hydra_plugins.example_xyz_plugin` to `hydra_plugins.my_xyz_plugin`.
- Install the new plugin (Run this in the plugin directory: `pip install -e .`)
- Run the included example app and make sure that the plugin is discovered:
```shell
$ python example/my_app.py --info plugins
Installed Hydra Plugins
***********************
        ...
        Launcher:
        ---------
                MyLauncher
        ...
```
- Run the example application to see that that your plugin is doing something.
- *[Optional]* If you want the plugin be embedded in your existing application/library, move the `hydra_plugins` directory 
   and make sure that it's included as a namespace module in your final Python package. See the `setup.py` 
   file included with the example plugin for hints (typically this involves using `find_namespace_packages(include=["hydra_plugins.*"])`).
- Hack on your plugin, Ensure that the recommended tests and any tests you want to add are passing.
