---
id: config_file
title: Configuration file
sidebar_label: Configuration file
---

It can get tedious to type all those command line arguments every time.
Fix it by creating a configuration file in YAML format.

``` text title="Directory layout"
$ tree
├── config.yaml
└── my_app.py
```

```yaml title="config.yaml"
# @package: _group_
db: 
  driver: mysql
  user: omry
  pass: secret
```

<div class="alert alert--info" role="alert">
The <b>@package</b> directive is new in Hydra 1.0.
This is an advanced topic and we will not cover it in this tutorial, You can learn more about 
it <a href="../../advanced/package_header">here</a>.<br/>
For now just put <b># @package: _group_</b> at the top of your config files.
</div><br/>

Specify the config name by passing a `config_name` parameter to the `@hydra.main()` decorator.
```python title="my_app.py" {1}
@hydra.main(config_name='config')
def my_app(cfg):
    print(cfg.pretty())
```
The config name is the name of your config file without the `.yaml` extension.
This config should be near your Python file. we will learn more about how Hydra find config files later.

`config.yaml` is loaded automatically when you run your application
```yaml
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can override values in the loaded config from the command line:
```yaml {1,4-5}
$ python my_app.py db.user=root db.pass=1234
db:
  driver: mysql
  user: root
  pass: 1234
```

### Strict mode
`Strict mode` is useful for catching mistakes earlier by preventing access to missing config fields.
It is enabled by default once you specify a configuration file, and can help with two classes of mistakes:

#### Accessing missing fields in the code
In the example below, there is a typo in `db.driver` in the code.
This will result in an error.

```python
@hydra.main(config_name='config')
def my_app(cfg : DictConfig) -> None:
    print(cfg.db.drover)  # typo: cfg.db.driver. Raises exception
```
With `Strict mode` disabled, `None` will be printed.

#### Command line override errors
In the example below, there is a typo in `db.driver` in the command line.  
This will result in an exception.
```text
$ python my_app.py db.drover=mariadb
Error merging overrides
Key 'drover' in not in struct
        full_key: db.drover
        reference_type=Optional[Dict[Any, Any]]
        object_type=dict
```
With `Strict mode` disabled, the `drover` field will be added to the `db` config node.

#### Disabling strict mode
It is not recommended to disable strict mode. You can do it by passing `strict=False` to `hydra.main()` 
```python
@hydra.main(config_name='config', strict=False)
def my_app(cfg : DictConfig) -> None:
    cfg.db.port = 3306 # Okay
```

You can also disable it selectively within specific context. See [open_dict](https://omegaconf.readthedocs.io/en/latest/usage.html#struct-flag) in the OmegaConf documentation.
Note that strict mode is referred to as `struct mode` in OmegaConf.

