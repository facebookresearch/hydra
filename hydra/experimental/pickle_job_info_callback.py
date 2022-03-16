# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging
import pickle
from pathlib import Path
from typing import Any

from omegaconf import DictConfig

from hydra.core.utils import JobReturn
from hydra.experimental.callback import Callback

log = logging.getLogger(__name__)


class PickleJobInfoCallback(Callback):
    output_dir: Path

    def on_job_start(self, config: DictConfig, **kwargs: Any) -> None:
        self.output_dir = Path(config.hydra.runtime.output_dir) / Path(
            config.hydra.output_subdir
        )
        filename = "config.pickle"
        self._save_pickle(obj=config, filename=filename, output_dir=self.output_dir)
        log.info(f"Saving job configs in {self.output_dir / filename}")

    def on_job_end(
        self, config: DictConfig, job_return: JobReturn, **kwargs: Any
    ) -> None:
        filename = "job_return.pickle"
        self._save_pickle(obj=job_return, filename=filename, output_dir=self.output_dir)
        log.info(f"Saving job_return in {self.output_dir / filename}")

    def _save_pickle(self, obj: Any, filename: str, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        assert output_dir is not None
        with open(str(output_dir / filename), "wb") as file:
            pickle.dump(obj, file, protocol=4)
