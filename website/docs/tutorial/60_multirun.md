---
id: multi-run
title: Multi-run
sidebar_label: Multi-run
---

Sometimes you want to run a parameter sweep.
To run a parameter sweep, use the `--multirun` (`-m`) flag and pass a comma separated list for each 
 dimension you want to sweep.
 
Here is a sweep over the db types (mysql,postgresql) and the schemas (warehouse,support,school).
Output does not contain the configuration prints.

```text
 $ python tutorial/50_composition/my_app.py schema=warehouse,support,school db=mysql,postgresql -m
[2019-10-01 14:44:16,254] - Launching 6 jobs locally
[2019-10-01 14:44:16,254] - Sweep output dir : multirun/2019-10-01/14-44-16
[2019-10-01 14:44:16,254] -     #0 : schema=warehouse db=mysql
[2019-10-01 14:44:16,321] -     #1 : schema=warehouse db=postgresql
[2019-10-01 14:44:16,390] -     #2 : schema=support db=mysql
[2019-10-01 14:44:16,458] -     #3 : schema=support db=postgresql
[2019-10-01 14:44:16,527] -     #4 : schema=school db=mysql
[2019-10-01 14:44:16,602] -     #5 : schema=school db=postgresql
```

The default launcher runs the jobs locally and serially.

There are plans to add additional Launchers, such as a Launcher that launches your application code on AWS.
