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
the configurations. Use a combination of the methods described below:

#### Using `@hydra.main()`
Specify a `config_path` in `@hydra.main()`. This path is relative to the application.
All the configuration under the path will be discovered by Hydra.

#### Overriding `hydra.searchpath` config

<ExampleGithubLink text="Example application" to="examples/advanced/config_search_path"/>

In some cases you may want to add multiple locations to the search path. 
For example, an app may want to read the configs from an additional Python module or 
an additional directory on the file system.  
Configure this using `hydra.searchpath` in your primary config or your command line.
:::info
hydra.searchpath can **only** be configured in the primary config. Attempting  to configure it in other configs will result in an error.
:::

Let's say we have the following configuration and application structure:
```bash
├── __init__.py
├── additonal_conf
│   ├── __init__.py
│   └── dataset
│       ├── cifar10.yaml
│       └── imagenet.yaml
├── conf
│   └── config.yaml
└── my_app.py
```
where `conf/config.yaml` is the primary config for `my_app.py`. At the same time, we also 
want to reference configuration from `additonal_conf/dataset` in `config.yaml`. In this case, we can add `additonal_conf` to 
`hydra.searchpath` so Hydra could discover the configurations under `additonal_conf`.

```yaml title="config.yaml"
defaults:
  - dataset: imagenet

hydra:
  searchpath:
    - pkg://additonal_conf
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
python my_app.py hydra.searchpath=[pkg://additonal_conf]
```

#### Overriding `--config-dir` from the command line
This is a less flexible alternative to `hydra.searchpath`. 
See this [page](/docs/advanced/hydra-command-line-flags) for more info.


#### Creating a `SearchPathPlugin`

<ExampleGithubLink text="ExampleSearchPathPlugin" to="examples/plugins/example_searchpath_plugin/"/>

If you do not have control of the primary config file but still want to provide 
configurations to the end users, you can choose to create a `SearchPathPlugin`.
Hydra auto discovers all the Plugins that's created under a `hydra_plugins` package. 
A `SearchPathPlugin` serves the purpose of adding to Hydra's config search path. 
For more details, please check the example plugin linked above.
 