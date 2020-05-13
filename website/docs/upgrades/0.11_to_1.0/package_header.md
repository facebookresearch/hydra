---
id: package_header
title: Package header
---

The `@package` header is described in details [here](/tutorials/basic/2_config_file.md#package-header).

You are encouraged to read the description, but here is the TLDR:
### Before
```yaml
db:
  driver: mysql
  host: localhost
  port: 3306
```
### After
The recommended method is to use the special package `_group_`.
```yaml
# @package _group_
driver: mysql
host: localhost
port: 3306
```

If you do not want to change your config at all, you can use the special package `_global_` 
```yaml
# @package _global_
db:
  driver: mysql
  host: localhost
  port: 3306
```

<div class="alert alert--info" role="alert">
<b>@package _group_</b> will become the default in Hydra 1.1 and you will no longer need to specify it.
By adding an explicit @package to your config now, you guarantee that your config will not break when you upgrade
to Hydra 1.1.
</div>
