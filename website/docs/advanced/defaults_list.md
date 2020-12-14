---
id: defaults_list
title: The Defaults List
---

## Introduction

:::important
Many of the features described in this page are new to Hydra 1.1 and are considered experimental.
Please report any issues.
:::

A Defaults List determines how to build a config object from other configs, and in what order. 
Each config can have a Defaults List as a top level element. The Defaults List itself is not a part of resulting config.

The most common items in the Default List are Config Group Defaults, which determines which config group option
to use from a particular config group.

```yaml
defaults:
 - db: mysql # use mysql as the choice for the db config group
```

Sometimes a config file should be loaded unconditionally. Such configs can be specified as a string in the 
Defaults List:
```yaml
defaults:
  - db/mysql  # use db/mysql.yaml unconditionally
```
Config files loaded this way are not a part of a config group and will always be loaded.
They cannot be overridden. In general it is recommended to use the first form (config group default) when possible.

## Defaults list resolution
When composing the [Output Config Object](/terminology.md#output-config-object), Hydra will first create the final Defaults List and will then compose the
config with it.

Creating the final defaults list is a complex process: Configs mentioned in the list may have
their own defaults list, sometimes defining the same config groups!

The behavior that process is implementing can be described by two simple rules:
1. The last appearance of a config group determines the final value for that group
2. First appearance of a config group determines the composition order for that group

The first rule allows you to always override a config group selection that was made earlier.
The second rules ensures that composition order is respected.

## Composition order and `_self_`
A config can contain both a Defaults List and config nodes.

The special element `_self_` can be added to determine the composition order of this config relative to the items
in the defaults list.

If `_self_` is not specified, it is implicitly inserted at the top of the defaults list.
This means that by default, elements in the defaults list are composed **after** the config declaring the Defaults List.

<div className="row">
<div className="col col--6">

```yaml title="Input without _self_"
defaults:
 - foo: bar

```
</div>

<div className="col  col--6">

```yaml title="Is equivalent to"
defaults:
 - _self_
 - foo: bar
```

</div>
</div>

An example with two config files:

<div className="row">
<div className="col col--6">

```yaml title="config.yaml"
defaults:
 - _self_
 - db: mysql
```

</div>

<div className="col  col--6">

```yaml title="db/mysql.yaml"
defaults:
 - mysql/engine: innodb
 - _self_
```
</div>
</div>


When composing `config.yaml`, the resulting defaults list will be:
```yaml
defaults:
 - config              # per defaults list in config.yaml, it comes first (_self_)
 - mysql/engine/innodb # first per defaults list in db/mysql  
 - db/mysql            # second per defaults list in db/mysql (_self_)
```

The last two items are added as a result of the expansion of `db/mysql.yaml`.

## Interpolation
The Defaults List supports a limited form of interpolation that differs from the normal interpolation in several aspects.
- The Defaults List is resolved before the config is computed, so it cannot refer to nodes from the computed config.
- The defaults list can interpolate with config groups directly

```yaml
defaults:
 - dataset: imagenet
 - model: alexnet
 - optional dataset_model: ${dataset}_{model} # will become imagenet_alexnet
```

See [Specializing Configs](/patterns/specializing_config.md) for a more detailed explanation of this example.

## Renaming packages
Packages of previously defined config groups can be overridden by later items in the Defaults List.
The syntax is similar to that described in [Basic Override syntax](/advanced/override_grammar/basic.md#modifying-the-defaults-list),
 
<div className="row">
<div className="col col--6">

```yaml title="Moving to package src"
defaults:
  - db: mysql
  - 'db@:src': _keep_
```

```yaml title="Renaming package from src to dst"
defaults:
  - db@src: mysql
  - 'db@src:dst': _keep_
```

```yaml title="Renaming package and changing choice"
defaults:
  - db: mysql
  - 'db@:src': postgresql
```

</div>

<div className="col  col--6">

```yaml title="Result"
defaults:
  - db@src: mysql

```

```yaml title="Result"
defaults:
  - db@dst: mysql

```

```yaml title="Result"
defaults:
  - db@dst: postgresql

```


</div>
</div>


## Deleting from the defaults list
Previously defined config groups can be deleted by later items in the Defaults List. 
The syntax is similar to that described in [Basic Override syntax](/advanced/override_grammar/basic.md#modifying-the-defaults-list),

```yaml
defaults:
 - db: mysql
 - ~db # will delete `db` from the list regardless of the choice
```

```yaml
defaults:
 - db: mysql
 - ~db: mysql # will delete db from the list if the selected value is mysql
```



## Config "Inheritance" via composition

TODO: should probably not be here

A common pattern is to "extend" a base config:
```yaml title="agent.yaml"
name: ???
age: ???
agency: mi6
```

```yaml title="bond.yaml"
defaults:
  - agent
  - _self_

name: Bond, James Bond
age: 7
```

In the above example, `bond.yaml` is overriding the name and age in `base.yaml`
The resulting config will thus be:
```yaml
name: Bond, James Bond
age: 7
agency: mi6
```

