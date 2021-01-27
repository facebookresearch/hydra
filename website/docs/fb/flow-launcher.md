---
id: flow-launcher
title: Flow Launcher
---

The Flow Launcher plugin provides a way to launch application via `flow`.

## Dependency
To use the flow launcher, add the following to your `TARGETS`
```commandline
//github/facebookresearch/hydra/plugins/hydra_flow_launcher:hydra_flow_launcher
```

## Usage
Add hydra/launcher=flow to your command line. Alternatively, override hydra/launcher in your config:
```commandline
defaults:
  - hydra/launcher: flow
```

You can discover the Launcher's config with:
```commandline
$ buck run @mode/opt  //github/facebookresearch/hydra/plugins/hydra_flow_launcher/example:my_app -- --cfg hydra -p hydra.launcher

# @package hydra.launcher
_target_: hydra_plugins.flow_launcher_plugin.flow_launcher.FlowLauncher
mode: flow
owner: ${env:USER}
entitlement: gpu_pnb_fair
pkg_version: fblearner.flow.canary:19e63cbf9945467281cf681bc8902c50
driver_path: ''
resource_requirements:
  gpu: 0
  cpu: 1
  memory: 10g
  region: null
  capabilities: []
  percent_cpu: null
run_as_secure_group: fair_research_and_engineering
retries: 2
tags: []
par_style: xar
```

You can override `resource_requirements` just like how you would via `flow-cli`.
The Launcher currently support both `par` and `xar` style. Please override `hydra.launcher.par_style` to match your application's packaging.


:::info NOTE
Flow launcher only supports `@mode/opt`.
:::

To run the example application:
```commandline
buck run @mode/opt  //github/facebookresearch/hydra/plugins/hydra_flow_launcher/example:my_app -- --multirun
```