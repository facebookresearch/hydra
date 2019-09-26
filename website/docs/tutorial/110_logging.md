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
You can enable DEBUG level logging from the command line with `-v` or `--verbose`.

``` text
$ python my_app.py -v __main__
[2019-06-27 00:54:39,440][__main__][INFO] - Info level message
[2019-06-27 00:54:39,441][__main__][DEBUG] - Debug level message
```
You can activate multiple loggers by passing a comma separated list to `-v`.
```yaml
$ python my_app.py -v hydra,mysql 
```
`-v root` activate debug logging for all loggers, even external libraries. 

Logging can be [customized](../configure_hydra/logging/).

