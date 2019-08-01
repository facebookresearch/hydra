---
id: example
title: Python logging
sidebar_label: Python logging
---

Hydra configures Python logging for your app.
```python
import logging
import sys

import hydra

# A logger for this file
log = logging.getLogger(__name__)


@hydra.main()
def experiment(_cfg):
    log.info("Info level message")
    log.debug("Debug level message")


if __name__ == "__main__":
    sys.exit(experiment())
```

When you run  your app, by default only INFO and higher (WARN, ERROR) would be logged.
Logging is sent to stdout and a file logger by default.
```text
$ python experiment.py
[2019-06-27 00:52:46,653][__main__][INFO] - Info level message
```

You can enable DEBUG level logging from the command line with the `-v` flag.
`-v` takes as an argument a comma separated list of loggers.
```text
$ python experiment.py -v __main__
[2019-06-27 00:54:39,440][__main__][INFO] - Info level message
[2019-06-27 00:54:39,441][__main__][DEBUG] - Debug level message
```
The root logger is a special logger, it is the parent of all loggers. By using `-v root` you get verbose logging from
all Python loggers, even from libraries.

```text
$ python experiment.py -v root
[2019-06-27 00:53:24,346][__main__][INFO] - Info level message
[2019-06-27 00:53:24,346][__main__][DEBUG] - Debug level message
```

Logging can be [customized](../../configure_hydra/customize_working_directory/example)


Check the [runnable example](https://github.com/fairinternal/hydra/blob/master/demos/2_logging/logging_example.py).

