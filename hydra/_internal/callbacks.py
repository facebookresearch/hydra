# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from omegaconf import DictConfig, OmegaConf

from hydra.core.singleton import Singleton
from hydra.types import TaskFunction

if TYPE_CHECKING:
    from hydra.core.utils import JobReturn


class CallbacksCache(metaclass=Singleton):
    """
    A singleton class to cache callbacks so they are not reinstantiated during
    compose config and start run.
    """

    @staticmethod
    def instance() -> "CallbacksCache":
        return Singleton.instance(CallbacksCache)  # type: ignore

    cache: Dict[int, "Callbacks"]

    def __init__(self) -> None:
        self.cache = {}


class Callbacks:
    callbacks: List[Any]

    def __init__(
        self, config: Optional[DictConfig] = None, check_cache: bool = True
    ) -> None:
        if config is None:
            return
        cache = CallbacksCache.instance().cache
        if check_cache:
            cached_callback = cache.get(id(config))
            if cached_callback is not None:
                self.callbacks = cached_callback.callbacks
                return

        self.callbacks = []
        from hydra.utils import instantiate

        if config is not None and OmegaConf.select(config, "hydra.callbacks"):
            for params in config.hydra.callbacks.values():
                self.callbacks.append(instantiate(params))
        cache[id(config)] = self

    def _notify(self, function_name: str, reverse: bool = False, **kwargs: Any) -> None:
        callbacks = reversed(self.callbacks) if reverse else self.callbacks
        for c in callbacks:
            try:
                getattr(c, function_name)(**kwargs)
            except Exception as e:
                warnings.warn(
                    f"Callback {type(c).__name__}.{function_name} raised {type(e).__name__}: {e}"
                )

    def on_run_start(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_run_start", config=config, **kwargs)

    def on_run_end(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_run_end", config=config, reverse=True, **kwargs)

    def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(function_name="on_multirun_start", config=config, **kwargs)

    def on_multirun_end(self, config: DictConfig, **kwargs: Any) -> None:
        self._notify(
            function_name="on_multirun_end", reverse=True, config=config, **kwargs
        )

    def on_job_start(
        self, config: DictConfig, *, task_function: TaskFunction, **kwargs: Any
    ) -> None:
        self._notify(
            function_name="on_job_start",
            config=config,
            task_function=task_function,
            **kwargs,
        )

    def on_job_end(
        self, config: DictConfig, job_return: "JobReturn", **kwargs: Any
    ) -> None:
        self._notify(
            function_name="on_job_end",
            config=config,
            job_return=job_return,
            reverse=True,
            **kwargs,
        )

    def on_compose_config(
        self,
        config: DictConfig,
        config_name: Optional[str],
        overrides: List[str],
    ) -> None:
        self._notify(
            function_name="on_compose_config",
            config=config,
            config_name=config_name,
            overrides=overrides,
        )
