---
id: app_packaging
title: Application packaging
sidebar_label: Application packaging 
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/advanced/hydra_app_example"/>

You can package your Hydra application along with its configuration.
An example <GithubLink to="examples/advanced/hydra_app_example">standalone application</GithubLink> is included in the repo.

Run it with:
```yaml
$ python examples/advanced/hydra_app_example/hydra_app/main.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

Install it with:
```text
$ pip install examples/advanced/hydra_app_example
...
Successfully installed hydra-app-0.1
```

Once installed, run the installed app with:
```yaml
$ hydra_app
dataset:
  name: imagenet
  path: /datasets/imagenet
```

The installed app will use the packaged configuration files.
