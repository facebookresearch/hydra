---
id: example
title: Customizing logging
sidebar_label: Customizing logging
---

This example shows you how to use your own python logging configuration file.
The modified logging configuration differs from the default in the following:
 * It outputs to stdout and not to a log file as well
 * It uses a simpler log pattern, without the timestamp etc.

Note that the resulting config will be a combination of the default logging config and your specification,
With your specification overriding the default.

.hydra/hydra.yaml
```yaml
defaults:
  - logging
```

.hydra/logging.yaml
```yaml
hydra:
  # python logging configuration
  logging:
    formatters:
      simple:
        format: '[%(levelname)s] - %(message)s'
    root:
      handlers: [console]
```
 
Output:

```bash
$ python example.py
[INFO] - Info level message
```