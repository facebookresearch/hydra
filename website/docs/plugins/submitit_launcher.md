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
Once installed, add `hydra/launcher=submitit` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - hydra/launcher: submitit_slurm
```

Note that this plugin expects a valid environment in the target host. usually this means a shared file system between
the launching host and the target host.

Submitit actually implements 2 different launchers: `submitit_slurm` to run on a SLURM cluster, and `local` to test locally.
```python
@dataclass
class BaseParams:
    """Configuration shared by all executors
    """

    submitit_folder: str = "${hydra.sweep.dir}/.submitit/%j"

    # maximum time for the job in minutes
    timeout_min: int = 60
    # number of cpus to use for each task
    cpus_per_task: int = 1
    # number of gpus to use on each node
    gpus_per_node: int = 0
    # number of tasks to spawn on each node
    tasks_per_node: int = 1
    # memory to reserve for the job on each node (in GB)
    mem_gb: int = 4
    # number of nodes to use for the job
    nodes: int = 1
    # name of the job
    name: str = "${hydra.job.name}"


@dataclass
class SlurmParams(BaseParams):
    """Slurm configuration overrides and specific parameters
    """

    # Params are used to configure sbatch, for more info check:
    # https://github.com/facebookincubator/submitit/blob/master/submitit/slurm/slurm.py

    # Following parameters are slurm specific
    # More information: https://slurm.schedmd.com/sbatch.html
    #
    # slurm partition to use on the cluster
    partition: Optional[str] = None
    comment: Optional[str] = None
    constraint: Optional[str] = None
    exclude: Optional[str] = None

    # Following parameters are submitit specifics
    #
    # USR1 signal delay before timeout
    signal_delay_s: int = 120
    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    # check the following for more info on slurm_max_num_timeout
    # https://github.com/facebookincubator/submitit/blob/master/docs/checkpointing.md
    max_num_timeout: int = 0
```

See [Submitit documentation](https://github.com/facebookincubator/submitit) for full details about the parameters above.

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_submitit_launcher/example) using this launcher is provided in the plugin repository.

You can discover the launcher parameters with:
```text
$ python my_app.py --cfg hydra --package hydra.launcher
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

