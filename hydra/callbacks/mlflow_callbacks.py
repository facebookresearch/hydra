import logging
import os

from omegaconf import DictConfig

from hydra.callbacks.callbacks import Callbacks
import mlflow

log = logging.getLogger(__name__)


class MLflow(Callbacks):
    def pre_run(self, cfg: DictConfig) -> None:
        mlflow.set_tracking_uri(f"file:///{os.getcwd()}/.mlflow")
