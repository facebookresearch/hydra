# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import decimal
import sys
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Set, Union

from antlr4 import TerminalNode, Token
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
ElementType = Union[
    str, int, bool, float, List[Any], Dict[str, Any], Iterable[float], Iterable[int]
]
ParsedElementType = Optional[
    Union[ElementType, QuotedString, Iterable[int], Iterable[float]]
]


@dataclass
class Sweep:
    ...


@dataclass
class ChoiceSweep(Sweep):
    # simple form: a,b,c
    # explicit form: choices(a,b,c)
    simple_form: bool
    choices: List[ParsedElementType]
    tags: Set[str] = field(default_factory=set)


@dataclass
class RangeSweep(Sweep):
    """
    Discrete range of numbers
    """

    start: Union[int, float]
    stop: Union[int, float]
    step: Union[int, float] = 1
    tags: Set[str] = field(default_factory=set)


@dataclass
class IntervalSweep(Sweep):
    start: float
    end: float
    tags: Set[str] = field(default_factory=set)


def float_range(start: float, stop: float, step: float) -> Iterable[float]:
    dstart = decimal.Decimal(start)
    dstop = decimal.Decimal(stop)
    dstep = decimal.Decimal(step)
    if step > 0:
        while dstart < dstop:
            yield float(dstart)
            dstart += dstep
    elif step < 0:
        while dstart > dstop:
            yield float(dstart)
            dstart += dstep
    else:
        raise HydraException(
            f"Invalid range values (start:{start}, stop:{stop}, step:{step})"
        )


@dataclass
class Key:
    # the config-group or config dot-path
    key_or_group: str
    pkg1: Optional[str] = None
    pkg2: Optional[str] = None


