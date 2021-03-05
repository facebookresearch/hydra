---
id: workdir
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Example application" to="examples/configure_hydra/workdir"/>

Below are a few examples of customizing output directory patterns.

### Configuration for run

Run output directory grouped by date:
```yaml
hydra:
  run:
    dir: ./outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
```

Run output directory grouped by job name:
```yaml
hydra:
  run:
    dir: outputs/${hydra.job.name}/${now:%Y-%m-%d_%H-%M-%S}
```

Run output directory can contain user configuration variables:
```yaml
hydra:
  run:
    dir: outputs/${now:%Y-%m-%d_%H-%M-%S}/opt:${optimizer.type}
```

### Configuration for multirun

Sweep sub directory contains the job number for the job instance:
```yaml
hydra:
  sweep:
    dir: sweep_dir
    subdir: ${hydra.job.num}
```
Run the example application
```bash
python my_app.py --multirun a=a1,a2,a3 
```

Would create working dir structure like:
```bash
$ tree sweep_dir -d
sweep_dir
├── 0
├── 1
└── 2
```

### Using `hydra.job.override_dirname`

<ExampleGithubLink text="Example application" to="examples/configure_hydra/job_override_dirname"/>

This field is populated automatically using your command line arguments and is typically being used as a part of your 
output directory pattern. It is meant to be used along with the configuration for working dir, especially
in `hydra.sweep.subdir`.

For example, we configure the example application like the following
```yaml
hydra:
  sweep:
    dir: multirun
    subdir: ${hydra.job.override_dirname}
```

then run the application with command-line overrides:

```bash
python my_app.py --multirun a=a1 b=b1
```
Would result in creating a output dir `multirun/a=a1,b=b1`

You can further customized the output dir creation by configuring`hydra.job.override_dirname`.

In particular, the separator char `=` and the item separator char `,` can be modified by overriding 
`hydra.job.config.override_dirname.kv_sep` and `hydra.job.config.override_dirname.item_sep`.
Command line override keys can also be automatically excluded from the generated `override_dirname`.

An example of a case where the exclude is useful is a random seed.

```yaml
hydra:
  run:
    dir: output/${hydra.job.override_dirname}/seed=${seed}
  job:
    config:
      override_dirname:
        exclude_keys:
          - seed
```
With this configuration, running
```bash
$ python my_app.py --multirun a=a1,a2 b=b1 seed=1,2
```

Would result in a directory structure like:
```
$ tree multirun -d
multirun
├── a=a1,b=b1
│   ├── seed=1
│   └── seed=2
└── a=a2,b=b1
    ├── seed=1
    └── seed=2
```
