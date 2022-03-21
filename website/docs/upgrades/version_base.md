---
id: version_base
title: version_base
---

Hydra since version 1.2 supports backwards compatible upgrades by default
through the use of the `version_base` parameter to **@hydra.main()** and **hydra.initialize()**.

There are three classes of values that the `version_base` parameter supports,
given new and existing users greater control of the default behaviors to use.

1. If the `version_base` parameter is **not specified**, Hydra 1.x will use defaults compatible with version 1.1.
Also in this case, a warning is issued to indicate an explicit `version_base` is preferred.

2. If the `version_base` parameter is **None**, then the defaults are chosen for the current minor Hydra version.
For example for Hydra 1.2, then would imply `config_path=None` and `hydra.job.chdir=False`.

3. If the `version_base` parameter is an **explicit version string** like "1.1",
then the defaults appropriate to that version are used.
