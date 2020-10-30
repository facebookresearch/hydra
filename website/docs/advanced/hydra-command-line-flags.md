---
id: hydra-command-line-flags
title: Hydra's command line flags
---

Hydra is using the command line for two things:

- Configuring your application (See [Override Grammar](override_grammar/basic.md))
- Controlling Hydra

Any argparse argument that is prefixed by `--`  or `'-` is controlling Hydra.
The rest of the arguments are used to configure your application.


You can view the Hydra specific flags via `--hydra-help`.
<details><summary>Example output</summary>

``` title="Example --hydra-help output"
$ python my_app.py --hydra-help
Hydra (1.0.0rc3)
See https://hydra.cc for more info.

== Flags ==
--help,-h : Application's help
--hydra-help : Hydra's help
--version : Show Hydra's version and exit
--cfg,-c : Show config instead of running [job|hydra|all]
--package,-p : Config package to show
--run,-r : Run a job
--multirun,-m : Run multiple jobs with the configured launcher and sweeper
--shell-completion,-sc : Install or Uninstall shell completion:
    Bash - Install:
    eval "$(python my_app.py -sc install=bash)"
    Bash - Uninstall:
    eval "$(python my_app.py -sc uninstall=bash)"

    Fish - Install:
    python my_app.py -sc install=fish | source
    Fish - Uninstall:
    python my_app.py -sc uninstall=fish | source

--config-path,-cp : Overrides the config_path specified in hydra.main().
                    The config_path is relative to the Python file declaring @hydra.main()
--config-name,-cn : Overrides the config_name specified in hydra.main()
--config-dir,-cd : Adds an additional config dir to the config search path
--info,-i : Print Hydra information
Overrides : Any key=value arguments to override config values (use dots for.nested=overrides)

== Configuration groups ==
Compose your configuration from those groups (For example, append hydra/job_logging=disabled to command line)

hydra/help: default
hydra/hydra_help: default
hydra/hydra_logging: default, disabled, hydra_debug
hydra/job_logging: default, disabled
hydra/launcher: basic, rq, submitit_local, submitit_slurm
hydra/output: default
hydra/sweeper: ax, basic, nevergrad


Use '--cfg hydra' to Show the Hydra config.
```

</details>

#### --help,-h : 
Shows the jpplication's help. This can be [customized](configure_hydra/app_help.md).
<details><summary>Example output</summary>

``` 
$ python my_app.py --help
my_app is powered by Hydra.

== Configuration groups ==
Compose your configuration from those groups (group=option)

db: mysql, postgresql


== Config ==
Override anything in the config (foo.bar=value)

db:
  driver: mysql
  user: omry
  pass: secret


Powered by Hydra (https://hydra.cc)
Use --hydra-help to view Hydra specific help
```

</details>

#### --version
Show Hydra's version and exit


#### --cfg,-c

Show config instead of running. Takes as parameter one of `job`, `hydra` or `all`.
<details><summary>Example output</summary>

```yaml
$ python my_app.py --cfg job
# @package _global_
db:
  driver: mysql
  user: omry
  pass: secret
```
</details>

#### --package,-p
Used in conjunction with --cfg.
-p select a specific config package to show.

<details><summary>Example output</summary>

```yaml
$ python my_app.py --cfg hydra -p hydra.job
# @package hydra.job
name: my_app
override_dirname: ''
id: ???
num: ???
config_name: config
env_set: {}
env_copy: []
config:
  override_dirname:
    kv_sep: '='
    item_sep: ','
    exclude_keys: []
```
</details>

#### --run,-r

Run is the default mode and is not normally needed.

#### --multirun,-m

Run multiple jobs with the configured launcher and sweeper. See [](/tutorials/basic/running_your_app/2_multirun.md).

#### --shell-completion,-sc
Install or Uninstall [shell tab completion](/tutorials/basic/running_your_app/6_tab_completion.md).

#### --config-path,-cp
Overrides the config_path specified in hydra.main(). The config_path is relative to the Python file declaring @hydra.main()

#### --config-name,-cn
Overrides the config_name specified in hydra.main()

#### --config-dir,-cd
Adds an additional config directory to the [config search path](search_path.md).
This is useful for installed apps that want to allow their users to provide additional configs.

#### --info,-i
Print Hydra information. This includes installed plugins, search path, composition trace, generated config and more.

