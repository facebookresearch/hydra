# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import List, Union

from hydra.core.override_parser.types import IntervalSweep, Override, Transformer

ValueType = Union[str, int, float]


@dataclass
class HPOParameter:
    name: str
    type: str
    log: bool
    values: List[ValueType]
    tags: List[str]


def create_hpo_parameter_from_override(override: Override):
    name = override.get_key_element()
    log = False
    hpo_type = None
    tags = []
    if override.is_sweep_override():
        tags = override.value().tags
        if override.is_choice_sweep():
            hpo_type = "choice"
            values = list(override.sweep_iterator(transformer=Transformer.encode))
        elif override.is_range_sweep():
            hpo_type = "range"
            values = [val for val in override.sweep_iterator()]
        elif override.is_interval_sweep():
            hpo_type = "interval"
            value = override.value()
            assert isinstance(value, IntervalSweep)
            values = [value.start, value.end]
    elif not override.is_hydra_override():
        hpo_type = "fixed"
        values = [override.value()]
    if "log" in tags:
        log = True
    if hpo_type:
        return HPOParameter(name=name, type=hpo_type, log=log, values=values, tags=tags)
    return None
