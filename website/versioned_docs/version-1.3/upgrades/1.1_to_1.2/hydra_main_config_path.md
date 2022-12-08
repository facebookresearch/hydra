---
id: changes_to_hydra_main_config_path
title: Changes to @hydra.main() and hydra.initialize()
---

Prior to Hydra 1.2, **@hydra.main()** and **hydra.initialize()** default `config path` was the directory containing the Python app (calling **@hydra.main()** or **hydra.initialize()**).
Starting with Hydra 1.1 we give [control over the default config path](../1.0_to_1.1/hydra_main_config_path.md),
and starting with Hydra 1.2, with [version_base](../version_base.md) >= "1.2", we choose a default config_path=None, indicating that no directory should be added to the config search path.
