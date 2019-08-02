---
id: working_directory
title: Working directory
sidebar_label: Working directory
---

Hydra manages the working directory for your app.
The following app prints the current working directory and create a file containing the current time
in it:

```python
import os
import hydra
import datetime


@hydra.main()
def experiment(_cfg):
    print("Working directory : {}".format(os.getcwd()))
    with open("output.txt", "w") as f:
        f.write("The time is {}\n".format(datetime.datetime.now()))


if __name__ == "__main__":
    experiment()
```

Every time you run the app, a new working directory is automatically created:
```text
$ python experiment.py
Working directory : outputs/2019-07-26_13-49-27

$ python experiment.py
Working directory : outputs/2019-07-26_13-49-29
```

Let's take a look at one of those working directories:
```text
$ tree outputs/2019-07-26_13-49-27
outputs/2019-07-26_13-49-27
├── config.yaml
├── output.txt
├── overrides.yaml
└── experiment.log
```

We have 4 files there:
* `config.yaml`: A yaml dump of the configuration object your app ran with
* `output.txt`: The file created by the app
* `overrides.yaml`: A configuration constructed from the passed in command line arguments
* `experiment.log`: A log file created for this job. Since we did not log anything it's empty.

Check the [runnable example](https://github.com/facebookresearch/hydra/blob/master/demos/1_working_directory/working_directory.py).