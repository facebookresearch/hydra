# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="configs/completion_test/config.yaml")
def run_cli(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    run_cli()
