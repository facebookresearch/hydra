# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import asdict

import pytest

from hydra_plugins.hydra_nevergrad_sweeper.core import CommandlineSpec
from tests import get_override_sweep, get_override_element

from hydra.core.override_parser.types import Override


@pytest.mark.parametrize(  # type: ignore
    "string,expected",
    [
        (
            get_override_sweep(["blu", "blublu"]),
            CommandlineSpec(options=["blu", "blublu"], cast="str"),
        ),
        (
            get_override_sweep([0, 1, 2]),
            CommandlineSpec(options=["0", "1", "2"], cast="int"),
        ),
        (
            get_override_element("str:0,1,2"),
            CommandlineSpec(options=["0", "1", "2"], cast="str"),
        ),
        (
            get_override_sweep([0.0, 12.0, 2.0]),
            CommandlineSpec(options=["0.0", "12.0", "2.0"], cast="float"),
        ),
        (
            get_override_element("int:1:12"),
            CommandlineSpec(bounds=(1.0, 12.0), cast="int"),
        ),
        (
            get_override_element("1:12"),
            CommandlineSpec(bounds=(1.0, 12.0), cast="float"),
        ),
        (
            get_override_element("log:0.01:1.0"),
            CommandlineSpec(bounds=(0.01, 1.0), cast="float", log=True),
        ),
        (
            get_override_element("int:log:1:1200"),
            CommandlineSpec(bounds=(1.0, 1200.0), cast="int", log=True),
        ),
    ],
)
def test_commandline_spec_parse(string: Override, expected: CommandlineSpec) -> None:
    param = CommandlineSpec.parse(string)
    for attr, value in asdict(expected).items():
        assert getattr(param, attr) == value, f"Wrong value for {attr}"
    # the following equality fails for unknown reasons (only if running all tests)
    # assert param == expected
