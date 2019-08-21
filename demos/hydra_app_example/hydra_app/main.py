#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra


@hydra.main(config_path="config.yaml")
def main(cfg):
    print(cfg.pretty())


# this function is required to allow automatic detection of the module name when running
# from a binary script.
def entry():
    main()


if __name__ == "__main__":
    main()
