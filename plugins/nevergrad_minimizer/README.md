# Hydra example Launcher plugin

```yaml
hydra:
  sweeper:
    class: hydra_plugins.nevergrad_minimizer.NevergradMinimizer
    params:
      foo: 10
      bar: abcde
```

#### Example app using custom sweeper:
```text
$ python example/my_app.py -m db=mnist,cifar batch_size=4,8,16 lr='Log(a_min=0.001,a_max=0.1)' dropout=0.001:1.0