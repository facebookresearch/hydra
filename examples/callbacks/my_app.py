# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
from omegaconf import OmegaConf, DictConfig
from example_callbacks import ExampleCallbacks
from mlflow import log_param

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    log_param( "a", 2 )


if __name__ == "__main__":
    my_app()
