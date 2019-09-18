---
id: config_file
title: Config file
sidebar_label: Config file
---

Your app evolves, and you now want to use a configuration file to make things more manageable:

### Configuration file
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
python experiment.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

You can override values in the loaded config from the command line:
```yaml
python experiment.py
dataset:
  name: imagenet
  path: /datasets/new_imagenet
```


### Strict mode
Enabling strict mode will change the behavior of the `cfg` object in the following way:
* Reading a key that is not there will result in a KeyError instead of returning None
* Writing key that is not there would result in a KeyError instead of inserting the key
This effects also command line overrides.

This is useful for catching mistakes in the code or in the command line earlier.

You can learn more about this OmegaConf functionality [here](https://omegaconf.readthedocs.io/en/latest/usage.html#configuration-flags)

This can be turned on via a `strict=True` in your hydra.main decorator:

```python
@hydra.main(config_path='config.yaml', strict=True)
def experiment(cfg):
    # this would result in an exception
    if cfg.bad_key:
        pass
    # this would also result in an exception
    cfg.bad_key = True
```

As well as trying to insert new variables into the config via the command line:
```text
$ python demos/3_config_file/strict_config.py dataset.oops=true
Traceback (most recent call last):
...
KeyError: 'Accessing unknown key in a struct : dataset.oops'
text

Check the [runnable examples](https://github.com/facebookresearch/hydra/blob/master/demos/3_config_file).