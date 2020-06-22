---
id: submitit_launcher
title: Submitit Launcher plugin
sidebar_label: Submitit Launcher plugin
---
[![PyPI](https://img.shields.io/pypi/v/hydra-submitit-launcher)](https://pypi.org/project/hydra-submitit-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-submitit-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-submitit-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-submitit-launcher.svg)](https://pypistats.org/packages/hydra-submitit-launcher)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_submitit_launcher/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_submitit_launcher)

The Submitit Launcher plugin provides a [SLURM ](https://slurm.schedmd.com/documentation.html) Launcher based on [Submitit](https://github.com/facebookincubator/submitit).


### Installation
This plugin requires Hydra 1.0 (Release candidate)
```commandline
$ pip install hydra-submitit-launcher --pre
```


### Usage
Once installed, add `hydra/launcher=submitit_slurm` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - hydra/launcher: submitit_slurm
```

Note that this plugin expects a valid environment in the target host. usually this means a shared file system between
the launching host and the target host.

Submitit actually implements 2 different launchers: `submitit_slurm` to run on a SLURM cluster, and `submitit_local` for basic local tests.

You can discover the slurm launcher parameters with:
```text
$ python foo.py hydra/launcher=submitit_slurm --cfg hydra -p hydra.launcher
# @package hydra.launcher
cls: hydra_plugins.hydra_submitit_launcher.submitit_launcher.SlurmSubmititLauncher
params:
  submitit_folder: ${hydra.sweep.dir}/.submitit/%j
  timeout_min: 60
  cpus_per_task: 1
  gpus_per_node: 0
  tasks_per_node: 1
  mem_gb: 4
  nodes: 1
  name: ${hydra.job.name}
  partition: null
  comment: null
  constraint: null
  exclude: null
  signal_delay_s: 120
  max_num_timeout: 0
```

Similarly, you can discover the local launcher parameters with:
```text
$ python my_app.py hydra/launcher=submitit_local --cfg hydra -p hydra.launcher
# @package hydra.launcher
cls: hydra_plugins.hydra_submitit_launcher.submitit_launcher.LocalSubmititLauncher
params:
  submitit_folder: ${hydra.sweep.dir}/.submitit/%j
  timeout_min: 60
  cpus_per_task: 1
  gpus_per_node: 0
  tasks_per_node: 1
  mem_gb: 4
  nodes: 1
  name: ${hydra.job.name} 
```

You can set all these parameters in your configuration file and/or override them in the commandline: 
```text
python foo.py hydra/launcher=submitit_slurm hydra.launcher.params.timeout_min=3
```

For more details, including descriptions for each parameter, check out the [config file](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_submitit_launcher/hydra_plugins/hydra_submitit_launcher/config.py). You can also check the [Submitit documentation](https://github.com/facebookincubator/submitit).


### Example

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_submitit_launcher/example) using this launcher is provided in the plugin repository.

Starting the app with `python my_app.py task=1,2,3 -m` will launch 3 executions (you can override the launcher to run locally for testing by adding `hydra/launcher=submitit_local`):

```text
$ python my_app.py task=1,2,3 -m
[HYDRA] Sweep output dir : multirun/2020-05-28/15-05-22
[HYDRA]        #0 : task=1
[HYDRA]        #1 : task=2
[HYDRA]        #2 : task=3
```
You will be able to see the output of the app in the output dir:
```commandline
$ tree
.
├── 0
│   └── my_app.log
├── 1
│   └── my_app.log
├── 2
│   └── my_app.log
└── multirun.yaml

$ cat 0/my_app.log 
[2020-05-28 15:05:23,511][__main__][INFO] - Process ID 15887 executing task 1 ...
[2020-05-28 15:05:24,514][submitit][INFO] - Job completed successfully
```

