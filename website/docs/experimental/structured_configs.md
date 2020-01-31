---
id: structured_configs
title: Structured configs
sidebar_label: Structured configs
---
Structured configs are a new feature of OmegaConf allow configuration to be defined through Python code.
Those configuration objects are the same as those defined through config files, with one important difference:
Structured configs are strongly typed, this typing can be used by static type checkers like Mypy or PyCharm, but OmegaConf 
goes further and extend the type safety to runtime modifications.
This covers config composition and override, and can help you catch configuration mistakes much earlier.


<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
Structured configs are a new feature with significant surface area. Please report any difficulties or issues you are running into.
Struc
</div>
<br/>

Spend some time reading about the features of [structured config](https://omegaconf.readthedocs.io/en/latest/structured_config.html) in the OmegaConf documentation.

TODO: additional documentation.


