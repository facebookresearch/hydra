---
id: terminology
title: Terminology
---
This page describes some of the common concepts in Hydra.
It does not contain a comprehensive description of each item, nor is it a usage guide.  
Most concepts here are described in much more details throughout the documentation.

## Config
A config is an entity containing user configuration, composed of Config Nodes.
Configs are always converted to OmegaConf DictConfig or ListConfig objects.

## Primary Config
The config named in `@hydra.main()` or in `hydra.experimental.compose()`.

### Config Node
Alternative names: Node

A node in the config, can be a parent container or a leaf value.
 - Containers can be DictConfig and ListConfig (representing a dictionary and a list)
 - Leaf values can represent supported primitive types, such as `int`, `float`, `bool`, `enum` and `str`.
 
A DictConfig node can have an underlying Structured Config type that is used for runtime mutation validation.

### Config File
A YAML file

### Structured Config
A dataclass or an instance of a dataclass that is used to construct a config.  
The constructed config object is using the underlying type for runtime type validation.  
Duck typing (The usage of the underlying type for type annotation) enables static type checking of the config.

## Config Search Path:
Alternative names: Search Path
   
The Config Search Path is a list of virtual paths that is searched in order to find configs.  
Conceptually, this is similar to the Python PYTHONPATH or the Java CLASSPATH.  
When a config searched in the config search path, the first matching config is used.
Each config search path element has a schema prefix such as file:// or pkg:// that is corresponding to a ConfigSourcePlugin.

## Config Group
Alternative names: Group

A config group is a logical directory in the Config Search Path. The Config Group options are the union of all the configs in that
directory across the Config Search Path.
Config Groups can be hierarchical and in that case the path elements are separated by a forward slash ('/') 
regardless of the operating system.

## Config Group Option
Alternative names: Option

One of the configs in a Config Group.

## Defaults List
Alternative names: Defaults

A special list in the Primary Config. The Defaults List contains composition instructions Hydra is using when creating the 
final config object.
The defaults list is removed from the final config object. 

## Package
A package is the parent lineage of a node. You also think of it as the path of the node in the config object.
The package of a Config can be overridden via the command line or via the defaults list.

# Examples

```yaml title="foo/oompa/loompa.yaml"
a:
  b:
    c: 10
```

- Config Group: foo/oompa
- Config Group Option: loompa
- Package: a.b
- Node: examples nodes: `c:10`, `b: {c: 10}` and `a: {b: {c: 10}}`
- Structured Config:
```python
@dataclass
class User:
  name: str = MISSING
  age: int = MISSING

# The real type of cfg is DictConfig but we can ducktype it 
# as User to get static type safety
cfg: User = OmegaConf.structured(User)
```
 - Defaults List:
```yaml title="config.yaml"
defaults:
  - db: mysql
```
 