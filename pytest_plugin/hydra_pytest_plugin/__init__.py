# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from typing import Any

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
