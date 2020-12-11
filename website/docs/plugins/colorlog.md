---
id: colorlog
title: Colorlog plugin
sidebar_label: Colorlog plugin
---
[![PyPI](https://img.shields.io/pypi/v/hydra-colorlog)](https://pypi.org/project/hydra-colorlog/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-colorlog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-colorlog)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-colorlog.svg)](https://pypistats.org/packages/hydra-colorlog)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_colorlog/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_colorlog)

Adds <a class="external" href="https://github.com/borntyping/python-colorlog" target="_blank">colorlog</a> colored logs for `hydra/job_logging` and `hydra/hydra_logging`.


### Installation
```commandline
pip install hydra_colorlog --upgrade
```

### Usage
Override `hydra/job_logging` and `hydra/hydra_logging` your config:

```yaml
defaults:
  - hydra/job_logging: colorlog
    override: true
  - hydra/hydra_logging: colorlog
    override: true 
```

See included [example](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_colorlog/example).
 
![Colored log output](/plugins/colorlog/colorlog.png)
