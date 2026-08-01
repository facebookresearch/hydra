---
id: version_base
title: version_base
---

Hydra since version 1.2 supports backwards compatible upgrades by default
through the use of the `version_base` parameter to **@hydra.main()** and **hydra.initialize()**.

## Hydra 1.3.5 deprecation

Hydra 1.3.5 emits `Hydra14MigrationWarning` when `version_base` is omitted or
set to `"1.1"`. Those cases select Hydra 1.1 compatibility behavior that Hydra
1.4 removes. Hydra 1.4 also stops accepting `version_base="1.2"`, although that
value already selects the surviving behavior in Hydra 1.3.

Follow [Preparing for Hydra 1.4](1.3_to_1.4/prepare_for_1_4.md) while your
application is still running on Hydra 1.3. Set `version_base="1.3"` explicitly
and resolve any compatibility problems before installing Hydra 1.4.

There are three classes of values that the `version_base` parameter supports,
given new and existing users greater control of the default behaviors to use.

1. If the `version_base` parameter is **not specified**, Hydra 1.3 will use defaults compatible with version 1.1.
Hydra 1.3.5 emits `Hydra14MigrationWarning` because Hydra 1.4 removes this compatibility behavior.

2. If the `version_base` parameter is **None**, then the defaults are chosen for the current minor Hydra version.
For example, for Hydra 1.3 this implies `config_path=None` and `hydra.job.chdir=False`.

3. If the `version_base` parameter is an **explicit version string** like "1.3",
then the defaults appropriate to that version are used.

Before upgrading to Hydra 1.4, use `version_base="1.3"` temporarily and test
the application. After upgrading, remove the parameter.
