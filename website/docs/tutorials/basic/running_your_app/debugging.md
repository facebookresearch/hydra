---
id: debugging
title: Debugging
sidebar_label: Debugging
---
Hydra provides a few options to improve debuggability.

### Printing the configuration
Print the config for your app without running your function by adding `--cfg` or `-c` to the command line.

The `--cfg` option takes one argument indicating which part of the config to print:
* `job` : Your config
* `hydra` : Hydra's config
* `all` : The full config, which is a union of `job` and `hydra`.

```yaml
# A normal run:
$ python my_app.py
MySQL connecting to localhost with user=root and password=1234

# just show the config without running your function:
$ python my_app.py --cfg job
db:
  host: localhost
  user: root
  password: 1234
```
The printed config includes any modifications done via the command line:
```yaml {3}
$ python my_app.py db.host=10.0.0.1 --cfg job
db:
  host: 10.0.0.1
  user: root
  password: 1234
```

### Hydra verbose debugging
Hydra prints some very useful information in `DEBUG` log level.
This includes:
* Installed plugins : What Hydra plugins are installed in the environment
* Config search path : The configuration search path
* Composition trace : Which config files were used to compose your configuration, and in what order.

This is often used with `-c job` to just see the config without running the application.
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
