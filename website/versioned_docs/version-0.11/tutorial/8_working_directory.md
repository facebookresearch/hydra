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
├── .hydra
│   ├── config.yaml
│   ├── hydra.yaml
│   └── overrides.yaml
└── my_app.log
```

We have the Hydra output directory (`.hydra` by default) and the application log file.
Inside the configuration output directory we have:
* `config.yaml`: A dump of the user specified configuration
* `hydra.yaml`: A dump of the Hydra configuration
* `overrides.yaml`: The command line overrides used

And in the main output directory:
* `my_app.log`: A log file created for this run

### Original working directory

You can still access the original working directory if you need to:

```python
import os
import hydra
from hydra import utils

@hydra.main()
def my_app(_cfg):
    print("Current working directory  : {}".format(os.getcwd()))
    print("Original working directory : {}".format(utils.get_original_cwd()))
    print("to_absolute_path('foo')    : {}".format(utils.to_absolute_path("foo")))
    print("to_absolute_path('/foo')   : {}".format(utils.to_absolute_path("/foo")))


$ python examples/tutorial/8_working_directory/original_cwd.py
Current working directory  : /Users/omry/dev/hydra/outputs/2019-10-23/10-53-03
Original working directory : /Users/omry/dev/hydra
to_absolute_path('foo')    : /Users/omry/dev/hydra/foo
to_absolute_path('/foo')   : /foo
```


Working directory can be [customized](../configure_hydra/workdir.md).
