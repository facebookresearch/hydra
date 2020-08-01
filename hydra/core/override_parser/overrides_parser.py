# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import decimal
import sys
import warnings
from copy import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

from antlr4 import RuleContext, TerminalNode, Token
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import LexerNoViableAltException, RecognitionException
from antlr4.tree.Tree import ParseTree

from hydra.errors import HydraException, OverrideParseException

try:
    from hydra.grammar.gen.OverrideLexer import (
        CommonTokenStream,
        InputStream,
        OverrideLexer,
    )
    from hydra.grammar.gen.OverrideParser import OverrideParser
    from hydra.grammar.gen.OverrideVisitor import OverrideVisitor

except ModuleNotFoundError:
    print(
        "Error importing generated parsers, run `python setup.py antlr` to regenerate."
    )
    sys.exit(1)


class OverrideType(Enum):
    CHANGE = 1
    ADD = 2
    DEL = 3


class ValueType(Enum):
    ELEMENT = 1
    CHOICE_SWEEP = 2
    SIMPLE_CHOICE_SWEEP = 3
    RANGE_SWEEP = 4
    INTERVAL_SWEEP = 5


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


# Ideally we would use List[ElementType] and Dict[str, ElementType] but Python does not seem
# to support recursive type definitions.
ElementType = Union[str, int, bool, float, List[Any], Dict[str, Any]]
ParsedElementType = Optional[Union[ElementType, QuotedString]]


@dataclass
class Sweep:
    ...


@dataclass
class ChoiceSweep(Sweep):
    # simple form: a,b,c
    # explicit form: choices(a,b,c)
    list: List[ParsedElementType]
    tags: Set[str] = field(default_factory=set)
    simple_form: bool = False


@dataclass
class FloatRange(object):
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


class CastType(Enum):
    INT = 1
    FLOAT = 2
    BOOL = 3
    STR = 4


@dataclass
class Cast:
    CastValueType = Union[
        str,
        int,
        bool,
        float,
        List[Any],
        Dict[str, Any],
        ChoiceSweep,
        RangeSweep,
        IntervalSweep,
    ]

    cast_type: CastType
    value: CastValueType
    input_line: str

    def convert(self) -> CastValueType:
        try:
            value: Any
            if isinstance(self.value, QuotedString):
                value = self.value.text
            else:
                value = self.value
            return self._convert(value=value, cast_type=self.cast_type)
        except (ValueError, OverflowError) as e:
            raise HydraException(f"Error evaluating `{self.input_line}` : {e}") from e

    @staticmethod
    def _convert(value: CastValueType, cast_type: CastType) -> CastValueType:
        if isinstance(value, list):
            ret_list = []
            for item in value:
                ret_list.append(Cast._convert(value=item, cast_type=cast_type))
            return ret_list
        elif isinstance(value, dict):
            ret_dict: Dict[str, Any] = {}
            for key, value in value.items():
                ret_dict[key] = Cast._convert(value=value, cast_type=cast_type)
            return ret_dict
        elif isinstance(value, ChoiceSweep):
            choices = []
            for item in value.list:
                choice = Cast._convert(value=item, cast_type=cast_type)
                assert isinstance(choice, (str, int, bool, float, list, dict))
                choices.append(choice)
            return ChoiceSweep(simple_form=value.simple_form, list=list(choices))
        elif isinstance(value, IntervalSweep):
            raise HydraException(
                "Intervals are always interpreted as floating-point intervals and cannot be casted"
            )
        elif isinstance(value, RangeSweep):
            if cast_type not in (CastType.INT, CastType.FLOAT):
                raise HydraException("Range can only be casted to int or float")
            start = Cast._convert(value.start, cast_type=cast_type)
            stop = Cast._convert(value.stop, cast_type=cast_type)
            step = Cast._convert(value.step, cast_type=cast_type)
            assert isinstance(start, (int, float))
            assert isinstance(stop, (int, float))
            assert isinstance(step, (int, float))
            return RangeSweep(start=start, stop=stop, step=step)
        elif isinstance(value, QuotedString):
            value = value.text
        if cast_type == CastType.INT:
            return int(value)
        elif cast_type == CastType.FLOAT:
            return float(value)
        elif cast_type == CastType.BOOL:
            if isinstance(value, str):
                if value.lower() == "false":
                    return False
                elif value.lower() == "true":
                    return True
                else:
                    raise ValueError(f"Cannot cast '{value}' to bool")
            return bool(value)

        elif cast_type == CastType.STR:
            if isinstance(value, bool):
                return str(value).lower()
            else:
                return str(value)
        else:
            assert False


