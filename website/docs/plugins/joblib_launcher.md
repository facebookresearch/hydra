---
id: joblib_launcher
title: Joblib Launcher plugin
sidebar_label: Joblib Launcher plugin
---
[![PyPI](https://img.shields.io/pypi/v/hydra-joblib-launcher)](https://pypi.org/project/hydra-joblib-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-joblib-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-joblib-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-joblib-launcher.svg)](https://pypistats.org/packages/hydra-joblib-launcher)

The Joblib Launcher plugin provides a launcher for parallel tasks based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

Install with 
```
pip install hydra_joblib_launcher
```

<div class="alert alert--info" role="alert">
NOTE: This plugin depends on Hydra 1.0 which is not yet released, if you want to try it install Hydra from master
</div><br/>


Once installed, override `hydra/launcher` in your config:

```yaml
defaults:
  - hydra/launcher: joblib
```

By default, process-based parallelism using all available CPU cores is used. By overriding the default configuration, it is e.g. possible limit the number of parallel executions.

The default configuration packaged with the plugin is:
```yaml
hydra:
  launcher:
    class: hydra_plugins.hydra_joblib_launcher.JoblibLauncher
    params: # See JobLibConf class below
      ... 
```

The JobLibConf class is defined [here](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_joblib_launcher/hydra_plugins/hydra_joblib_launcher/config.py):

It looks like this: 

```python
@dataclass
class JobLibConf:
    # maximum number of concurrently running jobs. if -1, all CPUs are used
    n_jobs: int = -1

    # allows to hard-code backend, otherwise inferred based on prefer and require
    backend: Optional[str] = None

    # processes or threads, soft hint to choose backend
    prefer: str = "processes"

    # null or sharedmem, sharedmem will select thread-based backend
    require: Optional[str] = None

    # if greater than zero, prints progress messages
    verbose: int = 0

    # timeout limit for each task
    timeout: Optional[int] = None

    # number of batches to be pre-dispatched
    pre_dispatch: str = "2*n_jobs"

    # number of atomic tasks to dispatch at once to each worker
    batch_size: str = "auto"

    # folder used for memmapping large arrays for sharing memory with workers
    temp_folder: Optional[str] = None

    # thresholds size of arrays that triggers automated memmapping
    max_nbytes: Optional[str] = None

    # memmapping mode for numpy arrays passed to workers
    mmap_mode: str = "r"
```

See [`Joblib.Parallel` documentation](https://joblib.readthedocs.io/en/latest/parallel.html) for full details about the parameters above.

<div class="alert alert--info" role="alert">
NOTE: The only supported JobLib backend is Loky (process-based parallelism).
</div><br/>

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_joblib_launcher/example) using this launcher is provided in the plugin repository.

Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will launch five parallel executions:

```text
$ python my_app.py --multirun task=1,2,3,4,5
[HYDRA] Joblib.Parallel(n_jobs=-1,verbose=0,timeout=None,pre_dispatch=2*n_jobs,batch_size=auto,temp_folder=None,max_nbytes=None,mmap_mode=r,backend=loky) is launching 5 jobs
[HYDRA] Launching jobs, sweep output dir : multirun/2020-02-18/10-00-00
[__main__][INFO] - Process ID 14336 executing task 2 ...
[__main__][INFO] - Process ID 14333 executing task 1 ...
[__main__][INFO] - Process ID 14334 executing task 3 ...
[__main__][INFO] - Process ID 14335 executing task 4 ...
[__main__][INFO] - Process ID 14337 executing task 5 ...
```
