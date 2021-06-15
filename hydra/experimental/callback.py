# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any

from omegaconf import DictConfig

from hydra.core.utils import JobReturn

logger = logging.getLogger(__name__)


class Callback:
    def on_run_start(self, config: DictConfig, **kwargs: Any) -> None:
        """
        Called in RUN mode before job starts.
        """
        ...

    def on_run_end(self, config: DictConfig, **kwargs: Any) -> None:
        """
        Called in RUN mode after job ends.
        """
        ...

    def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:
        """
        Called in MULTIRUN mode before any job starts.
        """
        ...

    def on_multirun_end(self, config: DictConfig, **kwargs: Any) -> None:
        """
        Called in MULTIRUN mode after all jobs end.
        """
        ...

    def on_job_start(self, config: DictConfig, **kwargs: Any) -> None:
        """
        Called in both RUN and MULTIRUN modes, once for each Hydra job (before running
        application code).
        """
        ...

    def on_job_end(
        self, config: DictConfig, job_return: JobReturn, **kwargs: Any
    ) -> None:
        """
        Called in both RUN and MULTIRUN modes, once for each Hydra job (after running
        application code).
        """
        ...
