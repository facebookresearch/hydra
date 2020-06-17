# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from typing import Any, Callable, Optional

import pytest


@pytest.fixture(scope="function")  # type: ignore
def hydra_restore_singletons() -> Any:

    from hydra.core.singleton import Singleton

    """
    Restore singletons state after the function returns
    """
    state = copy.deepcopy(Singleton.get_state())
    yield
    Singleton.set_state(state)


@pytest.fixture(scope="function")  # type: ignore
def hydra_global_context() -> Callable[[str, Optional[str], Optional[bool]], Any]:
    def _(
        task_name: str = "task",
        config_dir: Optional[str] = None,
        strict: Optional[bool] = None,
    ) -> "GlobalHydraContext":
        from hydra.test_utils.test_utils import GlobalHydraContext

        ctx = GlobalHydraContext()
        ctx.task_name = task_name
        ctx.config_dir = config_dir
        ctx.strict = strict
        return ctx

    return _
