---
id: hierarchical_static_config
title: A hierarchical static configuration
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/structured_configs/2_static_complex"/>


Dataclasses can be nested and then accessed via a common root.  The entire tree is type checked.

```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

@dataclass
class UserInterface:
    title: str = "My app"
    width: int = 1024
    height: int = 768

@dataclass
class MyConfig:
    db: MySQLConfig = MySQLConfig()
    ui: UserInterface = UserInterface()

cs = ConfigStore.instance()
cs.store(name="config", node=MyConfig)

@hydra.main(config_path=None, config_name="config")
def my_app(cfg: MyConfig) -> None:
    print(f"Title={cfg.ui.title}, size={cfg.ui.width}x{cfg.ui.height} pixels")

if __name__ == "__main__":
    my_app()
```