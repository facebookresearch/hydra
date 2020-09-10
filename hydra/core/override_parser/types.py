# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import decimal
import fnmatch
from copy import copy
from dataclasses import dataclass, field
from enum import Enum
from random import shuffle
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Union, cast

from omegaconf import OmegaConf
from omegaconf._utils import is_structured_config

from hydra.core.config_loader import ConfigLoader
from hydra.core.object_type import ObjectType
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
        else:
            assert False
        return f"{q}{text}{q}"


@dataclass
class Sweep:
    tags: Set[str] = field(default_factory=set)


@dataclass
class ChoiceSweep(Sweep):
    # simple form: a,b,c
    # explicit form: choices(a,b,c)
    list: List["ParsedElementType"] = field(default_factory=list)
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

    start: Optional[Union[int, float]] = None
    stop: Optional[Union[int, float]] = None
    step: Union[int, float] = 1

    shuffle: bool = False

    def range(self) -> Union[range, FloatRange]:
        assert self.start is not None
        assert self.stop is not None

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
            return FloatRange(start, stop, step)


@dataclass
class IntervalSweep(Sweep):
    start: Optional[float] = None
    end: Optional[float] = None

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, IntervalSweep):
            eq = (
                self.start == other.start
                and self.end == other.end
                and self.tags == other.tags
            )

            st = type(self.start)
            ost = type(other.start)
            et = type(self.end)
            ose = type(other.end)
            eq = eq and st == ost and et is ose
            return eq
        else:
            return NotImplemented


# Ideally we would use List[ElementType] and Dict[str, ElementType] but Python does not seem
# to support recursive type definitions.
ElementType = Union[str, int, float, bool, List[Any], Dict[str, Any]]
ParsedElementType = Optional[Union[ElementType, QuotedString]]
TransformerType = Callable[[ParsedElementType], Any]


class OverrideType(Enum):
    CHANGE = 1
    ADD = 2
    DEL = 3


class ValueType(Enum):
    ELEMENT = 1
    CHOICE_SWEEP = 2
    GLOB_CHOICE_SWEEP = 3
    SIMPLE_CHOICE_SWEEP = 4
    RANGE_SWEEP = 5
    INTERVAL_SWEEP = 6


@dataclass
class Key:
    # the config-group or config dot-path
    key_or_group: str
    pkg1: Optional[str] = None
    pkg2: Optional[str] = None


@dataclass
class Glob:
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)

    def filter(self, names: List[str]) -> List[str]:
        def match(s: str, globs: List[str]) -> bool:
            for g in globs:
                if fnmatch.fnmatch(s, g):
                    return True
            return False

        res = []
        for name in names:
            if match(name, self.include) and not match(name, self.exclude):
                res.append(name)

        return res


class Transformer:
    @staticmethod
    def identity(x: ParsedElementType) -> ParsedElementType:
        return x

    @staticmethod
    def str(x: ParsedElementType) -> str:
        return Override._get_value_element_as_str(x)

    @staticmethod
    def encode(x: ParsedElementType) -> ParsedElementType:
        # use identity transformation for the primitive types
        # and str transformation for others
        if isinstance(x, (str, int, float, bool)):
            return x
        return Transformer.str(x)


