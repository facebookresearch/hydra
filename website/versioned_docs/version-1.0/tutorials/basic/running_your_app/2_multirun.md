---
id: multi-run
title: Multi-run
sidebar_label: Multi-run
---

Sometimes you want to run a parameter sweep.
A parameter sweep is a method of evaluating a function (or a program) with a pre-determined set of parameters.
The examples below will clarify what this means.

To run a parameter sweep, use the `--multirun` (`-m`) flag and pass a comma separated list for each
dimension you want to sweep.  

To run your program with the 3 different schemas in schema config group:
```
$ python my_app.py -m schema=warehouse,support,school
```

Here is sweep over the db types (mysql,postgresql) and the schemas (warehouse,support,school).
Output does not contain the configuration prints.

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

:::info
Hydra supports other kind of sweeps, for example a range sweep: **x=range(1,10)** or a glob: **support=glob(*)**.  
See the [Extended Override syntax](/advanced/override_grammar/extended.md) for details.
:::

### Sweeper
The sweeping logic is implemented by a simple sweeper that is built into Hydra.
Additional sweepers are available as plugins.
For example, the [Ax Sweeper](/plugins/ax_sweeper.md) can automatically find the best parameter combination!

### Launcher
A Launcher is what runs your job, Hydra comes with a simple launcher that runs the jobs locally and serially.
However, other launchers are available as plugins. For example - The [JobLib Launcher](/plugins/joblib_launcher.md)
can execute the different parameter combinations in parallel on your local machine using multi-processing.

There are plans to add additional Launchers, such as a Launcher that launches your application code on AWS.
