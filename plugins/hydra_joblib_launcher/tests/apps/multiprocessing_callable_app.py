# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig


class CallableTask:
    def __init__(self, marker: str) -> None:
        self.marker = marker

    def __call__(self, cfg: DictConfig) -> None:
        output_dir = Path(HydraConfig.get().runtime.output_dir)
        (output_dir / "result.txt").write_text(
            f"{self.marker}-{cfg.job}",
            encoding="utf-8",
        )


app = hydra.main(version_base=None, config_path=None)(CallableTask("callable"))


if __name__ == "__main__":
    app()
