# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
from omegaconf import OmegaConf


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg):
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
