import logging
import os

from omegaconf import DictConfig

from hydra.callbacks.callbacks import Callbacks
import mlflow

log = logging.getLogger(__name__)


class MLflow(Callbacks):
    def pre_sweep(self, cfg: DictConfig) -> None:
        log.info(f"mlflow callbacks pre-sweep, setting tracking url")
        mlflow.set_tracking_uri(f"file:///{os.getcwd()}/.mlflow")
