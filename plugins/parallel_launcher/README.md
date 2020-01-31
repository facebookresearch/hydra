# Parallel Launcher

This plugin provides a launcher for [embrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel) tasks. It is based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

An example app using the plugin is provided in `plugins/parallel_launcher/example`. Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will launch five parallel executions.

The maximum number of concurrently running jobs can be restricted by providing `hydra.launcher.params.n_jobs`. In the example application, `n_jobs` is set to -1, which means that all available CPUs may be used:

`hydra_plugins/parallel_launcher/conf/hydra/launcher/example.yaml`:
```yaml
hydra:
  launcher:
    class: hydra_plugins.parallel_launcher.ParallelLauncher
    params:
      n_jobs: -1
```

Output of the example application:
```text
$ python example/my_app.py --multirun task=1,2,3,4,5
[2020-01-31 11:32:22,454][HYDRA] Sweep output dir : multirun/2020-01-31/11-32-22
[2020-01-31 11:32:22,455][HYDRA] ParallelLauncher(n_jobs=-1) is launching 5 jobs
[2020-01-31 11:32:22,455][HYDRA] Sweep output dir : multirun/2020-01-31/11-32-22
Executing task 1 ...
Executing task 3 ...
Executing task 2 ...
Executing task 4 ...
Executing task 5 ...
```

All available keyword arguments for `joblib.Parallel` can be set through the config. For full reference, refer to the [Joblib documentation](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html).

The plugin is based on the idea and inital implementation of @emilemathieutmp in [#357](https://github.com/facebookresearch/hydra/issues/357).
