---
id: working_directory
title: Working directory
sidebar_label: Working directory
---

Hydra manages the working directory for your app.
Instead of coming up with a location to save your output to, you can just save them to the
current working directory.

The following app prints the current working directory to demonstrate it:

Python file (`my_app.py`):
```python
import os
import hydra

@hydra.main()
def my_app(_cfg):
    print("Working directory : {}".format(os.getcwd()))

if __name__ == "__main__":
    my_app()
```

Every time you run the app, a new working directory is automatically created:
```text
$ python my_app.py
Working directory : outputs/2019-07-26_13-49-27

$ python my_app.py
Working directory : outputs/2019-07-26_13-49-29
```

Let's take a look at one of those working directories:
```text
$ tree outputs/2019-07-26_13-49-27
outputs/2019-07-26_13-49-27
├── config.yaml
├── overrides.yaml
└── my_app.log
```

We have 4 files there:
* `config.yaml`: A yaml dump of the configuration object your app ran with
* `overrides.yaml`: A configuration constructed from the passed in command line arguments
* `my_app.log`: A log file created for this job. Since we did not log anything it's empty.

Working directory can be [customized](../configure_hydra/workdir).
