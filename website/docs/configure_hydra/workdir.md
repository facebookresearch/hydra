---
id: workdir
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---

See the [intro](intro) for details about how to apply the customization.

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
    subdir: ${hydra.job.num}_${hydra.job.num}_${hydra.job.override_dirname}
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

Run output directory can contain override parameters for the job
```yaml
hydra:
  run:
    dir: output/${hydra.job.override_dirname}
```


### Configuring hydra.job.override_dirname
`hydra.job.override_dirname` can be configured via hydra.job.config.override_dirname.
You can exclude keys such as `random_seed` or change the separator used to construct override_dirname.

```yaml
hydra:
  job:
    config:
      # configuration for the ${hydra.job.override_dirname} runtime variable
      override_dirname:
        kv_sep: '='
        item_sep: ','
        exclude_keys: []
```