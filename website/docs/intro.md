---
id: doc1
title: Introduction
sidebar_label: Introduction
---
# Introduction
Hydra is an experimentation framework, this means it can help write
flexible code before you are sure what exactly you want to be doing.
It is particularly well suited for research code, but is generic enough that it would 
fit many other use cases.

## Hydra's main features
* Dynamically composes a configuration from your own configuration primitives 
* Tweaking the composed configuration using arbitrary command line arguments
* Manages the working directory for your runs
* Configures python logger for your experiments
* Provides an ability to sweep on multiple dimensions from the command line
* A unified interface to run experiments locally or remotely

## Plugins
Hydra has a plugins architecture, allowing extending it to integrate with various systems without pulling 
in unnecessary dependencies into the core framework.

The following plugins are implemented: 
### Launchers
* hydra-submitit: A plugin that allow launching jobs to a cluster using (Submitit)[https://github.com/fairinternal/submitit]
* hydra-fairtask: A plugin that allow launching jobs to a cluster using (Fairtask)[https://github.com/fairinternal/fairtask]

