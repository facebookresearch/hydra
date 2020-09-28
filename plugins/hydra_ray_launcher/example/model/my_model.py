# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)


class MyModel:
    def __init__(self, random_seed: int):
        self.random_seed = random_seed
        log.info("Init my model")

    def save(self, checkpoint_path: str) -> None:
        checkpoint_dir = Path(checkpoint_path)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        log.info(f"Created dir for checkpoints. dir={checkpoint_dir}")
        with open(checkpoint_dir / f"checkpoint_{self.random_seed}.pt", "w") as f:
            f.write(f"checkpoint@{datetime.now()}")
