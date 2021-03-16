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

There are a few ways to modify the config search path, enabling Hydra to access configuration in 
different locations.
Use a combination of the methods described below:

#### Using `@hydra.main()`
Using the  `config_path` parameter `@hydra.main()`.  The `config_path` is relative to location of the Python script.

#### Overriding `hydra.searchpath` config

<ExampleGithubLink text="Example application" to="examples/advanced/config_search_path"/>

In some cases you may want to add multiple locations to the search path. 
For example, an app may want to read the configs from an additional Python module or 
an additional directory on the file system.  
Configure this using `hydra.searchpath` in your primary config or your command line.
:::info
hydra.searchpath can **only** be configured in the primary config. Attempting  to configure it in other configs will result in an error.
:::

Let's say we have the following configuration structure and application code:
<div className="row">
<div className="col col--4">

```bash
├── __init__.py
├── additonal_conf
│   ├── __init__.py
│   └── dataset
│       └── imagenet.yaml
├── conf
│   ├── config.yaml
│   └── dataset
│       └── cifar10.yaml
└── my_app.py
```
</div>
<div className="col  col--8">

```python title="my_app.py"

@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```
</div>
</div>

`conf/config.yaml` is the primary config for `my_app.py`. To reference `additonal_conf/dataset/imagenet` 
in `config.yaml`, we can add `additonal_conf` to 
`hydra.searchpath` so Hydra could discover the configurations under `additonal_conf`.

<div className="row">
<div className="col col--7">

```yaml title="config.yaml"
defaults:
  - dataset: imagenet

hydra:
  searchpath:
    - pkg://additonal_conf
    # You can also use file based schema:
    # - file:///etc/my_app
    # - file://${env:HOME}/.my_app
```

</div>

<div className="col  col--5">

```python title="my_app.py output"
dataset:
  name: imagenet
  path: /datasets/imagenet






```
</div>
</div>







In addition to override `hydra.searchpath` in primary config, one can also override from the command line.

```bash title="command line override"
python my_app.py 'hydra.searchpath=[pkg://additonal_conf]'
```

#### Overriding `--config-dir` from the command line
This is a less flexible alternative to `hydra.searchpath`. 
See this [page](/docs/advanced/hydra-command-line-flags) for more info.


#### Creating a `SearchPathPlugin`

<ExampleGithubLink text="ExampleSearchPathPlugin" to="examples/plugins/example_searchpath_plugin/"/>

Framework authors may want to add their configs to the search path automatically once their package is installed,
eliminating the need for any actions from the users.
This can be achieved using a `SearchPathPlugin`. Check the example plugin linked above for more details.
