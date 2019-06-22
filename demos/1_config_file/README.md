## Config file
This example introduces a config file that is loaded automatically for your function.

```python
@hydra.main(config_path='config.yaml')
def experiment(cfg):
    ...
```

```text
$ python demos/1_minimal/minimal.py run
[2019-06-21 18:15:37,073][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_18-15-37
[2019-06-21 18:15:37,074][__main__][INFO] - Configuration:
best_app:
  dataset: bar
  model: foo
  name: minimal
```

As before, you can override the config from the command line:
```text
$ python demos/1_minimal/minimal.py run best_app.dataset=pub
[2019-06-21 18:16:24,535][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_18-16-24
[2019-06-21 18:16:24,536][__main__][INFO] - Configuration:
best_app:
  dataset: pub
  model: foo
  name: minimal
```