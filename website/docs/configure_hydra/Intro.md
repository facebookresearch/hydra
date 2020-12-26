---
id: intro
title: Overview
sidebar_label: Introduction
---

Many things in Hydra can be customized. This includes:
* Launcher configurations
* Sweeper configuration
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
```yaml title="hydra/config"
defaults:
  - job_logging : default     # Job's logging config
  - launcher: basic           # Launcher config
  - sweeper: basic            # Sweeper config
  - output: default           # Output directory
```
You can view the Hydra config structure [here](https://github.com/facebookresearch/hydra/tree/master/hydra/conf).

You can view the Hydra config using `--cfg hydra`:
```yaml title="$ python my_app.py --cfg hydra"
hydra:
  run:
    dir: outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
  sweep:
    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${hydra.job.num}
  launcher:
    _target_: hydra._internal.core_plugins.basic_launcher.BasicLauncher
  sweeper:
    _target_: hydra._internal.core_plugins.basic_sweeper.BasicSweeper
    max_batch_size: null
  hydra_logging:
    version: 1
    formatters:
    ...
```

## Runtime variables
The Hydra config is large. To reduce clutter in your own config it's being deleted from the config object
Hydra is passing to the function annotated by `@hydra.main()`.

There are two ways to access the Hydra config:

#### In your config, using the `hydra` resolver:
```yaml
config_name: ${hydra:job.name}
```
Pay close attention to the syntax: The resolver name is `hydra`, and the `key` is passed after the colon.

#### In your code, using the HydraConfig singleton.
```python
from hydra.core.hydra_config import HydraConfig

@hydra.main()
def my_app(cfg: DictConfig) -> None:
    print(HydraConfig.get().job.name)
```

The following variables are populated at runtime.  

#### hydra.job:
- **hydra.job.name** : Job name, defaults to the Python file name without the suffix. can be overridden.
- **hydra.job.override_dirname** : Pathname derived from the overrides for this job
- **hydra.job.num** : job serial number in sweep
- **hydra.job.id** : Job ID in the underlying jobs system (SLURM etc)

#### hydra.runtime:
- *hydra.runtime.version*: Hydra's version
- *hydra.runtime.cwd*: Original working directory the app was executed from

#### hydra.choices
A dictionary containing the final choices of the Defaults List. Can be accessed 
via the HydraConfig singleton or config interpolation e.g. `model : ${hydra:choices.model}`.

### Hydra resolvers
Hydra supports several [OmegaConf resolvers](https://github.com/facebookresearch/hydra/blob/master/hydra/core/utils.py) by default.

**hydra**: Interpolates into the `hydra` config node. e.g. Use `${hydra:job.name}` to get the Hydra job name.

**now**: Creates a string representing the current time using 
[strftime](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior). 
e.g. for formatting the time you can use something like`${now:%H-%M-%S}`.

**python_version**: Return a string representing the runtime python version by calling `sys.version_info`.
Takes an optional argument of a string with the values major, minor or macro.
e.g:
```yaml
default: ${python_version:}          # 3.8
major:   ${python_version:major}     # 3
minor:   ${python_version:minor}     # 3.8
micro:   ${python_version:micro}     # 3.8.2
```

You can learn more about OmegaConf <a class="external" href="https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation" target="_blank">here</a>.
