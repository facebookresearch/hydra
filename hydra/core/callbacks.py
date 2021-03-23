# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import warnings
from typing import Any, List

from omegaconf import DictConfig

from hydra._internal.callback import Callback
from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn
from hydra.utils import instantiate


class Callbacks(metaclass=Singleton):
    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "Callbacks":
        ret = Singleton.instance(Callbacks, *args, **kwargs)
        assert isinstance(ret, Callbacks)
        return ret

    def __init__(self) -> None:
        self.callbacks: List[Callback] = []

    def instantiate_callbacks(self, config: DictConfig) -> None:
        if config.hydra.callbacks is None:
            raise RuntimeError("Hydra Callbacks is not configured")

        assert len(self.callbacks) == 0, "Callbacks already instantiated."

        for params in config.hydra.callbacks.values():
            self.callbacks.append(instantiate(params))

    def _notify(
        self,
        function_name: str,
        **kwargs: Any,
    ) -> None:
        for c in self.callbacks:
            try:
                getattr(c, function_name)(**kwargs)
            except Exception as e:
                warnings.warn(
                    f"Exception occurred during {function_name} with callback {type(c).__name__}, error message: {e}"
                )

    def on_run_start(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        self._notify(
            function_name="on_run_start",
            config=config,
            **kwargs,
        )

    def on_run_end(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        self._notify(
            function_name="on_run_end",
            config=config,
            **kwargs,
        )

    def on_multirun_start(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        self._notify(
            function_name="on_multirun_start",
            config=config,
            **kwargs,
        )

    def on_multirun_end(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        self._notify(
            function_name="on_multirun_end",
            config=config,
            **kwargs,
        )

    def on_job_start(
        self,
        config: DictConfig,
        **kwargs: Any,
    ) -> None:
        self._notify(
            function_name="on_job_start",
            config=config,
            **kwargs,
        )

    def on_job_end(
        self,
        config: DictConfig,
        job_return: JobReturn,
        **kwargs: Any,
    ) -> None:
        self._notify(
            function_name="on_job_end",
            config=config,
            job_return=job_return,
            **kwargs,
        )
