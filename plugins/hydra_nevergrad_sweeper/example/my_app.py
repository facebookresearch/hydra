# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_name="config")
def dummy_training(cfg: DictConfig) -> float:
    """A dummy function to minimize
    Minimum is 0.0 at:
    lr = 0.12, dropout=0.33, db=mnist, batch_size=4
    """
    do = cfg.dropout
    bs = cfg.batch_size
    out = float(
        abs(do - 0.33) + int(cfg.db == "mnist") + abs(cfg.lr - 0.12) + abs(bs - 4)
    )
    log.info(
        f"dummy_training(dropout={do:.3f}, lr={cfg.lr:.3f}, db={cfg.db}, batch_size={bs}) = {out:.3f}",
    )
    return out


if __name__ == "__main__":
    dummy_training()
