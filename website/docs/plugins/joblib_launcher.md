---
id: joblib_launcher
title: Joblib Launcher plugin
sidebar_label: Joblib Launcher plugin
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

[![PyPI](https://img.shields.io/pypi/v/hydra-joblib-launcher)](https://pypi.org/project/hydra-joblib-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-joblib-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-joblib-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-joblib-launcher.svg)](https://pypistats.org/packages/hydra-joblib-launcher)<ExampleGithubLink text="Example application" to="plugins/hydra_joblib_launcher/example"/><ExampleGithubLink text="Plugin source" to="plugins/hydra_joblib_launcher"/>

The Joblib Launcher plugin provides a launcher for parallel tasks based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

### Process backends

The launcher supports two process backends:

| Backend | Advantages | Tradeoffs |
| --- | --- | --- |
| `loky` (default) | Robust process management and Cloudpickle support for dynamically defined Python objects. It remains the default for compatibility. | Workers are reused between Hydra jobs, so arbitrary application caches or process-global state can leak between jobs. Cloudpickling the task can also fail when it reaches some native-library objects. |
| `multiprocessing` | Runs every Hydra job in a fresh worker process and sends module-level function tasks by reference instead of Cloudpickling them. This provides strict process isolation and avoids serializing module-level native-library objects referenced by the task. | Functions must be defined at module scope. Custom decorators around `@hydra.main` must use `functools.wraps`. |

Loky runs jobs in the parent process when `n_jobs=1`. The multiprocessing
backend retains per-job worker isolation while executing one job at a time.

### Installation
```commandline
pip install hydra-joblib-launcher --upgrade
```

### Usage
Once installed, add `hydra/launcher=joblib` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - override hydra/launcher: joblib
```
By default, the launcher uses process-based parallelism with all available CPU
cores. Set `hydra.launcher.n_jobs` to limit the number of jobs that can run
concurrently.

The JobLibLauncherConf backing the config is defined <GithubLink to="plugins/hydra_joblib_launcher/hydra_plugins/hydra_joblib_launcher/config.py">here</GithubLink>:

You can discover the Joblib Launcher parameters with:
```yaml title="$ python your_app.py hydra/launcher=joblib --cfg hydra -p hydra.launcher"
# @package hydra.launcher
_target_: hydra_plugins.hydra_joblib_launcher.joblib_launcher.JoblibLauncher
n_jobs: -1
inner_max_num_threads: null
backend: loky
prefer: processes
require: null
verbose: 0
timeout: null
pre_dispatch: 2*n_jobs
batch_size: auto
temp_folder: null
max_nbytes: null
mmap_mode: r
```
There are several standard approaches for configuring plugins. Check [this page](../patterns/configuring_plugins.md) for more information.

See [`Joblib.Parallel` documentation](https://joblib.readthedocs.io/en/latest/parallel.html) for full details about the parameters above.

`backend` selects the backend used by this launcher. Because a backend is
always selected explicitly, `prefer` does not change it. `require` must be
compatible with the selected backend; `require=sharedmem` is unsupported
because this launcher does not support a thread-based backend.

#### Controlling native library thread pools

When using libraries that manage native thread pools, such as OpenBLAS, MKL, OpenMP, Numba, or NumExpr, set `inner_max_num_threads` to limit the number of native threads available to each Joblib worker process:

```yaml
hydra:
  launcher:
    n_jobs: 8
    inner_max_num_threads: 1
```

This can help avoid oversubscription when multiple Hydra jobs run in parallel and each job calls into a multithreaded native library. For arbitrary environment variables, use [`hydra.job.env_set`](../configure_hydra/job.md#hydrajobenv_set) instead.

<div class="alert alert--info" role="alert">
Select the `multiprocessing` backend to execute every job in a fresh worker
process:

```yaml
hydra:
  launcher:
    backend: multiprocessing
    n_jobs: 4
```

The launcher automatically sets Joblib's `batch_size=1` so that each pool task
contains one Hydra job, and `maxtasksperchild=1` so that the worker exits after
that task. These are internal correctness settings, not user configuration.
Conflicting values are rejected.

`inner_max_num_threads` is supported only by `loky`. Custom decorators around
`@hydra.main` must follow the
[Hydra task-decorator requirements](../advanced/decorating_main.md). Callable
task objects are copied to each worker, so all state stored on them must support
Python pickling.
</div><br/>

An <GithubLink to="plugins/hydra_joblib_launcher/example">example application</GithubLink> using this launcher is provided in the plugin repository.

Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will launch five parallel executions:

```text
$ python my_app.py --multirun task=1,2,3,4,5
[HYDRA] Joblib.Parallel(n_jobs=10,backend=loky,prefer=processes,require=None,verbose=0,timeout=None,pre_dispatch=2*n_jobs,batch_size=auto,temp_folder=None,max_nbytes=None,mmap_mode=r) is launching 5 jobs
[HYDRA] Launching jobs, sweep output dir : multirun/2020-02-18/10-00-00
[__main__][INFO] - Process ID 14336 executing task 2 ...
[__main__][INFO] - Process ID 14333 executing task 1 ...
[__main__][INFO] - Process ID 14334 executing task 3 ...
[__main__][INFO] - Process ID 14335 executing task 4 ...
[__main__][INFO] - Process ID 14337 executing task 5 ...
```
