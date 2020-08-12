# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

import pytest

from hydra._internal.core_plugins.basic_sweeper import BasicSweeper
from hydra.core.override_parser.overrides_parser import OverridesParser


@pytest.mark.parametrize(  # type:ignore
    "args,max_batch_size,expected",
    [
        pytest.param(["x=10"], None, [[["x=10"]]], id="simple"),
        pytest.param(["x=10,20"], None, [[["x=10"], ["x=20"]]], id="split_1d"),
        pytest.param(["x=[10,20]"], None, [[["x=[10,20]"]]], id="not_split_yaml_list"),
        pytest.param(
            ["x=[a,b,c],[d,e,f]"],
            None,
            [[["x=[a,b,c]"], ["x=[d,e,f]"]]],
            id="list_of_lists",
        ),
        pytest.param(
            ["a=1,2", "b=10,11"],
            None,
            [[["a=1", "b=10"], ["a=1", "b=11"], ["a=2", "b=10"], ["a=2", "b=11"]]],
            id="no_batching",
        ),
        pytest.param(
            ["a=1,2", "b=10,11"],
            1,
            [
                [["a=1", "b=10"]],
                [["a=1", "b=11"]],
                [["a=2", "b=10"]],
                [["a=2", "b=11"]],
            ],
            id="batches_of_1",
        ),
        pytest.param(
            ["a=1,2", "b=10,11"],
            2,
            [[["a=1", "b=10"], ["a=1", "b=11"]], [["a=2", "b=10"], ["a=2", "b=11"]]],
            id="batches_of_2",
        ),
        pytest.param(["a=range(0,3)"], None, [[["a=0"], ["a=1"], ["a=2"]]], id="range"),
    ],
)
def test_split(
    args: List[str], max_batch_size: Optional[int], expected: List[List[List[str]]]
) -> None:
    parser = OverridesParser.create()
    ret = BasicSweeper.split_arguments(
        parser.parse_overrides(args), max_batch_size=max_batch_size
    )
    lret = [list(x) for x in ret]
    assert lret == expected
