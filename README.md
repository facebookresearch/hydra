# Hydra
Hydra is a experimentation framework providing the following:
 * A unified interface to run experiments locally or remotely
 * Dynamically composes a configuration from your own configuration primitives
 * Ability to override values in composed configurations from the command line
 * Creates a working directory per job run for you
 * Provides an ability to sweep on multiple dimensions from the command line
 * Configures python logger for your experiments

# Using
## Install
A proper pip package will be available after Hydra is open sourced.

You can install/upgrade by running the following command:
```
python3 -m pip install --upgrade --upgrade-strategy=eager git+ssh://git@github.com/fairinternal/hydra.git@master
```
## Uninstall
```
python3 -m pip uninstall hydra -y
```

# Basic usage
Go through the [demos](demos/README.md) to get a gentle incremental intruduction, starting from the most basic.

# Runtime config variables
The following variables can be used in hydra config or job config

| function   | arguments        | description                                                                                | Example                       | Example output      |
| ---------- |------------------| ------------------------------------------------------------------------------------------ | ------------------------------|---------------------|
| now        | strftime pattern | date/time pattern                                                                          | ${now:%Y-%m-%d_%H-%M-%S}      | 2019-07-10_11-47-35 |
| job        | name             | Job name, defaults to python file name without suffix. Used for log filename, job name etc | ${job:name                    | example_sweep       |
|            | override_dirname | Pathname derived from the overrides for this job                                           | /path/${job:override_dirname} | /path/a:1,b:I       |
|            | num              | job serial number in sweep                                                                 | ${job:num}                    | 0                   |
|            | id               | Job ID in the underlying jobs system (slurm, chronos etc)                                  | ${job:id}                     | 14445406            |
|            |                  |                                                                                            |                               |                     |


# Developing
## Install:
Checkout this repository, run the following and start hacking:
```
python setup.py develop
```

## Uninstall
```
python setup.py develop --uninstall
```