# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging
from typing import Any

from omegaconf import DictConfig

from hydra.core.utils import JobReturn, JobStatus
from hydra.experimental.callback import Callback

log = logging.getLogger(__name__)


class LogJobReturnCallback(Callback):
    def on_job_end(
        self, config: DictConfig, job_return: JobReturn, **kwargs: Any
    ) -> None:
        if job_return.status == JobStatus.COMPLETED:
            log.info(f"Succeeded with return value: {job_return.return_value}")
        elif job_return.status == JobStatus.FAILED:
            log.error("", exc_info=job_return._return_value)
        else:
            log.error("Status unknown. This should never happen.")
