---
id: workdir
title: Customizing working directory pattern
sidebar_label: Customizing working directory pattern
---

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

### Customizing outputs with substitution through the CLI 

Outputs can also be configured through the CLI, like any other configuration.

>python train.py model.nb_layers=3 hydra.run.dir=3_layers

This feature can become really powerful to write multiruns without boilerplate using substitution.

> python train.py --multirun model.nb_layers=1,2,3,5 hydra.sweep.dir=multiruns/layers_effect hydra.sweep.subdir=\&#0036;{model.nb_layers}


With bash, be careful to escape the $ symbol. Otherwise, bash will try to resolve the substitution, instead of passing it to Hydra.
