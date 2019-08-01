---
id: example
title: Sweep example
sidebar_label: Sweep example
---

Hydra supports running jobs on Slurm and Chronos using [fairtask](https://github.com/fairinternal/fairtask)
and [submitit](https://github.com/fairinternal/submitit)

Both launchers are Hydra plugins, and each takes some specific configuration for things like how many GPUs to use etc.
See [this](https://github.com/fairinternal/hydra/tree/master/demos/6_sweep/conf/.hydra) for an example Hydra
configuration that can run on Slurm and submitit.

Running parameter sweeps is easy, just add --sweep or -s to your your app execution.
The following command would run a single job on Slurm, with all your default options:
```text
$ python demos/6_sweep/experiment.py  -s
[2019-08-01 16:24:36,851][INFO] - Sweep output dir : /checkpoint/omry/outputs/2019-08-01_16-24-36
[2019-08-01 16:24:36,899][INFO] - Launching 1 jobs to slurm queue
[2019-08-01 16:24:36,899][INFO] -       #0 :
```

Let's take a peak at the output:
```text
$ tree -a  /checkpoint/omry/outputs/2019-08-01_16-24-36
/checkpoint/omry/outputs/2019-08-01_16-24-36
├── 0_16248207
│   ├── config.yaml
│   ├── experiment.log
│   └── overrides.yaml
└── .slurm
    ├── slurm-16248207.err
    └── slurm-16248207.out
```

* `config.yaml` holds the composed config for this job.
* `experiment.log` is the log output
* `overrides.yaml` contains the command line overrides used to launch this job.
 
In addition, there is a hidden `.slurm` sub directory that keeps stdout and stderr for each slurm job.


You can also sweep an arbitrary number of dimensions:
```text
$ python experiment.py  -s optimizer=adam,nesterov random_seed=0,1,3
[2019-07-27 22:41:01,474][INFO] - Sweep output dir : /checkpoint/omry/outputs/2019-07-27_22-41-01
[2019-07-27 22:41:01,526][INFO] - Launching 6 jobs to slurm queue
[2019-07-27 22:41:01,526][INFO] -       #0 : optimizer=adam random_seed=0
[2019-07-27 22:41:01,526][INFO] -       #1 : optimizer=adam random_seed=1
[2019-07-27 22:41:01,527][INFO] -       #2 : optimizer=adam random_seed=3
[2019-07-27 22:41:01,527][INFO] -       #3 : optimizer=nesterov random_seed=0
[2019-07-27 22:41:01,527][INFO] -       #4 : optimizer=nesterov random_seed=1
[2019-07-27 22:41:01,527][INFO] -       #5 : optimizer=nesterov random_seed=3
Dask dashboard for "slurm" at http://localhost:8005.
```

In the example above we a total of 6 jobs, 3 for adam and 3 for nesterov with different random seeds.

You can switch between fairtask and submitit by overriding launcher to fairtask or submitit, or changing the 
default in the .hydra/hydra.yaml config file.

For example:
```text
$ experiment.py  -s   launcher=submitit
[2019-07-27 22:42:48,060][INFO] - Sweep output dir : /checkpoint/omry/outputs/2019-07-27_22-42-48
[2019-07-27 22:42:48,062][INFO] -       #0 :
```

Sweep support is currently very basic and this area will improve further.

Check the [runnable example](https://github.com/fairinternal/hydra/tree/master/demos/6_sweep).