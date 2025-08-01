---
id: job
sidebar_label: Job Configuration
hide_title: true
---
## Job configuration

The job configuration resides in `hydra.job`.
The structure definition is below, the latest definition [in the code](https://github.com/facebookresearch/hydra/blob/master/hydra/conf/__init__.py).

<details>
  <summary>Expand definition</summary>

  ```python
  # job runtime information will be populated here
  @dataclass
  class JobConf:
      # Job name, populated automatically unless specified by the user (in config or cli)
      name: str = MISSING

      # Concatenation of job overrides that can be used as a part
      # of the directory name.
      # This can be configured in hydra.job.config.override_dirname
      override_dirname: str = MISSING

      # Job ID in underlying scheduling system
      id: str = MISSING

      # Job number if job is a part of a sweep
      num: int = MISSING

      # The config name used by the job
      config_name: Optional[str] = MISSING

      # Environment variables to set remotely
      env_set: Dict[str, str] = field(default_factory=dict)
      # Environment variables to copy from the launching machine
      env_copy: List[str] = field(default_factory=list)

      # Job config
      @dataclass
      class JobConfig:
          @dataclass
          # configuration for the ${hydra.job.override_dirname} runtime variable
          class OverrideDirname:
              kv_sep: str = "="
              item_sep: str = ","
              exclude_keys: List[str] = field(default_factory=list)

          override_dirname: OverrideDirname = field(default_factory=OverrideDirname)

      config: JobConfig = field(default_factory=JobConfig)
  ```
</details>

## Documentation
### hydra.job.name
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/1.0_branch/examples/configure_hydra/job_name)

The job name is used by different things in Hydra, such as the log file name (`${hydra.job.name}.log`).
It is normally derived from the Python file name (file: `train.py` -> name: `train`).
You can override it via the command line or your config file.

### hydra.job.override_dirname
This field is populated automatically using your command line arguments and is typically being used as a part of your
output directory pattern.
For example, the command line arguments:
```bash
$ python foo.py a=10 b=20
```
Would result in `hydra.job.override_dirname` getting the value a=10,b=20.
When used with the output directory override, it can automatically generate directories that represent the
command line arguments used in your run.
```yaml
hydra:
  run:
    dir: output/${hydra.job.override_dirname}
```

The generation of override_dirname can be controlled by `hydra.job.config.override_dirname`.
In particular, the separator char `=` and the item separator char `,` can be modified, and in addition some command line
override keys can be automatically excluded from the generated `override_dirname`.
An example of a case where the exclude is useful is a random seed.

```yaml
hydra:
  run:
    dir: output/${hydra.job.override_dirname}/seed=${seed}
  job:
    config:
      override_dirname:
        exclude_keys:
          - seed
```
With this configuration, running
```bash
$ python foo.py a=10 b=20 seed=999
```

Would result in a directory like:
```
output/a=10,b=20/seed=999
```
Allowing you to more easily group identical runs with different random seeds together.

### hydra.job.id
The job ID is populated by active Hydra launcher. For the basic launcher, the job ID is just a serial job number, but
for other systems this could be the SLURM job ID or the AWS Instance ID.

### hydra.job.num
Serial job number within this current sweep run. (0 to n-1)

### hydra.job.config_name
The config name used by the job, this is populated automatically to match the config name in @hydra.main()

### hydra.job.env_set
A Dict[str, str] that is used to set the environment variables of the running job.
Some common use cases are to set environment variables that are effecting underlying libraries, for example
```yaml
hydra:
  job:
    env_set:
      OMP_NUM_THREADS: 1
```
Disables multithreading in Intel IPP and MKL.

Another example, is to use interpolation to automatically set the rank
for [Torch Distributed](https://pytorch.org/tutorials/intermediate/dist_tuto.html) run to match the job number
in the sweep.

```yaml
hydra:
  job:
    env_set:
      RANK: ${hydra:job.num}
```

### hydra.job.env_copy
In some cases you want to automatically copy local environment variables to the running job environment variables.
This is particularly useful for remote runs.
```yaml
hydra:
  job:
    env_copy:
      - AWS_KEY
```
