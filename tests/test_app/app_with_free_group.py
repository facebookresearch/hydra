# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="config_with_free_group/config.yaml")
def my_app(_cfg):
    print(_cfg.pretty())


if __name__ == "__main__":
    my_app()
