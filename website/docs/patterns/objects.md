---
id: objects
title: Creating objects and calling functions
sidebar_label: Creating objects and calling functions
---
### Instantiating objects and calling methods and functions
Use `hydra.utils.call()` (or its alias `hydra.utils.instantiate()`) to instantiate objects, call functions and call class methods. While `instantiate` is an alias for `call`, you may prefer to use `call` for invoking functions and class methods, and `instantiate` for creating objects.

```python
def call(config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An ObjectConf or DictConfig describing what to call and what params to use
    :param args: optional positional parameters pass-through
    :param kwargs: optional named parameters pass-through
    :return: the return value from the specified class or method
    """
```

### ObjectConf definition
ObjectConf is defined in `hydra.types.ObjectConf`:
```python
@dataclass
class ObjectConf(Dict[str, Any]):
    # class, class method or function name
    cls: str = MISSING
    # parameters to pass to cls when calling it
    params: Any = field(default_factory=dict)
```

### Example config node
```yaml
# target class name, function name or class method fully qualified name
cls: foo.Bar
# optional parameters dictionary to pass when calling the target
params:
  x: 10
```


#### Example usage

models.py
```python
class Foo:
  def __init__(x: int, y: int) -> None:
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
  cls: models.Foo
  params:
    x: 10
    y: 20
    
myclassmethod:
  cls: models.Foo.class_method
  params:
    z: 5

mystaticmethod:
  cls: models.Foo.static_method
  params:
    z: 15

myfunction:
  cls: models.bar
  params:
    z: 15
```

Now to test these instantiate / call them as follows:
```python
import hydra

@hydra.main(config_path="config.yaml")
def app(cfg):
  foo1: Foo = hydra.utils.call(cfg.myobject)  # Foo(10, 20)
  foo2: Foo = hydra.utils.call(cfg.myclassmethod)  # Foo(5, 10)
  ret1: int = hydra.utils.call(cfg.mystaticmethod)  # 16
  ret2: int = hydra.utils.call(cfg.myfunction)  # 17
```
### Real World Example
One of the best ways to drive different behavior in the application is to instantiate different implementations of an interface.
The code using the instantiated object only knows the interface which remains constant, but the behavior
is determined by the actual object instance.

A Database connection interface may have a `connect()` method, implemented by different database drivers.

```python
class DBConnection:
    def connect(self):
        pass

class MySQLConnection(DBConnection):
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        print(
            "MySQL connecting to {} with user={} and password={}".format(
                self.host, self.user, self.password
            )
        )

class PostgreSQLConnection(DBConnection):
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        print(
            "PostgreSQL connecting to {} "
            "with user={} and password={} and database={}".format(
                self.host, self.user, self.password, self.database
            )
        )
```

To support this, we can have a parallel config structure:
```text
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

Config file: `config.yaml`
```yaml
defaults:
  - db: mysql
```
Config file: `db/mysql.yaml`
```yaml
db:
  cls: tutorial.objects_example.objects.MySQLConnection
  params:
    host: localhost
    user: root
    password: 1234
```
db/postgresql.yaml:
```yaml
db:
  cls: tutorial.objects_example.objects.PostgreSQLConnection
  params:
    host: localhost
    user: root
    password: 1234
    database: tutorial
```

With this, you can instantiate the object from the configuration with a single line of code:
```python
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg):
    connection = hydra.utils.instantiate(cfg.db)
    connection.connect()
```

MySQL is the default per the `config.yaml` file:
```text
$ python my_app.py
MySQL connecting to localhost with user=root and password=1234
```
Change the instantiated object class and override values from the command line:
```text
$ python my_app.py db=postgresql db.params.password=abcde
PostgreSQL connecting to localhost with user=root and password=abcde and database=tutorial
```
