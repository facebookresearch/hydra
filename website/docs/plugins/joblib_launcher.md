---
id: joblib_launcher
title: Joblib Launcher plugin
sidebar_label: Joblib Launcher plugin
---
[![PyPI](https://img.shields.io/pypi/v/hydra-joblib-launcher)](https://pypi.org/project/hydra-joblib-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-joblib-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-joblib-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-joblib-launcher.svg)](https://pypistats.org/packages/hydra-joblib-launcher)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_joblib_launcher/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_joblib_launcher)

The Joblib Launcher plugin provides a launcher for parallel tasks based on [`Joblib.Parallel`](https://joblib.readthedocs.io/en/latest/parallel.html).

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
By default, process-based parallelism using all available CPU cores is used. By overriding the default configuration, it is e.g. possible limit the number of parallel executions.

The JobLibLauncherConf backing the config is defined [here](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_joblib_launcher/hydra_plugins/hydra_joblib_launcher/config.py):

You can discover the Joblib Launcher parameters with:
```yaml title="$ python your_app.py hydra/launcher=joblib --cfg hydra -p hydra.launcher"
# @package hydra.launcher
_target_: hydra_plugins.hydra_joblib_launcher.joblib_launcher.JoblibLauncher
n_jobs: 10
backend: null
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
