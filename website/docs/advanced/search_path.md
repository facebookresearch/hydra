---
id: search_path
title: Config search path
sidebar_label: Config search path
---

Hydra uses a search path approach to find configuration files as it composes your configuration object.
This is still work in progress, more details will be added here later.

For now, you can inspect the search path and the configurations loaded by Hydra by turning on verbose logging for the `hydra` logger:

```text
$ python tutorial/defaults/my_app.py  hydra.verbose=hydra
```