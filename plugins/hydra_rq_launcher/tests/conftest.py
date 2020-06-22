# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest  # type: ignore


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    # Tests use fake redis server by setting REDIS_MOCK to True
    monkeypatch.setenv("REDIS_MOCK", "True")
