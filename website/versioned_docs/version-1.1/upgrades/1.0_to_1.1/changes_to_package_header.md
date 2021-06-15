---
id: changes_to_package_header
title: Changes to Package Header
---

Hydra 1.0 introduced the package header and required everyone to specify it in their configs.
This was done to facilitate a transition from a model where the packages are global
to a model where - by default - package are derived from the config group.

e.g: Change of the default package for `server/db/mysql.yaml` from `_global_` to `server.db`.

Hydra 1.1 completes this transition. 
- If a package header is not specified, the config will have the default package as described above.
- \_group\_ and \_name\_ in package header are deprecated (You can still use a literal package header).


:::info
Another important change in Hydra 1.1 is the 
[Changes to default composition order](./changes_to_default_composition_order.md).
:::

### Migration

If your header is `# @package _group_`, remove the header.
<div className="row">
<div className="col col--6">

```yaml title="db/mysql.yaml in Hydra 1.0"
# @package _group_
host: localhost
```

</div>

<div className="col  col--6">

```yaml title="db/mysql.yaml in Hydra 1.1"
host: localhost

```
</div>
</div>

If your header is using `_group_` or `_name_` to specify a package other than the default package, 
Specify the literal package:

<div className="row">
<div className="col col--6">

```yaml title="db/mysql.yaml in Hydra 1.0"
# @package _group_._name_
host: localhost
```

</div>

<div className="col  col--6">

```yaml title="db/mysql.yaml in Hydra 1.1"
# @package db.mysql
host: localhost
```
</div>
</div>

### Compatibility with both Hydra 1.0 and 1.1
If your configs should be compatible with both Hydra 1.0 and Hydra 1.1, use literal package headers.
<div className="row">
<div className="col col--6">

```yaml title="db/mysql.yaml in Hydra 1.0"
# @package _group_
host: localhost
```

</div>

<div className="col  col--6">

```yaml title="db/mysql.yaml in Hydra 1.1"
# @package db
host: localhost
```
</div>
</div>