@dataclass
class Key:
    # the config-group or config dot-path
    key_or_group: str
    pkg1: Optional[str] = None
    pkg2: Optional[str] = None


@dataclass
class Ordering:
    list_or_sweep: Union[List[ParsedElementType], ChoiceSweep, RangeSweep]

    def order(self) -> Union[List[ParsedElementType], ChoiceSweep, RangeSweep]:
        raise NotImplementedError()


@dataclass
class Sort(Ordering):

    reverse: bool = False

    def order(self) -> Union[List[ParsedElementType], ChoiceSweep, RangeSweep]:
        def _sorted(lst: List[Any]) -> List[Any]:
            try:
                return sorted(lst, reverse=self.reverse)
            except TypeError as e:
                raise HydraException(f"Error sorting: {e}") from e

        if isinstance(self.list_or_sweep, ChoiceSweep):
            ret = copy(self.list_or_sweep)
            ret.list = _sorted(self.list_or_sweep.list)
            return ret
        elif isinstance(self.list_or_sweep, RangeSweep):
            assert False  # TODO
        else:
            return _sorted(self.list_or_sweep)


@dataclass
class Shuffle(Ordering):
    def order(self) -> Union[List[ParsedElementType], ChoiceSweep, RangeSweep]:
        assert False  # TODO


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

    def choices_as_strings(self) -> List[str]:
        """
        Converts the sweep_choices from a List[ParsedElements] to a List[str] that can be used in the
        value component of overrides (the part after the =)
        """
        assert self.value_type in (
            ValueType.CHOICE_SWEEP,
            ValueType.SIMPLE_CHOICE_SWEEP,
        )
        if isinstance(self._value, list):
            lst = self._value
        elif isinstance(self._value, ChoiceSweep):
            lst = self._value.list
        else:
            assert False

        return [
            Override._get_value_element_as_str(Override._convert_value(x)) for x in lst
        ]

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
        )

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