@dataclass
class Override:
    # The type of the override (Change, Add or Remove config option or config group choice)
    type: OverrideType

    # the config-group or config dot-path
    key_or_group: str

    # The type of the value, None if there is no value
    value_type: Optional[ValueType]

    # The parsed value (component after the =).
    _value: Union[ParsedElementType, ChoiceSweep, RangeSweep, IntervalSweep]

    # When updating a config group option, the first package
    pkg1: Optional[str] = None
    # When updating a config group, the second package (used when renaming a package)
    pkg2: Optional[str] = None

    # Input line used to construct this
    input_line: Optional[str] = None

    # Configs repo
    config_loader: Optional[ConfigLoader] = None

    def is_delete(self) -> bool:
        """
        :return: True if this override represents a deletion of a config value or config group option
        """
        return self.type == OverrideType.DEL

    def is_add(self) -> bool:
        """
        :return: True if this override represents an addition of a config value or config group option
        """
        return self.type == OverrideType.ADD

    def get_source_package(self) -> Optional[str]:
        return self.pkg1

    def get_subject_package(self) -> Optional[str]:
        return self.pkg1 if self.pkg2 is None else self.pkg2

    @staticmethod
    def _convert_value(value: ParsedElementType) -> Optional[ElementType]:
        if isinstance(value, list):
            return [Override._convert_value(x) for x in value]
        elif isinstance(value, dict):
            return {k: Override._convert_value(v) for k, v in value.items()}
        elif isinstance(value, QuotedString):
            return value.text
        else:
            return value

    def value(
        self,
    ) -> Optional[Union[ElementType, ChoiceSweep, RangeSweep, IntervalSweep]]:
        """
        :return: the value. replaces Quoted strings by regular strings
        """
        if isinstance(self._value, Sweep):
            return self._value
        else:
            return Override._convert_value(self._value)

    def sweep_iterator(
        self, transformer: TransformerType = Transformer.identity
    ) -> Iterator[ElementType]:
        """
        Converts CHOICE_SWEEP, SIMPLE_CHOICE_SWEEP, GLOB_CHOICE_SWEEP and
        RANGE_SWEEP to a List[Elements] that can be used in the value component
        of overrides (the part after the =). A transformer may be provided for
        converting each element to support the needs of different sweepers
        """
        if self.value_type not in (
            ValueType.CHOICE_SWEEP,
            ValueType.SIMPLE_CHOICE_SWEEP,
            ValueType.GLOB_CHOICE_SWEEP,
            ValueType.RANGE_SWEEP,
        ):
            raise HydraException(
                f"Can only enumerate CHOICE and RANGE sweeps, type is {self.value_type}"
            )

        lst: Any
        if isinstance(self._value, list):
            lst = self._value
        elif isinstance(self._value, ChoiceSweep):
            if self._value.shuffle:
                lst = copy(self._value.list)
                shuffle(lst)
            else:
                lst = self._value.list
        elif isinstance(self._value, RangeSweep):
            if self._value.shuffle:
                lst = list(self._value.range())
                shuffle(lst)
                lst = iter(lst)
            else:
                lst = self._value.range()
        elif isinstance(self._value, Glob):
            if self.config_loader is None:
                raise HydraException("ConfigLoader is not set")

            ret = self.config_loader.get_group_options(
                self.key_or_group, results_filter=ObjectType.CONFIG
            )
            return iter(self._value.filter(ret))
        else:
            assert False

        return map(transformer, lst)

    def sweep_string_iterator(self) -> Iterator[str]:
        """
        Converts CHOICE_SWEEP, SIMPLE_CHOICE_SWEEP, GLOB_CHOICE_SWEEP and RANGE_SWEEP
        to a List of strings that can be used in the value component of overrides (the
        part after the =)
        """
        iterator = cast(Iterator[str], self.sweep_iterator(transformer=Transformer.str))
        return iterator

    def get_source_item(self) -> str:
        pkg = self.get_source_package()
        if pkg is None:
            return self.key_or_group
        else:
            return f"{self.key_or_group}@{pkg}"

    def is_package_rename(self) -> bool:
        return self.pkg2 is not None

    def is_sweep_override(self) -> bool:
        return self.value_type is not None and self.value_type != ValueType.ELEMENT

    def is_choice_sweep(self) -> bool:
        return self.value_type in (
            ValueType.SIMPLE_CHOICE_SWEEP,
            ValueType.CHOICE_SWEEP,
            ValueType.GLOB_CHOICE_SWEEP,
        )

    def is_discrete_sweep(self) -> bool:
        """
        :return: true if this sweep can be enumerated
        """
        return self.is_choice_sweep() or self.is_range_sweep()

    def is_range_sweep(self) -> bool:
        return self.value_type == ValueType.RANGE_SWEEP

    def is_interval_sweep(self) -> bool:
        return self.value_type == ValueType.INTERVAL_SWEEP

    def is_hydra_override(self) -> bool:
        kog = self.key_or_group
        return kog.startswith("hydra.") or kog.startswith("hydra/")

    def get_key_element(self) -> str:
        def get_key() -> str:
            if self.pkg1 is None and self.pkg2 is None:
                return self.key_or_group
            elif self.pkg1 is not None and self.pkg2 is None:
                return f"{self.key_or_group}@{self.pkg1}"
            elif self.pkg1 is None and self.pkg2 is not None:
                return f"{self.key_or_group}@:{self.pkg2}"
            else:
                return f"{self.key_or_group}@{self.pkg1}:{self.pkg2}"

        def get_prefix() -> str:
            if self.is_delete():
                return "~"
            elif self.is_add():
                return "+"
            else:
                return ""

        return f"{get_prefix()}{get_key()}"

    @staticmethod
    def _get_value_element_as_str(
        value: ParsedElementType, space_after_sep: bool = False
    ) -> str:
        # str, QuotedString, int, bool, float, List[Any], Dict[str, Any]
        comma = ", " if space_after_sep else ","
        colon = ": " if space_after_sep else ":"
        if value is None:
            return "null"
        elif isinstance(value, QuotedString):
            return value.with_quotes()
        elif isinstance(value, list):
            s = comma.join(
                [
                    Override._get_value_element_as_str(
                        x, space_after_sep=space_after_sep
                    )
                    for x in value
                ]
            )
            return "[" + s + "]"
        elif isinstance(value, dict):
            s = comma.join(
                [
                    f"{k}{colon}{Override._get_value_element_as_str(v, space_after_sep=space_after_sep)}"
                    for k, v in value.items()
                ]
            )
            return "{" + s + "}"
        elif isinstance(value, (str, int, bool, float)):
            return str(value)
        elif is_structured_config(value):
            print(value)
            return Override._get_value_element_as_str(
                OmegaConf.to_container(OmegaConf.structured(value))
            )
        else:
            assert False

    def get_value_string(self) -> str:
        """
        return the value component from the input as is (the part after the first =).
        """
        assert self.input_line is not None
        idx = self.input_line.find("=")
        if idx == -1:
            raise ValueError(f"No value component in {self.input_line}")
        else:
            return self.input_line[idx + 1 :]

    def get_value_element_as_str(self, space_after_sep: bool = False) -> str:
        """
        Returns a string representation of the value in this override
        (similar to the part after the = in the input string)
        :param space_after_sep: True to append space after commas and colons
        :return:
        """
        if isinstance(self._value, Sweep):
            # This should not be called for sweeps
            raise HydraException("Cannot convert sweep to str")
        return Override._get_value_element_as_str(
            self._value, space_after_sep=space_after_sep
        )
