# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="config.yaml")
def my_app(cfg):
    print(cfg.pretty())
    return (abs(cfg.dropout - 0.5) + int(cfg.db == "mnist")) + abs(cfg.lr - 0.01) + cfg.batch_size


if __name__ == "__main__":
    my_app()