class CLIVisitor(OverrideVisitor):  # type: ignore
    def visitPackage(self, ctx: OverrideParser.PackageContext) -> str:
        return ctx.getText()  # type: ignore

    def visitPackageOrGroup(self, ctx: OverrideParser.PackageOrGroupContext) -> str:
        return ctx.getText()  # type: ignore

    def visitKey(self, ctx: OverrideParser.KeyContext) -> Key:
        # key : packageOrGroup (AT package? (COLON package)? )?;

        nc = ctx.getChildCount()
        pkg1 = None
        pkg2 = None
        if nc == 1:
            # packageOrGroup
            key = ctx.getChild(0).getText()
        elif nc > 1:
            key = ctx.getChild(0).getText()
            if ctx.getChild(1).symbol.text == "@:":
                pkg1 = None
                pkg2 = ctx.getChild(2).getText()
            elif ctx.getChild(1).symbol.text == "@":
                pkg1 = ctx.getChild(2).getText()
                if nc > 3:
                    assert ctx.getChild(3).symbol.text == ":"
                    pkg2 = ctx.getChild(4).getText()
            else:
                assert False

        else:
            assert False

        return Key(key_or_group=key, pkg1=pkg1, pkg2=pkg2)

    def is_ws(self, c: Any) -> bool:
        return isinstance(c, TerminalNode) and c.symbol.type == OverrideLexer.WS

    def visitNumber(self, ctx: OverrideParser.NumberContext) -> Union[int, float]:
        node = ctx.getChild(0)
        if self.is_ws(node):
            node = ctx.getChild(1)

        if node.symbol.type == OverrideLexer.INT:
            return int(node.symbol.text)
        elif node.symbol.type == OverrideLexer.FLOAT:
            return float(node.symbol.text)
        else:
            assert False

    def visitPrimitive(
        self, ctx: OverrideParser.PrimitiveContext
    ) -> Optional[Union[QuotedString, int, bool, float, str]]:
        ret: Optional[Union[int, bool, float, str]]

        if ctx.castPrimitive() is not None:
            cast = self.visitCastPrimitive(ctx.castPrimitive()).convert()
            assert isinstance(cast, (int, bool, float, str))
            return cast

        first_idx = 0
        last_idx = ctx.getChildCount()
        # skip first if whitespace
        if self.is_ws(ctx.getChild(0)):
            first_idx = 1
        if self.is_ws(ctx.getChild(-1)):
            last_idx = last_idx - 1
        num = last_idx - first_idx
        if num > 1:
            ret = ctx.getText().strip()
        else:
            node = ctx.getChild(first_idx)
            if node.symbol.type == OverrideLexer.QUOTED_VALUE:
                text = node.getText()
                qc = text[0]
                text = text[1:-1]
                if qc == "'":
                    quote = Quote.single
                    text = text.replace("\\'", "'")
                elif qc == '"':
                    quote = Quote.double
                    text = text.replace('\\"', '"')
                return QuotedString(text=text, quote=quote)
            elif node.symbol.type in (OverrideLexer.ID, OverrideLexer.INTERPOLATION):
                ret = node.symbol.text
            elif node.symbol.type == OverrideLexer.INT:
                ret = int(node.symbol.text)
            elif node.symbol.type == OverrideLexer.FLOAT:
                ret = float(node.symbol.text)
            elif node.symbol.type == OverrideLexer.NULL:
                ret = None
            elif node.symbol.type == OverrideLexer.BOOL:
                text = node.getText().lower()
                if text == "true":
                    ret = True
                elif text == "false":
                    ret = False
                else:
                    assert False
            else:
                return node.getText()  # type: ignore
        return ret

    def visitListValue(
        self, ctx: OverrideParser.ListValueContext
    ) -> List[ParsedElementType]:
        if ctx.sortList():
            ordered = self.visitSortList(ctx.sortList()).order()
            assert isinstance(ordered, list)
            return ordered

        if ctx.castList():
            cast = self.visitCastList(ctx.castList()).convert()
            assert isinstance(cast, list)
            return cast

        ret: List[ParsedElementType] = []

        # TODO: simplify
        children = ctx.getChildren()
        first = next(children)
        assert isinstance(first, TerminalNode) and first.symbol.text == "["
        while True:
            child = next(children)
            if isinstance(child, TerminalNode):
                if child.symbol.text == ",":
                    continue
                if child.symbol.text == "]":
                    break
            elif isinstance(child, OverrideParser.ElementContext):
                ret.append(self.visitElement(child))
            else:
                assert False
        return ret

    def visitDictValue(
        self, ctx: OverrideParser.DictValueContext
    ) -> Dict[str, ParsedElementType]:
        if ctx.castDict():
            cast = self.visitCastDict(ctx.castDict()).convert()
            assert isinstance(cast, dict)
            return cast

        ret = {}
        children = ctx.getChildren()
        open = next(children)
        assert isinstance(open, TerminalNode) and open.symbol.text == "{"
        first = True
        while True:
            item = next(children)
            if isinstance(item, TerminalNode):
                if item.symbol.text == "}":
                    break
                if not first and item.symbol.text == ",":
                    continue

            pkey = item.getText()

            sep = next(children)
            assert sep.symbol.text == ":"

            value = next(children)
            if isinstance(value, OverrideParser.ElementContext):
                ret[pkey] = self.visitElement(value)
            else:
                assert False
            first = False

        return ret

    def visitElement(self, ctx: OverrideParser.ElementContext) -> ParsedElementType:
        assert ctx.getChildCount() == 1
        ret: ParsedElementType

        if ctx.listValue() is not None:
            ret = self.visitListValue(ctx.listValue())
        elif ctx.dictValue() is not None:
            ret = self.visitDictValue(ctx.dictValue())
        elif ctx.primitive() is not None:
            return self.visitPrimitive(ctx.primitive())
        elif ctx.sort() is not None:
            sorted_element = self.visitSort(ctx.sort()).order()
            assert isinstance(
                sorted_element, (str, int, bool, float, list, dict, QuotedString)
            )
            return sorted_element
        elif ctx.cast() is not None:
            cast = self.visitCast(ctx.cast()).convert()
            assert isinstance(cast, (str, int, bool, float, list, dict, QuotedString))
            return cast
        else:
            assert False
        return ret

    def visitValue(
        self, ctx: OverrideParser.ValueContext
    ) -> Union[ChoiceSweep, RangeSweep, IntervalSweep, ParsedElementType]:
        if self.is_matching_terminal(ctx, "<EOF>"):
            return ""
        if ctx.element() is not None:
            return self.visitElement(ctx.element())
        if ctx.sweep() is not None:
            return self.visitSweep(ctx.sweep())
        assert False

    def visitOverride(self, ctx: OverrideParser.OverrideContext) -> Override:
        override_type = OverrideType.CHANGE
        children = ctx.getChildren()
        first_node = next(children)
        if isinstance(first_node, TerminalNode):
            symbol_text = first_node.symbol.text
            if symbol_text == "+":
                override_type = OverrideType.ADD
            elif symbol_text == "~":
                override_type = OverrideType.DEL
            else:
                assert False
            key_node = next(children)
        else:
            key_node = first_node

        key = self.visitKey(key_node)
        value: Union[ChoiceSweep, RangeSweep, IntervalSweep, ParsedElementType]
        eq_node = next(children)
        if (
            override_type == OverrideType.DEL
            and isinstance(eq_node, TerminalNode)
            and eq_node.symbol.type == Token.EOF
        ):
            value = None
            value_type = None
        else:
            assert self.is_matching_terminal(eq_node, "=")
            if ctx.value() is None:
                value = ""
                value_type = ValueType.ELEMENT
            else:
                value = self.visitValue(ctx.value())
                if isinstance(value, ChoiceSweep):
                    if value.simple_form:
                        value_type = ValueType.SIMPLE_CHOICE_SWEEP
                    else:
                        value_type = ValueType.CHOICE_SWEEP
                elif isinstance(value, IntervalSweep):
                    value_type = ValueType.INTERVAL_SWEEP
                elif isinstance(value, RangeSweep):
                    value_type = ValueType.RANGE_SWEEP
                else:
                    value_type = ValueType.ELEMENT

        return Override(
            type=override_type,
            key_or_group=key.key_or_group,
            _value=value,
            value_type=value_type,
            pkg1=key.pkg1,
            pkg2=key.pkg2,
        )

    def is_matching_terminal(self, node: ParseTree, text: str) -> bool:
        return isinstance(node, TerminalNode) and node.getText() == text

    def visitSweep(
        self, ctx: OverrideParser.SweepContext
    ) -> Union[ChoiceSweep, RangeSweep, IntervalSweep]:
        if ctx.simpleChoiceSweep() is not None:
            return self.visitSimpleChoiceSweep(ctx.simpleChoiceSweep())
        elif ctx.choiceSweep() is not None:
            return self.visitChoiceSweep(ctx.choiceSweep())
        elif ctx.rangeSweep() is not None:
            return self.visitRangeSweep(ctx.rangeSweep())
        elif ctx.intervalSweep() is not None:
            return self.visitIntervalSweep(ctx.intervalSweep())
        elif ctx.castSweep():
            cast = self.visitCastSweep(ctx.castSweep()).convert()
            assert isinstance(cast, (ChoiceSweep, RangeSweep, IntervalSweep))
            return cast
        elif ctx.sortSweep():
            srt = self.visitSortSweep(ctx.sortSweep()).order()
            assert isinstance(srt, (ChoiceSweep, RangeSweep, IntervalSweep))
            return srt
        assert False

    def visitRangeSweep(self, ctx: OverrideParser.RangeSweepContext) -> RangeSweep:
        if ctx.taggedRangeSweep():
            return self.visitTaggedRangeSweep(ctx.taggedRangeSweep())

        assert self.is_matching_terminal(ctx.getChild(0), "range")
        assert self.is_matching_terminal(ctx.getChild(1), "(")
        start = self.visitNumber(ctx.number(0))
        stop = self.visitNumber(ctx.number(1))
        step_ctx = ctx.number(2)
        if step_ctx is not None:
            step = self.visitNumber(step_ctx)
            return RangeSweep(start=start, stop=stop, step=step)
        else:
            return RangeSweep(start=start, stop=stop)

    def visitIntervalSweep(
        self, ctx: OverrideParser.IntervalSweepContext
    ) -> IntervalSweep:
        if ctx.taggedIntervalSweep() is not None:
            return self.visitTaggedIntervalSweep(ctx.taggedIntervalSweep())

        assert self.is_matching_terminal(ctx.getChild(0), "interval")
        start = self.visitNumber(ctx.number(0))
        end = self.visitNumber(ctx.number(1))
        return IntervalSweep(start=start, end=end)

    def visitSimpleChoiceSweep(
        self, ctx: OverrideParser.SimpleChoiceSweepContext
    ) -> ChoiceSweep:
        ret = []
        for child in ctx.getChildren(
            predicate=lambda x: not self.is_matching_terminal(x, ",")
        ):
            ret.append(self.visitElement(child))
        return ChoiceSweep(simple_form=True, list=ret)

    def visitChoiceSweep(self, ctx: OverrideParser.ChoiceSweepContext) -> ChoiceSweep:
        if ctx.taggedChoiceSweep() is not None:
            return self.visitTaggedChoiceSweep(ctx.taggedChoiceSweep())

        if ctx.element():
            return ChoiceSweep(list=[self.visitElement(ctx.element())])

        if ctx.simpleChoiceSweep() is not None:
            sweep = self.visitSimpleChoiceSweep(ctx.simpleChoiceSweep())
            sweep.simple_form = False
            return sweep

        assert False

    def visitTagList(self, ctx: OverrideParser.TagListContext) -> Set[str]:
        ret = set()
        start = 0
        stop = None
        if self.is_matching_terminal(ctx.getChild(0), "tags"):
            start = 3
            stop = -1

        for child in ctx.children[start:stop]:
            if not self.is_matching_terminal(child, ","):
                ret.add(child.getText())

        return ret

    def visitTaggedSweep(self, ctx: OverrideParser.TaggedSweepContext) -> Sweep:
        taglist = ctx.tagList()
        sweep = self.visitSweep(ctx.sweep())
        sweep.tags = self.visitTagList(taglist) if taglist is not None else set()
        return sweep

    def visitTaggedChoiceSweep(
        self, ctx: OverrideParser.TaggedChoiceSweepContext
    ) -> ChoiceSweep:
        sweep = self.visitChoiceSweep(ctx.choiceSweep())
        taglist = ctx.tagList()
        sweep.tags = self.visitTagList(taglist) if taglist is not None else set()
        return sweep

    def visitTaggedIntervalSweep(
        self, ctx: OverrideParser.TaggedIntervalSweepContext
    ) -> IntervalSweep:
        sweep = self.visitIntervalSweep(ctx.intervalSweep())
        taglist = ctx.tagList()
        sweep.tags = self.visitTagList(taglist) if taglist is not None else set()
        return sweep

    def visitTaggedRangeSweep(
        self, ctx: OverrideParser.TaggedRangeSweepContext
    ) -> RangeSweep:
        sweep = self.visitRangeSweep(ctx.rangeSweep())
        taglist = ctx.tagList()
        sweep.tags = self.visitTagList(taglist) if taglist is not None else set()
        return sweep

    def _get_cast_type(self, node: ParseTree) -> CastType:
        if self.is_matching_terminal(node, "int"):
            return CastType.INT
        elif self.is_matching_terminal(node, "float"):
            return CastType.FLOAT
        elif self.is_matching_terminal(node, "str"):
            return CastType.STR
        elif self.is_matching_terminal(node, "bool"):
            return CastType.BOOL
        else:
            assert False, f"Unexpected cast type : {node.getText()}"

    def visitCast(self, ctx: OverrideParser.CastContext) -> Cast:
        if ctx.castPrimitive():
            return self.visitCastPrimitive(ctx.castPrimitive())
        elif ctx.castList():
            return self.visitCastList(ctx.castList())
        elif ctx.castDict():
            return self.visitCastDict(ctx.castDict())
        elif ctx.castSweep() is not None:
            return self.visitCastSweep(ctx.castSweep())
        else:
            assert False

    def visitCastPrimitive(self, ctx: OverrideParser.CastPrimitiveContext) -> Cast:
        return self._cast(
            ctx, "primitive", (int, float, bool, str, QuotedString, dict, list)
        )

    def visitCastList(self, ctx: OverrideParser.CastListContext) -> Cast:
        return self._cast(ctx, "listValue", list)

    def visitCastDict(self, ctx: OverrideParser.CastDictContext) -> Cast:
        return self._cast(ctx, "dictValue", dict)

    def visitCastSweep(self, ctx: OverrideParser.CastSweepContext) -> Cast:
        return self._cast(ctx, "sweep", Sweep)

    def _cast(
        self,
        ctx: RuleContext,
        child_type: str,
        expected_types: Union[Type[Any], Tuple[Type[Any], ...]],
    ) -> Cast:
        cast_type = self._get_cast_type(ctx.getChild(0))
        node = ctx.getChild(2)
        child_type = child_type.replace(child_type[0], child_type[0].upper(), 1)
        value = getattr(self, f"visit{child_type}")(node)
        assert isinstance(value, expected_types)
        return Cast(cast_type=cast_type, value=value, input_line=ctx.getText())

    def visitSort(self, ctx: OverrideParser.SortContext) -> Sort:
        if ctx.sortList():
            return self.visitSortList(ctx.sortList())
        elif ctx.sortSweep():
            return self.visitSortSweep(ctx.sortSweep())
        else:
            assert False

    def visitSortList(self, ctx: OverrideParser.SortListContext) -> Sort:
        if self.is_matching_terminal(ctx.getChild(-4), "reverse"):
            reverse = ctx.getChild(-2).getText().lower() == "true"
        else:
            reverse = False

        if ctx.listValue():
            lst = self.visitListValue(ctx.listValue())
            return Sort(list_or_sweep=lst, reverse=reverse)
        else:
            assert False

    def visitSortSweep(self, ctx: OverrideParser.SortSweepContext) -> Sort:
        if self.is_matching_terminal(ctx.getChild(-4), "reverse"):
            reverse = ctx.getChild(-2).getText().lower() == "true"
        else:
            reverse = False

        if ctx.sweep():
            sweep = self.visitSweep(ctx.sweep())
            assert isinstance(sweep, (ChoiceSweep, RangeSweep))
            return Sort(list_or_sweep=sweep, reverse=reverse)
        else:
            assert False


