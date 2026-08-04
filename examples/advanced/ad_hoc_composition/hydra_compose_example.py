# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import OmegaConf

from hydra import compose, initialize

if __name__ == "__main__":
    # initialize the Hydra subsystem.
    # This is needed for apps that cannot have a standard @hydra.main() entry point
    initialize(config_path="conf")
    cfg = compose("config.yaml", overrides=["db=mysql", "db.user=${oc.env:USER}"])
    print(OmegaConf.to_yaml(cfg, resolve=True))
