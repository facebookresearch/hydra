# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="conf")
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
