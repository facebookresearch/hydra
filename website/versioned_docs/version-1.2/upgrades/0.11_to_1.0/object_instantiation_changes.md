---
id: object_instantiation_changes
title: Object instantiation changes
hide_title: true
---


## Object instantiation changes
Hydra 1.0.0 is deprecating ObjectConf and the corresponding config structure to a simpler one without the params node.
This removes a level of nesting from command line and configs overrides.

<div className="row">
<div className="col col--6">

```yaml title="Hydra 0.11"
class: my_app.MySQLConnection
params:
  host: localhost
  user: root
  password: 1234
```

</div>

<div className="col  col--6">

```yaml title="Hydra 1.0"
_target_: my_app.MySQLConnection
host: localhost
user: root
password: 1234

```


</div>
</div>

## Hydra configuration
Hydra plugins are configured using the same mechanism.
This means that this change will effect how all plugins are configured and overridden.
This is a breaking change for code overriding configs in such plugins, but luckily it's easy to fix.

As an example, a Sweeper plugin override will change as follows:

<div className="row">
<div className="col col--6">

```shell script title="Hydra 0.11"
hydra.sweeper.params.max_batch_size=10
```

</div>

<div className="col  col--6">

```shell script title="Hydra 1.0"
hydra.sweeper.max_batch_size=10
```

</div>
</div>