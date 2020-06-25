# Hydra example Launcher plugin

This plugin provides an example for how to write a custom Launcher for Hydra.
The configuration for this launcher is in packages with the plugin:

`hydra_plugins/example_launcher_plugiun/conf/hydra/launcher/example.yaml`:
```yaml
hydra:
  launcher:
    cls: hydra_plugins.example_launcher_plugin.ExampleLauncher
    params:
      foo: 10
      bar: abcde
```
The example application is overriding the Launcher used by Hydra.
When the launcher is initialized, its "using" the foo and bar parameters.

Output of the example application:
```text
$ python example/my_app.py --multirun db=postgresql,mysql
[2019-10-22 19:45:05,060] - Example Launcher(foo=10, bar=abcde) is launching 2 jobs locally
[2019-10-22 19:45:05,060] - Sweep output dir : multirun/2019-10-22/19-45-05
[2019-10-22 19:45:05,060] -     #0 : db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user

[2019-10-22 19:45:05,135] -     #1 : db=mysql
db:
  driver: mysql
  pass: secret
  user: omry
```
