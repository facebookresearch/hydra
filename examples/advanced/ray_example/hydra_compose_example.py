# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
from hydra.experimental import compose
import ray
import time


@ray.remote
def train(overrides, cfg):
    print(cfg.pretty())
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
