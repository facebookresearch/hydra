# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, List

from hydra.core.override_parser.types import (
    Override,
    OverrideType,
    ValueType,
    ChoiceSweep,
)


def get_override_sweep(val: List[Any]) -> Override:
    return Override(
        type=OverrideType.CHANGE,
        key_or_group="test",
        value_type=ValueType.CHOICE_SWEEP,
        _value=ChoiceSweep(tags=set(), list=val, simple_form=False, shuffle=False),
    )


def get_override_element(val: Any) -> Override:
    return Override(
        type=OverrideType.CHANGE,
        key_or_group="test",
        value_type=ValueType.ELEMENT,
        _value=val,
    )
