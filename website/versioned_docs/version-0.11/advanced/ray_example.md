---
id: ray_example
title: Ray example
sidebar_label: Ray example
---

[Ray](https://github.com/ray-project/ray) is a framework for building and running distributed applications.
Hydra can be used with Ray to configure Ray itself as well as complex remote calls through the compose API.
A future plugin will enable launching to Ray clusters directly from the command line.

```python
import hydra
from hydra.experimental import compose
import ray
import time
from omegaconf import OmegaConf

@ray.remote
def train(overrides, cfg):
    print(OmegaConf.to_yaml(cfg))
    time.sleep(5)
    return overrides, 0.9


@hydra.main(config_path="conf/config.yaml")
def main(cfg):
    ray.init(**cfg.ray.init)

    results = []
    for model in ["alexnet", "resnet"]:
        for dataset in ["cifar10", "imagenet"]:
            overrides = [f"dataset={dataset}", f"model={model}"]
            run_cfg = compose(overrides=overrides)
            ret = train.remote(overrides, run_cfg)
            results.append(ret)

    for overrides, score in ray.get(results):
        print(f"Result from {overrides} : {score}")


if __name__ == "__main__":
    main()
```

Output:
```yaml
(pid=11571) dataset:
(pid=11571)   name: cifar10
(pid=11571)   path: /datasets/cifar10
(pid=11571) model:
(pid=11571)   num_layers: 7
(pid=11571)   type: alexnet
(pid=11571) 
(pid=11572) dataset:
(pid=11572)   name: imagenet
(pid=11572)   path: /datasets/imagenet
(pid=11572) model:
(pid=11572)   num_layers: 7
(pid=11572)   type: alexnet
(pid=11572) 
(pid=11573) dataset:
(pid=11573)   name: cifar10
(pid=11573)   path: /datasets/cifar10
(pid=11573) model:
(pid=11573)   num_layers: 50
(pid=11573)   type: resnet
(pid=11573)   width: 10
(pid=11573) 
(pid=11574) dataset:
(pid=11574)   name: imagenet
(pid=11574)   path: /datasets/imagenet
(pid=11574) model:
(pid=11574)   num_layers: 50
(pid=11574)   type: resnet
(pid=11574)   width: 10
(pid=11574) 
Result from ['dataset=cifar10', 'model=alexnet'] : 0.9
Result from ['dataset=imagenet', 'model=alexnet'] : 0.9
Result from ['dataset=cifar10', 'model=resnet'] : 0.9
Result from ['dataset=imagenet', 'model=resnet'] : 0.9
```