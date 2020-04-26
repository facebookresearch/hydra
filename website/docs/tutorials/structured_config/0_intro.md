---
id: intro
title: Introduction to Structured Configs
sidebar_label: Introduction to Structured Configs
---
This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the [Basic Tutorial](/tutorials/basic/1_simple_cli_app.md).

Structured Configs enables the use of Python [dataclasses](https://docs.python.org/3.7/library/dataclasses.html) to 
describe your configuration structure and types. They enable:

* **Static type checking** when using static type checkers (mypy, PyCharm, etc.)
* **Runtime type checking** as you compose or mutate your config 

#### Structured Configs supports:
- Primitive types (int, bool, float, str, Enums) 
- Nesting of structured configs
- Containers (List and Dict) containing primitives or Structured Configs
- Optional fields

#### Structured Configs Limitations:
- `Union` types are not supported (except `Optional`)
- User methods are not supported

#### There are two primary patterns for using Structured configs

- As a [config](/tutorials/structured_config/2_minimal_example.md), in place of configuration files (often a starting place)
- As a [config schema](/tutorials/structured_config/6_schema.md) validating configuration files (better for complex use cases)

With both patterns, you get everything Hydra has to offer (Config composition, Command line overrides etc).
This tutorial covers both. \***Read it in order**\*.

Structured Configs are a feature of OmegaConf. This tutorial does not assume any knowledge of them.
It is recommended that you visit the <a class="external" href="https://omegaconf.readthedocs.io/en/latest/structured_config.html" target="_blank">OmegaConf Structured Configs page</a> to learn more later.

<div class="alert alert--info" role="alert">
1. The APIs and behaviors described in this tutorial are experimental and may change in a future version<br/> 
2. Structured configs are new, please report any issues<br/>
</div>
<br/>
