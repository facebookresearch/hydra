---
id: configuring_plugins
title: Configuring Plugins
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

Hydra plugins usually comes with sensible defaults which works with minimal configuration.
There are two primary ways to customize the configuration of a plugin:
- Overriding it directly in your primary config
- Extending the config and using it from your primary config.
	
The first method is the simpler, but it makes it harder to switch to a different plugin configuration.
The second method is a bit more complicated, but makes it easier to switch between different plugin configurations.


The following methods apply to all Hydra plugins. In the following examples, we will configure a imaginary Launcher plugin
`MoonLauncher`. The Launcher has two modes: `falcon9`, which actually launches the application to the Moon and 
`sim` which simulates a launch.

The config schema for MoonLauncher looks like:



<div className="row">
<div className="col col--6">

```python
@dataclass
class Falcon9Conf:
  ton_fuel:  int = 10




```
</div>
<div className="col  col--6">

```python
@dataclass
class Simulation:
  ton_fuel:  int = 10
  window_size:
    width: 1024
    height: 768

```
</div>
</div>



### Overriding in primary config
We can directly override Launcher config in primary config.

<div className="row">
<div className="col col--4">

```yaml title="config.yaml" 
a: 1

hydra:
  launcher:
    ton_fuel: 2









```
</div>
<div className="col col--4">

```commandline title="command-line override" 
hydra/launcher=falcon9


```
```yaml title="resulting launcher config"  {3}
hydra:
  launcher:
    ton_fuel: 2



```
</div>
<div className="col col--4">

```commandline title="command-line override" 
hydra/launcher=sim


```
```yaml title="resulting launcher config"  {3}
hydra:
  launcher:
    ton_fuel: 2
    window_size:
      width: 1024
      height: 768
```
</div>
</div>


This approach makes the assumption that the Launcher used has all the fields we are overriding.
If we wanted to override a field that exists in the Simulation Launcher but not in the Falcon9 Launcher, 
like `window_size.width`, we would no longer be able to use the Falcon9 Launcher! The next section solves this problem.

### Extending plugin default config

This section assumes that you are familiar with the contents of [Common Patterns/Extending Configs](patterns/extending_configs.md).

Extending plugin default config has several advantages:
- Separate configuration concerns, keep primary config clean.
- Easier to switch between different plugin configurations.
- Provides flexibility when a Plugin has different modes
that requires different schema.


Say that we want to override certain values for different Launcher mode:

<div className="row">
<div className="col col--6">

```yaml title="hydra/launcher/my_falcon9.yaml" {4}
defaults:
  - falcon9

ton_fuel: 2


```
</div>
<div className="col col--6">

```yaml title="hydra/sweeper/my_sim.yaml" {5}
defaults:
  - sim

window_size:
  width: 768

```
</div>
</div>

We can easily user command-line overrides to get the configuration needed:
<div className="row">

<div className="col col--6">

```commandline title="command-line override" 
hydra/launcher=my_falcon9


```
```yaml title="resulting launcher config"  {3}
hydra:
  launcher:
    ton_fuel: 2



```
</div>
<div className="col col--6">

```commandline title="command-line override" 
hydra/launcher=my_sim


```
```yaml title="resulting launcher config"  {5}
hydra:
  launcher:
    ton_fuel: 10
    window_size:
      width: 768
      height: 768
```
</div>
</div>
