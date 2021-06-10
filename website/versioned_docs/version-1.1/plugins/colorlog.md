---
id: colorlog
title: Colorlog plugin
sidebar_label: Colorlog plugin
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

[![PyPI](https://img.shields.io/pypi/v/hydra-colorlog)](https://pypi.org/project/hydra-colorlog/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-colorlog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-colorlog)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-colorlog.svg)](https://pypistats.org/packages/hydra-colorlog)<ExampleGithubLink text="Example application" to="plugins/hydra_colorlog/example"/><ExampleGithubLink text="Plugin source" to="plugins/hydra_colorlog"/>

Adds <a class="external" href="https://github.com/borntyping/python-colorlog" target="_blank">colorlog</a> colored logs for `hydra/job_logging` and `hydra/hydra_logging`.


### Installation
```commandline
pip install hydra_colorlog --upgrade
```

### Usage
Override `hydra/job_logging` and `hydra/hydra_logging` in your config:

```yaml
defaults:
  - override hydra/job_logging: colorlog
  - override hydra/hydra_logging: colorlog
```

There are several standard approaches for configuring plugins. Check [this page](../patterns/configuring_plugins.md) for more information.

See included <GithubLink to="plugins/hydra_colorlog/example">example application</GithubLink>.
 
![Colored log output](/plugins/colorlog/colorlog.png)
