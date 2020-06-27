# Hydra example Launcher plugin

This plugin provides an example for how to write a custom Sweeper for Hydra.
The provided example has a custom configuration for the sweeper that takes two parameters, foo and bar:
```yaml
hydra:
  sweeper:
    target: hydra_plugins.example_sweeper.ExampleSweeper
    params:
      foo: 10
      bar: abcde
```

#### Example app using custom sweeper:
```text
$ python example/my_app.py -m db=mysql,postgresql
[2019-11-14 11:42:47,941][HYDRA] ExampleSweeper (foo=10, bar=abcde) sweeping
[2019-11-14 11:42:47,941][HYDRA] Sweep output dir : multirun/2019-11-14/11-42-47
[2019-11-14 11:42:47,942][HYDRA] Launching 2 jobs locally
[2019-11-14 11:42:47,942][HYDRA]        #0 : db=mysql
db:
  driver: mysql
  pass: secret
  user: omry

[2019-11-14 11:42:48,011][HYDRA]        #1 : db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user
```