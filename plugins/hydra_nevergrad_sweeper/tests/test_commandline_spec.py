# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import asdict

import pytest  # type: ignore

from hydra_plugins.hydra_nevergrad_sweeper.core import CommandlineSpec


@pytest.mark.parametrize(  # type: ignore
    "string,expected",
    [
        ("blu,blublu", CommandlineSpec(options=["blu", "blublu"], cast="str")),
        ("0,1,2", CommandlineSpec(options=["0", "1", "2"], cast="float")),
        ("str:0,1,2", CommandlineSpec(options=["0", "1", "2"], cast="str")),
        (
            "0.0,12.0,2.0",
            CommandlineSpec(options=["0.0", "12.0", "2.0"], cast="float"),
        ),
        ("int:1:12", CommandlineSpec(bounds=(1.0, 12.0), cast="int")),
        ("1:12", CommandlineSpec(bounds=(1.0, 12.0), cast="float")),
        ("log:0.01:1.0", CommandlineSpec(bounds=(0.01, 1.0), cast="float", log=True),),
        (
            "int:log:1:1200",
            CommandlineSpec(bounds=(1.0, 1200.0), cast="int", log=True),
        ),
    ],
)
def test_commandline_spec_parse(string: str, expected: CommandlineSpec) -> None:
    param = CommandlineSpec.parse(string)
    for attr, value in asdict(expected).items():
        assert getattr(param, attr) == value, f"Wrong value for {attr}"
    # the following equality fails for unknown reasons (only if running all tests)
    # assert param == expected
