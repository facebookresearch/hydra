---
id: terminology
title: Terminology
---
## Overview
This page describes some common concepts in Hydra, most of which are covered in greater details throughout the documentation.

## Input Configs
Input configs are used to construct the config object used by the application.  
Supported input configs are:
- Config Files ([YAML](https://yaml.org/) files)
- [Structured Configs](#structured-config)
  
## Overrides
[Overrides](override_grammar/basic) is list of strings that can be used to manipulate the config composition process.

Overrides can be used in the command line. In the examples below, `key=value` is an override:
```shell
$ python my_app.py key=value
```
And in the [**Compose API**](compose_api.md):
```python
cfg = compose(config_name, overrides=["key=value"])
```


### Primary Config
The input config named in [**@hydra.main()**](../tutorials/basic/your_first_app/2_config_file.md) or in 
the [**Compose API**](compose_api.md).  

### Structured Config

A Config object initialized with a class decorated with [@dataclass](https://docs.python.org/3/library/dataclasses.html) or [@attr.s](https://www.attrs.org/en/stable/), or an instance of such a class.   
Structured Configs provides additional type information that enables static and runtime type checking.

There are two primary patterns for using Structured Configs:
- As an [Input Config](#input-configs).
- As a schema validating Config Files and command line arguments.

```python title="Example Schema"
@dataclass
class User:
  name: str
  age: int
```

## Defaults List
A list in an [Input Config](#input-configs) that instructs Hydra how compose the config. 
```yaml title="Defaults List in a YAML config"
defaults:
  - db: mysql      # An overridable defaults list entry
  - schema/school  # A non-overridable defaults list entry
```

### Config Group
A Config Group is directory in the [Config Search Path](#config-search-path) that contains [Input Configs](#input-configs).
Config Groups can be nested, and in that case the path elements are separated by a forward slash ('/') regardless of the operating system.


### Config Group Option
An Input Config in a Config Group. When used in a Defaults List, a Config Group Option can be a single Input Config, or a list of Input Configs from the same Config Group. 

## Config Node
A Config Node is either a **Value Node** (a primitive type), or a **Container Node**.  A **Container Node** is a list or dictionary of **Value Nodes**.

## Package
A Package is the path to [Config Node](#config-node) in the [Config Object](#output-config-object).
By default, the Package of a Config Group Option is derived from the Config Group.
*e.g:* Config Group Options in **mi6/agent** will have the package **mi6.agent** by default.


## Package Directive
The [Package Directive](overriding_packages.md#overriding-the-package-via-the-package-directive) specifies the root [Package](#package) of a [Config File](#input-configs). It can appear at the top of YAML config file.

## Output Config
A config composed from the [Input Configs](#input-configs) and [Overrides](#overrides) by **@hydra.main()**, or the Compose API.

## Example of core concepts

<div className="row">
<div className="col col--4">

```yaml title="config.yaml"
defaults:
 - mi6/agent: james_bond

```

</div>

<div className="col col--4">

```yaml title="mi6/agent/james_bond.yaml" {1}
# @package bond.james
codename: '007'

```

</div>
<div className="col col--4">

```yaml title="Output config" {1,2}
bond:
  james:
    codename: '007'
```
</div>
</div>

- [Input Configs](#input-configs): **config.yaml**, **mi6/agent/james_bond.yaml**
- [Config Group](#config-group): mi6/agent
- [Config Group Option](#config-group-option): james_bond
- [Container Node](#config-node): **{agent: {codename: '007'}}**
    - [Value Node](#config-node): **'007'**
    - [Packages](#package): **<empty\>**, **mi6**, **mi6.agent**, **mi6.agent.codename**
- [Package directive](#package-directive) : **# @package bond.james**, overriding the default Package for the containing Input Config 

 
## Config Search Path
The [Config Search Path](search_path.md) is a list of paths that are searched in order to find configs. It is similar to
the Python [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH).

## Plugins
[Plugins](plugins.md) extend Hydra's capabilities. Hydra has several plugin types, for examples Launcher and Sweeper.