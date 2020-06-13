---
id: debugging
title: Debugging
sidebar_label: Debugging
---
Hydra provides a few options to improve debuggability.

### Printing the configuration
Print the config for your app without running your function by adding `--cfg` or `-c` to the command line.

The `--cfg` option takes one argument indicating which part of the config to print:
* `job` : Your config
* `hydra` : Hydra's config
* `all` : The full config, which is a union of `job` and `hydra`.

```yaml
# A normal run:
$ python my_app.py
MySQL connecting to localhost with user=root and password=1234

# just show the config without running your function:
$ python my_app.py --cfg job
db:
  host: localhost
  user: root
  password: 1234
```
The printed config includes any modifications done via the command line:
```yaml {3}
$ python my_app.py db.host=10.0.0.1 --cfg job
db:
  host: 10.0.0.1
  user: root
  password: 1234
```

You can use `--package` or `-p` to select a a specific config package:
```yaml
python my_app.py --cfg hydra --package hydra.job
# @package hydra.job
name: my_app
config_name: config
...
```

### Info
Hydra can print information about your plugins, config search path, composition trace and more using the  
`--info` flag.
```text
$ python my_app.py --info
```

Subset of output (Complete [example](http://paste.ubuntu.com/p/JWh2cKgGtD/))
```commandline
Config search path
...
Profiling information
...
Composition trace
...
Config
...
```


