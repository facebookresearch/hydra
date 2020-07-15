---
id: instantiate
title: Instantiate objects and calling functions
sidebar_label: Instantiate objects and calling functions
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

For using these functions, the config must have a key called `target`. If a key called `params` is also present, its value is passed as keyword arguments to class/function specificed by `target`.

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

models.py
```python
class Foo:
  def __init__(self, x: int, y: int) -> None:
    self.x = x
    self.y = y

  @classmethod
  def class_method(self, z: int) -> Any:
    return self(z, 10)

  @staticmethod
  def static_method(z: int) -> int:
    return z + 1

def bar(z: int) -> int:
  return z + 2
```
config.yaml
```yaml
myobject:
  target: models.Foo
  params:
    x: 10
    y: 20
    
myclassmethod:
  target: models.Foo.class_method
  params:
    z: 5

mystaticmethod:
  target: models.Foo.static_method
  params:
    z: 15

myfunction:
  target: models.bar
  params:
    z: 15
```

Now to test these, `instantiate` (or `call`) them as follows:

```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo1: Foo = hydra.utils.instantiate(cfg.myobject)  # Foo(10, 20)
  foo2: Foo = hydra.utils.instantiate(cfg.myclassmethod)  # Foo(5, 10)
  ret1: int = hydra.utils.instantiate(cfg.mystaticmethod)  # 16
  ret2: int = hydra.utils.instantiate(cfg.myfunction)  # 17
```

These methods also support functions built into the standard library:

```yaml
# fully qualified name of the in-built function
target: builtins.str
# optional parameters dictionary to pass when calling the target
params:
  object: 42

```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo: str = hydra.utils.instantiate(cfg)  # "42"

```

Another useful scenario is when we want to create the `None` object. In that case, set `target = None`:

```yaml
target: None
# parameters are ignored when target is set to None
params:
  object: 42

```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo = hydra.utils.instantiate(cfg)  # None