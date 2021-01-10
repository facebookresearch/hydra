---
id: logging
title: Customizing logging
sidebar_label: Customizing logging
---
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/configure_hydra/logging)

Hydra is configuring Python standard logging library with the dictConfig method. You can learn more about it [here](https://docs.python.org/3/howto/logging.html).
There are two logging configurations, one for Hydra itself and one for the executed jobs.

This example demonstrates how to customize the logging behavior of your Hydra app, by making the following changes
to the default logging behavior:

 * Outputs only to stdout (no log file)
 * Output a simpler log line pattern

```yaml title="config.yaml"
defaults:
  - override hydra/job_logging: custom
```

```yaml title="hydra/job_logging/custom.yaml"
# @package _group_
version: 1
formatters:
  simple:
    format: '[%(levelname)s] - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    stream: ext://sys.stdout
root:
  handlers: [console]

disable_existing_loggers: false
```

This is what the default logging looks like:
```
$ python my_app.py hydra/job_logging=default
[2020-08-24 13:43:26,761][__main__][INFO] - Info level message
```

And this is what the custom logging looks like:
```text
$ python my_app.py 
[INFO] - Info level message
```

