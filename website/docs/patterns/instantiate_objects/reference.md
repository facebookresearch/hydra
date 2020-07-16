---
id: instantiate_objects_reference
title: Reference for instantiating objects
sidebar_label: Reference for instantiating objects
---

Hydra provides `hydra.utils.instantiate()` (and its alias `hydra.utils.call()`) for instantiating objects and calling functions. Prefer `instantiate` for creating objects and `call` for invoking functions.

```python
def instantiate(config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An ObjectConf or DictConfig describing what to instantiate and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class
    """
```

For using these functions, the config must have a key called `target`. If a key called `params` is also present, its value is passed as keyword arguments to class/function specified by `target`.

### Example config
```yaml
# target function name or class method fully qualified name
target: foo.Bar
# optional parameters dictionary to pass when calling the target
params:
  x: 10
```

### Example ObjectConf definition
ObjectConf is defined in `hydra.types.ObjectConf`:
```python
@dataclass
class ObjectConf(Dict[str, Any]):
    # class, class method or function name
    target: str = MISSING
    # parameters to pass to target when calling it
    params: Any = field(default_factory=dict)
```


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
  def class_method(self, x: int) -> Any:
    return self(x, 10)
    
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
  target: example.Foo
  params:
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
  target: builtins.str
  params:
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