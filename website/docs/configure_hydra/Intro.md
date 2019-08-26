---
id: intro
title: Overview
sidebar_label: Introduction
---

## Hydra config
Hydra is highly customizable, and is composed in the following order:

### default configuration in package
This configuration comes with the Hydra code, and it not directly changeable by the end user.

*Scope*: global, this is effecting all Hydra runs and is the first thing that is used
to compose the Hydra configuration.

### Job config (`config.yaml`)
You can configure Hydra directly through your job config.

*Scope*: Hydra application

### Command line arguments
Command line arguments can override Hydra configs.

*Scope*: Single app run

## Customization examples
### Working directories
Job output directory can be [customized](workdir) both for local and for cluster (sweep) runs.

### Logging
The default logging should be sufficient for most use cases but you can [customize](logging) 
the logging in your own project 

### Plugins
Many plugins requires configuration, see the documentation of individual plugins for more information about how to configure them.

TODO: Document plugins

