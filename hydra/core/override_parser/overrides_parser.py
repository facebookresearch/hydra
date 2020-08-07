# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# TODO: this is huge, break into smaller files
import sys
import warnings
from copy import copy
from dataclasses import dataclass
from enum import Enum
from random import shuffle
from typing import Any, Dict, Iterator, List, Optional, Union

from antlr4 import TerminalNode, Token
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import LexerNoViableAltException, RecognitionException
from antlr4.tree.Tree import TerminalNodeImpl

import hydra.core.override_parser.grammar_functions as grammar_functions
from hydra.core.override_parser.functions import FunctionCall, Functions
from hydra.core.override_parser.types import (
    ChoiceSweep,
    ElementType,
    IntervalSweep,
    ParsedElementType,
    Quote,
    QuotedString,
    RangeSweep,
    Sweep,
)
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

    def sweep_string_iterator(self) -> Iterator[str]:
        """
        Converts the sweep_choices from a List[ParsedElements] to a List[str] that can be used in the
        value component of overrides (the part after the =)
        """
        if self.value_type not in (
            ValueType.CHOICE_SWEEP,
            ValueType.SIMPLE_CHOICE_SWEEP,
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
        else:
            assert False

        return map(Override._get_value_element_as_str, lst)

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
    def __init__(self, functions: Functions):
        self.functions = functions

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
        return isinstance(c, TerminalNodeImpl) and c.symbol.type == OverrideLexer.WS

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
                else:
                    assert False
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

        # TODO: simplify
        children = ctx.getChildren()
        first = next(children)
        assert isinstance(first, TerminalNodeImpl) and first.symbol.text == "["
        while True:
            child = next(children)
            if isinstance(child, TerminalNodeImpl):
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
        assert isinstance(open, TerminalNodeImpl) and open.symbol.text == "{"
        first = True
        while True:
            item = next(children)
            if isinstance(item, TerminalNodeImpl):
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
        assert isinstance(ctx, OverrideParser.ElementContext)
        if ctx.function():
            return self.visitFunction(ctx.function())  # type: ignore
        elif ctx.primitive():
            return self.visitPrimitive(ctx.primitive())
        elif ctx.listValue():
            return self.visitListValue(ctx.listValue())
        elif ctx.dictValue():
            return self.visitDictValue(ctx.dictValue())
        else:
            assert False

    def visitValue(
        self, ctx: OverrideParser.ValueContext
    ) -> Union[ChoiceSweep, RangeSweep, IntervalSweep, ParsedElementType]:
        if self.is_matching_terminal(ctx, "<EOF>"):
            return ""
        if ctx.element():
            return self.visitElement(ctx.element())
        elif ctx.sweep() is not None:
            return self.visitSweep(ctx.sweep())
        assert False

    def visitOverride(self, ctx: OverrideParser.OverrideContext) -> Override:
        override_type = OverrideType.CHANGE
        children = ctx.getChildren()
        first_node = next(children)
        if isinstance(first_node, TerminalNodeImpl):
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

    def is_matching_terminal(self, node: Any, text: str) -> bool:
        return isinstance(node, TerminalNodeImpl) and node.getText() == text

    def visitSweep(
        self, ctx: OverrideParser.SweepContext
    ) -> Union[ChoiceSweep, RangeSweep, IntervalSweep]:
        if ctx.simpleChoiceSweep() is not None:
            return self.visitSimpleChoiceSweep(ctx.simpleChoiceSweep())
        assert False

    def visitSimpleChoiceSweep(
        self, ctx: OverrideParser.SimpleChoiceSweepContext
    ) -> ChoiceSweep:
        ret = []
        for child in ctx.getChildren(
            predicate=lambda x: not self.is_matching_terminal(x, ",")
        ):
            ret.append(self.visitElement(child))
        return ChoiceSweep(simple_form=True, list=ret)

    def visitFunction(self, ctx: OverrideParser.FunctionContext) -> Any:
        args = []
        kwargs = {}
        children = ctx.getChildren()
        func_name = next(children).getText()
        assert self.is_matching_terminal(next(children), "(")
        in_kwargs = False
        while True:
            cur = next(children)
            if self.is_matching_terminal(cur, ")"):
                break

            if isinstance(cur, OverrideParser.ArgNameContext):
                in_kwargs = True
                name = cur.getChild(0).getText()
                cur = next(children)
                value = self.visitElement(cur)
                kwargs[name] = value
            else:
                if self.is_matching_terminal(cur, ","):
                    continue
                if in_kwargs:
                    raise HydraException("positional argument follows keyword argument")
                value = self.visitElement(cur)
                args.append(value)

        function = FunctionCall(name=func_name, args=args, kwargs=kwargs)
        try:
            return self.functions.eval(function)
        except Exception as e:
            text = ctx.getText()
            raise HydraException(f"Error evaluating '{text}': {e}") from e


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
    functions: Functions

    @classmethod
    def create(cls) -> "OverridesParser":
        return cls(create_functions())

    def __init__(self, functions: Functions):
        self.functions = functions

    def parse_rule(self, s: str, rule_name: str) -> Any:
        error_listener = HydraErrorListener()
        istream = InputStream(s)
        lexer = OverrideLexer(istream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        stream = CommonTokenStream(lexer)
        parser = OverrideParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        visitor = CLIVisitor(self.functions)
        rule = getattr(parser, rule_name)
        tree = rule()
        ret = visitor.visit(tree)
        if isinstance(ret, Override):
            ret.input_line = s
        return ret

    def parse_override(self, s: str) -> Override:
        ret = self.parse_rule(s, "override")
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


def create_functions() -> Functions:
    functions = Functions()
    # casts
    functions.register(name="int", func=grammar_functions.cast_int)
    functions.register(name="str", func=grammar_functions.cast_str)
    functions.register(name="bool", func=grammar_functions.cast_bool)
    functions.register(name="float", func=grammar_functions.cast_float)
    # sweeps
    functions.register(name="choice", func=grammar_functions.choice)
    functions.register(name="range", func=grammar_functions.range)
    functions.register(name="interval", func=grammar_functions.interval)
    # misc
    functions.register(name="tag", func=grammar_functions.tag)
    functions.register(name="sort", func=grammar_functions.sort)
    functions.register(name="shuffle", func=grammar_functions.shuffle)
    return functions
