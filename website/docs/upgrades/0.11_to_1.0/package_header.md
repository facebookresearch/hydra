---
id: package_header
title: Upgrading package header
---
The `@package` header is described in details [here](/advanced/package_header.md).
You are encouraged to read the details, but the TLDR is:

- For configs mentioned in `hydra.main()` (Primary config files), you don't need to do anything.
- For configs in config groups, read on.

### Before
```yaml title="db/mysql.yaml"
db:
  driver: mysql
  host: localhost
  port: 3306
```
### After
The recommended method is to use the special package `_group_`.
```yaml title="db/mysql.yaml"
# @package _group_
driver: mysql
host: localhost
port: 3306
```

If you do not want to change your config structure, use `@package _global_`. 
```yaml title="db/mysql.yaml"
# @package _global_
db:
  driver: mysql
  host: localhost
  port: 3306
```

<div class="alert alert--info" role="alert">
For configs in config groups, <b>@package _group_</b> will become the default in Hydra 1.1 and you will no longer need to specify it.
By adding an explicit @package to these configs now, you guarantee that your configs will not break when you upgrade to Hydra 1.1.
</div>
