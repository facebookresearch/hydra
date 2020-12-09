---
id: fbcode-configerator-config-source
title: Configerator Config Source Plugin
---

The ConfigeratorConfigSource plugin makes it possible for Hydra applications to consume a domain of configs from configerator.

### Dependency

Add the following to your `TARGET` file
```commandline
//fair_infra/fbcode_hydra_plugins/configerator_config_source:configerator_config_source
```

### Usage

1. Since `configerator` does not have a client for listing configs under a path, you need to group your configs under
a `domain` for Hydra to access. 
   1. Matching the name of your domain and directory of configs is necessary for the plugin to extract information on the full config names, due to limitations from Configerator APIs
   1. For example, the config paths returned by Configerator API could look like `fair_infra/hydra_plugins/configerator_config_source/example/db/mysql`. The plugin needs to know where the directory of configs begins ([`example`](https://fburl.com/diffusion/7c0c5tig)), in order to determine the full config name (`db/mysql`). So in this case the domain should be named [`example.cconf`](https://fburl.com/diffusion/pyymoo1t)
1. Create a [SearchPathPlugin](https://hydra.cc/docs/next/advanced/search_path) to add the Configerator path to the list of search paths.
   1.The path you add in your SearchPathPlugin should be the name of your domain of configs, such as in this [example SearchPathPlugin](https://fburl.com/diffusion/ljggtux5)
   
   Note: There will be an easier way to add the Configerator path to the list of search paths, with a planned change in Hydra 1.1 to [allow configuring the search path via the config file](https://github.com/facebookresearch/hydra/issues/274).

### Example:

#### Example SearchPathPlugin
[`ConfigeratorExampleSearchPathPlugin`](https://fburl.com/diffusion/vwa82fbg) adds the example configerator domain to the search path of the example applications.

#### Reading primary config from configerator
This example reads its primary config from configerator [here](https://fburl.com/diffusion/twk3smkj) which has a default list defined.

```commandline
$ buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example/primary_config:my_app 
...
Parsing buck files: finished in 1.1 sec
...
{'driver': 'mysql', 'user': 'alau'}
```

#### Compose config with configerator
This example reads its primary config from local yaml file `primary_config.yaml` but reads config groups info from configerator.

```commandline
$ buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example/config_group:my_app -- +db=mysql
...
Parsing buck files: finished in 1.1 sec
...
{'foo': 'bar', 'driver': 'mysql', 'user': 'alau'}
```
