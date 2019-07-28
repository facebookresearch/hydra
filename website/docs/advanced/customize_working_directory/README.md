---
id: example
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---


This example customizes the working directory in both run and sweeps using the following config snippet:

```yaml
hydra:
  run:
    dir: ./outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
  sweep:
    dir: /checkpoint/${env:USER}/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${job:num}_${job:id}_${job:override_dirname}
```

This cause output jobs to be grouped by day.
In addition, for sweep the directory name would reflect the sweep parameters.

```bash
$ python demos/99_hydra_configuration/workdir/custom_workdir.py
Working directory : /private/home/omry/dev/hydra/outputs/2019-07-10/15-50-36
```

```bash
python demos/99_hydra_configuration/workdir/custom_workdir.py -s a=1,2 b=10,20
Sweep output dir : /checkpoint/omry/outputs/2019-07-10/17-07-58
        #0 : a=1 b=10
        #1 : a=1 b=20
        #2 : a=2 b=10
        #3 : a=2 b=20
Dask dashboard for "slurm" at http://localhost:8001.
```

Note how the sub directories contains the job number, slurm ID and then the sweep parameters:

```bash
$ tree /checkpoint/omry/outputs/2019-07-10/17-07-58
/checkpoint/omry/outputs/2019-07-10/17-07-58
├── 0_14460332_a:1,b:10
│   ├── config.yaml
│   ├── main.log
│   └── overrides.yaml
├── 1_14460333_a:1,b:20
│   ├── config.yaml
│   ├── main.log
│   └── overrides.yaml
├── 2_14460334_a:2,b:10
│   ├── config.yaml
│   ├── main.log
│   └── overrides.yaml
└── 3_14460335_a:2,b:20
    ├── config.yaml
    ├── main.log
    └── overrides.yaml
```

### Grouping by script name
You can group by script name by using the ${job:name} variable name in the config, for example: 
```/outputs/${job:name}/${now:%Y-%m-%d-%H-%M-%S}```