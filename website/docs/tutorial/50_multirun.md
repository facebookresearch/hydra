---
id: multi-run
title: Multi-run
sidebar_label: Multi-run
---

Sometimes you want to run a parameter sweep.
To run a parameter sweep, use the `--multirun` (`-m`) flag and pass a comma separated list for each 
 dimension you want to sweep.
 
Here is a sweep over both db configurations and the two tables `tbl_1` and `tbl_2` (4 runs total). 

```text
$ python my_app.py -m db=mysql,postgresql db.table=tbl_1,tbl_2
[2019-09-25 14:53:41,265] - Launching 4 jobs locally
[2019-09-25 14:53:41,265] - Sweep output dir : multirun/2019-09-25/14-53-41
[2019-09-25 14:53:41,265] -     #0 : db=mysql db.table=tbl_1
db:
  driver: mysql
  pass: secret
  table: tbl_1
  user: omry

[2019-09-25 14:53:41,313] -     #1 : db=mysql db.table=tbl_2
db:
  driver: mysql
  pass: secret
  table: tbl_2
  user: omry

[2019-09-25 14:53:41,364] -     #2 : db=postgresql db.table=tbl_1
db:
  driver: postgresql
  pass: drowssap
  table: tbl_1
  timeout: 10
  user: postgre_user

[2019-09-25 14:53:41,413] -     #3 : db=postgresql db.table=tbl_2
db:
  driver: postgresql
  pass: drowssap
  table: tbl_2
  timeout: 10
  user: postgre_user

```

The default launcher runs the jobs locally and serially.

There are plans to add additional Launchers, such as a Launcher that launches your application code on AWS.
