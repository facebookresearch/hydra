---
id: multi-run
title: Multi-run
sidebar_label: Multi-run example
---

Hydra can run the same job multiple time with different arguments in each run using a mode called multirun.
To turn on multi-run, use -m or --multirun and pass comma separated list for each value you want
to sweep over, for example:
```text
$ python demos/0_minimal/minimal.py --multirun x=1,2 b=x,y
[2019-08-14 23:39:30,808][basic_launcher][INFO] - Launching 4 jobs locally
[2019-08-14 23:39:30,808][basic_launcher][INFO] - Sweep output dir : ./outputs/2019-08-14_23-39-30
[2019-08-14 23:39:30,808][basic_launcher][INFO] -       #0 : x=1 b=x
b: x
x: 1

[2019-08-14 23:39:30,860][basic_launcher][INFO] -       #1 : x=1 b=y
b: y
x: 1

[2019-08-14 23:39:30,916][basic_launcher][INFO] -       #2 : x=2 b=x
b: x
x: 2

[2019-08-14 23:39:30,976][basic_launcher][INFO] -       #3 : x=2 b=y
b: y
x: 2
```

The default launcher runs the jobs locally and serially, but you can switch to other launchers like fairtask and submitit:

For example:
```text
$ $ python demos/6_sweep/experiment.py -m optimizer=nesterov,adam launcher=fairtask
[2019-08-14 23:39:49,372][fairtask_launcher][INFO] - Sweep output dir : /checkpoint/omry/outputs/2019-08-14_23-39-49
[2019-08-14 23:39:49,534][fairtask_launcher][INFO] - Launching 2 jobs to slurm queue
[2019-08-14 23:39:49,534][fairtask_launcher][INFO] -    #0 : optimizer=nesterov
[2019-08-14 23:39:49,534][fairtask_launcher][INFO] -    #1 : optimizer=adam
```

Sweep support is currently very basic and this area will improve further.

Check the [runnable example](https://github.com/facebookresearch/hydra/tree/master/demos/6_sweep).