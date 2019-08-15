## Hydra
### 08/14/2019
#### New basic launcher and changes to remote launcher
Changes to how cluster execution happens:
Before this diff, -s|--sweep would activate the default launcher (fairtask or submitit, if configured), and 
also activate the basic sweeper to generate multiple jobs and launch them.
After this diff, -s replaced by the -m|multirun.
--multirun runs multiple in the same way -s did, but by default it runs locally using a new basic launche. 
the new will execute the jobs locally and serially.

```text
$ python demos/0_minimal/minimal.py -m a=1,2
[2019-08-14 20:37:29,391][hydra.launcher.basic_launcher][INFO] - Launching 2 jobs locally
[2019-08-14 20:37:29,391][hydra.launcher.basic_launcher][INFO] - Sweep output dir : ./outputs/2019-08-14_20-37-29
[2019-08-14 20:37:29,391][hydra.launcher.basic_launcher][INFO] -        #0 : a=1
a: 1

[2019-08-14 20:37:29,452][hydra.launcher.basic_launcher][INFO] -        #1 : a=2
a: 2
```
To select a different launcher:
```text
$ python demos/6_sweep/experiment.py -m launcher=fairtask a=1,2 b=10,20
[2019-08-14 20:12:28,221][hydra_plugins.fairtask.fairtask_launcher][INFO] - Sweep output dir : /checkpoint/omry/outputs/2019-08-14_20-12-28
[2019-08-14 20:12:28,301][hydra_plugins.fairtask.fairtask_launcher][INFO] - Launching 4 jobs to slurm queue
[2019-08-14 20:12:28,301][hydra_plugins.fairtask.fairtask_launcher][INFO] -     #0 : a=1 b=10
[2019-08-14 20:12:28,301][hydra_plugins.fairtask.fairtask_launcher][INFO] -     #1 : a=1 b=20
[2019-08-14 20:12:28,301][hydra_plugins.fairtask.fairtask_launcher][INFO] -     #2 : a=2 b=10
[2019-08-14 20:12:28,301][hydra_plugins.fairtask.fairtask_launcher][INFO] -     #3 : a=2 b=20
```

#### Initial support for config search path
This is implemented and used internally but is not yet available to the end user.
More on this in a followup update.

#### disabled logging
Introduced a method for disabling hydra and/or the job logging completely:
```
$ python demos/2_logging/logging_example.py -m a=1,2 hydra_logging=disabled job_logging=disabled
```
Another change to logging is that if you are cusotmizng it you will now need to specify a complete logging
config snippet for your job (Your logging could would replace, not merge with the default one)

#### Config load tracing
You can now see how your config is composed by activating verbose logging for hydra:
```text
$ python demos/6_sweep/experiment.py -v hydra
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: pkg://hydra.default_conf/default_hydra.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: /private/home/omry/dev/hydra/demos/6_sweep/conf/.hydra/hydra.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: /private/home/omry/dev/hydra/demos/6_sweep/conf/config.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: pkg://hydra.default_conf.hydra_logging/default.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: pkg://hydra.default_conf.job_logging/default.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: /private/home/omry/dev/hydra/demos/6_sweep/conf/.hydra/launcher/fairtask.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: pkg://hydra.default_conf.sweeper/basic.yaml
[2019-08-14 20:55:54,453][hydra.hydra][DEBUG] - Loaded: /private/home/omry/dev/hydra/demos/6_sweep/conf/optimizer/nesterov.yaml
[2019-08-14 20:55:54,476][__main__][INFO] - optimizer:
  lr: 0.001
  type: nesterov
```
####
Official Mac OS support.
Hydra is now tested on Mac OS in the continuous integration (CircleCI)
If you are using it on Mac and it's misbehaving please file an issue.

### 08/10/2019
Reworked internal configuration loading to make Hydra more consistent and flexible.
It is now possible to override all of the Hydra configuration option from:
 * .hydra/hydra.yaml in the config path.
 * directly from the job config
 * from the command line
Merging is done in this order:
 - default Hydra configuration
 - .hydra/hydra.yaml in the config path
 - job configuration hydra branch
 - command line overrides starting with hydra.


#### Incompatible changes
If you were using anything on the left below you need to change your code / config / command line.
- ${job:name} -> hydra.job.name
- ${job:override_dirname} -> hydra.job.override_dirname
- ${job:num} -> hydra.job.num
- ${job:id} -> hydra.job.id
- ${hydra:num_jobs) -> hydra.job.num_jobs
- Logging configuration node for job changed from `hydra.task_logging` to `hydra.job_logging`

### 07/24/2019
* Separated logging into hydra_logging and task_logging [#24](https://github.com/fairinternal/hydra/issues/24)
* Integrated code coverage into nox (current coverage 80%)
* Improved test coverage [#23](https://github.com/fairinternal/hydra/issues/23)
