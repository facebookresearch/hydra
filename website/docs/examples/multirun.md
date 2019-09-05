---
id: multi-run
title: Multi-run
sidebar_label: Multi-run example
---

Hydra can run the same job multiple time with different arguments in each run using a mode called multirun.
To turn on multi-run, use -m or --multirun and pass comma separated list for each value you want
to sweep over, for example:
```text
$ python demos/5_config_groups/experiment.py -m optimizer=adam,nesterov
[2019-09-03 17:47:21,646] - Launching 2 jobs locally
[2019-09-03 17:47:21,646] - Sweep output dir : multirun/2019-09-03/17-47-21
[2019-09-03 17:47:21,646] -     #0 : optimizer=adam
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam

[2019-09-03 17:47:21,720] -     #1 : optimizer=nesterov
optimizer:
  lr: 0.001
  type: nesterov
```

The default launcher runs the jobs locally and serially, but you can switch to other launchers like fairtask and submitit:

For example:
```text
> python demos/6_sweep/experiment.py -m optimizer=nesterov,adam random_seed=1,2,3 hydra/launcher=fairtask
[2019-09-03 17:58:19,452] - Sweep output dir : multirun/2019-09-03/17-58-19
[2019-09-03 17:58:19,775] - Launching 6 jobs to slurm queue
[2019-09-03 17:58:19,776] -     #0 : optimizer=nesterov random_seed=1
[2019-09-03 17:58:19,776] -     #1 : optimizer=nesterov random_seed=2
[2019-09-03 17:58:19,776] -     #2 : optimizer=nesterov random_seed=3
[2019-09-03 17:58:19,776] -     #3 : optimizer=adam random_seed=1
[2019-09-03 17:58:19,776] -     #4 : optimizer=adam random_seed=2
[2019-09-03 17:58:19,776] -     #5 : optimizer=adam random_seed=3
```

Sweep support is currently very basic and this area will improve further.

Check the [runnable example](https://github.com/facebookresearch/hydra/tree/master/demos/6_sweep).