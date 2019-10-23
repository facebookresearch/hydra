---
id: objects
title: Creating objects
sidebar_label: Creating objects
---
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
  class: tutorial.objects_example.objects.MySQLConnection
  params:
    host: localhost
    user: root
    password: 1234
```
db/postgresql.yaml:
```yaml
db:
  class: tutorial.objects_example.objects.PostgreSQLConnection
  params:
    host: localhost
    user: root
    password: 1234
    database: tutorial
```

With this, you can instantiate the object from the configuration with a single line of code:
```python
@hydra.main(config_path="conf/config.yaml")
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
