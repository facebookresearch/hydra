---
id: extending_configs
title: Extending Configs
---
[![Example application](https://img.shields.io/badge/-Example%20applications-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/patterns/extending_configs)

A common pattern is to extend an existing config, overriding and/or adding new config values to it.
The extension is done by including the base configuration, and then overriding the chosen values in the current config.

#### Extending a config from the same config group:

<div className="row">
<div className="col col--4">

```yaml title="config.yaml"
defaults:
  - db: mysql 





```
</div>
<div className="col col--4">

```yaml title="db/mysql.yaml" {2}
defaults:
  - base_mysql

user: omry
password: secret
port: 3307
encoding: utf8
```
</div>
<div className="col col--4">

```yaml title="db/base_mysql.yaml"
host: localhost
port: 3306
user: ???
password: ???



```
</div>
</div>

Output:
```yaml title="$ python my_app.py"
db:
  host: localhost   # from db/base_mysql
  port: 3307        # overriden by db/mysql.yaml 
  user: omry        # populated by db/mysql.yaml
  password: secret  # populated by db/mysql.yaml
  encoding: utf8    # added by db/mysql.yaml
```

#### Extending a config from another config group:
To extend a config from a different config group, include it using an absolute path (/), and override
the package to `_here_`.

```yaml title="db/mysql.yaml" {2}
defaults:
  - /db_schema/base_mysql@_here_
```

It is otherwise identical to extending a config within the same config group.
