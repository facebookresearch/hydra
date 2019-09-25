# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main()
def my_app(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
