---
id: search_path
title: Config search path
sidebar_label: Config search path
---

Hydra uses a search path approach to find configuration files as it composes the configuration object.
`SearchPathPlugin` can manipulate the search path.

You can inspect the search path and the configurations loaded by Hydra by turning on verbose logging for the `hydra` logger:

```text
$ python my_app.py hydra.verbose=hydra
```