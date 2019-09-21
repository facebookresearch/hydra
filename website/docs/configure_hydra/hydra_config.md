---
id: hydra_config
title: Hydra configuration
sidebar_label: Hydra configuration
---

Anything under the hydra branch of the config can be overridden in various ways.
See the [intro](intro) for details about how to apply the customization.

```yaml
hydra:
  run:
    # Output directory for normal runs
    dir: ./outputs/${now:%Y-%m-%d_%H-%M-%S}
  sweep:
    # Output directory for sweep runs
    dir: /checkpoint/${env:USER}/outputs/${now:%Y-%m-%d_%H-%M-%S}
    # Output sub directory for sweep runs.
    subdir: ${hydra.job.num}_${hydra.job.id}
```

## Runtime variables
The following variables are populated at runtime.
You can access them as config variables.

- *hydra.job.name* : Job name, defaults to python file name without suffix. can be overridden.
- *hydra.job.override_dirname* : Pathname derived from the overrides for this job
- *hydra.job.num* : job serial number in sweep
- *hydra.job.id* : Job ID in the underlying jobs system (Slurm etc) 
- *hydra.job.num_jobs*: Number of jobs the launcher is starting in this sweep
