---
id: extending_configs
title: Extending Configs
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Example application" to="examples/patterns/extending_configs"/>

A common pattern is to extend an existing config, overriding and/or adding new config values to it.
The extension is done by including the base configuration, and then overriding the chosen values in the current config.

:::info
This page assumes that you are familiar with the contents of [The Defaults List](../advanced/defaults_list.md).
:::

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
  port: 3307        # overridden by db/mysql.yaml 
  user: omry        # populated by db/mysql.yaml
  password: secret  # populated by db/mysql.yaml
  encoding: utf8    # added by db/mysql.yaml
```

#### Extending a config from another config group:
To extend a config from a different config group, include it using an absolute path (/), and override
the package to *\_here\_*. (*\_here\_* is described in [Packages](../advanced/overriding_packages.md#default-list-package-keywords))

```yaml title="db/mysql.yaml" {2}
defaults:
  - /db_schema/base_mysql@_here_
```

It is otherwise identical to extending a config within the same config group.
