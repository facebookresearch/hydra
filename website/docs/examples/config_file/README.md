---
id: example
title: Config file
sidebar_label: Config file
---

Your app evolves, and you now want to use a configuration file to make things more manageable:

Configuration file (`config.yaml`):
```yaml
dataset:
  name: imagenet
  path: /datasets/imagenet
```

You can pass in a config file for your app by specifying a config_path parameter to the `@hydra.main()` decoration.
The location of the `config_path` is relative to your python file.

Python file (`experiment.yaml`):
```python
import hydra


@hydra.main(config_path='config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```

`config.yaml` gets loaded automatically when you run the app.
```yaml
$ python experiment.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

You can override values in the loaded config from the command line:
```yaml
$ python experiment.py dataset.path=/datasets/new_imagenet
dataset:
  name: imagenet
  path: /datasets/new_imagenet
```

Check the [runnable example](https://github.com/fairinternal/hydra/blob/master/demos/3_config_file).

