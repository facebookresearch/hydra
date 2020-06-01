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
  - hydra/launcher: submitit
```

Note that this plugin expects a valid environment in the target host. usually this means a shared file system between
the launching host and the target host.

Submitit supports 3 types of queues: auto, local and slurm. Its config looks like this
```python
class QueueType(Enum):
    auto = "auto"
    local = "local"
    slurm = "slurm"


@dataclass
class SlurmQueueConf:
    nodes: int = 1
    gpus_per_node: int = 1
    ntasks_per_node: int = 1
    mem: str = "${hydra.launcher.mem_limit}GB"
    cpus_per_task: int = 10
    time: int = 60
    partition: str = "dev"
    signal_delay_s: int = 120
    job_name: str = "${hydra.job.name}"
    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    max_num_timeout: int = 0


@dataclass
class LocalQueueConf:
    gpus_per_node: int = 1
    tasks_per_node: int = 1
    timeout_min: int = 60


@dataclass
class AutoQueueConf:
    slurm_max_num_timeout: int = 0
    gpus_per_node: int = 1
    timeout_min: int = 60


@dataclass
class QueueParams:
    slurm: SlurmQueueConf = SlurmQueueConf()
    local: LocalQueueConf = LocalQueueConf()
    auto: AutoQueueConf = AutoQueueConf()


@dataclass
class SubmititConf:
    queue: QueueType = QueueType.local

    folder: str = "${hydra.sweep.dir}/.${hydra.launcher.params.queue}"

    queue_parameters: QueueParams = QueueParams()
```

See [Submitit documentation](https://github.com/facebookincubator/submitit) for full details about the parameters above.

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_submitit_launcher/example) using this launcher is provided in the plugin repository.

Starting the app with `python my_app.py task=1,2,3 -m` will launch 3 executions:

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

