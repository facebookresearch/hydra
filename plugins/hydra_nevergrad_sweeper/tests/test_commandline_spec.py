# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import asdict

import pytest  # type: ignore
from hydra.core.override_parser.types import Override

from hydra_plugins.hydra_nevergrad_sweeper.core import CommandlineSpec
from tests import get_choice_sweep, get_range_sweep


@pytest.mark.parametrize(  # type: ignore
    "string,expected",
    [
        # choice(blu, blublu)
        (
            get_choice_sweep(["blu", "blublu"]),
            CommandlineSpec(options=["blu", "blublu"]),
        ),
        # choice(0, 1, 2)
        (get_choice_sweep([0, 1, 2]), CommandlineSpec(options=[0, 1, 2]),),
        (
            get_choice_sweep([0.0, 12.0, 2.0]),
            CommandlineSpec(options=[0.0, 12.0, 2.0]),
        ),
        (get_choice_sweep(["0", "1", "2"]), CommandlineSpec(options=["0", "1", "2"]),),
        (get_range_sweep(start=1, stop=12), CommandlineSpec(bounds=(1, 12)),),
        # tag(log, range(0.01. 1.0))
        (
            get_range_sweep(tags={"log"}, start=0.01, stop=1.0),
            CommandlineSpec(bounds=(0.01, 1.0), log=True),
        ),
        # tag(log, step, range(1, 12, 3))
        (
            get_range_sweep(tags={"log", "step"}, start=1, stop=12, step=3),
            CommandlineSpec(bounds=(1, 12), step=3.0, log=True),
        ),
    ],
)
def test_commandline_spec_parse(string: Override, expected: CommandlineSpec) -> None:
    param = CommandlineSpec.parse(string)
    for attr, value in asdict(expected).items():
        assert getattr(param, attr) == value, f"Wrong value for {attr}"
    # the following equality fails for unknown reasons (only if running all tests)
    # assert param == expected
