---
id: multi-run
title: Multi-run
sidebar_label: Multi-run
---

Hydra can run the same job multiple time with different arguments in each run using a mode called multi-run.
To turn on multi-run, use `-m` or `--multirun` and pass comma separated list for each value you want
to sweep over.

To run the application 4 times, with both mysql and postgresql and with with the databases of hydra and chimera:
```text
$ python my_app.py -m db=mysql,postgresql db.database=hydra,chimera
[2019-09-25 09:27:37,529] - Launching 4 jobs locally
[2019-09-25 09:27:37,529] - Sweep output dir : multirun/2019-09-25/09-27-37
[2019-09-25 09:27:37,529] -     #0 : db=mysql db.database=hydra
db:
  database: hydra
  driver: mysql
  pass: secret
  user: omry

[2019-09-25 09:27:37,575] -     #1 : db=mysql db.database=chimera
db:
  database: chimera
  driver: mysql
  pass: secret
  user: omry

[2019-09-25 09:27:37,627] -     #2 : db=postgresql db.database=hydra
db:
  database: hydra
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user

[2019-09-25 09:27:37,675] -     #3 : db=postgresql db.database=chimera
db:
  database: chimera
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user
```

The default launcher runs the jobs locally and serially.
Launcher plugins can change this. At the moment there are no public Launcher plugins but there will be some soon.
For example, a Launcher plugin for AWS would be able to launch your code to an AWS instance.
