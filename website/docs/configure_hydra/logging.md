---
id: logging
title: Customizing logging
sidebar_label: Customizing logging
---
Hydra is configuring Python standard logging library with the dictConfig method. You can learn more about it [here](https://docs.python.org/3/howto/logging.html).
There are actually two logging configurations, one for Hydra itself and one for the executed jobs.

 
This example demonstrates how to to customize the logging behavior of your Hydra app, by making the following changes
to the default logging behavior:

 * It outputs to stdout and not to a log file as well
 * It uses a simpler log pattern, without the timestamp etc.

Note that the resulting config will be a combination of the default logging config and your specification,
With your specification overriding the default.

conf/config.yaml
```yaml
defaults:
  - hydra/job_logging : logging
```

conf/hydra/job_logging/logging.yaml
```yaml
hydra:
  # python logging configuration
  job_logging:
    formatters:
      simple:
        format: '[%(levelname)s] - %(message)s'
    root:
      handlers: [console]
```

Output:

```bash
$ python demos/99_hydra_configuration/logging/main.py hydra/job_logging=logging
[2019-08-14 21:07:31,382][__main__][INFO] - Info level message
$ python demos/99_hydra_configuration/logging/main.py
[INFO] - Info level message
```

Check the [runnable example](https://github.com/facebookresearch/hydra/tree/master/demos/99_hydra_configuration/logging).