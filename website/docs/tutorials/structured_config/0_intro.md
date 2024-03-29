---
id: intro
title: Introduction to Structured Configs
sidebar_label: Introduction to Structured Configs
---

import GithubLink from "@site/src/components/GithubLink"

This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the [Basic Tutorial](/tutorials/basic/your_first_app/1_simple_cli.md).
The examples in this tutorial are available <GithubLink to="examples/tutorials/structured_configs">here</GithubLink>.

Structured Configs use Python [dataclasses](https://docs.python.org/3.8/library/dataclasses.html) to 
describe your configuration structure and types. They enable:

* **Runtime type checking** as you compose or mutate your config 
* **Static type checking** when using static type checkers (mypy, PyCharm, etc.)

#### Structured Configs supports:
- Primitive types (`int`, `bool`, `float`, `str`, `Enums`, `bytes`, `pathlib.Path`) 
- Nesting of Structured Configs
- Containers (List and Dict) containing primitives, Structured Configs, or other lists/dicts
- Optional fields

#### Structured Configs Limitations:
- `Union` types are only partially supported (see [OmegaConf docs on unions](https://omegaconf.readthedocs.io/en/latest/structured_config.html#union-types))
- User methods are not supported

See the [OmegaConf docs on Structured Configs](https://omegaconf.readthedocs.io/en/latest/structured_config.html) for more details.

#### There are two primary patterns for using Structured configs with Hydra

- As a [config](/tutorials/structured_config/1_minimal_example.md), in place of configuration files (often a starting place)
- As a [config schema](/tutorials/structured_config/5_schema.md) validating configuration files (better for complex use cases)

With both patterns, you still get everything Hydra has to offer (config composition, Command line overrides etc).
This tutorial covers both. \***Read it in order**\*.

Hydra supports OmegaConf's Structured Configs via the `ConfigStore` API.
This tutorial does not assume any knowledge of them.
It is recommended that you visit the <a class="external" href="https://omegaconf.readthedocs.io/en/latest/structured_config.html" target="_blank">OmegaConf Structured Configs page</a> to learn more later.
