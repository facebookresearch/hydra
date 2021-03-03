# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from pytest import fixture


@fixture(autouse=True)
def env_setup(monkeypatch: Any) -> None:
    # Tests use fake redis server by setting REDIS_MOCK to True
    monkeypatch.setenv("REDIS_MOCK", "True")
