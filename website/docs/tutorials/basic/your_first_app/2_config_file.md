---
id: config_file
title: Specifying a config file
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/basic/your_first_hydra_app/2_config_file"/>

It can get tedious to type all those command line arguments. 
You can solve it by creating a configuration file next to my_app.py.
Hydra configuration files are yaml files and should have the .yaml file extension.

```yaml title="config.yaml"
db: 
  driver: mysql
  user: omry
  password: secret
```

Specify the config name by passing a `config_name` parameter to the `@hydra.main()` decorator.
Note that you should omit the `.yaml` extension.
```python title="my_app.py" {1}
@hydra.main(config_name='config')
def my_app(cfg):
    print(OmegaConf.to_yaml(cfg))
```

`config.yaml` is loaded automatically when you run your application.
```yaml
$ python my_app.py
db:
  driver: mysql
  user: omry
  password: secret
```

You can override values in the loaded config from the command line.  
Note the lack of the `+` prefix.
```yaml {4-5}
$ python my_app.py db.user=root db.password=1234
db:
  driver: mysql
  user: root
  password: 1234
```

You can enable [tab completion](/tutorials/basic/running_your_app/6_tab_completion.md) for your Hydra applications.