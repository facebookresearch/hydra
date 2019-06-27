## Config file
You can pass in a single config file for your job.
This file is relative to your python file (config_file.py) here.

```python
@hydra.main(config_path='config.yaml')
def experiment(cfg):
    print("Configuration:\n{}".format(cfg.pretty()))
```

config.yaml:
```yaml
app:
  name: the nameless one
```

```text
$ python demos/3_config_file/config_file.py
Configuration:
app:
  name: the nameless one
```

As before, You can pass in arbitrary configuration from the command line, which will override the values from the config file.
```text
$ python demos/3_config_file/config_file.py app.name=morte
Configuration:
app:
  name: morte
```

[Prev](../2_logging/README.md) [Up](../README.md) [Next](../4_compose/README.md)
