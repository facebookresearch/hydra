---
id: logging
title: Customizing logging
sidebar_label: Customizing logging
---
Hydra is configuring Python standard logging library with the dictConfig method. You can learn more about it [here](https://docs.python.org/3/howto/logging.html).
There are two logging configurations, one for Hydra itself and one for the executed jobs.
 
This example demonstrates how to to customize the logging behavior of your Hydra app, by making the following changes
to the default logging behavior:

 * Outputs only to stdout (no log file)
 * Output a simpler log line pattern

Project structure:
```text
$ tree
├── conf
│   ├── config.yaml
│   └── hydra
│       └── job_logging
│           └── custom.yaml
└── main.py
```

config.yaml defaults the application to the custom logging.

Config file: `config.yaml`
```yaml
defaults:
  - hydra/job_logging : custom
```
Config file: `hydra/job_logging/custom.yaml`

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
```bash
$ python main.py hydra/job_logging=default
[2019-09-26 18:58:05,477][__main__][INFO] - Info level message
```

And this is what the custom logging looks like:
```bash
$ python main.py
[INFO] - Info level message
```
