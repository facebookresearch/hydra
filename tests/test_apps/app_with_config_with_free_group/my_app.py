# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="conf/config.yaml")
def my_app(_):
    pass


if __name__ == "__main__":
    my_app()
