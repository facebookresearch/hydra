# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra
from omegaconf import DictConfig
from optuna.trial import Trial


@hydra.main(config_path="custom-search-space", config_name="config")
def three_dimensional_sphere(cfg: DictConfig) -> float:
    x: float = cfg.x
    y: float = cfg.y
    z: float = cfg.z
    return x ** 2 + y ** 2 + z ** 2


def configure(cfg: DictConfig, trial: Trial) -> None:
    x_value = trial.params["x"]
    trial.suggest_float(
        "z",
        x_value - cfg.max_z_difference_from_x,
        x_value + cfg.max_z_difference_from_x,
    )


if __name__ == "__main__":
    three_dimensional_sphere()