class HydraErrorListener(ErrorListener):  # type: ignore
    def syntaxError(
        self,
        recognizer: Any,
        offending_symbol: Any,
        line: Any,
        column: Any,
        msg: Any,
        e: Any,
    ) -> None:
        if msg is not None:
            raise HydraException(msg) from e
        else:
            raise HydraException(str(e)) from e

    def reportAmbiguity(
        self,
        recognizer: Any,
        dfa: Any,
        startIndex: Any,
        stopIndex: Any,
        exact: Any,
        ambigAlts: Any,
        configs: Any,
    ) -> None:
        warnings.warn(
            message="reportAmbiguity: please file an issue with minimal repro instructions",
            category=UserWarning,
        )

    def reportAttemptingFullContext(
        self,
        recognizer: Any,
        dfa: Any,
        startIndex: Any,
        stopIndex: Any,
        conflictingAlts: Any,
        configs: Any,
    ) -> None:
        warnings.warn(
            message="reportAttemptingFullContext: please file an issue with a minimal repro instructions",
            category=UserWarning,
        )

    def reportContextSensitivity(
        self,
        recognizer: Any,
        dfa: Any,
        startIndex: Any,
        stopIndex: Any,
        prediction: Any,
        configs: Any,
    ) -> None:
        warnings.warn(
            message="reportContextSensitivity: please file an issue with minimal a repro instructions",
            category=UserWarning,
        )


