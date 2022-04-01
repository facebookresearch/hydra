---
id: search_path
title: Config Search Path
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

The Config Search Path is a list of paths that Hydra searches in order to find configs. It is similar to
the Python `PYTHONPATH`. 
 - When a config is requested, The first matching config in the search path is used.
 - Each search path element has a schema prefix such as `file://` or `pkg://` that corresponds to a `ConfigSourcePlugin`.
    - `file://` points to a file system path. It can either be an absolute path or a relative path.
    Relative path will be resolved to absolute based on the current working dir. Path separator is `/` on all Operating
    Systems.
    - `pkg://` points to an importable Python module, with `.` being the separator. `__init__.py` files are needed in 
    directories for Python to treat them as packages.

You can inspect the search path and the configurations loaded by Hydra via the `--info` flag:

```bash
$ python my_app.py --info searchpath
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
an additional directory on the file system. Another example is in unit testing,
where the defaults list in a config loaded from the `tests/configs` folder may
make reference to another config from the `app/configs` folder. If the
`config_path` or `config_dir` argument passed to `@hydra.main` or to one of the
[initialization methods](compose_api.md#initialization-methods) points to
`tests/configs`, the configs located in `app/configs` will not be discoverable
unless Hydra's search path is modified.

You can configure `hydra.searchpath` in your primary config or from the command line.
:::info
hydra.searchpath can **only** be configured in the primary config. Attempting  to configure it in other configs will result in an error.
:::

In this example, we add a second config directory - `additional_conf`, next to the first config directory:

<div className="row">
<div className="col col--4">

```bash
├── __init__.py
├── conf
│   ├── config.yaml
│   └── dataset
│       └── cifar10.yaml
├── additonal_conf
│   ├── __init__.py
│   └── dataset
│       └── imagenet.yaml
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

`conf/config.yaml` is the primary config for `my_app.py`, config groups `cifar10` and `imagenet` are 
under different folders. 
We can add `additonal_conf` to  `hydra.searchpath` for Hydra to discover `dataset/imagenet`.

<div className="row">
<div className="col col--7">

```yaml title="config.yaml"
defaults:
  - dataset: cifar10

hydra:
  searchpath:
    - pkg://additonal_conf
    # You can also use file based schema:
    # - file:///etc/my_app
    # - file://${oc.env:HOME}/.my_app
```

</div>

<div className="col  col--5">

```python title="my_app.py output"
dataset:
  name: cifar10
  path: /datasets/cifar10






```
</div>
</div>

Overriding `dataset=imagenet` from the commandline:

<div className="row">
<div className="col col--6">

```bash title="command line override"
python my_app.py dataset=imagenet


```

</div>

<div className="col  col--6">

```python title="my_app.py output"
dataset:
  name: imagenet
  path: /datasets/imagenet
```
</div>
</div>





`hydra.searchpath` can be defined or overridden via the command line as well:

```bash title="command line override"
python my_app.py 'hydra.searchpath=[pkg://additonal_conf]'
```

#### Overriding `--config-dir` from the command line
This is a less flexible alternative to `hydra.searchpath`. 
See this [page](hydra-command-line-flags.md) for more info.


#### Creating a `SearchPathPlugin`

<ExampleGithubLink text="ExampleSearchPathPlugin" to="examples/plugins/example_searchpath_plugin/"/>

Framework authors may want to add their configs to the search path automatically once their package is installed,
eliminating the need for any actions from the users.
This can be achieved using a `SearchPathPlugin`. Check the example plugin linked above for more details.
