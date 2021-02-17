import hydra
import logging
import time

log = logging.getLogger(__name__)


@hydra.main(config_name="config")
def docker_app(cfg) -> None:
    log.info(f"Executing task {cfg.task}")
    time.sleep(1)


if __name__ == '__main__':
    docker_app()
