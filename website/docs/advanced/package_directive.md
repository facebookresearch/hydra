---
id: package_directive
title: The @package directive
---

### Goals
 - Formalize the convention that the package of the config file matches the config group name  
   (e.g. The package of `hydra/launcher/basic.yaml` is `hydra.launcher`).
 - A config file can be merged into multiple packages in the final config object via package overrides.  

### Overview
A `@package directive` specifies a common [package](/terminology.md#package) for all nodes in the config file.
It must be placed at the top of each `config group file`.

### Package directive specification

``` text title="Definition"
# @package PACKAGE_SPEC
PACKAGE_SPEC : _global_ | COMPONENT[.COMPONENT]*
COMPONENT    : _group_ | _name_ | \w+

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

### Interpreting the @package directive
#### A package directive with a literal
```yaml title="mysql.yaml"
# @package foo.bar
db:
  host: localhost
  port: 3306
```
Is equivalent to:
```yaml
foo:
  bar:
    db:
      host: localhost
      port: 3306
``` 

#### A package directive with `_group_` and `_name_`
```yaml title="db/mysql.yaml"
# @package _group_._name_
host: localhost
port: 3306
```
Is equivalent to:
```yaml
db:
  mysql:
    host: localhost
    port: 3306
```

### Overriding the package directive
You can override the package directive through the defaults list or the command line.

The following example adds the `mysql` config in under the packages `src` and `dst`.
```yaml title="config.yaml"
defaults:
 - db@db.src: mysql
 - db@db.dst: mysql
```

Is equivalent to:
```yaml
db:
  src:
    host: localhost
    port: 3306
  dst:
    host: localhost
    port: 3306
```

You can manipulate packages in the defaults list through the command line.  
For example, you can rename the `dst` package to `backup`:
```
$ python foo.py db@db.dst:db.backup=mysql
```
For more details, see the [Command line overrides](advanced/command_line_overrides.md) page.

### History and future of the package directive
The primary config, named in `@hydra.main()` should not have a package directive.

For config files in config groups the default depends on the version:
 - In **Hydra 0.11**, there was an implicit default of `_global_`
 - **Hydra 1.0** the default is `_global_`  
 A warning is issued for each **config group file** without a `@package` directive.
 - In **Hydra 1.1** the default for **config group files** will become `_group_`

By adding an explicit `@package` to your configs files, you guarantee that they  
will not break when you upgrade to Hydra 1.1.

