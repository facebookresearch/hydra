---
id: intro
title: Configuring  Hydra
sidebar_label: Introduction
---

Hydra comes pre-packages with sensible default configuration that covers the basic use cases.
You can customize that behavior by creating a `.hydra/hydra.yaml` file under your job config path.

### Working directories
Job output directory can be [customized](workdir) both for local and for cluster (sweep) runs.

### Logging
The default logging should be sufficient for most use cases but you can [customize](logging) 
the logging in your own project 

### Task name
By default, the task name is simply the name of the python file without the .py extension.
In some cases you may want to [customize](task_name) it.

### Plugins
Many plugins requires configuration via the .hydra directory.
See the documentation of individual plugins for more information about how to configure them.

## Runtime config variables
The following variables can be used in the Hydra configuration files and in the job configuration files:

| function   | arguments        | description                                                                                | Example                       | Example output      |
| ---------- |------------------| ------------------------------------------------------------------------------------------ | ------------------------------|---------------------|
| now        | strftime pattern | date/time pattern                                                                          | ${now:%Y-%m-%d_%H-%M-%S}      | 2019-07-10_11-47-35 |
| hydra      | num_jobs         | Number of jobs the launcher is starting in this sweep                                      | ${hydra:num_jobs}             | 2                   |
| job        | name             | Job name, defaults to python file name without suffix. Used for log filename, job name etc | ${job:name}                   | example_sweep       |
|            | override_dirname | Pathname derived from the overrides for this job                                           | /path/${job:override_dirname} | /path/a:1,b:I       |
|            | num              | job serial number in sweep                                                                 | ${job:num}                    | 0                   |
|            | id               | Job ID in the underlying jobs system (slurm, chronos etc)                                  | ${job:id}                     | 14445406            |



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
    * If config_path is a file, it's loaded as the base, otherwise an empty config is created
    * If the config contains a defaults block, anything from it is merged into the config
    * command line overrides are merged with the config
    
Note that the Hydra config from .hydra is loaded using the same function as your own config.
