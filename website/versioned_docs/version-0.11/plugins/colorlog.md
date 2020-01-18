---
id: colorlog
title: Colorlog plugin
sidebar_label: Colorlog plugin
---
Adds <a class="external" href="https://github.com/borntyping/python-colorlog" target="_blank">colorlog</a> colored logs for `hydra/job_logging` and `hydra/hydra_logging`.

Install with 
```
pip install hydra_colorlog
```

Once installed, override `hydra/job_logging` and `hydra/hydra_logging` your config:

```yaml
defaults:
  - hydra/job_logging: colorlog
  - hydra/hydra_logging: colorlog
```

See included [example](https://github.com/facebookresearch/hydra/tree/0.11_branch/plugins/hydra_colorlog/example).
 
![Colored log output](/plugins/colorlog/colorlog.png)
