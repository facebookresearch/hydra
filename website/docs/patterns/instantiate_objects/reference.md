---
id: instantiate_objects_reference
title: Reference
sidebar_label: Reference
---

Hydra provides `hydra.utils.call()` (and its alias `hydra.utils.instantiate()`) for instantiating objects and calling functions. Prefer `instantiate` for creating objects and `call` for invoking functions.

```python
def call(
    config: Union[ObjectConf, TargetConf, DictConfig, Dict[Any, Any]],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    :param config: An object describing what to call and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class or method
    """
    ...

# Alias for call
instantiate = call
```

For using these functions, the config must have a key called `_target_`. Any additional parameters are passed as keyword arguments to class/function specified by `_target_`.

### Example config
```yaml
# target function name or class method fully qualified name
_target_: foo.Bar
# additional parameters to pass when calling the target
x: 10
```

### Example ObjectConf definition
`TargetConf` is defined in `hydra.types.TargetConf`:

<div className="row">

<div className="col col--6">

```python title="Definition"
@dataclass
class TargetConf:
    # class or function name
    _target_: str = MISSING

```

</div><div className="col col--6">

```python title="Use it by subclassing and adding fields" 
@dataclass
class UserConf(TargetConf):
    _target_ : str = "module.User"
    name: str = MISSING
    age: int = MISSING
```

</div>
</div>

#### Example usage

example.py
```python
class Foo:

  # target: example.Foo
  def __init__(self, x: int, y: int, z:int = 30) -> None:
    self.x = x
    self.y = y
    self.z = z

  # target: example.Foo.class_method
  @classmethod
  def class_method(cls, x: int) -> Any:
    return cls(x, 10)
    
  # target: example.Foo.static_method
  @staticmethod
  def static_method(z: int) -> int:
    return z + 1

# target: example.bar
def bar(z: int) -> int:
  return z + 2

```

To instantiate a `example.Foo` object:

config.yaml
```yaml
foo:
  _target_: example.Foo
  x: 10
  y: 20
```

Now, to test these, `instantiate` (or `call`) them as follows:

```python
from hydra.utils import instantiate
# foo is as described in the config
foo: Foo = instantiate(cfg.foo) # Foo(x = 10, y = 20, z = 30)
# you can also override the config values on the callsite:
foo2: Foo = instantiate(cfg.foo, x=100) # Foo(x = 100, y = 20, z = 30)
# and even pass additional fields that are not in the config. 
foo3: Foo = instantiate(cfg.foo, z=100) # Foo(x = 10, y = 20, z = 100)
```

We can also call functions from the standard library:

```yaml
myobject:
  _target_: builtins.str
  object: 42
```  

```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo: str = hydra.utils.instantiate(cfg)  # "42"

```

We can create the `None` object by setting the config to `None`:

```yaml
myobject: null
```

```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo = hydra.utils.instantiate(cfg.myobject)  # None