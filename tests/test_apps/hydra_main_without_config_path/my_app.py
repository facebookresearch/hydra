# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig


@hydra.main()
def my_app(_: DictConfig) -> None:
    config_sources = HydraConfig.get().runtime.config_sources
    # Check that no directory has been added to the Config search path
    for source in config_sources:
        assert (
            source.schema != "file"
        ), f"Found a config source with file schema: {source}"


if __name__ == "__main__":
    my_app()