class OverridesParser:
    @staticmethod
    def parse_rule(s: str, rule_name: str) -> Any:
        error_listener = HydraErrorListener()
        istream = InputStream(s)
        lexer = OverrideLexer(istream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        stream = CommonTokenStream(lexer)
        parser = OverrideParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        visitor = CLIVisitor()
        rule = getattr(parser, rule_name)
        tree = rule()
        ret = visitor.visit(tree)
        if isinstance(ret, Override):
            ret.input_line = s
        return ret

    def parse_override(self, s: str) -> Override:
        ret = OverridesParser.parse_rule(s, "override")
        assert isinstance(ret, Override)
        return ret

    def parse_overrides(self, overrides: List[str]) -> List[Override]:
        ret: List[Override] = []
        for override in overrides:
            try:
                parsed = self.parse_rule(override, "override")
            except HydraException as e:
                cause = e.__cause__
                if isinstance(cause, LexerNoViableAltException):
                    prefix = "LexerNoViableAltException: "
                    start = len(prefix) + cause.startIndex + 1
                    msg = f"{prefix}{override}" f"\n{'^'.rjust(start)}"
                    e.__cause__ = None
                elif isinstance(cause, RecognitionException):
                    prefix = f"{e}: "
                    offending_token: Token = cause.offendingToken
                    start = len(prefix) + offending_token.start + 1
                    msg = f"{prefix}{override}" f"\n{'^'.rjust(start)}"
                    e.__cause__ = None
                else:
                    msg = f"Error parsing override '{override}'" f"\n{e}"
                raise OverrideParseException(
                    override=override,
                    message=f"{msg}"
                    f"\nSee https://hydra.cc/docs/next/advanced/command_line_syntax for details",
                ) from e.__cause__
            assert isinstance(parsed, Override)
            ret.append(parsed)
        return ret
