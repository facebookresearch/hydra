## Hydra
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
