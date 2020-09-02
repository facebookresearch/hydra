---
id: adding_a_package_directive
title: Adding an @package directive
---
Hydra 1.0 introduces the concept of a config `package`. A `package` is the common parent 
path of all nodes in the config file.

 - In Hydra 0.11, there was an implicit default of `_global_` ("")
 - In Hydra 1.1 the default will be `_group_` (the name of the config group).
 - Hydra 1.0 maintains the implicit default of `_global_` and issues a warning for 
any config group file without a `@package` directive.

By adding an explicit `@package` to these configs now, you guarantee that your configs 
will not break when you upgrade to Hydra 1.1.

The `@package` directive is described in details [here](/advanced/overriding_packages.md).  

## Upgrade instructions:
### Recommended (~10 seconds per config file):
`Case 1`: For config files where the common parent path matches the config group name:  
 - Add `# @package _group_` to the top of every config group file
 - Remove the common parent path config file like in the example below.

`Case 2`: For files without a common parent path:
 - Add `# @package _global_`.

### Alternative (not recommended):
 - If you do not want to restructure the config at this time use `Case 2` for all your config files.

### Example for `case 1`:

#### Before
```yaml title="db/mysql.yaml"
db:
  driver: mysql
  host: localhost
  port: 3306
```
#### After
```yaml title="db/mysql.yaml"
# @package _group_
driver: mysql
host: localhost
port: 3306
```
The interpretations of the before and after files are identical.

### Example for `case 2`:
```yaml title="env/prod.yaml"
# @package _global_
db:
  driver: mysql
  host: 10.0.0.11
  port: 3306

webserver:
  host: 10.0.0.11
  port: 443
```
