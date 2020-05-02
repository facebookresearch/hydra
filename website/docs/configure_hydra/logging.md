---
id: logging
title: Customizing logging
sidebar_label: Customizing logging
---
Hydra is configuring Python standard logging library with the dictConfig method. You can learn more about it [here](https://docs.python.org/3/howto/logging.html).
There are two logging configurations, one for Hydra itself and one for the executed jobs.

This example demonstrates how to customize the logging behavior of your Hydra app, by making the following changes
to the default logging behavior:

 * Outputs only to stdout (no log file)
 * Output a simpler log line pattern

`config.yaml`:
```yaml
hydra:
  job_logging:
    formatters:
      simple:
        format: '[%(levelname)s] - %(message)s'
    root:
      handlers: [console]
```

This is what the the default logging looks like:
```text
$ python main.py
[2019-09-26 18:58:05,477][__main__][INFO] - Info level message
```

And this simplified logging looks like:
```bash
$ python main.py
[INFO] - Info level message
```
