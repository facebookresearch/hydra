---
id: defaults_list
title: The Defaults List
---

## Introduction

:::important
Many of the features described in this page are new. Please report any issues.
:::

The Defaults List is a list in an input config that instructs Hydra how to build the output config.
Each input config can have a Defaults List as a top level element. The Defaults List itself
is not a part of output config.

```text title="Defaults List YAML syntax"
defaults:
 (- CONFIG|GROUP_DEFAULT)*

CONFIG                 : (CONFIG_GROUP/)?CONFIG_NAME(@PACKAGE)?
GROUP_DEFAULT          : [optional|override]? CONFIG_GROUP(@PACKAGE)?: OPTION
OPTION                 : CONFIG_NAME|CONFIG_NAMES|null
```

*CONFIG* : A config to use when creating the output config. e.g. `db/mysql`, `db/mysql@backup`.

*GROUP_DEFAULT* : An *overridable* config. e.g. `db: mysql`, `db@backup: mysql`.
- ***override*** : Overrides the option of a previously defined GROUP_DEFAULT.
- ***optional*** : By default, an OPTION that do not exist causes an error; optional suppresses the error.
- ***null*** : A place-holder for a future override. If it is not overridden the entry is ignored.

*CONFIG_NAME*: The name of a config, without the file system extension. e.g. `mysql` and not `mysql.yaml`.

*CONFIG_NAMES* : A list of config names. e.g. `[mysql, sqlite]`

*CONFIG_GROUP* : A path to a set of configs.
The path is relative to the containing config.
It can be made absolute by prefixing it with a `/`.
The path separator is `/` regardless of the operating system.

*OPTION*: The currently selected *CONFIG_NAME* or *CONFIG_NAMES* from a *CONFIG_GROUP*.

*PACKAGE* : Where to place the content of the config within the output config.
It is relative to the Package of the containing config by default. See [Packages](overriding_packages.md).

## An example

```text title="Config directory structure"
├── server
│   ├── db
│   │   ├── mysql.yaml
│   │   └── sqlite.yaml
│   └── apache.yaml
└── config.yaml
```
Input configs:
<div className="row">
<div className="col col--4">

```yaml title="config.yaml"
defaults:
  - server/apache

debug: false



```
</div>

<div className="col col--4">

```yaml title="server/apache.yaml"
defaults:
  - db: mysql

name: apache



```
</div>

<div className="col col--4">

```yaml title="server/db/mysql.yaml"
name: mysql
```

```yaml title="server/db/sqlite.yaml"
name: sqlite
```
</div></div>

Output config:
```yaml title="$ python my_app.py"
server:
  db:
    name: mysql
  name: apache
debug: false
```

## Overriding Config Group options
A Config Group's option can be overridden using a new *GROUP_DEFAULT* with the ***override*** keyword.
If a Group Default is overridden more than once, the last one, in depth first order, wins.

Extending the previous example:

<div className="row">
<div className="col col--6">

```yaml title="config.yaml" {3}
defaults:
  - server/apache
  - override server/db: sqlite

debug: false
```
</div>
<div className="col col--6">

```yaml title="$ python my_app.py" {2,3}
server:
  db:
    name: sqlite
  name: apache
debug: false
```
</div>
</div>

A Config Group's option can also be overridden via the command line. e.g:
```
$ python my_app.py server/db=sqlite
```

## Composition order
The Defaults List is ordered:
- If multiple configs define the same value, the last one wins.
- If multiple configs contribute to the same dictionary, the result is the combined dictionary.

By default, the content of a config is overriding the content of configs in the defaults list.

<div className="row">
<div className="col col--6">

```yaml title="config.yaml" {5}
defaults:
  - db: mysql

db:
  host: backup
```

</div>

<div className="col  col--6">

```yaml title="Result: db.host from config" {3}
db:
  driver: mysql    # db/mysql.yaml
  host: backup     # config.yaml
  port: 3306       # db/mysql.yaml

```

</div>
</div>

The `_self_` entry determines the relative position of **this** config in the Defaults List.
If it is not specified, it is added automatically as the last item.

