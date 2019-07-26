---
id: example
title: Working directory
sidebar_label: Working directory
---

Hydra manages the working directory for your app.
The following basic Hydra app prints the current working directory, and then create a file containing the current time
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
$ python working_directory.py
Working directory : outputs/2019-07-26_13-49-27

$ python working_directory.py
Working directory : outputs/2019-07-26_13-49-29
```

Let's take a look at one of those working working directories:
```text
$ tree outputs/2019-07-26_13-49-27
outputs/2019-07-26_13-49-27
├── config.yaml
├── output.txt
├── overrides.yaml
└── working_directory.log
```

We have 4 files there:
* config.yaml: A yaml dump of the configuration object your app ran with
* output.txt: The file out app created
* overrides.yaml: A configuration constructed from the passed in command line
* working_directory.log: A log file created for this job. since we did not log anything it's empty.