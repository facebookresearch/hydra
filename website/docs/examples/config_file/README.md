---
id: example
title: Config file
sidebar_label: Config file
---

You can pass in a config file for your job.
This file location is relative to your Python file location.

### config_file.py
```python
import hydra


@hydra.main(config_path='config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```

### config.yaml
```yaml
dataset:
  name: imagenet
  path: /datasets/imagenet
```

### Output
The config gets loaded automatically:
```yaml
$ python experiment.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

You can override the loaded config from the command line:
```yaml
$ python experiment.py dataset.path=/datasets/new_imagenet
dataset:
  name: imagenet
  path: /datasets/new_imagenet
```