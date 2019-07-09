import sys

import hydra


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    sys.exit(experiment())
