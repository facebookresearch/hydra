---
id: overriding_packages
title: Overriding packages
---

[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/advanced/package_overrides)

The contents of a config file can be relocated, or replicated, within the config, via package overrides.

### Package specification

``` text title="Definition of a package"
PACKAGE      : _global_ | COMPONENT[.COMPONENT]*
COMPONENT    : _group_ | _name_ | \w+

_global_     : the top level package (equivalent to the empty string).
_group_      : the config group in dot notation: foo/bar/zoo.yaml -> foo.bar
_name_       : the config file name: foo/bar/zoo.yaml -> zoo
```

### Overriding the package in a file via a package directive

A `@package directive` specifies a common [package](/terminology.md#package) for all nodes in the config file.
It must be placed at the top of each `config group file`.

```text title="Package directive examples"
# @package foo.bar
# @package _global_
# @package _group_
# @package _group_._name_
# @package foo._group_._name_
```
#### Examples
##### A package directive with a literal
<div className="row">
<div className="col col--6">

```yaml title="mysql.yaml" {1-2}
# @package foo.bar

db:
  host: localhost
  port: 3306
```

</div>

<div className="col  col--6">

```yaml title="Interpretation" {1-2}
foo:
  bar:
    db:
      host: localhost
      port: 3306
``` 

</div>
</div>


##### A package directive with `_group_` and `_name_`

<div className="row">
<div className="col col--6">

```yaml title="db/mysql.yaml" {1-2}
# @package _group_._name_

host: localhost
port: 3306
```
</div><div className="col  col--6">

```yaml title="Interpretation" {1-2}
db:
  mysql:
    host: localhost
    port: 3306
``` 
</div></div>

### Overriding the package via the defaults list
The following example adds the `mysql` config in the packages `db.src` and `db.dst`.


<div className="row">
<div className="col col--6">

```yaml title="config.yaml"
defaults:
 - db@db.src: mysql
 - db@db.dst: mysql




```
</div><div className="col  col--6">

```yaml title="Interpretation"
db:
  src:
    host: localhost
    port: 3306
  dst:
    host: localhost
    port: 3306
```
</div></div>


### History and future of the package directive
The primary config, named in `@hydra.main()` should not have a package directive.

For config files in config groups the default depends on the version:
 - In **Hydra 0.11**, there was an implicit default of `_global_`
 - **Hydra 1.0** the default is `_global_`  
 A warning is issued for each **config group file** without a `@package` directive.
 - In **Hydra 1.1** the default for **config group files** will become `_group_`

By adding an explicit `@package` to your configs files, you guarantee that they  
will not break when you upgrade to Hydra 1.1.