@dataclass
class Override:
    # The type of the override (Change, Add or Remove config option or config group choice)
    type: OverrideType

    # the config-group or config dot-path
    key_or_group: str

    # The type of the value, None if there is no value
    value_type: Optional[ValueType]

    # The parsed value (component after the =).
    # Can be a string, quoted string, int, float, bool list and dict
    _value: ParsedElementType

    # When updating a config group option, the first package
    pkg1: Optional[str] = None
    # When updating a config group, the second package (used when renaming a package)
    pkg2: Optional[str] = None

    # Optional tags, only supported for sweep overrides
    tags: Set[str] = field(default_factory=set)

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

    def value(self) -> Optional[ElementType]:
        """
        :return: the value. replaces Quoted strings by regular strings
        """
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
        assert isinstance(self._value, list)
        return [
            Override._get_value_element(Override._convert_value(x)) for x in self._value
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
    def _get_value_element(
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
                    Override._get_value_element(x, space_after_sep=space_after_sep)
                    for x in value
                ]
            )
            return "[" + s + "]"
        elif isinstance(value, dict):
            s = comma.join(
                [
                    f"{k}{colon}{Override._get_value_element(v, space_after_sep=space_after_sep)}"
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

    def get_value_element(self, space_after_sep: bool = False) -> str:
        """
        Returns a string representation of the value in this override
        (similar to the part after the = in the input string)
        :param space_after_sep: True to append space after commas and colons
        :return:
        """
        return Override._get_value_element(self._value, space_after_sep=space_after_sep)

    def is_tagged(self, tag_name: str) -> bool:
        return tag_name in self.tags

    def __repr__(self) -> str:
        return f"{self.input_line} ({type(self._value).__name__})"


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
        ret: List[ParsedElementType] = []
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
        child = ctx.getChild(0)
        if isinstance(child, OverrideParser.ListValueContext):
            ret = self.visitListValue(child)
        elif isinstance(child, OverrideParser.DictValueContext):
            ret = self.visitDictValue(child)
        elif isinstance(child, OverrideParser.PrimitiveContext):
            return self.visitPrimitive(child)
        else:
            assert False
        return ret

    def visitValue(self, ctx: OverrideParser.ValueContext) -> ParsedElementType:
        child_ret = self.visitChildren(ctx)
        if len(child_ret) == 0:
            return ""
        else:
            assert len(child_ret) == 1
            ret = child_ret[0]
            return ret  # type: ignore

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
        value: ParsedElementType
        tags: Set[str] = set()
        eq_node = next(children)
        if (
            override_type == OverrideType.DEL
            and isinstance(eq_node, TerminalNode)
            and eq_node.symbol.type == Token.EOF
        ):
            value = None
            value_type = None
        else:
            assert eq_node.symbol.text == "="
            value_node = next(children)
            value = self.visitValue(value_node)
            if isinstance(value, ChoiceSweep):
                tags = value.tags
                if value.simple_form:
                    value_type = ValueType.SIMPLE_CHOICE_SWEEP
                else:
                    value_type = ValueType.CHOICE_SWEEP
                value = value.choices
            elif isinstance(value, IntervalSweep):
                tags = value.tags
                value_type = ValueType.INTERVAL_SWEEP
            elif isinstance(value, RangeSweep):
                tags = value.tags
                value_type = ValueType.RANGE_SWEEP
                start = value.start
                stop = value.stop
                step = value.step
                if (
                    isinstance(start, int)
                    and isinstance(stop, int)
                    and (step is None or isinstance(step, int))
                ):
                    if step is not None:
                        value = range(start, stop, step)
                    else:
                        value = range(start, stop)
                else:
                    if step is not None:
                        value = float_range(start, stop, step)
                    else:
                        value = float_range(start, stop)
            else:
                value_type = ValueType.ELEMENT

        return Override(
            type=override_type,
            key_or_group=key.key_or_group,
            _value=value,
            value_type=value_type,
            pkg1=key.pkg1,
            pkg2=key.pkg2,
            tags=tags,
        )

    def is_matching_terminal(self, node: ParseTree, text: str) -> bool:
        return isinstance(node, TerminalNode) and node.getText() == text

    def visitSweep(
        self, ctx: OverrideParser.SweepContext
    ) -> Union[ChoiceSweep, RangeSweep, IntervalSweep]:
        ret = self.visitChildren(ctx)
        assert isinstance(ret, list) and len(ret) == 1
        r = ret[0]
        assert isinstance(r, (ChoiceSweep, RangeSweep, IntervalSweep))
        return r

    def visitRangeSweep(self, ctx: OverrideParser.RangeSweepContext) -> RangeSweep:
        assert self.is_matching_terminal(ctx.getChild(0), "range(")
        assert self.is_matching_terminal(ctx.getChild(2), ",")
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
        assert self.is_matching_terminal(ctx.getChild(0), "interval(")
        assert self.is_matching_terminal(ctx.getChild(2), ",")
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
            ret.append(self.visitValue(child))
        return ChoiceSweep(simple_form=True, choices=ret)

    def visitChoiceSweep(self, ctx: OverrideParser.ChoiceSweepContext) -> ChoiceSweep:
        def collect(start: int, end: int, simple_form: bool) -> ChoiceSweep:
            ret: List[ParsedElementType] = []
            for idx in range(start, end):
                child = ctx.getChild(idx)
                if isinstance(child, TerminalNode):
                    assert child.symbol.text == ","
                    continue
                if isinstance(child, OverrideParser.ElementContext):
                    ret.append(self.visitElement(child))
                else:
                    assert False
            return ChoiceSweep(choices=ret, simple_form=simple_form)

        if (
            isinstance(ctx.getChild(0), TerminalNode)
            and ctx.getChild(0).symbol.text == "choice("
        ):
            return collect(1, ctx.getChildCount() - 1, simple_form=False)
        else:
            return collect(0, ctx.getChildCount(), simple_form=True)

    def aggregateResult(self, aggregate: List[Any], nextResult: Any) -> List[Any]:
        aggregate.append(nextResult)
        return aggregate

    def visitTagList(self, ctx: OverrideParser.TagListContext) -> Set[str]:
        ret = set()

        for child in ctx.getChildren(
            predicate=lambda x: not self.is_matching_terminal(x, ",")
        ):
            ret.add(child.getText().strip())

        return ret

    def visitTaggedSweep(self, ctx: OverrideParser.TaggedSweepContext) -> Sweep:
        taglist = ctx.tagList()
        sweep = self.visitSweep(ctx.sweep())
        sweep.tags = self.visitTagList(taglist) if taglist is not None else set()
        return sweep

    def defaultResult(self) -> List[Any]:
        return []


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
