---
id: fbcode
title: Hydra at fbcode
---

## Differences in fbcode

### Open source plugins
#### Supported:
 - hydra_ax_sweeper
 - hydra_colorlog
 - hydra_nevergrad_sweeper
 
#### Unsupported:
 - joblib launcher: Joblib's Loki backend does not work correctly when executed from a par file.

### Facebook specified plugins
 - fbcode_defaults : Changes configuration defaults to be appropriate for fbcode (e.g: Output directories are in `fbcode/outputs` and `fbcode/multirun`)

#### TARGETS
Hydra includes buck TARGETS you can use in fbcode. In general, if there is TARGET there are two options:
1. You can depend on the TARGETS to use Hydra or a plugin.
2. The TARGETS contains a runnable example.

targets are under `github/facebookresearch/hydra`:
- [:`hydra`](https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra) : Primary target to use in most cases. Includes `hydra_oss` and the `fbcode_defaults`.
- `:hydra_oss` : Vanilla Hydra without any Facebook specific targets.
- [`plugins`](https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/plugins): Plugins that have a TARGETS file are runnable in fbcode.
- [`examples`](https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/examples): Examples that have a TARGETS file are runnable in `fbcode`. All tutorials (in [`examples/tutorials`](https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/examples)) are supported. An example TARGET file can be found [here](https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/examples/tutorials/basic/your_first_hydra_app/5_composition).