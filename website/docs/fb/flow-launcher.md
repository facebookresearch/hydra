---
id: flow-launcher
title: Flow Launcher
---

The Flow Launcher plugin provides a way to launch application via `flow`.

## Dependency
To use the Flow Launcher, add the following to your `TARGETS`
```commandline
//github/facebookresearch/hydra/plugins/hydra_flow_launcher:hydra_flow_launcher
```

## Usage
Add hydra/launcher=flow to your command line. Alternatively, override hydra/launcher in your config:
```commandline
defaults:
  - hydra/launcher: flow
```

<details>
  <summary>Discover Flow Launcher's config</summary>

  ```yaml title="$ buck run @mode/opt  //path:my_app -- --cfg hydra -p hydra.launcher"

  # @package hydra.launcher
  _target_: hydra_plugins.flow_launcher_plugin.flow_launcher.FlowLauncher
  mode: flow
  owner: ${oc.env:USER}
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
  ```
</details>



The Launcher currently support both `par` and `xar` style. You can override `resource_requirements` just like how you would via `flow-cli`.


:::info NOTE
Flow launcher only supports `@mode/opt`.
:::

To run the example application:
```commandline
buck run @mode/opt  //github/facebookresearch/hydra/plugins/hydra_flow_launcher/example:my_app -- --multirun
```
