# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, List

from hydra.core.override_parser.types import (
    ChoiceSweep,
    Override,
    OverrideType,
    RangeSweep,
    ValueType,
)


def get_choice_sweep(val: List[Any]) -> Override:
    return Override(
        type=OverrideType.CHANGE,
        key_or_group="choice",
        value_type=ValueType.CHOICE_SWEEP,
        _value=ChoiceSweep(tags=set(), list=val, simple_form=False, shuffle=False),
    )


def get_range_sweep(**params) -> Override:
    return Override(
        type=OverrideType.CHANGE,
        key_or_group="range",
        value_type=ValueType.RANGE_SWEEP,
        _value=RangeSweep(**params),
    )


def get_override_element(val: Any) -> Override:
    return Override(
        type=OverrideType.CHANGE,
        key_or_group="test",
        value_type=ValueType.ELEMENT,
        _value=val,
    )