<div className="row">
<div className="col col--6">

```yaml title="config.yaml" {2,6}
defaults:
  - _self_
  - db: mysql # Overrides this config

db:
  host: backup
```
</div>
<div className="col  col--6">

```yaml title="Result: All values from db/mysql" {3}
db:
  driver: mysql    # db/mysql.yaml
  host: localhost  # db/mysql.yaml
  port: 3306       # db/mysql.yaml


```
</div>
</div>

With `_self_` at the top of the Defaults List, the host field defined in *config.yaml* now precedes the host field defined
in *db/mysql.yaml*, and as a result is overridden.

## Interpolation in the Defaults List

Config Group Options can be selected using interpolation.
```yaml
defaults:
  - server: apache
  - db: mysql
  - combination_specific_config: ${server}_${db}  # apache_mysql
```
Interpolation keys can be config groups with any @package overrides.
For example: `${db/engine}`, `${db@backup}`

The selected option for *combination_specific_config* depends on the final selected options for *db* and *server*.
e.g., If *db* is overridden to *sqlite*, *combination_specific_config* will become *apache_sqlite*.

#### Restrictions:

 - Interpolation keys in the Defaults List cannot reference values in the Final Config Object (it does not yet exist).
 - Defaults List interpolation keys are absolute (even in nested configs).
 - The subtree expanded by an Interpolated Config may not contain Default List overrides.

See [Patterns/Specializing Configs](/patterns/specializing_config.md) for more information.

## Debugging the Defaults List
Hydra's config composition process is as follows:

 - The Defaults Tree is created.
 - The Final Defaults List is created via a DFS walk of the Defaults Tree.
 - The Output Config is composed from the entries in the Final Defaults List.

You can inspect these artifacts via command line flags:

- `--info defaults-tree` shows the Defaults Tree.
- `--info defaults` Shows the Final Defaults List.
- `--cfg job|hydra|all` Shows the Output Config.

Example outputs:

<details>
  <summary>python my_app.py <b>--info defaults-tree</b></summary>
  ```yaml title=""
  <root>:
    hydra/config:
      hydra/hydra_logging: default
      hydra/job_logging: default
      hydra/launcher: basic
      hydra/sweeper: basic
      hydra/output: default
      hydra/help: default
      hydra/hydra_help: default
      _self_
    config:
      server/apache:
        server/db: mysql
        _self_
      _self_
  ```
</details>
<details>
  <summary>python my_app.py <b>--info defaults</b></summary>

  ```text
  Defaults List
  *************
  | Config path                 | Package             | _self_ | Parent        |
  -------------------------------------------------------------------------------
  | hydra/hydra_logging/default | hydra.hydra_logging | False  | hydra/config  |
  | hydra/job_logging/default   | hydra.job_logging   | False  | hydra/config  |
  | hydra/launcher/basic        | hydra.launcher      | False  | hydra/config  |
  | hydra/sweeper/basic         | hydra.sweeper       | False  | hydra/config  |
  | hydra/output/default        | hydra               | False  | hydra/config  |
  | hydra/help/default          | hydra.help          | False  | hydra/config  |
  | hydra/hydra_help/default    | hydra.hydra_help    | False  | hydra/config  |
  | hydra/config                | hydra               | True   | <root>        |
  | server/db/mysql             | server.db           | False  | server/apache |
  | server/apache               | server              | True   | config        |
  | config                      |                     | True   | <root>        |
  -------------------------------------------------------------------------------
  ```
</details>
<details>
  <summary>python my_app.py <b>--cfg job</b></summary>

  ```yaml
  server:
    db:
      name: mysql
    name: apache
  debug: false
  ```
</details>

## Related topics
- [Packages](overriding_packages.md)
- [Common Patterns/Extending Configs](patterns/extending_configs.md)
- [Common Patterns/Configuring Experiments](patterns/configuring_experiments.md)
- [Selecting multiple configs from a Config Group](patterns/select_multiple_configs_from_config_group.md)
