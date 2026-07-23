---
id: workdir
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Example application" to="examples/configure_hydra/workdir"/>

Hydra automatically creates an output directory used to store log files and
save yaml configs. This directory can be configured by setting `hydra.run.dir`
(for single hydra runs) or `hydra.sweep.dir`/`hydra.sweep.subdir` (for multirun
sweeps). At runtime, the path of the output directory can be
[accessed](Intro.md#accessing-the-hydra-config) via the `hydra.runtime.output_dir` variable.
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


### Using `hydra_override_dirname`

<ExampleGithubLink text="Example application" to="examples/configure_hydra/job_override_dirname"/>

The `hydra_override_dirname` resolver derives a directory name from your command line arguments. It is typically used as a part of your output directory pattern, especially in `hydra.sweep.subdir`.

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
    subdir: ${hydra_override_dirname:}
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

You can further customize the output dir creation by passing options to the resolver.
In particular, the separator char `=`, the item separator char `,`, and excluded command line override keys can be configured directly at the use site.

An example of a case where the exclude is useful is a random seed.

```yaml
hydra:
  sweep:
    dir: multirun
    subdir: '${hydra_override_dirname:{exclude_keys: [seed]}}/seed=${seed}'
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

Custom separators can be specified the same way:

```yaml
hydra:
  sweep:
    subdir: '${hydra_override_dirname:{kv_sep: "-", item_sep: "_", exclude_keys: [seed]}}'
```

For more control, `element_resolver` can apply a custom OmegaConf resolver to each directory name element before the elements are joined.
The resolver must be registered separately before Hydra starts.
For example, this replaces path separators, including Windows path separators, with `_`:

```python
from omegaconf import OmegaConf

OmegaConf.register_resolver(
    "pathsafe",
    lambda value: str(value).replace("/", "_").replace("\\", "_"),
)
```

```yaml
hydra:
  sweep:
    subdir: '${hydra_override_dirname:{item_sep: "/", element_resolver: pathsafe}}'
```
