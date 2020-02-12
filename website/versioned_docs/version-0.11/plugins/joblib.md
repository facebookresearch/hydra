---
id: joblib
title: Joblib plugin
sidebar_label: Joblib plugin
---

The Joblib plugin provides a launcher for parallel tasks based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

Install with 
```
pip install hydra_joblib_launcher
```

Once installed, override `hydra/launcher` in your config:

```yaml
defaults:
  - hydra/launcher: joblib
```

Per default, process-based parallelism using all available CPU cores is used. By overriding the default configuration, it is e.g. possible to switch to thread-based parallelism and limit the number of parallel executions.

The default configuration packaged with the plugin is:

```yaml
hydra:
  launcher:
    class: hydra_plugins.hydra_joblib_launcher.JoblibLauncher
    params:
      joblib: ${hydra.joblib}

  joblib:
    # maximum number of concurrently running jobs. if -1, all CPUs are used
    n_jobs: -1

    # allows to hard-code backend, otherwise inferred based on prefer and require
    backend: null

    # processes or threads, soft hint to choose backend
    prefer: processes

    # null or sharedmem, sharedmem will select thread-based backend
    require: null

    # if greater than zero, prints progress messages
    verbose: 0

    # timeout limit for each task
    timeout: null

    # number of batches to be pre-dispatched
    pre_dispatch: 2*n_jobs

    # number of atomic tasks to dispatch at once to each worker
    batch_size: auto

    # folder used for memmapping large arrays for sharing memory with workers
    temp_folder: null

    # thresholds size of arrays that triggers automated memmapping
    max_nbytes: 1M

    # memmapping mode for numpy arrays passed to workers
    mmap_mode: r
```

Note that `n_jobs` defaults to -1 (all available CPUs) and `prefer` defaults to `processes`. Depending on the application, `threads` might be a good alternative. All arguments specified in `joblib` are passed to `Joblib.Parallel` (see [`Joblib.Parallel` documentation](https://joblib.readthedocs.io/en/latest/parallel.html) for full details). 

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_joblib_launcher/example) using this launcher is provided in `plugins/hydra_joblib_launcher/example`. Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will launch five parallel executions:

```text
$ python example/my_app.py --multirun task=1,2,3,4,5
[HYDRA] Sweep output dir : multirun/2020-02-05/13-59-56
[HYDRA] Joblib.Parallel(n_jobs=-1,backend=None,prefer=processes,require=None,verbose=0,timeout=None,pre_dispatch=2*n_jobs,batch_size=auto,temp_folder=None,max_nbytes=1M,mmap_mode=r) is launching 5 jobs
[HYDRA] Sweep output dir : multirun/2020-02-05/13-59-56
[__main__][INFO] - Process ID 14336 executing task 2 ...
[__main__][INFO] - Process ID 14333 executing task 1 ...
[__main__][INFO] - Process ID 14334 executing task 3 ...
[__main__][INFO] - Process ID 14335 executing task 4 ...
[__main__][INFO] - Process ID 14337 executing task 5 ...
```
