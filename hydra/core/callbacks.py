# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings
from typing import Any

from omegaconf import DictConfig

from hydra.core.utils import JobReturn
from hydra.utils import instantiate


class Callbacks:
    def __init__(self, config: DictConfig) -> None:
        self.callbacks = []
        if config.hydra.callbacks is not None:
            for params in config.hydra.callbacks.values():
                self.callbacks.append(instantiate(params))

    def _notify(self, function_name: str, **kwargs: Any) -> None:
        for c in self.callbacks:
            try:
                getattr(c, function_name)(**kwargs)
            except Exception as e:
                warnings.warn(
                    f"Exception occurred during {function_name} with callback {type(c).__name__}, error message: {e}"
                )

    def on_run_start(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_run_start", config=config, **kwargs)

    def on_run_end(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_run_end", config=config, **kwargs)

    def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_multirun_start", config=config, **kwargs)

    def on_multirun_end(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_multirun_end", config=config, **kwargs)

    def on_job_start(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_job_start", config=config, **kwargs)

    def on_job_end(
        self, config: DictConfig, job_return: JobReturn, **kwargs: Any
    ) -> None:
        self._notify(
            function_name="on_job_end", config=config, job_return=job_return, **kwargs
        )
