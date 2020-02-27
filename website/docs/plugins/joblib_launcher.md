---
id: joblib_launcher
title: Joblib Launcher plugin
sidebar_label: Joblib Launcher plugin
---

The Joblib Launcher plugin provides a launcher for parallel tasks based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

Install with 
```
pip install hydra_joblib_launcher
```

Once installed, override `hydra/launcher` in your config:

```yaml
defaults:
  - hydra/launcher: joblib
```

By default, process-based parallelism using all available CPU cores is used. By overriding the default configuration, it is e.g. possible limit the number of parallel executions.

The default configuration packaged with the plugin is:
TODO : UPDATE
```yaml
hydra:
  launcher:
    class: hydra_plugins.hydra_joblib_launcher.JoblibLauncher
    params:
      joblib: ${hydra.joblib}

  joblib:
    # maximum number of concurrently running jobs. if -1, all CPUs are used
    n_jobs: -1

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
    max_nbytes: null

    # memmapping mode for numpy arrays passed to workers
    mmap_mode: r
```

`n_jobs` defaults to -1 (all available CPUs). See [`Joblib.Parallel` documentation](https://joblib.readthedocs.io/en/latest/parallel.html) for full details on arguments. Note that the backend is hard-coded to use process-based parallelism (Joblib's loky backend), since thread-based parallelism is incompatible with Hydra.

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_joblib_launcher/example) using this launcher is provided in `plugins/hydra_joblib_launcher/example`. Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will launch five parallel executions:

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
