# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
