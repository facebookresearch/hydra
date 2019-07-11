# Hydra config
Hydra is very flexible and can be customized.

## Anatomy of a Hydra run
When Hydra runs your code, the following things happen:
* Hydra config is created:
    * Default Hydra config from package is loaded
    * Optional Hydra config from .hydra under your job config root is loaded
    * Your config is overlayed over the default config
    * Any command line overrides overrides that starts with hydra. are being merged in
* Your job config is created:
    *  All your config files are loaded from the config root:
        * @hydra.main() : the directory of your python file
        * @hydra.main(config_path='conf/') : conf relative to your python file
        * @hydra.main(config_path='conf/config.yaml') : conf relative to your python file
    * It config_path is a file, it's loaded as the base, otherwise an empty config is created
    * If the config contains a defaults block, anything from it is merged into the config
    * command line overrides are merged with the config
    
Note that the Hydra config from .hydra is loaded using the same function as your own config.

## Runtime config variables
The following variables can be used in hydra config or the job config:

| function   | arguments        | description                                                                                | Example                       | Example output      |
| ---------- |------------------| ------------------------------------------------------------------------------------------ | ------------------------------|---------------------|
| now        | strftime pattern | date/time pattern                                                                          | ${now:%Y-%m-%d_%H-%M-%S}      | 2019-07-10_11-47-35 |
| job        | name             | Job name, defaults to python file name without suffix. Used for log filename, job name etc | ${job:name}                   | example_sweep       |
|            | override_dirname | Pathname derived from the overrides for this job                                           | /path/${job:override_dirname} | /path/a:1,b:I       |
|            | num              | job serial number in sweep                                                                 | ${job:num}                    | 0                   |
|            | id               | Job ID in the underlying jobs system (slurm, chronos etc)                                  | ${job:id}                     | 14445406            |
|            |                  |                                                                                            |                               |                     |

## Working directories
This is the default configuration for hydra config (from [default_conf/hydra.yaml](../hydra/default_conf/hydra.yaml))
Hydra separate the config for the working directory into run and sweep.
Run is for local runs, and sweep is from cluster runs (Slurm, Chronos etc).

### Run:
Just the run directory, typically timestamped and relative to your current working directory.

### Sweep:
Divided into dir and subdir.
Dir is the parent dir for all the swipe job working directories and subdir is the dir for each job.

```yaml
hydra:
  run:
    dir: ./outputs/${now:%Y-%m-%d_%H-%M-%S}
  sweep:
    dir: /checkpoint/${env:USER}/outputs/${now:%Y-%m-%d_%H-%M-%S}
    # you can also use ${job:override_dirname} to have a directory name with job sweep arguments
    subdir: ${job:num}_${job:id}
```

Those can be customized in the job .hydra/hydra.yaml config.

Check the [workdir config](../demos/99_hydra_configuration/workdir) demo.



## Logging
[Default logging](../hydra/default_conf/logging.yaml) should be sufficient for most use cases but you can customize
the logging in your own project. 
If you want something different check the [logging config](../demos/99_hydra_configuration/logging) demo.

