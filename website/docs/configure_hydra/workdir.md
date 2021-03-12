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
We will run the application with same command but different configurations:

```bash
python my_app.py --multirun a=a1,a2,a3 
```


Default multirun dir configurations:
<div className="row">
<div className="col col--8">

```yaml title="config.yaml"
hydra:
  sweep:
    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${hydra.job.num}

```
</div>
<div className="col  col--4">

```bash title="workding dir created"
$ tree my_app -d
my_app
├── 0
├── 1
└── 2
```
</div>
</div>


Similar configuration patterns in run can be applied to config multirun dir as well.

For example, multirun output directory grouped by job name, and sub dir by job num:
<div className="row">
<div className="col col--6">

```yaml title="config.yaml"
hydra:
  sweep:
    dir: ${hydra.job.name}
    subdir: ${hydra.job.num}

```
</div>
<div className="col  col--6">

```bash title="workding dir created"
$ tree my_app -d
my_app
├── 0
├── 1
└── 2
```
</div>
</div>


### Using `hydra.job.override_dirname`

<ExampleGithubLink text="Example application" to="examples/configure_hydra/job_override_dirname"/>

This field is populated automatically using your command line arguments and is typically being used as a part of your 
output directory pattern. It is meant to be used along with the configuration for working dir, especially
in `hydra.sweep.subdir`.

If we run the example application with the following commandline overrides and configs:

```bash
python my_app.py --multirun batch_size=32 learning_rate=0.1,0.01
```


<div className="row">
<div className="col col--6">

```yaml title="config.yaml"
hydra:
  sweep:
    dir: multirun
    subdir: ${hydra.job.override_dirname}
```
</div>
<div className="col  col--6">

```bash title="working dir created"
$ tree multirun -d
multirun
├── batch_size=32,learning_rate=0.01
└── batch_size=32,learning_rate=0.1
```
</div>
</div>

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
$ python my_app.py --multirun  batch_size=32 learning_rate=0.1,0.01 seed=1,2
```

Would result in a directory structure like:
```
$ tree multirun -d
multirun
├── batch_size=32,learning_rate=0.01
│   ├── seed=1
│   └── seed=2
└── batch_size=32,learning_rate=0.1
    ├── seed=1
    └── seed=2
```

