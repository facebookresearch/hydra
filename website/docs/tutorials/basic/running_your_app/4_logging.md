---
id: logging
title: Logging
sidebar_label: Logging
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/blob/master/examples/tutorials/basic/running_your_hydra_app/4_logging/my_app.py)

People often do not use Python logging due to the setup cost.
Hydra solves that by configuring the Python logging for you.


By default Hydra logs at the INFO level to both the console and a log file in the automatic working directory.

Example of logging with Hydra:

```python
import logging
from omegaconf import DictConfig
import hydra

# A logger for this file
log = logging.getLogger(__name__)

@hydra.main()
def my_app(_cfg: DictConfig) -> None:
    log.error("Error level message")
    log.warning("Warning level message")
    log.info("Info level message")
    log.debug("Debug level message")

if __name__ == "__main__":
    my_app()

$ python my_app.py
[2021-01-04 11:17:20,261][__main__][ERROR] - Error level message
[2021-01-04 11:17:20,261][__main__][WARNING] - Warning level message
```
By default, Python log level is WARNING.
You can enable DEBUG level logging from the command line  by overriding `hydra.verbose`.

`hydra.verbose` can be a Boolean, a String or a List:

Examples:
* `hydra.verbose=true` : Sets the log level of **all** loggers to `DEBUG`
* `hydra.verbose=NAME` : Sets the log level of the logger `NAME` to `DEBUG`
* `hydra.verbose=[NAME1,NAME2]`: Sets the log level of the loggers `NAME1` and `NAME2` to `DEBUG`

Example output:
``` text
$ python my_app.py hydra.verbose=[__main__,hydra]
[2021-01-04 11:18:32,776][HYDRA] Hydra 1.1.0                 
[2021-01-04 11:18:32,776][HYDRA] ===============               
[2021-01-04 11:18:32,776][HYDRA] Installed Hydra Plugins
[2021-01-04 11:18:32,776][HYDRA] ***********************
...
[2021-01-04 11:18:32,994][__main__][ERROR] - Error level message
[2021-01-04 11:18:32,994][__main__][WARNING] - Warning level message
[2021-01-04 11:18:32,994][__main__][INFO] - Info level message
[2021-01-04 11:18:32,994][__main__][DEBUG] - Debug level message
```

You can disable the logging output by setting `hydra/job_logging` to `disabled`   
```commandline
$ python my_app.py hydra/job_logging=disabled
<NO OUTPUT>
```

To completely prevent Hydra from configuring the logging, set `hydra/job_logging=none` and `hydra/hydra_logging=none`.

Logging can be [customized](/configure_hydra/logging.md).
