# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import importlib

import pytest

from hydra.experimental import compose, initialize_with_module, initialize


def test_compose1(hydra_global_context):
    with hydra_global_context():
        ret = compose(overrides=["+a=10", "+b=20"])
        assert ret == {"a": 10, "b": 20}


@pytest.mark.parametrize(
    "overrides,expected",
    [
        ([], {}),
        (["+db=mysql"], {"db": {"driver": "mysql", "user": "omry", "pass": "secret"}}),
        (
            ["+db=mysql", "db.pass=12345"],
            {"db": {"driver": "mysql", "user": "omry", "pass": 12345}},
        ),
    ],
)
def test_compose2(hydra_global_context, overrides, expected):
    with hydra_global_context(config_dir="../sample_configs"):
        ret = compose(overrides=overrides)
        assert ret == expected
