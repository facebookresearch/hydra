---
id: search_path
title: Config Search Path
---

The Config Search Path is a list of paths that are searched in order to find configs. It is similar to
the Python PYTHONPATH.

 - When a config is requested, The first matching config in the search path is used.
 - Each search path element has a schema prefix such as file:// or pkg:// that is corresponding to a ConfigSourcePlugin.
 - `SearchPathPlugin` can manipulate the search path.

You can inspect the search path and the configurations loaded by Hydra by turning on verbose logging for the `hydra` logger:

```text
$ python my_app.py hydra.verbose=hydra
```