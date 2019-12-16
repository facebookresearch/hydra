---
id: debugging
title: Debugging
sidebar_label: Debugging
---
Hydra provides a few options to improve debuggability.

### Printing the configuration
Print the config that would be used for a job without actually running it by adding '-c job' or '--cfg job' to your command line:
```yaml
# A normal run:
$ python tutorial/objects_example/my_app.py
MySQL connecting to localhost with user=root and password=1234

# just show the config without running your function:
$ python tutorial/objects_example/my_app.py -c job
[2019-09-29 11:09:14,134] -
db:
  class: tutorial.objects_example.my_app.MySQLConnection
  params:
    host: localhost
    password: 1234
    user: root
```
The printed config would be the actual config the job received with the rest of the command line arguments:
```yaml
$ python tutorial/objects_example/my_app.py db=postgresql db.params.database=tutorial2 --cfg job
[2019-09-29 11:14:55,977] -
db:
  class: tutorial.objects_example.my_app.PostgreSQLConnection
  params:
    database: tutorial2
    host: localhost
    password: 1234
    user: root
```

The `--cfg` option takes one argument indicating which part of the config to print:
* `job` : Your config 
* `hydra` : Hydra's config
* `all` : The full config, which is a union of `job` and `hydra`.

### Hydra verbose debugging
Hydra prints some very useful information in `DEBUG` log level.
This includes:
* Installed plugins : What Hydra plugins are installed in the environment 
* Config search path : The configuration search path
* Composition trace : Which config files were used to compose your configuration, at what order and where did they came from.

This is often used with `-c` to just see the config without running the application.
Example output:
```text
$ python my_app.py hydra.verbose=hydra --cfg job
[2019-09-29 13:35:46,780] - Installed Hydra Plugins
[2019-09-29 13:35:46,780] - ***********************
[2019-09-29 13:35:46,780] -     SearchPathPlugin:
[2019-09-29 13:35:46,780] -     -----------------
[2019-09-29 13:35:46,781] -     Sweeper:
[2019-09-29 13:35:46,781] -     --------
[2019-09-29 13:35:46,782] -             BasicSweeper
[2019-09-29 13:35:46,782] -     Launcher:
[2019-09-29 13:35:46,782] -     ---------
[2019-09-29 13:35:46,783] -             BasicLauncher
[2019-09-29 13:35:46,783] -
[2019-09-29 13:35:46,783] - Hydra config search path
[2019-09-29 13:35:46,783] - ************************
[2019-09-29 13:35:46,783] - | Provider | Search path                           |
[2019-09-29 13:35:46,783] - ----------------------------------------------------
[2019-09-29 13:35:46,783] - | hydra  | pkg://hydra.conf                        |
[2019-09-29 13:35:46,783] - | main   | /Users/omry/dev/hydra/tutorial/logging  |
[2019-09-29 13:35:46,783] -
[2019-09-29 13:35:46,783] - Composition trace
[2019-09-29 13:35:46,783] - *****************
[2019-09-29 13:35:46,783] - | Provider | Search path     | File      |
...
```
