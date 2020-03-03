# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="config.yaml")
def dummy_training(cfg: Any) -> float:
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
        f"dummy_training(dropout={do}, lr={cfg.lr}, db={cfg.db}, batch_size={bs}) = {out}",
    )
    return out


if __name__ == "__main__":
    dummy_training()
