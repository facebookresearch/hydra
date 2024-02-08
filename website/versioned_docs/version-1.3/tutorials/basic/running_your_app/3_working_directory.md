---
id: working_directory
title: Output/Working directory
sidebar_label: Output/Working directory
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/basic/running_your_hydra_app/3_working_directory"/>

Hydra can solve the problem of your needing to specify a new output directory for each run, by
creating a directory for each run and executing your code within that output directory.
By default, this output directory is used to store Hydra output for the run (Configuration, Logs etc).

Every time you run the app, a new output directory is created.
You can retrieve the path of the output directy by
[inspecting the Hydra config](/configure_hydra/Intro.md#accessing-the-hydra-config) as in the example below.

```python title="my_app.py"
import os
from omegaconf import DictConfig
import hydra

@hydra.main(version_base=None)
def my_app(_cfg: DictConfig) -> None:
    print(f"Working directory : {os.getcwd()}")
    print(f"Output directory  : {hydra.core.hydra_config.HydraConfig.get().runtime.output_dir}")
```
```text
$ python my_app.py
Working directory : /home/omry/dev/hydra
Output directory  : /home/omry/dev/hydra/outputs/2019-09-25/15-16-17

$ python my_app.py
Working directory : /home/omry/dev/hydra
Output directory  : /home/omry/dev/hydra/outputs/2019-09-25/15-16-19
```

Let's take a look at one of the output directories:
```text
$ tree outputs/2019-09-25/15-16-17
outputs/2019-09-25/15-16-17
├── .hydra
│   ├── config.yaml
│   ├── hydra.yaml
│   └── overrides.yaml
└── my_app.log
```

We have the Hydra output directory (`.hydra` by default), and the application log file.
Inside the Hydra output directory we have:
* `config.yaml`: A dump of the user specified configuration
* `hydra.yaml`: A dump of the Hydra configuration
* `overrides.yaml`: The command line overrides used

And in the main output directory:
* `my_app.log`: A log file created for this run

You can configure the name of the output directory using
the [customizing the working directory](/configure_hydra/workdir.md) pattern.


### Automatically change current working dir to job's output dir

By setting `hydra.job.chdir=True`, you can configure
Hydra's `@hydra.main` decorator to change python's working directory by calling
`os.chdir` before passing control to the user's decorated main function.
As of Hydra v1.2, `hydra.job.chdir` defaults to `False`.

Setting `hydra.job.chdir=True` enables convenient use of the output directory to
store output for the application (For example, a database dump file).

```bash
# check current working dir
$ pwd
/home/jasha/dev/hydra

# for Hydra >= 1.2, working dir remains unchanged by default
$ python my_app.py
Working directory : /home/jasha/dev/hydra
Output directory  : /home/jasha/dev/hydra/outputs/2023-04-18/13-43-24

# working dir changed to output dir
$ python my_app.py hydra.job.chdir=True
Working directory : /home/jasha/dev/hydra/outputs/2023-04-18/13-43-17
Output directory  : /home/jasha/dev/hydra/outputs/2023-04-18/13-43-17

# output dir and files are still created even if `chdir` is disabled:
$ tree -a outputs/2023-04-18/13-43-24/
outputs/2023-04-18/13-43-24/
├── .hydra
│   ├── config.yaml
│   ├── hydra.yaml
│   └── overrides.yaml
└── my_app.log
```


### Changing or disabling Hydra's output subdir 
You can change the `.hydra` subdirectory name by overriding `hydra.output_subdir`.
You can disable its creation by overriding `hydra.output_subdir` to `null`.


### Accessing the original working directory in your application

With `hydra.job.chdir=True`, you can still access the original working directory by importing `get_original_cwd()` and `to_absolute_path()` in `hydra.utils`:

```python
from hydra.utils import get_original_cwd, to_absolute_path

@hydra.main(version_base=None)
def my_app(_cfg: DictConfig) -> None:
    print(f"Current working directory : {os.getcwd()}")
    print(f"Orig working directory    : {get_original_cwd()}")
    print(f"to_absolute_path('foo')   : {to_absolute_path('foo')}")
    print(f"to_absolute_path('/foo')  : {to_absolute_path('/foo')}")

if __name__ == "__main__":
    my_app()
```

```text title="$ python examples/tutorial/8_working_directory/original_cwd.py"
Current working directory  : /Users/omry/dev/hydra/outputs/2019-10-23/10-53-03
Original working directory : /Users/omry/dev/hydra
to_absolute_path('foo')    : /Users/omry/dev/hydra/foo
to_absolute_path('/foo')   : /foo
```

The name of the generated working directories can be [customized](/configure_hydra/workdir.md).
