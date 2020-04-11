import copy
from typing import Any

import pytest

from hydra.core.singleton import Singleton


@pytest.fixture(scope="function")  # type: ignore
def restore_singletons() -> Any:
    """
    A fixture to restore singletons state after this the function.
    This is useful for functions that are making a one-off change to singlestons that should not effect
    other tests
    """
    state = copy.deepcopy(Singleton.get_state())
    yield
    Singleton.set_state(state)
