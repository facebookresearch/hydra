# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import decimal
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from hydra.errors import HydraException


class Quote(Enum):
    single = 0
    double = 1


@dataclass
class QuotedString:
    text: str

    quote: Quote

    def with_quotes(self) -> str:
        if self.quote == Quote.single:
            q = "'"
            text = self.text.replace("'", "\\'")
        elif self.quote == Quote.double:
            q = '"'
            text = self.text.replace('"', '\\"')
        return f"{q}{text}{q}"


@dataclass
class Sweep:
    ...


@dataclass
class ChoiceSweep(Sweep):
    # simple form: a,b,c
    # explicit form: choices(a,b,c)
    list: List["ParsedElementType"]
    tags: Set[str] = field(default_factory=set)
    simple_form: bool = False
    shuffle: bool = False


@dataclass
class FloatRange:
    start: Union[decimal.Decimal, float]
    stop: Union[decimal.Decimal, float]
    step: Union[decimal.Decimal, float]

    def __post_init__(self) -> None:
        self.start = decimal.Decimal(self.start)
        self.stop = decimal.Decimal(self.stop)
        self.step = decimal.Decimal(self.step)

    def __iter__(self) -> Any:
        return self

    def __next__(self) -> float:
        assert isinstance(self.start, decimal.Decimal)
        assert isinstance(self.stop, decimal.Decimal)
        assert isinstance(self.step, decimal.Decimal)
        if self.step > 0:
            if self.start < self.stop:
                ret = float(self.start)
                self.start += self.step
                return ret
            else:
                raise StopIteration
        elif self.step < 0:
            if self.start > self.stop:
                ret = float(self.start)
                self.start += self.step
                return ret
            else:
                raise StopIteration
        else:
            raise HydraException(
                f"Invalid range values (start:{self.start}, stop:{self.stop}, step:{self.step})"
            )


@dataclass
class RangeSweep(Sweep):
    """
    Discrete range of numbers
    """

    start: Union[int, float]
    stop: Union[int, float]
    step: Union[int, float] = 1
    tags: Set[str] = field(default_factory=set)

    shuffle: bool = False

    def range(self) -> Union[range, FloatRange]:
        start = self.start
        stop = self.stop
        step = self.step
        if (
            isinstance(start, int)
            and isinstance(stop, int)
            and (step is None or isinstance(step, int))
        ):
            return range(start, stop, step)
        else:
            if step is not None:
                return FloatRange(start, stop, step)
            else:
                return FloatRange(start, stop)


@dataclass
class IntervalSweep(Sweep):
    start: float
    end: float
    tags: Set[str] = field(default_factory=set)


# Ideally we would use List[ElementType] and Dict[str, ElementType] but Python does not seem
# to support recursive type definitions.
ElementType = Union[str, int, float, bool, List[Any], Dict[str, Any]]
ParsedElementType = Optional[Union[ElementType, QuotedString]]
