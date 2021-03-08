---
id: search_path
title: Config Search Path
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

The Config Search Path is a list of paths that Hydra searches in order to find configs. It is similar to
the Python `PYTHONPATH`. 
 - When a config is requested, The first matching config in the search path is used.
 - Each search path element has a schema prefix such as `file://` or `pkg://` that is corresponding to a `ConfigSourcePlugin`.

You can inspect the search path and the configurations loaded by Hydra by turning on verbose logging for the `hydra` logger:

```bash
$ python my_app.py hydra.verbose=hydra
```

There's a few options to modify the config search path so Hydra could discover 
the configurations. You can pick and choose some or all of the following methods below
to provide configuration to your apps.

### Set `config_name`/`config_path` in`hydra.main()`
This is the most common use case: all config files are grouped under one directory and
has a relative path to the application. You can add them to the search path by setting `config_path` 
or `config_name`.

### Override `hydra.searchpath` config

<ExampleGithubLink text="Example application" to="examples/advanced/config_search_path"/>

Sometimes your configurations are not grouped nicely in one folder - 
you may need to read configurations from multiple locations, so passing one directory to `config_path` 
won't work. In this case, you can pass in a list of config paths via `hydra.searchpath` in 
the primary config or override from the command line.

Let's say we have the following configuration and application structure:
```bash
$ tree  config_search_path
config_search_path
├── __init__.py
├── conf
│   └── config.yaml
├── dataset
│   ├── cifar10.yaml
│   └── imagenet.yaml
└── my_app.py
```
where `conf/config.yaml` is the primary config for `my_app.py`. However at the same time, we also 
want to reference configuration from `dataset` in `config.yaml`. In this case, we can add `dataset` to 
`hydra.searchpath` so Hydra could discover the configurations under `dataset`.

```yaml title="config.yaml"
defaults:
  - dataset: imagenet

hydra:
  searchpath:
    - pkg://examples.advanced.config_search_path
```

```python title="my_app.py"

@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```

```python title="my_app.py output"
dataset:
  name: imagenet
  path: /datasets/imagenet
```

In addition to override `hydra.searchpath` in primary config, one can also override from the command line.

```bash title="command line override"
python my_app.py hydra.searchpath=[pkg://examples.advanced.config_search_path]
```

### Override `--config-dir` from the command line
This is a less flexible alternative to `hydra.searchpath`. See this [page](/docs/advanced/hydra-command-line-flags) for more info.


### Create `SearchPathPlugin`

<ExampleGithubLink text="ExampleSearchPathPlugin" to="examples/plugins/example_searchpath_plugin/"/>

Hydra auto discovers all the Plugins that's created under a `hydra_plugins` package. So if modifying `hydra.searchpath` 
is not an option for you, you can still create a `SearchPathPlugin` for the configs to be discovered. 
For more details, please check the example plugin linked above.
 