# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import time

import hydra


@hydra.main(config_path="conf/config.yaml")
def my_app(cfg):
    print(f"Executing task {cfg.task} ...")
    time.sleep(1)


if __name__ == "__main__":
    my_app()
