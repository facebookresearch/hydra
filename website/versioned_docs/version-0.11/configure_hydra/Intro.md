---
id: intro
title: Overview
sidebar_label: Introduction
---

Many things in Hydra can be customized, this includes:
* Logging configuration
* Run and Multirun output directory patterns
* Application help (--help and --hydra-help)

Hydra can be customized using the same methods you are already familiar with from the tutorial.
You can include some Hydra config snippet in your own config to override it directly, or compose in different
configurations provided by plugins or by your own code. You can also override everything in Hydra from the command 
line just like with your own configuration.

The Hydra configuration actually lives in the same config object as your configuration, but is removed prior to running
your function to reduce confusion.
You can view the configuration with `--cfg hydra|job|all`

The Hydra configuration itself is composed from multiple config files. here is a partial list:
```yaml
defaults:
  - hydra/job_logging : default     # Job's logging config
  - hydra/launcher: basic           # Launcher config
  - hydra/sweeper: basic            # Sweeper config
  - hydra/output: default           # Output directory
```
You can view the Hydra config structure [here](https://github.com/facebookresearch/hydra/tree/0.11_branch/hydra/conf).

This is a subset of the composed Hydra configuration node:

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

`hydra.job`:
- *hydra.job.name* : Job name, defaults to python file name without suffix. can be overridden.
- *hydra.job.override_dirname* : Pathname derived from the overrides for this job
- *hydra.job.num* : job serial number in sweep
- *hydra.job.id* : Job ID in the underlying jobs system (Slurm etc) 

`hydra.runtime`:
- *hydra.runtime.version*: Hydra's version
- *hydra.runtime.cwd*: Original working directory the app was executed from

