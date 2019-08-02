import logging

import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    log.info(cfg.pretty())


if __name__ == "__main__":
    experiment()
