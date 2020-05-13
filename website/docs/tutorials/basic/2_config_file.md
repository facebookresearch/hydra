---
id: config_file
title: Configuration file
sidebar_label: Configuration file
---

It can get tedious to type all those command line arguments every time.
Fix it by creating a configuration file in YAML format.

Configuration file: `config.yaml`
```yaml
# @package: _group_
db: 
  driver: mysql
  user: omry
  pass: secret
```
(The @package directive is explain later in this page).

Specify the config file by passing a `config_path` parameter to the `@hydra.main()` decorator.
The location of the `config_path` is relative to your Python file.

Python file: `my_app.py`
```python
@hydra.main(config_path='config.yaml')
def my_app(cfg):
    print(cfg.pretty())
```

`config.yaml` is loaded automatically when you run your application
```yaml
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can override values in the loaded config from the command line:
```yaml
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
This will result in an exception.

```python
@hydra.main(config_path='config.yaml')
def my_app(cfg : DictConfig) -> None:
    print(cfg.db.drover)  # typo: cfg.db.driver. Raises exception
```
With `Strict mode` disabled, `None` will be printed.

#### Command line override errors
In the example below, there is a typo in `db.driver` in the command line.  
This will result in an exception.
```text
$ python my_app.py db.drover=mariadb
Traceback (most recent call last):
...
AttributeError: Accessing unknown key in a struct : db.drover
```
With `Strict mode` disabled, the `drover` field will be added to the `db` config node.

#### Disabling strict mode
It is not recommended to disable strict mode. You can do it by passing `strict=False` to `hydra.main()` 
```python
@hydra.main(config_path='config.yaml', strict=False)
def my_app(cfg : DictConfig) -> None:
    cfg.db.port = 3306 # Okay
```

You can also disable it selectively within specific context. See [open_dict](https://omegaconf.readthedocs.io/en/latest/usage.html#struct-flag) in the OmegaConf documentation.
Note that strict mode is referred to as `struct mode` in OmegaConf.


### Package Header
TLDR:
Add `# @package _group_` to the top of your config files.
You are encouraged to read the rest, but if you have to take one thing from this section, it should be it.

Hydra 1.0 introduces a @package header described in details in [this design doc](https://docs.google.com/document/d/10aU2axeJj_p_iv1Hp9VulYLL5qyvhErg89MKFGbkZO4/edit?usp=sharing).

The header contains the @package directive, defined as:

`@package`: `_global_` | `package-path`
- `_global_`: Global package, this is the default behavior in Hydra `0.11`
- `package-path`: Explicit package path, such as `oompa.loompa`, the following keywords are replaced at runtime:
- `_group_`: config group in dot notation: `foo/bar/zoo.yaml` -> `foo.bar`
- `_name_`: config name: `foo/bar/zoo.yaml` -> `zoo`

### Header format
The header format is generic:
```yaml
# @oompa a.b.c
# @loompa: yup
x: 10
```
The resulting header is 
```python
{"oompa": "a.b.c", "loompa": "yup"}
```
Both colon and whitespace are accepted as a separator between the key and the value.
Unrecognized header keys (like `oompa` and `loompa`) are ignored.
