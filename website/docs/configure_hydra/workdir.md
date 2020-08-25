---
id: workdir
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---

[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/configure_hydra/workdir)

Below are a few examples of customizing output directory patterns.

Run output directory grouped by day:
```yaml
hydra:
  run:
    dir: ./outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
```

Sweep sub directory contains the the job number and the override parameters for the job instance:
```yaml
hydra:
  sweep:
    subdir: ${hydra.job.num}_${hydra.job.override_dirname}
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

Run output directory can contain override parameters for the job:

See [Override dirname](./job#hydrajoboverride_dirname) in the Job configuration page for details on how to customize
`hydra.job.override_dirname`.

```yaml
hydra:
  run:
    dir: output/${hydra.job.override_dirname}
```
