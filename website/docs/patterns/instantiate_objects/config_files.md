---
id: config_files
title: Config files example
sidebar_label: Config files example
---
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/patterns/instantiate_objects)

This example demonstrates the use of config files to instantiated objects.

```python
class DBConnection:
    def connect(self):
        ...

class MySQLConnection(DBConnection):
    def __init__(self, host: str, user: str, password: str) -> None:
        self.host = host
        self.user = user
        self.password = password

    def connect(self) -> None:
        print(f"MySQL connecting to {self.host}")


class PostgreSQLConnection(DBConnection):
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self) -> None:
        print(f"PostgreSQL connecting to {self.host}")
```

To support this, we can have a parallel config structure:
```text
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

Config files:
<div className="row">

<div className="col col--6">

```yaml title="db/mysql.yaml"
# @package _group_
_target_: my_app.MySQLConnection
host: localhost
user: root
password: 1234

```

</div>

<div className="col col--6">

```yaml title="db/postgresql.yaml"
# @package _group_
_target_: my_app.PostgreSQLConnection
host: localhost
user: root
password: 1234
database: tutorial
```

</div>
</div>


```yaml title="config.yaml"
defaults:
  - db: mysql
```



With this, you can instantiate the object from the configuration with a single line of code:
```python
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg):
    connection = hydra.utils.instantiate(cfg.db)
    connection.connect()
```