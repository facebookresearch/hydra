---
id: command_line_overrides
title: Command line overrides
---
You can manipulate your configuration via the command line. This includes:
- Manipulation of the defaults list
- Manipulation of the resulting config object

Both of those looks similar in the command line.
Command line overrides matching a Config group are manipulating the Defaults List; The rest are manipulating the resulting config object.

```text  title="Defaults List overrides"
PACKAGE   : PATH[.PATH]*
PATH      : [A-Za-z0-9_-]+ 
OPTION    : .*

# Changing an existing item
GROUP[@SRC_PKG[:DEST_PKG]][=OPTION]

# Appending a new item
+GROUP@[SRC_PKG]=OPTION

# Deleting an existing item
~GROUP[@PACKAGE][=OPTION]
```

```text title="Config overrides"
KEY=VALUE
KEY   : .+
VALUE : .+

# Changing an existing item
KEY=VALUE

# Appending a new item
+KEY=VALUE

# Deleting an existing item
~KEY[=VALUE]
```

# Examples
## Config values
- Overriding a config value : `foo.bar=value`
- Appending a config value : `+foo.bar=value`
- Removing a config value : `~foo.bar`, `~foo.bar=value`

## Defaults list
- Overriding selected Option: `db=mysql`
- Overriding selected Option and renaming package: `db@src_pkg:dst_pkg=mysql`
- Renaming package: `db@src_pkg:dst_pkg`
- Appending to defaults: `+experiment=exp1`
- Deleting from defaults: `~db`, `~db=mysql`

When renaming a package, if the current item in the defaults list does not have a package, 
use the empty string for the source package, e.g: `db@:dst_package`.  