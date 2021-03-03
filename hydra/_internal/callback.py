# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any

from omegaconf import DictConfig

from hydra.core.utils import JobReturn

logger = logging.getLogger(__name__)


class Callback:
    def on_run_start(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        ...

    def on_run_end(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        ...

    def on_multirun_start(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        ...

    def on_multirun_end(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        ...

    def on_job_start(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        ...

    def on_job_end(
        self,
        config: DictConfig,
        job_return: JobReturn,
        **kwargs: Any,
    ) -> None:
        ...
