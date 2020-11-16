import logging
import os

from omegaconf import DictConfig

from hydra.callback.callback import Callback
import mlflow

log = logging.getLogger(__name__)


class MLflow(Callback):
    def __init__(self, tracking_uri: str):
        self.tracking_uri = tracking_uri

    def _set_tracking_uri(self):
        log.info(f"Setting mlflow tracking URI to be {self.tracking_uri}")
        mlflow.set_tracking_uri(self.tracking_uri)

    def pre_sweep(self, cfg: DictConfig) -> None:
        self._set_tracking_uri()

    def pre_run(self, cfg: DictConfig) -> None:
        self._set_tracking_uri()
