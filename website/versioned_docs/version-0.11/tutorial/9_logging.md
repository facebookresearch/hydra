---
id: logging
title: Logging
sidebar_label: Logging
---

People often do not use Python logging due to the setup cost.
Hydra solves that by configuring the Python logging for you.

By default Hydra logs at the INFO level to both console and a file.

Example of logging with Hydra:

```python
import logging

# A logger for this file
log = logging.getLogger(__name__)

@hydra.main()
def my_app(_cfg):
    log.info("Info level message")
    log.debug("Debug level message")

$ python my_app.py
[2019-06-27 00:52:46,653][__main__][INFO] - Info level message

```
You can enable DEBUG level logging from the command line  by overriding `hydra.verbose`.

`hydra.verbose` can be a Boolean, a String or a List:
Examples:
* `hydra.verbose=true` : Set **all** loggers log level to `DEBUG`
* `hydra.verbose=__main__` : Set the `__main__` logger log level to `DEBUG`
* `hydra.verbose=[__main__,hydra]`: Set the log levels of the loggers `__main__` and hydra log to `DEBUG`

Example output:
``` text
$ python my_app.py hydra.verbose=[__main__,hydra]
[2019-09-29 13:06:00,880] - Installed Hydra Plugins
[2019-09-29 13:06:00,880] - ***********************
...
[2019-09-29 13:06:00,896][__main__][INFO] - Info level message
[2019-09-29 13:06:00,896][__main__][DEBUG] - Debug level message
```

Logging can be [customized](../configure_hydra/logging.md).

