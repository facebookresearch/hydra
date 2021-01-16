---
id: multi-run
title: Multi-run
sidebar_label: Multi-run
---

Sometimes you want to run the same application with multiple different values for the same parameter.  
e.g. running a performance test on each of the databases.

To do that, use the `--multirun` (`-m`) flag and pass a comma separated list for each dimension you want to sweep.  

To run your program with the 3 different schemas in schema config group:
```
$ python my_app.py -m schema=warehouse,support,school
```

You can sweep over multiple parameters at the same time.  
The following sweeps over all combinations of the dbs and schemas.
```text
 $ python my_app.py schema=warehouse,support,school db=mysql,postgresql -m
[2019-10-01 14:44:16,254] - Launching 6 jobs locally
[2019-10-01 14:44:16,254] - Sweep output dir : multirun/2019-10-01/14-44-16
[2019-10-01 14:44:16,254] -     #0 : schema=warehouse db=mysql
[2019-10-01 14:44:16,321] -     #1 : schema=warehouse db=postgresql
[2019-10-01 14:44:16,390] -     #2 : schema=support db=mysql
[2019-10-01 14:44:16,458] -     #3 : schema=support db=postgresql
[2019-10-01 14:44:16,527] -     #4 : schema=school db=mysql
[2019-10-01 14:44:16,602] -     #5 : schema=school db=postgresql
```
The printed configurations have been omitted for brevity

:::info
Hydra supports other kinds of sweeps. For example a range sweep: **x=range(1,10)** or a glob: **support=glob(*)**. 
See the [Extended Override syntax](/advanced/override_grammar/extended.md) for details.
:::

### Sweeper
The default sweeping logic is built into Hydra. Additional sweepers are available as plugins.
For example, the [Ax Sweeper](/plugins/ax_sweeper.md) can automatically find the best parameter combination!

### Launcher
By default, Hydra runs your multi-run jobs locally and serially. 
Other launchers are available as plugins for launching in parallel and on different clusters. For example, the [JobLib Launcher](/plugins/joblib_launcher.md)
can execute the different parameter combinations in parallel on your local machine using multi-processing.

