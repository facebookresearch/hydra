# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union

from antlr4 import ParserRuleContext, TerminalNode, Token
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl

from hydra._internal.grammar.functions import FunctionCall, Functions
from hydra._internal.grammar.utils import _ESC_QUOTED_STR
from hydra.core.override_parser.types import (
    ChoiceSweep,
    Glob,
    IntervalSweep,
    Key,
    Override,
    OverrideType,
    ParsedElementType,
    Quote,
    QuotedString,
    RangeSweep,
    ValueType,
)
from hydra.errors import HydraException

try:
    from hydra.grammar.gen.OverrideLexer import OverrideLexer
    from hydra.grammar.gen.OverrideParser import OverrideParser
    from hydra.grammar.gen.OverrideParserVisitor import OverrideParserVisitor

except ModuleNotFoundError:
    print(
        "Error importing generated parsers, run `python setup.py antlr` to regenerate."
    )
    sys.exit(1)


class HydraOverrideVisitor(OverrideParserVisitor):  # type: ignore
    def __init__(self, functions: Functions):
        self.functions = functions

    def visitPackage(self, ctx: OverrideParser.PackageContext) -> str:
        return ctx.getText()  # type: ignore

    def visitPackageOrGroup(self, ctx: OverrideParser.PackageOrGroupContext) -> str:
        return ctx.getText()  # type: ignore

    def visitKey(self, ctx: OverrideParser.KeyContext) -> Key:
        # key : packageOrGroup (AT package)?

        nc = ctx.getChildCount()
        package = None
        if nc == 1:
            # packageOrGroup
            key = ctx.getChild(0).getText()
        elif nc > 1:
            key = ctx.getChild(0).getText()
            if ctx.getChild(1).symbol.text == "@":
                package = ctx.getChild(2).getText()
            else:
                assert False
        else:
            assert False

        return Key(key_or_group=key, package=package)

    def is_ws(self, c: Any) -> bool:
        return isinstance(c, TerminalNodeImpl) and c.symbol.type == OverrideLexer.WS

    def visitPrimitive(
        self, ctx: OverrideParser.PrimitiveContext
    ) -> Optional[Union[QuotedString, int, bool, float, str]]:
        return self._createPrimitive(ctx)

    def visitListContainer(
        self, ctx: OverrideParser.ListContainerContext
    ) -> List[ParsedElementType]:
        ret: List[ParsedElementType] = []

        idx = 0
        while True:
            element = ctx.element(idx)
            if element is None:
                break
            else:
                idx = idx + 1
                ret.append(self.visitElement(element))
        return ret

    def visitDictContainer(
        self, ctx: OverrideParser.DictContainerContext
    ) -> Dict[str, ParsedElementType]:
        assert self.is_matching_terminal(ctx.getChild(0), OverrideLexer.BRACE_OPEN)
        return dict(
            self.visitDictKeyValuePair(ctx.getChild(i))
            for i in range(1, ctx.getChildCount() - 1, 2)
        )

    def visitDictKey(self, ctx: OverrideParser.DictKeyContext) -> Any:
        return self._createPrimitive(ctx)

    def visitDictKeyValuePair(
        self, ctx: OverrideParser.DictKeyValuePairContext
    ) -> Tuple[str, ParsedElementType]:
        children = ctx.getChildren()
        item = next(children)
        assert isinstance(item, OverrideParser.DictKeyContext)
        pkey = self.visitDictKey(item)
        assert self.is_matching_terminal(next(children), OverrideLexer.COLON)
        value = next(children)
        assert isinstance(value, OverrideParser.ElementContext)
        return pkey, self.visitElement(value)

    def visitElement(self, ctx: OverrideParser.ElementContext) -> ParsedElementType:
        assert isinstance(ctx, OverrideParser.ElementContext)
        if ctx.function():
            return self.visitFunction(ctx.function())  # type: ignore
        elif ctx.primitive():
            return self.visitPrimitive(ctx.primitive())
        elif ctx.listContainer():
            return self.visitListContainer(ctx.listContainer())
        elif ctx.dictContainer():
            return self.visitDictContainer(ctx.dictContainer())
        else:
            assert False

    def visitValue(
        self, ctx: OverrideParser.ValueContext
    ) -> Union[ChoiceSweep, RangeSweep, IntervalSweep, ParsedElementType]:
        if ctx.element():
            return self.visitElement(ctx.element())
        elif ctx.simpleChoiceSweep() is not None:
            return self.visitSimpleChoiceSweep(ctx.simpleChoiceSweep())
        assert False

    def visitOverride(self, ctx: OverrideParser.OverrideContext) -> Override:
        override_type = OverrideType.CHANGE
        children = ctx.getChildren()
        first_node = next(children)
        if isinstance(first_node, TerminalNodeImpl):
            symbol_text = first_node.symbol.text
            if symbol_text == "+":
                override_type = OverrideType.ADD
                key_node = next(children)
                if self.is_matching_terminal(key_node, OverrideLexer.PLUS):
                    override_type = OverrideType.FORCE_ADD
                    key_node = next(children)

            elif symbol_text == "~":
                override_type = OverrideType.DEL
                key_node = next(children)
            else:
                assert False
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
            assert self.is_matching_terminal(eq_node, OverrideLexer.EQUAL)
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
                elif isinstance(value, Glob):
                    value_type = ValueType.GLOB_CHOICE_SWEEP
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
            package=key.package,
        )

    def is_matching_terminal(self, node: Any, symbol_type: int) -> bool:
        return isinstance(node, TerminalNodeImpl) and node.symbol.type == symbol_type

    def visitSimpleChoiceSweep(
        self, ctx: OverrideParser.SimpleChoiceSweepContext
    ) -> ChoiceSweep:
        ret = []
        for child in ctx.getChildren(
            predicate=lambda x: not self.is_matching_terminal(x, OverrideLexer.COMMA)
        ):
            ret.append(self.visitElement(child))
        return ChoiceSweep(simple_form=True, list=ret)

    def visitFunction(self, ctx: OverrideParser.FunctionContext) -> Any:
        args = []
        kwargs = {}
        children = ctx.getChildren()
        func_name = next(children).getText()
        assert self.is_matching_terminal(next(children), OverrideLexer.POPEN)
        in_kwargs = False
        while True:
            cur = next(children)
            if self.is_matching_terminal(cur, OverrideLexer.PCLOSE):
                break

            if isinstance(cur, OverrideParser.ArgNameContext):
                in_kwargs = True
                name = cur.getChild(0).getText()
                cur = next(children)
                value = self.visitElement(cur)
                kwargs[name] = value
            else:
                if self.is_matching_terminal(cur, OverrideLexer.COMMA):
                    continue
                if in_kwargs:
                    raise HydraException("positional argument follows keyword argument")
                value = self.visitElement(cur)
                args.append(value)

        function = FunctionCall(name=func_name, args=args, kwargs=kwargs)
        try:
            return self.functions.eval(function)
        except Exception as e:
            raise HydraException(
                f"{type(e).__name__} while evaluating '{ctx.getText()}': {e}"
            ) from e

    def _createPrimitive(
        self, ctx: ParserRuleContext
    ) -> Optional[Union[QuotedString, int, bool, float, str]]:
        ret: Optional[Union[int, bool, float, str]]
        first_idx = 0
        last_idx = ctx.getChildCount()
        # skip first if whitespace
        if self.is_ws(ctx.getChild(0)):
            if last_idx == 1:
                # Only whitespaces => this is not allowed.
                raise HydraException(
                    "Trying to parse a primitive that is all whitespaces"
                )
            first_idx = 1
        if self.is_ws(ctx.getChild(-1)):
            last_idx = last_idx - 1
        num = last_idx - first_idx
        if num > 1:
            # Concatenate, while un-escaping as needed.
            tokens = []
            for i, n in enumerate(ctx.getChildren()):
                if n.symbol.type == OverrideLexer.WS and (
                    i < first_idx or i >= last_idx
                ):
                    # Skip leading / trailing whitespaces.
                    continue
                tokens.append(
                    n.symbol.text[1::2]  # un-escape by skipping every other char
                    if n.symbol.type == OverrideLexer.ESC
                    else n.symbol.text
                )
            ret = "".join(tokens)
        else:
            node = ctx.getChild(first_idx)
            if node.symbol.type == OverrideLexer.QUOTED_VALUE:
                text = node.getText()
                qc = text[0]
                if qc == "'":
                    quote = Quote.single
                elif qc == '"':
                    quote = Quote.double
                else:
                    assert False
                text = self._unescape_quoted_string(text)
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
            elif node.symbol.type == OverrideLexer.ESC:
                ret = node.symbol.text[1::2]
            else:
                return node.getText()  # type: ignore
        return ret

    def _unescape_quoted_string(self, text: str) -> str:
        r"""
        Unescape a quoted string, by looking at \ that precede a quote.

        The input string should contain enclosing quotes, which are stripped away
        by this function.

        Due to the grammar definition of quoted strings, it is assumed that:
            * if there are \ preceding the closing quote, their number must be even
            * if there are \ preceding a quote in the middle of the string, their
              number must be odd

        Examples (with double quotes, but the same logic applies to single quotes):
            * "abc\"def"    -> abc"def
            * "abc\\\"def"  -> abc\"def
            * "abc\\"       -> abc\
            * "abc\\\\"     -> abc\\"
        """
        qc = text[0]  # quote character
        text = text[1:]  # remove first quote *but* keep the last one
        pattern = _ESC_QUOTED_STR[qc]
        match = pattern.search(text)

        if match is None:
            return text[0:-1]  # remove last quote

        tokens = []
        while match is not None:
            start, stop = match.span()
            # Add characters before the escaped sequence.
            tokens.append(text[0:start])
            # Un-escaping. Note that this works both for escaped quotes in the middle of
            # a string, as well as trailing backslashes where the end quote is stripped:
            #   \"    -> "  (escaped quote in the middle)
            #   \\"   -> \  (escaped trailing backslash)
            #   \\\"  -> \" (escaped backslash followed by escaped quote in the middle)
            #   \\\\" -> \\ (two escaped trailing backslashes)
            #   ...
            tokens.append(text[start + 1 : stop : 2])
            # Move on to next match.
            text = text[stop:]
            match = pattern.search(text)

        if len(text) > 1:
            # Add characters after the last match, removing the end quote.
            tokens.append(text[0:-1])

        return "".join(tokens)


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
