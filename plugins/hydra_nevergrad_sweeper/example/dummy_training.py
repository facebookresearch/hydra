# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import hydra


log = logging.getLogger(__name__)


@hydra.main(config_path="config.yaml")
def dummy_training(cfg):
    """A dummy function to minimize
    Minimum is 0.0 at:
    lr = 0.12, dropout=0.33, db=mnist, batch_size=4
    """
    do = cfg.dropout
    bs = cfg.batch_size
    out = abs(do - 0.33) + int(cfg.db == "mnist") + abs(cfg.lr - 0.12) + abs(bs - 4)
    logging.info("dummy_training(dropout=%s, lr=%s, db=%s, batch_size=%s) = %s",
                 do, cfg.lr, cfg.db, bs, out)
    return out


if __name__ == "__main__":
    dummy_training()
