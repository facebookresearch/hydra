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

1. Modify the `config_name` in the `@hydra.main` decorator of your application.
   1.To fetch a config file, one way is to  modify the `config_name` in the `@hydra.main` decorator of your application should be a logical path to a config within the domain passed to your SearchPathPlugin.

1. Your config file can contain a [defaults list](https://hydra.cc/docs/next/tutorials/basic/your_first_app/defaults) to select defaults for config groups. To use a defaults list in your config, import the [`configerator/source/fair_infra/hydra_plugins/configerator_config_source/defults`](https://fburl.com/diffusion/xhmy4bwc) thrift structure and specify a default_dict (for defaults in config groups) and/or default_string (for default configs)
- When the application is run, the configs specified in the defaults list are loaded by default.
- For example, [`config.cconf`](https://fburl.com/diffusion/tm9qbpm8) imports the `hydra_configerator_config_default` thrift to create the defaults list, with [`mysql`](https://fburl.com/diffusion/cxgennae) as the default for the [`db`](https://fburl.com/diffusion/99i3uxpu) config group

### Example:

An example [application](https://fburl.com/diffusion/pndzq58m) using the ConfigeratorConfigSource plugin and example [SearchPathPlugin](https://fburl.com/diffusion/j86krh3r) are provided. The example app has the decorator `@hydra.main(config_name=…)`, where config_name specifies the path to the configs that will be loaded and printed.

To run the app, run `buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example:my_app` from the fbsource/fbcode directory.
