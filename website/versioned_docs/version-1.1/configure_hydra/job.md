---
id: job
title: Job Configuration
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

The job configuration resides in `hydra.job`.
The Structured Config is below, the latest definition is <GithubLink to="hydra/conf/__init__.py">here</GithubLink>.

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

### hydra.job.name
<ExampleGithubLink text="Example application" to="examples/configure_hydra/job_name"/>

The job name is used by different things in Hydra, such as the log file name (`${hydra.job.name}.log`).
It is normally derived from the Python file name (The job name of the file `train.py` is `train`).
You can override it via the command line, or your config file.

### hydra.job.override_dirname
Enables the creation of an output directory which is based on command line overrides.
Learn more at the [Customizing Working Directory](/configure_hydra/workdir.md) page.

### hydra.job.id
The job ID is populated by the active Hydra launcher. For the basic launcher, the job ID is just a serial job number.
Other launchers will set it to an ID that makes sense like SLURM job ID.

### hydra.job.num
Serial job number within this current sweep run. (0 to n-1).

### hydra.job.config_name
The config name used by the job, this is populated automatically to match the config name in `@hydra.main()`.

### hydra.job.env_set
A `Dict[str, str]` that is used to set the environment variables of the running job.
Some common use cases are to automatically set environment variables that are affecting underlying libraries.
For example, the following will disables multithreading in Intel IPP and MKL:
```yaml
hydra:
  job:
    env_set:
      OMP_NUM_THREADS: 1
```

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
