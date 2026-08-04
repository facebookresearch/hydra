# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from functools import wraps
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, NoReturn

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf


class UnpickleableModule(ModuleType):
    def __reduce__(self) -> NoReturn:
        raise TypeError("This module facade must not be serialized")


module_facade = UnpickleableModule("module_facade")


def outer_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if args or kwargs:
            raise AssertionError("The outer decorator must not run inside a job")
        return func(*args, **kwargs)

    return wrapper


@outer_decorator
@hydra.main(config_path=None)
def app(cfg: DictConfig) -> Any:
    assert module_facade.__name__ == "module_facade"
    output_dir = Path(HydraConfig.get().runtime.output_dir)
    (output_dir / "result.txt").write_text(
        f"{os.getpid()} {cfg.runtime_value}",
        encoding="utf-8",
    )
    if cfg.get("return_lambda", False):
        return lambda value: value
    return None


if __name__ == "__main__":
    OmegaConf.register_resolver(
        "runtime_test",
        lambda value: f"resolved-{value}",
    )
    app()
