# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(config_path=".", config_name="config")
def dummy_training(cfg: DictConfig) -> float:
    """A dummy function to minimize
    Minimum is 0.0 at:
    lr = 0.12, dropout=0.33, opt=Adam, batch_size=4
    """
    do = cfg.dropout
    bs = cfg.batch_size
    out = float(
        abs(do - 0.33) + int(cfg.opt == "Adam") + abs(cfg.lr - 0.12) + abs(bs - 4)
    )
    log.info(
        f"dummy_training(dropout={do:.3f}, lr={cfg.lr:.3f}, opt={cfg.opt}, batch_size={bs}) = {out:.3f}",
    )
    if cfg.error:
        raise RuntimeError("cfg.error is True")

    if cfg.return_type == "float":
        return out

    if cfg.return_type == "dict":
        return dict(name="objective", type="objective", value=out)

    if cfg.return_type == "list":
        return [dict(name="objective", type="objective", value=out)]

    if cfg.return_type == "none":
        return None


if __name__ == "__main__":
    dummy_training()
