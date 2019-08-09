---
id: workdir
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---

This example customizes the working directory in both run and sweeps using the following config snippet:
You can put that snippet either in `.hydra/hydra.yaml` or in your own task
configuration (e.g. `conf/config.yaml`)
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

```text
python experiment.py -s a=1,2 b=10,20
Sweep output dir : /checkpoint/omry/outputs/2019-07-10/17-07-58
        #0 : a=1 b=10
        #1 : a=1 b=20
        #2 : a=2 b=10
        #3 : a=2 b=20
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

### Using job name
You can use the job name as a part of the output directory pattern.
The folloing example will group your output directories by the name of the job: 
```/outputs/${job:name}/${now:%Y-%m-%d-%H-%M-%S}```

### Using job configuration variables
You can use any configuration variable from your job configuration as a part of the output directory.
For example, in sweep runs - You may to have a directory structure that uses the parameters of the job, followed by
the random seed used in the job.
configuration:
```yaml
  sweep:
    dir: /checkpoint/${env:USER}/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${job:num}_${job:id}_${job:override_dirname}/${random_seed}
```

Check the [runnable example](https://github.com/facebookresearch/hydra/tree/master/demos/99_hydra_configuration/workdir).