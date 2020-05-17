---
id: package_header
title: The package header
---

## Overview
Each config file contains an optional header section at the top.
Currently the only supported directive in the header is `@package`.
A `package` is the `path` of a node in the config.
For example, the `package` of the node `{driver: mysql}` below is `db`.
```yaml
db:
  driver: mysql
``` 

By adding the `@package` directive to the header of your config, you can control the package for that config:
The following is equivalent to the previous example:
```yaml
# @package: db
driver: mysql
```

## Keywords
The `package` directive supports the following keywords:

`_global_` : The top level package (equivalent to the empty string). This is the default in Hydra 1.0 and older.

`_group_` : The config group of the file, for example, the `_group_` for the config file `foo/bar/zoo.yaml` is `foo.bar`.

`_name_` : The config name, for example - the `_name_` for the config file `foo/bar/zoo.yaml` is`zoo`

You can use both `_group_` and `_name_` as a part of the package specification, for example, for the config file `foo/bar/zoo.yaml`, 
the package `oompa._group_._name_` would equal `oompa.foo.bar.zoo`.
 
For primary config files mentioned in `@hydra.main`, the default package is `_global_`.
For config files in config groups, the recommended choice for the `@package` directive is `_group_`, and it will become the default in Hydra 1.1. 

## Overriding
You can override the `@package` directive via the command line or via the defaults list.
Source code for these examples is available [here](https://github.com/facebookresearch/hydra/tree/master/examples/advances/package_overrides).
### Examples structure
```
$ tree
├── conf
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   ├── simple.yaml
│   └── two_packages.yaml
├── simple.py
└── two_packages.py
```
Given the configs and application below
```yaml title="conf/simple.yaml"
defaults:
  - db: mysql
```

```yaml title="conf/db/mysql.yaml"
# @package: _group_
driver: mysql
user: omry
pass: secret
```

```python title="simple.py"
@hydra.main(config_path="conf", config_name="simple")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())
```

Running the app results in this output.
```yaml
$ python simple.py 
db:
  driver: mysql
  user: omry
  pass: secret
```

### Overriding via command line
You can override the package of `db/mysql.yaml` from the command line
```
$ python my_app.py db@source=mysql 
source:
  driver: mysql
  user: omry
  pass: secret
```

### Overriding via defaults list
You can also override package via the defaults list.
We are making it more interesting below by adding a second item to the defaults, with a different package 
```yaml title="two_packages.yaml"
defaults:
  - db@source: mysql
  - db@destination: mysql
```

```python title="two_packages.py"
@hydra.main(config_path="conf", config_name="two_packages")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())
```
Output:
```yaml
$ python two_packages.py 
source:
  driver: mysql
  user: omry
  pass: secret
destination:
  driver: mysql
  user: omry
  pass: secret
```

### Overriding via the command line, again
In the above example, db appears twice in the defaults with different package overrides.
If you wanted to override one of them to a different package, you need to specify exactly which one, and what is the new package.

You can do this with the syntax `GROUP_NAME@SOURCE_PACKAGE@DESTINATION_PACKAGE=OPTION`, for example,
to rename db@destination to db@backup, use:
```yaml
$ python two_packages.py db@destination:backup=mysql
source:
  driver: mysql
  user: omry
  pass: secret
backup:
  driver: mysql
  user: omry
  pass: secret
```

### The evolution of the `@package` header
The behavior of the `@package` is changing:
 - Before Hydra 1.0, the `@package` header was not supported, and the default behavior was equivalent to `@package _global_`. 
 - Hydra 1.0 introduces the `@package` header and make `_group_` the recommended choice, but does not change the default behavior.
If you omit the `@package` header you will receive a warning telling you to add a `@package` header, recommending `_group_`.
 - Hydra 1.1 will change the default to `_group_`.

The `@package` header is described in more detail in [this design doc](https://docs.google.com/document/d/10aU2axeJj_p_iv1Hp9VulYLL5qyvhErg89MKFGbkZO4/edit?usp=sharing).

### The config header format
The config header format is a generic dictionary style block at the top of your config files.
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
