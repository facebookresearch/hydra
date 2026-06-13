---
id: automatic_schema_matching
title: Automatic schema-matching
hide_title: true
---

In Hydra 1.0, when a config file is loaded, if a config with a matching name and group is present in the `ConfigStore`,
it is used as the schema for the newly loaded config.

There are several problems with this approach:

- **Inflexible**: This approach can only be used when a schema should validate a single config file.
It does not work if you want to use the same schema to validate multiple config files.
- **Unexpected**: This behavior can be unexpected. There is no way to tell this is going to happen when looking at a given
config file.

Hydra 1.1 deprecates this behavior in favor of an explicit config extension via the Defaults List.
This upgrade page aims to provide a summary of the required changes. It is highly recommended that you read the following pages:
- [Background: The Defaults List](../../advanced/defaults_list.md)
- [Background: Extending configs](../../patterns/extending_configs.md)
- [Tutorial: Structured config schema](../../tutorials/structured_config/5_schema.md)


## Migration
Before the upgrade, you have two different configs with the same name (a config file, and a Structured Config in the `ConfigStore`).
You need to rename one of them. Depending on the circumstances and your preference you may rename one or the other.
- If you control both configs, you can rename either of them.
- If you only control the config file, rename it.

### Option 1: rename the Structured Config
This option is less disruptive. Use it if you control the Structured Config.
1. Use a different name when storing the schema into the Config Store. Common choices:
   - `base_` prefix, e.g. `base_mysql`.
   - `_schema` suffix, e.g. `mysql_schema`.
2. Add the schema to the Defaults List of the extending config file.

<details>
  <summary>Click to show an example</summary>

  #### Hydra 1.0
  <div className="row">
  <div className="col col--6">

  ```yaml title="db/mysql.yaml"
  # @package _group_
  host: localhost
  port: 3306






  ```
  </div>
  <div className="col col--6">

  ```python title="db/mysql schema in the ConfigStore"
  @dataclass
  class MySQLConfig:
      host: str
      port: int

  cs = ConfigStore.instance()
  cs.store(group="db",
          name="mysql",
          node=MySQLConfig)
  ```
  </div>
  </div>

  #### Hydra 1.1
  <div className="row">
  <div className="col col--6">

  ```yaml title="db/mysql.yaml" {1,2}
  defaults:
    - base_mysql

  host: localhost
  port: 3306




  ```
  </div>
  <div className="col col--6">

  ```python title="db/mysql schema in the ConfigStore" {8}
  @dataclass
  class MySQLConfig:
      host: str
      port: int

  cs = ConfigStore.instance()
  cs.store(group="db",
           name="base_mysql",
           node=MySQLConfig)
  ```
  </div>
  </div>

</details>

### Option 2: rename the config file
This option is a bit more disruptive. Use it if you only control the config file.
1. Rename the config file. Common choices are `custom_` or `my_` prefix, e.g. `custom_mysql.yaml`. You can also use a domain specific name like `prod_mysql.yaml`.
2. Add the schema to the Defaults List of the extending config file.
3. Update references to the config name accordingly, e.g. on the command-line `db=mysql` would become `db=custom_mysql`, and in a defaults list `db: mysql` would become `db: custom_mysql`.


<details>
  <summary>Click to show an example</summary>

  #### Hydra 1.0
  <div className="row">
  <div className="col col--6">

  ```yaml title="db/mysql.yaml"
  # @package _group_
  host: localhost
  port: 3306
  ```
  ```yaml title="config.yaml"
  defaults:
    - db: mysql
  ```
  </div>
  <div className="col col--6">

  ```python title="db/mysql schema in the ConfigStore"
  @dataclass
  class MySQLConfig:
      host: str
      port: int

  cs = ConfigStore.instance()
  cs.store(group="db",
           name="mysql",
           node=MySQLConfig)

  ```
  </div>
  </div>

  #### Hydra 1.1
  Rename `db/mysql.yaml` to `db/custom_mysql.yaml` and explicitly add the schema to the Defaults List.
  <div className="row">

  <div className="col col--6">

  ```yaml title="db/custom_mysql.yaml" {1,2}
  defaults:
    - mysql

  host: localhost
  port: 3306
  ```
  ```yaml title="config.yaml" {2}
  defaults:
    - db: custom_mysql
  ```

  </div>
  <div className="col col--6">

  ```python title="db/mysql schema in the ConfigStore"





                     NO CHANGES






  ```
  </div>
  </div>

  Don't forget to also update your command line overrides from `db=mysql` to `db=custom_mysql`.
</details>
