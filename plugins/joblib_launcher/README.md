# Joblib Launcher

This plugin provides a launcher for parallel tasks based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

The configuration for this launcher is packaged with the plugin.

`hydra_plugins/joblib_launcher/conf/hydra/launcher/joblib.yaml`:
```yaml
hydra:
  launcher:
    class: hydra_plugins.joblib_launcher.JoblibLauncher
    joblib_arguments:
      backend: loky
      n_jobs: -1
```

All arguments specified in `joblib_arguments` are passed to `Joblib.Parallel`. `loky` is the default backend, depending on the application, `threading` can be an alternative (see [`Joblib.Parallel` documentation](https://joblib.readthedocs.io/en/latest/parallel.html) for details). `n_jobs` defaults to -1, which means that all available CPUs may be used.

An example application using the plugin is provided in `plugins/joblib_launcher/example`. It overwrites the launcher used by Hydra.

Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will launch five parallel executions.

Output of the example application:
```text
$ python example/my_app.py --multirun task=1,2,3,4,5
[2020-02-03 22:23:59,035][HYDRA] Sweep output dir : multirun/2020-02-03/22-23-59
[2020-02-03 22:23:59,037][HYDRA] Joblib.Parallel(backend=loky,n_jobs=-1) is launching 5 jobs
[2020-02-03 22:23:59,037][HYDRA] Sweep output dir : multirun/2020-02-03/22-23-59
[2020-02-03 22:23:59,681][__main__][INFO] - Process ID 95127 executing task 1 ...
[2020-02-03 22:23:59,687][__main__][INFO] - Process ID 95126 executing task 2 ...
[2020-02-03 22:23:59,691][__main__][INFO] - Process ID 95128 executing task 3 ...
[2020-02-03 22:23:59,699][__main__][INFO] - Process ID 95131 executing task 5 ...
[2020-02-03 22:23:59,703][__main__][INFO] - Process ID 95130 executing task 4 ...
```

This plugin is based on the idea and inital implementation of @emilemathieutmp in [#357](https://github.com/facebookresearch/hydra/issues/357).
