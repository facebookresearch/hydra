---
id: package_directive
title: The @package directive
---
A `@package directive` specifies a common package for all nodes in the config file.
It must be placed at the top of each `config group file`.

A `package` is the parent path of a config node (e.g hydra.launcher).

### Package directive specification

``` text title="Definition"
# @package PACKAGE_SPEC
PACKAGE_SPEC : _global_ | COMPONENT[.COMPONENT]*
COMPONENT    : _group_ | _name_ | [a-zA-Z0-9-_]+

_global_     : the top level package (equivalent to the empty string).
_group_      : the config group in dot notation: foo/bar/zoo.yaml -> foo.bar
_name_       : the config file name: foo/bar/zoo.yaml -> zoo
```

```python title="Examples"
# @package foo.bar
# @package _global_
# @package _group_
# @package _group_._name_
# @package foo._group_._name_
```

## Goals
 - Formalize the convention that the package of the config file matches the config group name  
   (e.g. The package of `hydra/launcher/basic.yaml` is `hydra.launcher`).
 - A config file can be merged into multiple packages in the final config object via package overrides.  

## Interpreting the @package directive
### A config with a literal package
```yaml
# @package container
db:
  host: localhost
webserver:
  domain: example.com
```
Is equivalent to:
```yaml
container:
    db:
      host: localhost
    webserver:
      domain: example.com
``` 

### A config using `_group_` and `_name_`
```yaml title="env/prod.yaml" {1}
# @package _group_._name_
db:
  host: 10.0.0.11
webserver:
  domain: example.com
```
Is equivalent to:
```yaml
env:
  prod:
    db:
      host: 10.0.0.11
    webserver:
      domain: example.com
```


## Default packages
The primary config, named in `@hydra.main()` should not have a package directive.

For config files in config groups the default depends on the version:
 - In Hydra 0.11, there was an implicit default of `_global_`
 - Hydra 1.0 the default is `_global_`  
 A warning is issued for each **config group file** without a `@package` directive.
 - In Hydra 1.1 the default for **config group files** will become `_group_`

By adding an explicit `@package` to your configs files, you guarantee that they  
will not break when you upgrade to Hydra 1.1.

