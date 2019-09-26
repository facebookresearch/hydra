---
id: working_directory
title: Output/Working directory
sidebar_label: Output/Working directory
---

Hydra solves the problem of your needing to specify a new output directory for each run, by 
creating a directory for each run and executing your code within that directory.

The working directory is used to:
* Store the output for the application (For example, a database dump file)
* Store the Hydra output for the run (Configuration, Logs etc)

Every time you run the app, a new working directory is automatically created:

Python file: `my_app.py`
```python
import os

@hydra.main()
def my_app(_cfg):
    print("Working directory : {}".format(os.getcwd()))

$ python my_app.py
Working directory : /home/omry/dev/hydra/outputs/2019-09-25/15-16-17

$ python my_app.py
Working directory : /home/omry/dev/hydra/outputs/2019-09-25/15-16-19

```

Let's take a look at one of those working directories:
```text
$ tree outputs/2019-09-25/15-16-17
outputs/2019-09-25/15-16-17
├── config.yaml
├── hydra.yaml
├── my_app.log
└── overrides.yaml
```

We have 4 files there:
* `config.yaml`: A dump of the user specified configuration
* `hydra.yaml`: A dump of the Hydra configuration
* `overrides.yaml`: The command line overrides used
* `my_app.log`: A log file created for this run

Working directory can be [customized](../configure_hydra/workdir).
