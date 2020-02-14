---
id: schema
title: Structured config as schema
---
We have seen how to use Structured configs as configuration, but they can also be used as a schema validating configuration files!

We have seeb the `ConfigStore` class already. There is another similar store called `SchemaStore`.
Schema store is used to store configuration shcmeas. when a config is loaded by Hydra, a schema with an identical name
is automatically looked up in the `SchemaStore`, and if found - is loaded and act as a schema for the newly loaded config.


