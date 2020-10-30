---
id: terminology
title: Terminology
---
## Overview
This page describes some of the common concepts in Hydra. 
Most of the concepts are described in much more details throughout the documentation.

## Input Configs
Input configs are used to construct the config object used by the application.  
Supported input configs are:
- Config Files ([YAML](https://yaml.org/) files)
- Command line arguments
- [Structured Configs](#structured-config) (Python [@dataclasses](https://docs.python.org/3/library/dataclasses.html))

### Primary Config
The input config named in [`@hydra.main()`](tutorials/basic/your_first_app/1_simple_cli.md) or in 
the [`Compose API`](experimental/hydra_compose.md).  


### Structured Config
A @dataclass or an instance of a @dataclass that is used to construct a config. These enable both runtime and static type checking.

There are two primary patterns for using Structured configs:
- As an [Input Config](#input-configs).
- As a schema validating Config Files and command line arguments.

```python title="Example:"
@dataclass
class User:
  name: str = MISSING
  age: int = MISSING
```


### Defaults List
A list in [input Config](#input-configs) that instructs Hydra how to build the config. 
The list is typically composed of [Config Group Options](#config-group-option).
```yaml title="Example: config.yaml"
defaults:
  - db: mysql
  - schema: school
```

### Config Group

A Config Group is a mutually exclusive set of [Config Group Options](#config-group-option). 
Config Groups can be hierarchical and in that case the path elements are separated by a forward slash ('/') 
regardless of the operating system.

### Config Group Option
One of the configs in a Config Group.

### Config Node
A Config Node is either a `Value Node` (a primitive type), or a `Container Node`.  A `Container Node` is a list or dictionary of `Value Nodes`.

### Package
A Package is the path of the [Config Node](#config-node) in the [Config Object](#output-config-object). 

### Package directive
The [Package Directive](advanced/overriding_packages.md) specifies the root [Package](#package) of an [Config File](#input-configs)

### Example
```yaml title="Input config: mi6/agent/james_bond.yaml"
# @package _group_
codename: '007'
```
```yaml title="Resulting config"
mi6:
    agent:
        codename: '007'
```
- [Config Group](#config-group): mi6/agent
- [Config Group Option](#config-group-option): james_bond  
- [Container Nodes](#config-node): `{codename: '007'}`, &nbsp;. . . &nbsp;,`{mi6: {agent: {codename: '007'}}}`
- [Value Node](#config-node): '007'
- [Packages](#package) `<empty>`, `mi6`, `mi6.agent`, `mi6.agent.codename`
- [Package directive](#package-directive) : `@package _group_`, which expands to `mi6.agent`

## Output Config Object
The config for the application. It is a dictionary of [Config Nodes](#config-node) generated from the [Input Configs](#input-configs).
 
## Misc
### Config Search Path
The [Config Search Path](advanced/search_path.md) is a list of paths that are searched in order to find configs. It is similar to
the Python [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH).

### Plugins
[Plugins](advanced/plugins.md) extend Hydra's capabilities. Some examples are Launcher and Sweeper.