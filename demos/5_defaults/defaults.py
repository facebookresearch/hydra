import sys

import hydra


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    print("Configuration:\n{}".format(cfg.pretty()))


if __name__ == "__main__":
    sys.exit(experiment())
