---
id: app_packaging
title: Application packaging
sidebar_label: Application packaging 
---

You can package your Hydra application along with its configuration.
There is a working example [here](https://github.com/facebookresearch/hydra/tree/0.11_branch/examples/advanced/hydra_app_example).

You can run it with:

```yaml
$ python examples/advanced/hydra_app_example/hydra_app/main.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

To install it, use:
```text
$ pip install examples/advanced/hydra_app_example
...
Successfully installed hydra-app-0.1
```

Run the installed app with:
```yaml
$ hydra_app
dataset:
  name: imagenet
  path: /datasets/imagenet
```

The installed app will use the packaged configuration files.
