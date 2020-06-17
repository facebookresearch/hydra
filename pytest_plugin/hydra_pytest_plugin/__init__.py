# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# Source of truth for version
__version__ = "1.0.0rc1"
import copy
from typing import Any, Callable, Optional

import pytest

from hydra.core.singleton import Singleton
from hydra.test_utils.test_utils import GlobalHydraContext


@pytest.fixture(scope="function")  # type: ignore
def hydra_restore_singletons() -> None:
    """
    Restore singletons state after the function returns
    """
    state = copy.deepcopy(Singleton.get_state())
    yield
    Singleton.set_state(state)


@pytest.fixture(scope="function")  # type: ignore
def hydra_global_context() -> Callable[
    [str, Optional[str], Optional[bool]], GlobalHydraContext
]:
    def _(
        task_name: str = "task",
        config_dir: Optional[str] = None,
        strict: Optional[bool] = None,
    ) -> Any:
        ctx = GlobalHydraContext()
        ctx.task_name = task_name
        ctx.config_dir = config_dir
        ctx.strict = strict
        return ctx

    return _
