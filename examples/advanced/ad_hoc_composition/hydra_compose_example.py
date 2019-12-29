# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.experimental import compose, initialize


if __name__ == "__main__":
    # initialize the Hydra subsystem.
    # This is needed for apps that cannot have a standard @hydra.main() entry point
    initialize(config_dir="conf", strict=True)

    cfg = compose("config.yaml", overrides=["db=mysql", "db.user=${env:USER}"])
    print(cfg.pretty(resolve=True))
