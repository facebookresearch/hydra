# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any, Dict

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


def lr_constraint_fn(
    parameterization: Dict[str, Any],
    /,
    *,
    max_lr: int,
) -> bool:
    """This function is used to prune experiments for nevergrad sweepers. Returns
    False if the experiment should be pruned, True otherwise.
    """

    return parameterization["lr"] < max_lr


@hydra.main(version_base=None, config_path=".", config_name="config")
def dummy_training(cfg: DictConfig) -> float:
    """A dummy function to minimize
    Minimum is 0.0 at:
    lr = 0.12, dropout=0.33, db=mnist, batch_size=4
    """
    print(cfg.arr)
    print(sum(cfg.arr))
    do = cfg.dropout
    bs = cfg.batch_size
    out = float(
        abs(do - 0.33)
        + int(cfg.db == "mnist")
        + abs(cfg.lr - 0.12)
        + abs(bs - 4)
        + sum(cfg.arr)
    )
    log.info(
        f"dummy_training(dropout={do:.3f}, lr={cfg.lr:.3f}, db={cfg.db}, batch_size={bs}, arr={cfg.arr}) = {out:.3f}",
    )
    if cfg.error:
        raise RuntimeError("cfg.error is True")
    return out


if __name__ == "__main__":
    dummy_training()
