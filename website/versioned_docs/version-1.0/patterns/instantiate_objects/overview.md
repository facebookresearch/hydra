---
id: overview
title: Instantiating objects with Hydra
sidebar_label: Overview
---

One of the best ways to drive different behavior in an application is to instantiate different implementations of an interface.
The code using the instantiated object only knows the interface which remains constant, but the behavior
is determined by the actual object instance.

Hydra provides `hydra.utils.call()` (and its alias `hydra.utils.instantiate()`) for instantiating objects and calling functions. Prefer `instantiate` for creating objects and `call` for invoking functions.

Call/instantiate supports:
- Class names : Call the `__init__` method
- Callables like functions, static functions, class methods and objects

```python
def call(config: Any, *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An object describing what to call and what params to use.
                   Must have a _target_ field.
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class or method
    """
    ...

# Alias for call
instantiate = call
```

The config passed to these functions must have a key called `_target_`, with the value of a fully qualified class name, class method, static method or callable.   
Any additional parameters are passed as keyword arguments to the target.

For example, your application may have a User class that looks like this:
```python title="user.py"
class User:
  name: str
  age : int
  
  def __init__(self, name: str, age: int):
    self.name = name
    self.age = age
```

<div className="row">

<div className="col col--6">

```yaml title="Config"
bond:
  _target_: user.User
  name: Bond
  age: 7
```


</div>

<div className="col col--6">

```python title="Instantiation"
user : User = instantiate(cfg.bond)
assert isinstance(user, user.User)
assert user.name == "Bond"
assert user.age == 7
```

</div>
</div>


For convenience, instantiate/call returns `None` when receiving `None` as input.
```python
assert instantiate(None) is None
```
