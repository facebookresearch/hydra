---
id: instantiate
title: Instantiate objects and calling functions
sidebar_label: Instantiate objects and calling functions
---

Hydra provides `hydra.utils.call()` (and its alias `hydra.utils.instantiate()`) for instantiating objects and calling functions While `instantiate` is an alias for `call`, you may prefer to use `call` for invoking functions and class methods, and `instantiate` for creating objects.	

```python
def call(config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An ObjectConf or DictConfig describing what to call and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified method
    """
```

```python
def instantiate(config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An ObjectConf or DictConfig describing what to instantiate and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class
    """
```

For using these functions, the config must have a key called `target`. Older versions of Hydra also supported the `cls` and `class` key but they are deprecated now (hence not recommended) and will be removed in Hydra 1.1 . If both `target` and `cls` (or `class`) keys are present, `target` key will be used.

If a key called `params` is also present, its value is passed as keyword arguments to class/function specificed by `target`. 

### ObjectConf definition for hydra.utils.instantiate
ObjectConf is defined in `hydra.types.ObjectConf`:
```python
@dataclass
class ObjectConf(Dict[str, Any]):
    # class, class method or function name
    target: str = MISSING
    # parameters to pass to target when calling it
    params: Any = field(default_factory=dict)
```

### Example config node for hydra.utils.call
```yaml
# target function name or class method fully qualified name
target: foo.Bar
# optional parameters dictionary to pass when calling the target
params:
  x: 10
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

Now to test these, `call` (or `instantiate`) them as follows:

```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo1: Foo = hydra.utils.call(cfg.myobject)  # Foo(10, 20)
  foo2: Foo = hydra.utils.call(cfg.myclassmethod)  # Foo(5, 10)
  ret1: int = hydra.utils.call(cfg.mystaticmethod)  # 16
  ret2: int = hydra.utils.call(cfg.myfunction)  # 17
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
  foo: str = hydra.utils.call(cfg)  # "42"

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
  foo = hydra.utils.call(cfg)  # None