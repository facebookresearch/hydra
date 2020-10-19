# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import re
from builtins import isinstance
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union

import pytest
from _pytest.python_api import RaisesContext

from hydra._internal.grammar.functions import Functions
from hydra.core.override_parser.overrides_parser import (
    OverridesParser,
    create_functions,
)
from hydra.core.override_parser.types import (
    ChoiceSweep,
    FloatRange,
    Glob,
    IntervalSweep,
    Key,
    Override,
    OverrideType,
    Quote,
    QuotedString,
    RangeSweep,
    Sweep,
    Transformer,
    ValueType,
)
from hydra.errors import HydraException

parser = OverridesParser(create_functions())


def parse_rule(value: str, rule_name: str) -> Any:
    return parser.parse_rule(value, rule_name)


def eq(item1: Any, item2: Any) -> bool:
    if isinstance(item1, float) and isinstance(item2, float):
        return item1 == item2 or math.isnan(item1) and math.isnan(item2)
    else:
        return item1 == item2  # type: ignore


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc", "abc", id="value:id"),
        pytest.param("abc123", "abc123", id="value:idint"),
        pytest.param("abc-123", "abc-123", id="value:id-int"),
        pytest.param("a b c\t-\t1 2 3", "a b c\t-\t1 2 3", id="value:str-ws-in"),
        pytest.param(" abc-123 ", "abc-123", id="value:str-ws-out"),
        pytest.param("123abc", "123abc", id="value:str-int-id"),
        pytest.param(r"a\,b", "a,b", id="value:str-esc-comma"),
        pytest.param(r"a\:b", "a:b", id="value:str-esc-colon"),
        pytest.param(r"a\=b", "a=b", id="value:str-esc-equal"),
        pytest.param(r"\ ab", " ab", id="value:str-esc-space"),
        pytest.param("ab\\\t", "ab\t", id="value:str-esc-tab"),
        pytest.param("ab\\\\", "ab\\", id="value:str-esc-backslash"),
        pytest.param(r"\,", ",", id="value:str-esc-comma-alone"),
        pytest.param(r"f\(a\, b\)", "f(a, b)", id="value:str-esc-parentheses"),
        pytest.param(r"\[a\, b\]", "[a, b]", id="value:str-esc-brackets"),
        pytest.param(r"\{a\: b\}", "{a: b}", id="value:str-esc-braces"),
        pytest.param(r"$\{foo.bar\}", "${foo.bar}", id="value:str-esc-braces"),
        pytest.param("xyz_${a.b.c}", "xyz_${a.b.c}", id="value:str_interpolation"),
        pytest.param(
            "${env:USER,root}", "${env:USER,root}", id="value:custom_interpolation"
        ),
        pytest.param("c:\\foo\\a-b.txt", "c:\\foo\\a-b.txt", id="value:windows_path"),
        # null
        pytest.param("null", None, id="value:null"),
        # int
        pytest.param("1", 1, id="value:int:pos"),
        pytest.param("+1", 1, id="value:int:explicit_pos"),
        pytest.param("1___0___", "1___0___", id="value:int:not_an_int"),
        # float
        pytest.param("0.51", 0.51, id="value:float:positive"),
        pytest.param("10e0", 10.0, id="value:float:exp"),
        pytest.param("+inf", math.inf, id="value:float:plus_inf"),
        # bool
        pytest.param("true", True, id="value:bool"),
        pytest.param(".", ".", id="value:dot"),
    ],
)
def test_element(value: str, expected: Any) -> None:
    ret = parse_rule(value, "element")
    assert eq(ret, expected)


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc", "abc", id="value:simple"),
        pytest.param("abc ", "abc", id="value:simple_ws"),
        pytest.param(" abc", "abc", id="ws_value:simple"),
        pytest.param("[1,2,3]", [1, 2, 3], id="value:list"),
        pytest.param("[1 ]", [1], id="value:list1_ws"),
        pytest.param("[1, 2, 3]", [1, 2, 3], id="value:list_ws"),
        pytest.param(
            "1,2,3", ChoiceSweep(list=[1, 2, 3], simple_form=True), id="sweep:int"
        ),
        pytest.param(
            "1, 2, 3", ChoiceSweep(list=[1, 2, 3], simple_form=True), id="sweep:int_ws"
        ),
        pytest.param(
            "${a}, ${b}, ${c}",
            ChoiceSweep(list=["${a}", "${b}", "${c}"], simple_form=True),
            id="sweep:interpolations",
        ),
        pytest.param(
            "[a,b],[c,d]",
            ChoiceSweep(list=[["a", "b"], ["c", "d"]], simple_form=True),
            id="sweep:lists",
        ),
        # bool
        pytest.param("true", True, id="value:bool"),
        pytest.param("True", True, id="value:bool"),
        pytest.param("TRUE", True, id="value:bool"),
        pytest.param("trUe", True, id="value:bool"),
        pytest.param("false", False, id="value:bool"),
        pytest.param("False", False, id="value:bool"),
        pytest.param("FALSE", False, id="value:bool"),
        pytest.param("faLse", False, id="value:bool"),
        # casts
        pytest.param("int(10.0)", 10, id="int(10.0)"),
        pytest.param("str(10.0)", "10.0", id="str(10.0)"),
        pytest.param("bool(10.0)", True, id="bool(10.0)"),
        pytest.param("float(10)", 10.0, id="float(10)"),
        pytest.param("float(float(10))", 10.0, id="float(float(10))"),
        # ordering
        pytest.param("sort([2,3,1])", [1, 2, 3], id="sort([2,3,1])"),
        pytest.param(
            "sort([2,3,1],reverse=true)", [3, 2, 1], id="sort([2,3,1],reverse=true)"
        ),
        pytest.param(
            "sort(3,2,1)",
            ChoiceSweep(simple_form=True, list=[1, 2, 3], tags=set()),
            id="sort(3,2,1)",
        ),
        pytest.param(
            "sort(a,c,b,reverse=true)",
            ChoiceSweep(simple_form=True, list=["c", "b", "a"], tags=set()),
            id="sort(a,c,b,reverse=true)",
        ),
        pytest.param(
            "float(sort(3,2,1))",
            ChoiceSweep(simple_form=True, list=[1.0, 2.0, 3.0], tags=set()),
            id="float(sort(3,2,1))",
        ),
        pytest.param(
            "sort(float(3,2,1))",
            ChoiceSweep(simple_form=True, list=[1.0, 2.0, 3.0], tags=set()),
            id="sort(float(3,2,1))",
        ),
        pytest.param(
            "sort(3,2,str(1))",
            pytest.raises(
                HydraException,
                match=re.escape(
                    "TypeError while evaluating 'sort(3,2,str(1))':"
                    " '<' not supported between instances of 'str' and 'int'"
                ),
            ),
            id="sort(3,2,str(1))",
        ),
        pytest.param(
            "shuffle(1,2,3)",
            ChoiceSweep(list=[1, 2, 3], shuffle=True, simple_form=True),
            id="shuffle(1,2,3)",
        ),
        pytest.param(
            "shuffle(choice(1,2,3))",
            ChoiceSweep(list=[1, 2, 3], shuffle=True),
            id="shuffle(choice(1,2,3))",
        ),
    ],
)
def test_value(value: str, expected: Any) -> None:
    if isinstance(expected, RaisesContext):
        with expected:
            parse_rule(value, "value")
    else:
        ret = parse_rule(value, "value")
        assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("[]", [], id="list:empty"),
        pytest.param("[1]", [1], id="list:item"),
        pytest.param(
            "['a b']",
            [QuotedString(text="a b", quote=Quote.single)],
            id="list:quoted_item",
        ),
        pytest.param(
            "['[a,b]']",
            [QuotedString(text="[a,b]", quote=Quote.single)],
            id="list:quoted_item",
        ),
        pytest.param("[[a]]", [["a"]], id="list:nested_list"),
        pytest.param("[[[a]]]", [[["a"]]], id="list:double_nested_list"),
        pytest.param("[1,[a]]", [1, ["a"]], id="list:simple_and_list_elements"),
    ],
)
def test_list_value(value: str, expected: Any) -> None:
    ret = parse_rule(value, "listValue")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        # list
        pytest.param("x=shuffle([1,2,3])", [1, 2, 3], id="shuffle:list"),
        pytest.param("x=shuffle(list=[1,2,3])", [1, 2, 3], id="shuffle:list"),
        # choice
        pytest.param(
            "x=shuffle(1,2,3)",
            ChoiceSweep(list=[1, 2, 3], simple_form=True, shuffle=True),
            id="x=shuffle:choice:simple",
        ),
        pytest.param(
            "x=shuffle(choice(1,2,3))",
            ChoiceSweep(list=[1, 2, 3], shuffle=True),
            id="shuffle:choice",
        ),
        # range
        pytest.param(
            "x=shuffle(range(1,10))",
            ChoiceSweep(list=[1, 2, 3, 4, 5, 6, 7, 8, 9], shuffle=True),
            id="shuffle:range",
        ),
    ],
)
def test_shuffle_sequence(value: str, expected: Any) -> None:
    ret = parser.parse_override(value)
    if isinstance(expected, Sweep):
        actual = list(ret.sweep_string_iterator())
        if isinstance(expected, ChoiceSweep):
            expected_str_list = list(map(str, expected.list))
        elif isinstance(expected, RangeSweep):
            expected_str_list = list(map(str, expected.range()))
        else:
            assert False

        assert sorted(expected_str_list) == sorted(actual)

        for i in range(1, 10):
            actual = list(ret.sweep_string_iterator())
            if actual != expected_str_list:
                return
        assert False
    else:
        val = ret.value()
        assert isinstance(val, list)
        assert sorted(val) == expected

        for i in range(1, 10):
            ret1 = parser.parse_override(value).value()
            if ret1 != expected:
                return
        assert False


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("{}", {}, id="dict"),
        pytest.param("{a:b}", {"a": "b"}, id="dict"),
        pytest.param("{a:10}", {"a": 10}, id="dict"),
        pytest.param("{a:[a,10]}", {"a": ["a", 10]}, id="dict"),
        pytest.param("{a:[true,10]}", {"a": [True, 10]}, id="dict"),
        pytest.param("{a:10,b:20}", {"a": 10, "b": 20}, id="dict"),
        pytest.param("{a:10,b:{}}", {"a": 10, "b": {}}, id="dict"),
        pytest.param("{a:10,b:{c:[1,2]}}", {"a": 10, "b": {"c": [1, 2]}}, id="dict"),
    ],
)
def test_dict_value(value: str, expected: Any) -> None:
    ret = parse_rule(value, "dictValue")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("choice(a)", ChoiceSweep(list=["a"]), id="sweep:choice(a)"),
        pytest.param(
            "choice(a,b)", ChoiceSweep(list=["a", "b"]), id="sweep:choice(a,b)"
        ),
        pytest.param(
            "choice (a,b)", ChoiceSweep(list=["a", "b"]), id="sweep:choice (a,b)"
        ),
        pytest.param(
            "choice( 10 , 20 )",
            ChoiceSweep(list=[10, 20]),
            id="sweep:choice( 10 , 20 )",
        ),
        pytest.param("choice(str(10))", ChoiceSweep(list=["10"]), id="choice(str(10))"),
    ],
)
def test_choice_sweep(value: str, expected: Any) -> None:
    ret = parse_rule(value, "function")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("a,b", ChoiceSweep(list=["a", "b"], simple_form=True), id="a,b"),
        pytest.param(
            "a,10,3.14",
            ChoiceSweep(list=["a", 10, 3.14], simple_form=True),
            id="a,10,3.14",
        ),
        pytest.param(
            "a , b", ChoiceSweep(list=["a", "b"], simple_form=True), id="a , b"
        ),
        pytest.param(
            "${a},${b}",
            ChoiceSweep(list=["${a}", "${b}"], simple_form=True),
            id="${a},${a}",
        ),
    ],
)
def test_simple_choice_sweep(value: str, expected: Any) -> None:
    ret = parse_rule(value, "simpleChoiceSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("range(10,11)", RangeSweep(start=10, stop=11, step=1), id="ints"),
        pytest.param("range (10,11)", RangeSweep(start=10, stop=11, step=1), id="ints"),
        pytest.param(
            "range(1,10,2)", RangeSweep(start=1, stop=10, step=2), id="ints_with_step"
        ),
        pytest.param(
            "range(start=1,stop=10,step=2)",
            RangeSweep(start=1, stop=10, step=2),
            id="ints_with_step",
        ),
        pytest.param(
            "range(1.0, 3.14)", RangeSweep(start=1.0, stop=3.14, step=1), id="floats"
        ),
        pytest.param(
            "range(1.0, 3.14, 0.1)",
            RangeSweep(start=1.0, stop=3.14, step=0.1),
            id="floats_with_step",
        ),
    ],
)
def test_range_sweep(value: str, expected: Any) -> None:
    ret = parse_rule(value, "function")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param(
            "interval(10,11)", IntervalSweep(start=10.0, end=11.0), id="interval(10,11)"
        ),
        pytest.param(
            "interval(2.72,3.14)", IntervalSweep(start=2.72, end=3.14), id="interval"
        ),
        pytest.param(
            "interval(start=2.72,end=3.14)",
            IntervalSweep(start=2.72, end=3.14),
            id="interval:named",
        ),
    ],
)
def test_interval_sweep(value: str, expected: Any) -> None:
    ret: IntervalSweep = parse_rule(value, "function")
    assert type(ret.start) is float
    assert type(ret.end) is float
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "rule,value,expected",
    [
        # errors
        pytest.param(
            "primitive",
            " ",
            pytest.raises(
                HydraException,
                match=re.escape("Trying to parse a primitive that is all whitespaces"),
            ),
            id="error:value:whitespace",
        ),
        pytest.param(
            "value",
            "[",
            pytest.raises(
                HydraException, match=re.escape("no viable alternative at input '['")
            ),
            id="error:partial_list",
        ),
        pytest.param(
            "override",
            "key=[]aa",
            pytest.raises(
                HydraException, match=re.escape("extraneous input 'aa' expecting <EOF>")
            ),
            id="error:left_overs",
        ),
        pytest.param(
            "override",
            "key=[1,2,3]'",
            pytest.raises(
                HydraException, match=re.escape("token recognition error at: '''")
            ),
            id="error:left_overs",
        ),
        pytest.param(
            "key",
            "foo@",
            pytest.raises(
                HydraException, match=re.escape("missing {DOT_PATH, ID} at '<EOF>'")
            ),
            id="error:left_overs",
        ),
        pytest.param(
            "key",
            "foo@abc:",
            pytest.raises(
                HydraException, match=re.escape("missing {DOT_PATH, ID} at '<EOF>'")
            ),
            id="error:left_overs",
        ),
    ],
)
def test_parse_errors(rule: str, value: str, expected: Any) -> None:
    with expected:
        parse_rule(value, rule)


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc", "abc", id="package"),
        pytest.param("abc.cde", "abc.cde", id="package"),
    ],
)
def test_package(value: str, expected: Any) -> None:
    ret = parse_rule(value, "package")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc", "abc", id="package"),
        pytest.param("abc.cde", "abc.cde", id="package"),
        pytest.param("a/b/c", "a/b/c", id="group"),
    ],
)
def test_package_or_group(value: str, expected: Any) -> None:
    ret = parse_rule(value, "packageOrGroup")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc", Key(key_or_group="abc"), id="abc"),
        pytest.param("abc/cde", Key(key_or_group="abc/cde"), id="abc/cde"),
        pytest.param("abc.cde", Key(key_or_group="abc.cde"), id="abc.cde"),
        pytest.param("list.0", Key(key_or_group="list.0"), id="list.0"),
        pytest.param(
            "package_or_group@pkg1",
            Key(key_or_group="package_or_group", pkg1="pkg1"),
            id="package_or_group@pkg1",
        ),
        pytest.param(
            "package_or_group@pkg1:pkg2",
            Key(key_or_group="package_or_group", pkg1="pkg1", pkg2="pkg2"),
            id="package_or_group@pkg1:pkg2",
        ),
        pytest.param(
            "package_or_group@:pkg2",
            Key(key_or_group="package_or_group", pkg1=None, pkg2="pkg2"),
            id="package_or_group@:pkg2",
        ),
    ],
)
def test_key(value: str, expected: Any) -> None:
    ret = parse_rule(value, "key")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("a", "a", id="a"),
        pytest.param("/:-\\+.$%*@", "/:-\\+.$%*@", id="accepted_specials"),
        pytest.param("abc10", "abc10", id="abc10"),
        pytest.param("a.b.c", "a.b.c", id="a.b.c"),
        pytest.param("list.0.bar", "list.0.bar", id="list.0.bar"),
        pytest.param("0.foo", "0.foo", id="0.foo"),
        pytest.param("10", 10, id="10"),
        pytest.param("10abc", "10abc", id="10abc"),
        pytest.param("abc-cde", "abc-cde", id="abc-cde"),
        pytest.param("true", True, id="primitive:bool"),
        pytest.param("True", True, id="primitive:bool"),
        pytest.param("TRUE", True, id="primitive:bool"),
        pytest.param("trUe", True, id="primitive:bool"),
        pytest.param("false", False, id="primitive:bool"),
        pytest.param("False", False, id="primitive:bool"),
        pytest.param("FALSE", False, id="primitive:bool"),
        pytest.param("faLse", False, id="primitive:bool"),
        pytest.param("abc", "abc", id="primitive:id"),
        pytest.param("abc123", "abc123", id="primitive:idint"),
        pytest.param("abc-123", "abc-123", id="primitive:id-int"),
        pytest.param("xyz_${a.b.c}", "xyz_${a.b.c}", id="primitive:str_interpolation"),
        pytest.param(
            "${env:USER,root}", "${env:USER,root}", id="primitive:custom_interpolation"
        ),
        pytest.param(
            "c:\\foo\\a-b.txt", "c:\\foo\\a-b.txt", id="primitive:windows_path"
        ),
        # null
        pytest.param("null", None, id="primitive:null"),
        # int
        pytest.param("0", 0, id="primitive:int:zero"),
        pytest.param("-1", -1, id="primitive:int:neg"),
        pytest.param("1", 1, id="primitive:int:pos"),
        pytest.param("10_0", 100, id="primitive:int:underscore"),
        # float
        pytest.param("0.0", 0.0, id="primitive:float:zero"),
        pytest.param("0.51", 0.51, id="primitive:float:positive"),
        pytest.param("1e-05", 1e-05, id="primitive:float:small"),
        pytest.param("-3.14", -3.14, id="primitive:float:negative"),
        pytest.param("3.1_4", 3.14, id="primitive:float:underscore"),
        pytest.param("10e0", 10.0, id="primitive:float:exp"),
        pytest.param("-10e1", -100.0, id="primitive:float:exp:neg"),
        pytest.param("inf", math.inf, id="primitive:float:inf"),
        pytest.param("INF", math.inf, id="primitive:float:inf"),
        pytest.param("-inf", -math.inf, id="primitive:float:inf:neg"),
        pytest.param("nan", math.nan, id="primitive:float:nan"),
        pytest.param("NaN", math.nan, id="primitive:float:nan"),
        # bool
        pytest.param("true", True, id="primitive:bool"),
        pytest.param("false", False, id="primitive:bool"),
        # quoted string
        pytest.param(
            "'foo \\'bar'",
            QuotedString(text="foo 'bar", quote=Quote.single),
            id="value:escape_single_quote",
        ),
        pytest.param(
            '"foo \\"bar"',
            QuotedString(text='foo "bar', quote=Quote.double),
            id="value:escape_double_quote",
        ),
        pytest.param(
            "'\t []{},=+~'",
            QuotedString(text="\t []{},=+~", quote=Quote.single),
            id="value:quoted_specials",
        ),
        pytest.param(
            '"\t []{},=+~"',
            QuotedString(text="\t []{},=+~", quote=Quote.double),
            id="value:quoted_specials",
        ),
        pytest.param(
            "'a b c'",
            QuotedString(text="a b c", quote=Quote.single),
            id="value:quoted_with_whitespace",
        ),
        pytest.param(
            "'a,b'",
            QuotedString(text="a,b", quote=Quote.single),
            id="value:quoted_with_comma",
        ),
        pytest.param(
            "'[1,2,3]'",
            QuotedString(text="[1,2,3]", quote=Quote.single),
            id="value:quoted_list",
        ),
        pytest.param(
            '"[1,2,3]"',
            QuotedString(text="[1,2,3]", quote=Quote.double),
            id="value:quoted_list",
        ),
        pytest.param(
            "\"[1,'2',3]\"",
            QuotedString(text="[1,'2',3]", quote=Quote.double),
            id="value:quoted_list_with_quoted_element",
        ),
        pytest.param(
            "'null'",
            QuotedString(text="null", quote=Quote.single),
            id="value:null:quoted",
        ),
        pytest.param(
            "'100'", QuotedString(text="100", quote=Quote.single), id="value:int:quoted"
        ),
        pytest.param(
            "'3.14'",
            QuotedString(text="3.14", quote=Quote.single),
            id="value:float:quoted",
        ),
        pytest.param(
            "'nan'",
            QuotedString(text="nan", quote=Quote.single),
            id="value:float:constant:quoted",
        ),
        pytest.param(
            "'inf'",
            QuotedString(text="inf", quote=Quote.single),
            id="value:float:constant:quoted",
        ),
        pytest.param(
            "'nan'",
            QuotedString(text="nan", quote=Quote.single),
            id="value:float:constant:quoted",
        ),
        pytest.param(
            "'true'",
            QuotedString(text="true", quote=Quote.single),
            id="value:bool:quoted",
        ),
        pytest.param(
            "'false'",
            QuotedString(text="false", quote=Quote.single),
            id="value:bool:quoted",
        ),
        # interpolations:
        pytest.param("${a}", "${a}", id="primitive:interpolation"),
        pytest.param("${a.b.c}", "${a.b.c}", id="primitive:interpolation"),
        pytest.param("${foo:a}", "${foo:a}", id="primitive:interpolation"),
        pytest.param("${foo:1,2,3}", "${foo:1,2,3}", id="primitive:interpolation"),
        pytest.param("${foo:[1,2,3]}", "${foo:[1,2,3]}", id="primitive:interpolation"),
    ],
)
def test_primitive(value: str, expected: Any) -> None:
    ret = parse_rule(value, "primitive")
    if isinstance(ret, QuotedString):
        assert value == ret.with_quotes()

    assert eq(ret, expected)


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc=xyz", False, id="no_rename"),
        pytest.param("abc@pkg=xyz", False, id="no_rename"),
        pytest.param("abc@pkg1:pkg2=xyz", True, id="rename"),
        pytest.param("abc@:pkg2=xyz", True, id="rename_from_current"),
    ],
)
def test_key_rename(value: str, expected: bool) -> None:
    ret = parse_rule(value, "override")
    assert ret.is_package_rename() == expected


@pytest.mark.parametrize(  # type: ignore
    "prefix,override_type",
    [
        pytest.param("", OverrideType.CHANGE, id="change"),
        pytest.param("+", OverrideType.ADD, id="add"),
        pytest.param("~", OverrideType.DEL, id="del"),
    ],
)
@pytest.mark.parametrize(  # type: ignore
    "value,expected_key,expected_value,expected_value_type",
    [
        pytest.param("key=value", "key", "value", ValueType.ELEMENT, id="simple_value"),
        pytest.param(
            "key='1,2,3'",
            "key",
            QuotedString(text="1,2,3", quote=Quote.single),
            ValueType.ELEMENT,
            id="simple_value",
        ),
        pytest.param(
            "key='שלום'",
            "key",
            QuotedString(text="שלום", quote=Quote.single),
            ValueType.ELEMENT,
            id="unicode",
        ),
        pytest.param(
            "key=value-123", "key", "value-123", ValueType.ELEMENT, id="id-int"
        ),
        pytest.param(
            "key=value-1.0", "key", "value-1.0", ValueType.ELEMENT, id="id-float"
        ),
        pytest.param(
            "key=value-true", "key", "value-true", ValueType.ELEMENT, id="id-bool"
        ),
        pytest.param("key=", "key", "", ValueType.ELEMENT, id="empty_value"),
        pytest.param(
            "key='foo,bar'",
            "key",
            QuotedString(text="foo,bar", quote=Quote.single),
            ValueType.ELEMENT,
            id="quoted_value",
        ),
        pytest.param(
            "key='foo , bar'",
            "key",
            QuotedString(text="foo , bar", quote=Quote.single),
            ValueType.ELEMENT,
            id="quoted_value",
        ),
        pytest.param(
            "key=1,2,3",
            "key",
            ChoiceSweep(list=[1, 2, 3], simple_form=True),
            ValueType.SIMPLE_CHOICE_SWEEP,
            id="choice",
        ),
        pytest.param(
            "key=choice(1)",
            "key",
            ChoiceSweep(list=[1]),
            ValueType.CHOICE_SWEEP,
            id="choice_1_element",
        ),
        pytest.param(
            "key=choice(1,2,3)",
            "key",
            ChoiceSweep(list=[1, 2, 3]),
            ValueType.CHOICE_SWEEP,
            id="choice_sweep",
        ),
        pytest.param(
            "key=[1,2],[3,4]",
            "key",
            ChoiceSweep(list=[[1, 2], [3, 4]], simple_form=True),
            ValueType.SIMPLE_CHOICE_SWEEP,
            id="choice",
        ),
        pytest.param(
            "key=choice([1,2],[3,4])",
            "key",
            ChoiceSweep(list=[[1, 2], [3, 4]]),
            ValueType.CHOICE_SWEEP,
            id="choice",
        ),
        pytest.param(
            "key=range(0,2)",
            "key",
            RangeSweep(start=0, stop=2),
            ValueType.RANGE_SWEEP,
            id="range",
        ),
        pytest.param(
            "key=range(1,5,2)",
            "key",
            RangeSweep(start=1, stop=5, step=2),
            ValueType.RANGE_SWEEP,
            id="range",
        ),
        pytest.param(
            "key=range(10.0, 11.0)",
            "key",
            RangeSweep(start=10.0, stop=11.0, step=1.0),
            ValueType.RANGE_SWEEP,
            id="range",
        ),
        pytest.param(
            "key=interval(0,1)",
            "key",
            IntervalSweep(start=0.0, end=1.0),
            ValueType.INTERVAL_SWEEP,
            id="interval",
        ),
        # tags
        pytest.param(
            "key=tag(a,b,choice([1,2],[3,4]))",
            "key",
            ChoiceSweep(list=[[1, 2], [3, 4]], tags={"a", "b"}),
            ValueType.CHOICE_SWEEP,
            id="choice:tags",
        ),
        pytest.param(
            "key=tag(a,b,interval(0,1))",
            "key",
            IntervalSweep(tags={"a", "b"}, start=0.0, end=1.0),
            ValueType.INTERVAL_SWEEP,
            id="interval:tags",
        ),
        pytest.param(
            "key=str([1,2])", "key", ["1", "2"], ValueType.ELEMENT, id="cast_list"
        ),
        pytest.param(
            "choice=reverse",
            "choice",
            "reverse",
            ValueType.ELEMENT,
            id="using_function_name_in_key",
        ),
    ],
)
def test_override(
    prefix: str,
    value: str,
    override_type: OverrideType,
    expected_key: str,
    expected_value: Any,
    expected_value_type: ValueType,
) -> None:
    line = prefix + value
    ret = parse_rule(line, "override")
    expected = Override(
        input_line=line,
        type=override_type,
        key_or_group=expected_key,
        _value=expected_value,
        value_type=expected_value_type,
    )
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param(
            "~x",
            Override(
                type=OverrideType.DEL, key_or_group="x", value_type=None, _value=None
            ),
            id="bare_del",
        ),
        pytest.param(
            "~x=10",
            Override(
                type=OverrideType.DEL,
                key_or_group="x",
                value_type=ValueType.ELEMENT,
                _value=10,
            ),
            id="specific_del",
        ),
        pytest.param(
            "~x=",
            Override(
                type=OverrideType.DEL,
                key_or_group="x",
                value_type=ValueType.ELEMENT,
                _value="",
            ),
            id="specific_del_empty_string",
        ),
    ],
)
def test_override_del(value: str, expected: Any) -> None:
    expected.input_line = value
    ret = parse_rule(value, "override")
    assert ret == expected


def test_parse_overrides() -> None:
    overrides = ["x=10", "y=[1,2]", "z=a,b,c", "z=choice(a,b,c)"]
    expected = [
        Override(
            type=OverrideType.CHANGE,
            key_or_group="x",
            value_type=ValueType.ELEMENT,
            _value=10,
            input_line=overrides[0],
        ),
        Override(
            type=OverrideType.CHANGE,
            key_or_group="y",
            value_type=ValueType.ELEMENT,
            _value=[1, 2],
            input_line=overrides[1],
        ),
        Override(
            type=OverrideType.CHANGE,
            key_or_group="z",
            value_type=ValueType.SIMPLE_CHOICE_SWEEP,
            _value=ChoiceSweep(list=["a", "b", "c"], simple_form=True),
            input_line=overrides[2],
        ),
        Override(
            type=OverrideType.CHANGE,
            key_or_group="z",
            value_type=ValueType.CHOICE_SWEEP,
            _value=ChoiceSweep(list=["a", "b", "c"]),
            input_line=overrides[3],
        ),
    ]
    ret = parser.parse_overrides(overrides)
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "override,expected",
    [
        # change
        pytest.param("key=value", "key", id="key"),
        pytest.param("key@pkg1=value", "key@pkg1", id="key@pkg1"),
        pytest.param("key@pkg1:pkg2=value", "key@pkg1:pkg2", id="key@pkg1:pkg2"),
        pytest.param("key@:pkg2=value", "key@:pkg2", id="key@:pkg2"),
        # add
        pytest.param("+key=value", "+key", id="+key"),
        pytest.param("+key@pkg1=value", "+key@pkg1", id="+key@pkg1"),
        pytest.param("+key@pkg1:pkg2=value", "+key@pkg1:pkg2", id="+key@pkg1:pkg2"),
        pytest.param("+key@:pkg2=value", "+key@:pkg2", id="+key@:pkg2"),
        # del
        pytest.param("~key=value", "~key", id="~key"),
        pytest.param("~key@pkg1=value", "~key@pkg1", id="~key@pkg1"),
        pytest.param("~key@pkg1:pkg2=value", "~key@pkg1:pkg2", id="~key@pkg1:pkg2"),
        pytest.param("~key@:pkg2=value", "~key@:pkg2", id="~key@:pkg2"),
    ],
)
def test_get_key_element(override: str, expected: str) -> None:
    ret = parse_rule(override, "override")
    assert ret.get_key_element() == expected


@pytest.mark.parametrize(  # type: ignore
    "override,expected,space_after_sep",
    [
        pytest.param("key=value", "value", False, id="str"),
        pytest.param("key='value'", "'value'", False, id="single_quoted"),
        pytest.param('key="value"', '"value"', False, id="double_quoted"),
        pytest.param("key='שלום'", "'שלום'", False, id="quoted_unicode"),
        pytest.param("key=10", "10", False, id="int"),
        pytest.param("key=3.1415", "3.1415", False, id="float"),
        pytest.param("key=[]", "[]", False, id="list"),
        pytest.param("key=[1,2,3]", "[1,2,3]", False, id="list"),
        pytest.param("key=[1,2,3]", "[1, 2, 3]", True, id="list"),
        pytest.param("key=['a b', 2, 3]", "['a b',2,3]", False, id="list"),
        pytest.param("key=['a b', 2, 3]", "['a b', 2, 3]", True, id="list"),
        pytest.param("key={}", "{}", False, id="dict"),
        pytest.param("key={a:10}", "{a:10}", False, id="dict"),
        pytest.param("key={a:10}", "{a: 10}", True, id="dict"),
        pytest.param("key={a:10,b:20}", "{a:10,b:20}", False, id="dict"),
        pytest.param("key={a:10,b:20}", "{a: 10, b: 20}", True, id="dict"),
        pytest.param("key={a:10,b:[1,2,3]}", "{a: 10, b: [1, 2, 3]}", True, id="dict"),
    ],
)
def test_override_get_value_element_method(
    override: str, expected: str, space_after_sep: bool
) -> None:
    ret = parse_rule(override, "override")
    assert ret.get_value_element_as_str(space_after_sep=space_after_sep) == expected


@pytest.mark.parametrize(  # type: ignore
    "override,expected",
    [
        pytest.param("key=value", "value", id="str"),
        pytest.param("key='value'", "value", id="quoted_str"),
        pytest.param('key="value"', "value", id="quoted_str"),
        pytest.param("key=10", 10, id="int"),
        pytest.param("key=3.1415", 3.1415, id="float"),
        pytest.param("key=[]", [], id="list"),
        pytest.param("key=[1,2,3]", [1, 2, 3], id="list"),
        pytest.param("key=[1,2,3]", [1, 2, 3], id="list"),
        pytest.param("key=['a b', 2, 3]", ["a b", 2, 3], id="list"),
        pytest.param("key=['a b', 2, 3]", ["a b", 2, 3], id="list"),
        pytest.param("key={}", {}, id="dict"),
        pytest.param("key={a:10}", {"a": 10}, id="dict"),
        pytest.param("key={a:10}", {"a": 10}, id="dict"),
        pytest.param("key={a:10,b:20}", {"a": 10, "b": 20}, id="dict"),
        pytest.param("key={a:10,b:20}", {"a": 10, "b": 20}, id="dict"),
        pytest.param("key={a:10,b:[1,2,3]}", {"a": 10, "b": [1, 2, 3]}, id="dict"),
    ],
)
def test_override_value_method(override: str, expected: str) -> None:
    ret = parse_rule(override, "override")
    assert ret.value() == expected


@pytest.mark.parametrize(  # type: ignore
    "start,stop,step,expected",
    [
        # empty
        pytest.param(0, 0, 1, [], id="FloatRange:empty"),
        pytest.param(0, 0, -1, [], id="FloatRange:empty"),
        pytest.param(10, 0, 1, [], id="FloatRange:empty"),
        pytest.param(0, 10, -1, [], id="FloatRange:empty"),
        # up
        pytest.param(0, 2, 1, [0.0, 1.0], id="FloatRange:up"),
        pytest.param(0, 2, 0.5, [0.0, 0.5, 1.0, 1.5], id="FloatRange:up"),
        pytest.param(0, 2, 1, [0.0, 1.0], id="FloatRange:up"),
        # down
        pytest.param(2, 0, -1, [2.0, 1.0], id="FloatRange:down"),
        pytest.param(10.0, 5.0, -2, [10.0, 8.0, 6.0], id="FloatRange:down"),
    ],
)
def test_float_range(
    start: float, stop: float, step: float, expected: List[float]
) -> None:
    res = list(FloatRange(start, stop, step))
    assert len(res) == len(expected)
    for i in range(len(res)):
        assert math.fabs(res[i] - expected[i]) < 10e-6


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        # choice
        pytest.param(
            "tag(choice(a,b))", ChoiceSweep(list=["a", "b"]), id="tag(choice(a,b))"
        ),
        pytest.param(
            "tag(tag1,tag2,choice(a,b))",
            ChoiceSweep(list=["a", "b"], tags={"tag1", "tag2"}),
            id="tag(tag1,tag2,choice(a,b))",
        ),
        # interval
        pytest.param(
            "tag(interval(0,2))",
            IntervalSweep(start=0.0, end=2.0),
            id="tag(interval(0,2))",
        ),
        pytest.param(
            "tag(tag1,tag2,interval(0,2))",
            IntervalSweep(start=0.0, end=2.0, tags={"tag1", "tag2"}),
            id="tag(tag1,tag2,interval(0,2))",
        ),
        # range
        pytest.param(
            "tag(range(1,2))", RangeSweep(start=1, stop=2), id="tag(range(1,2))"
        ),
        pytest.param(
            "tag(tag1,tag2,range(1,2))",
            RangeSweep(start=1, stop=2, tags={"tag1", "tag2"}),
            id="tag(tag1,tag2,range(1,2))",
        ),
        pytest.param(
            "tag(tag1,tag2,sweep=range(1,2))",
            RangeSweep(start=1, stop=2, tags={"tag1", "tag2"}),
            id="tag(tag1,tag2,sweep=range(1,2))",
        ),
    ],
)
def test_tag_sweep(value: str, expected: str) -> None:
    ret = parse_rule(value, "function")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        # value
        pytest.param("sort(1)", 1, id="sort:value"),
        pytest.param("sort({a:10})", {"a": 10}, id="sort:value"),
        # list
        pytest.param("sort([1])", [1], id="sort:list"),
        pytest.param("sort([1,2,3])", [1, 2, 3], id="sort:list"),
        pytest.param("sort(list=[1,2,3])", [1, 2, 3], id="sort:list:named"),
        pytest.param("sort(list=[])", [], id="sort:list:named:empty"),
        pytest.param(
            "sort(list=[1,2,3], reverse=True)", [3, 2, 1], id="sort:list:named:rev"
        ),
        # simple choice sweep
        pytest.param(
            "sort(1,2,3)",
            ChoiceSweep(list=[1, 2, 3], simple_form=True),
            id="sort:choice:simple",
        ),
        pytest.param(
            "sort(1,2,3,reverse=True)",
            ChoiceSweep(list=[3, 2, 1], simple_form=True),
            id="sort:choice:simple:rev",
        ),
        # choice sweep
        pytest.param(
            "sort(choice(1,2,3))", ChoiceSweep(list=[1, 2, 3]), id="sort:choice"
        ),
        pytest.param(
            "sort(sweep=choice(1,2,3))",
            ChoiceSweep(list=[1, 2, 3]),
            id="sort:choice:named",
        ),
        pytest.param(
            "sort(choice(1,2,3), reverse=True)",
            ChoiceSweep(list=[3, 2, 1]),
            id="sort:choice:rev",
        ),
        pytest.param(
            "sort(tag(a,b,choice(1,2,3)), reverse=True)",
            ChoiceSweep(list=[3, 2, 1], tags={"a", "b"}),
            id="sort:tag:choice:rev",
        ),
        # sort integer range
        pytest.param(
            "sort(range(1, 10))",
            RangeSweep(start=1, stop=10, step=1),
            id="sort(range(1, 10))",
        ),
        pytest.param(
            "sort(range(9,0,-1))",
            RangeSweep(start=1, stop=10, step=1),
            id="sort(range(1, 10))",
        ),
        pytest.param(
            "sort(range(1,10),reverse=True)",
            RangeSweep(start=9, stop=0, step=-1),
            id="sort(range(1,10),reverse=True)",
        ),
        pytest.param(
            "sort(sort(range(1, 10),reverse=true))",
            RangeSweep(start=1, stop=10, step=1),
            id="sort(sort(range(1, 10),reverse=true))",
        ),
        # sort float range
        pytest.param(
            "sort(range(0,2,0.5))",
            RangeSweep(start=0, stop=2, step=0.5),
            id="sort(range(0,2,0.5))",
        ),
        pytest.param(
            "sort(range(1.5,-0.5,-0.5))",
            RangeSweep(start=0.0, stop=2.0, step=0.5),
            id="sort(range(1.5,-0.5,-0.5))",
        ),
        pytest.param(
            "sort(range(0,2,0.5),reverse=true)",
            RangeSweep(start=1.5, stop=-0.5, step=-0.5),
            id="range:sort:reverse)",
        ),
        pytest.param(
            "shuffle(range(1, 10))",
            RangeSweep(start=1, stop=10, step=1, shuffle=True),
            id="range:shuffle",
        ),
    ],
)
def test_sort(value: str, expected: str) -> None:
    ret = parse_rule(value, "function")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        # simple choice sweep
        pytest.param(
            "shuffle(1,2,3)",
            ChoiceSweep(simple_form=True, list=[1, 2, 3], tags=set(), shuffle=True),
            id="shuffle:choice:simple",
        ),
        # choice sweep
        pytest.param(
            "shuffle(choice(1,2,3))",
            ChoiceSweep(list=[1, 2, 3], tags=set(), shuffle=True),
            id="shuffle:choice",
        ),
        pytest.param(
            "shuffle(tag(a,b,choice(1,2,3)))",
            ChoiceSweep(list=[1, 2, 3], tags={"a", "b"}, shuffle=True),
            id="shuffle:tag:choice",
        ),
        # range sweep
        pytest.param(
            "shuffle(range(10,1))",
            RangeSweep(start=10, stop=1, shuffle=True),
            id="shuffle:range",
        ),
        pytest.param(
            "shuffle(float(range(10,1))))",
            RangeSweep(start=10.0, stop=1.0, shuffle=True),
            id="shuffle:float:range",
        ),
        pytest.param(
            "shuffle(tag(a,b,range(1,10,2)))",
            RangeSweep(start=1, stop=10, step=2, tags={"a", "b"}, shuffle=True),
            id="shuffle:tag:range",
        ),
    ],
)
def test_sweep_shuffle(value: str, expected: str) -> None:
    ret = parse_rule(value, "function")
    assert ret == expected


@dataclass
class CastResults:
    int: Union[
        int,
        List[Union[int, List[int]]],
        Dict[str, Any],
        Sweep,
        RaisesContext[HydraException],
    ]
    float: Union[
        float,
        List[Union[float, List[float]]],
        Dict[str, Any],
        Sweep,
        RaisesContext[HydraException],
    ]
    bool: Union[
        bool,
        List[Union[bool, List[bool]]],
        Dict[str, Any],
        Sweep,
        RaisesContext[HydraException],
    ]
    str: Union[
        str,
        List[Union[str, List[str]]],
        Dict[str, Any],
        Sweep,
        RaisesContext[HydraException],
    ]

    @staticmethod
    def error(msg: str) -> Any:
        return pytest.raises(HydraException, match=f"^{re.escape(msg)}")


@pytest.mark.parametrize(  # type: ignore
    "value,expected_value",
    [
        # int
        pytest.param(10, CastResults(int=10, float=10.0, str="10", bool=True), id="10"),
        pytest.param(0, CastResults(int=0, float=0.0, str="0", bool=False), id="0"),
        # float
        pytest.param(
            10.0, CastResults(int=10, float=10.0, str="10.0", bool=True), id="10.0"
        ),
        pytest.param(
            0.0, CastResults(int=0, float=0.0, str="0.0", bool=False), id="0.0"
        ),
        pytest.param(
            "inf",
            CastResults(
                int=CastResults.error(
                    "OverflowError while evaluating 'int(inf)': cannot convert float infinity to integer"
                ),
                float=math.inf,
                str="inf",
                bool=True,
            ),
            id="inf",
        ),
        pytest.param(
            "nan",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int(nan)': cannot convert float NaN to integer"
                ),
                float=math.nan,
                str="nan",
                bool=True,
            ),
            id="nan",
        ),
        pytest.param(
            "1e6",
            CastResults(int=1000000, float=1e6, str="1000000.0", bool=True),
            id="1e6",
        ),
        pytest.param(
            "''",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int('')': invalid literal for int() with base 10:"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float('')': could not convert string to float:"
                ),
                str="",
                bool=CastResults.error(
                    "ValueError while evaluating 'bool('')': Cannot cast '' to bool"
                ),
            ),
            id="''",
        ),
        # string
        pytest.param(
            "'10'",
            CastResults(
                int=10,
                float=10.0,
                str="10",
                bool=CastResults.error(
                    "ValueError while evaluating 'bool('10')': Cannot cast '10' to bool"
                ),
            ),
            id="'10'",
        ),
        pytest.param(
            "'10.0'",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int('10.0')': invalid literal for int() with base 10: '10.0'"
                ),
                float=10.0,
                str="10.0",
                bool=CastResults.error(
                    "ValueError while evaluating 'bool('10.0')': Cannot cast '10.0' to bool"
                ),
            ),
            id="'10.0'",
        ),
        pytest.param(
            "'true'",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int('true')': invalid literal for int() with base 10: 'true'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float('true')': could not convert string to float: 'true'"
                ),
                str="true",
                bool=True,
            ),
            id="'true'",
        ),
        pytest.param(
            "'false'",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int('false')': invalid literal for int() with base 10: 'false'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float('false')': could not convert string to float: 'false'"
                ),
                str="false",
                bool=False,
            ),
            id="'false'",
        ),
        pytest.param(
            "'[1,2,3]'",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int('[1,2,3]')': invalid literal for int() with base 10: '[1,2,3]'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float('[1,2,3]')': could not convert string to float: '[1,2,3]'"
                ),
                str="[1,2,3]",
                bool=CastResults.error(
                    "ValueError while evaluating 'bool('[1,2,3]')': Cannot cast '[1,2,3]' to bool"
                ),
            ),
            id="'[1,2,3]'",
        ),
        pytest.param(
            "'{a:10}'",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int('{a:10}')': invalid literal for int() with base 10: '{a:10}'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float('{a:10}')': could not convert string to float: '{a:10}'"
                ),
                str="{a:10}",
                bool=CastResults.error(
                    "ValueError while evaluating 'bool('{a:10}')': Cannot cast '{a:10}' to bool"
                ),
            ),
            id="'{a:10}'",
        ),
        # bool
        pytest.param(
            "true", CastResults(int=1, float=1.0, str="true", bool=True), id="true"
        ),
        pytest.param(
            "false", CastResults(int=0, float=0.0, str="false", bool=False), id="false"
        ),
        # list
        pytest.param("[]", CastResults(int=[], float=[], str=[], bool=[]), id="[]"),
        pytest.param(
            "[0,1,2]",
            CastResults(
                int=[0, 1, 2],
                float=[0.0, 1.0, 2.0],
                str=["0", "1", "2"],
                bool=[False, True, True],
            ),
            id="[1,2,3]",
        ),
        pytest.param(
            "[1,[2]]",
            CastResults(
                int=[1, [2]], float=[1.0, [2.0]], str=["1", ["2"]], bool=[True, [True]]
            ),
            id="[1,[2]]",
        ),
        pytest.param(
            "[a,1]",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int([a,1])': invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float([a,1])': could not convert string to float: 'a'"
                ),
                str=["a", "1"],
                bool=CastResults.error(
                    "ValueError while evaluating 'bool([a,1])': Cannot cast 'a' to bool"
                ),
            ),
            id="[a,1]",
        ),
        # dicts
        pytest.param("{}", CastResults(int={}, float={}, str={}, bool={}), id="{}"),
        pytest.param(
            "{a:10}",
            CastResults(
                int={"a": 10}, float={"a": 10.0}, str={"a": "10"}, bool={"a": True}
            ),
            id="{a:10}",
        ),
        pytest.param(
            "{a:[0,1,2]}",
            CastResults(
                int={"a": [0, 1, 2]},
                float={"a": [0.0, 1.0, 2.0]},
                str={"a": ["0", "1", "2"]},
                bool={"a": [False, True, True]},
            ),
            id="{a:[0,1,2]}",
        ),
        pytest.param(
            "{a:10,b:xyz}",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int({a:10,b:xyz})': invalid literal for int() with base 10: 'xyz'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float({a:10,b:xyz})': could not convert string to float: 'xyz'"
                ),
                str={"a": "10", "b": "xyz"},
                bool=CastResults.error(
                    "ValueError while evaluating 'bool({a:10,b:xyz})': Cannot cast 'xyz' to bool"
                ),
            ),
            id="{a:10,b:xyz}",
        ),
        # choice
        pytest.param(
            "choice(0,1)",
            CastResults(
                int=ChoiceSweep(list=[0, 1]),
                float=ChoiceSweep(list=[0.0, 1.0]),
                str=ChoiceSweep(list=["0", "1"]),
                bool=ChoiceSweep(list=[False, True]),
            ),
            id="choice(0,1)",
        ),
        pytest.param(
            "2,1,0",
            CastResults(
                int=ChoiceSweep(list=[2, 1, 0], simple_form=True),
                float=ChoiceSweep(list=[2.0, 1.0, 0.0], simple_form=True),
                str=ChoiceSweep(list=["2", "1", "0"], simple_form=True),
                bool=ChoiceSweep(list=[True, True, False], simple_form=True),
            ),
            id="simple_choice:ints",
        ),
        pytest.param(
            "a,'b',1,1.0,true,[a,b],{a:10}",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int(a,'b',1,1.0,true,[a,b],{a:10})':"
                    " invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float(a,'b',1,1.0,true,[a,b],{a:10})':"
                    " could not convert string to float: 'a'"
                ),
                str=ChoiceSweep(
                    list=["a", "b", "1", "1.0", "true", ["a", "b"], {"a": "10"}],
                    simple_form=True,
                ),
                bool=CastResults.error(
                    "ValueError while evaluating 'bool(a,'b',1,1.0,true,[a,b],{a:10})': Cannot cast 'a' to bool"
                ),
            ),
            id="simple_choice:types",
        ),
        pytest.param(
            "choice(a,b)",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int(choice(a,b))': invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float(choice(a,b))': could not convert string to float: 'a'"
                ),
                str=ChoiceSweep(list=["a", "b"]),
                bool=CastResults.error(
                    "ValueError while evaluating 'bool(choice(a,b))': Cannot cast 'a' to bool"
                ),
            ),
            id="choice(a,b)",
        ),
        pytest.param(
            "choice(1,a)",
            CastResults(
                int=CastResults.error(
                    "ValueError while evaluating 'int(choice(1,a))': invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "ValueError while evaluating 'float(choice(1,a))': could not convert string to float: 'a'"
                ),
                str=ChoiceSweep(list=["1", "a"]),
                bool=CastResults.error(
                    "ValueError while evaluating 'bool(choice(1,a))': Cannot cast 'a' to bool"
                ),
            ),
            id="choice(1,a)",
        ),
        # interval
        pytest.param(
            "interval(1.0, 2.0)",
            CastResults(
                int=IntervalSweep(start=1, end=2),
                float=IntervalSweep(start=1.0, end=2.0),
                str=CastResults.error(
                    "ValueError while evaluating 'str(interval(1.0, 2.0))': Intervals cannot be cast to str"
                ),
                bool=CastResults.error(
                    "ValueError while evaluating 'bool(interval(1.0, 2.0))': Intervals cannot be cast to bool"
                ),
            ),
            id="interval(1.0, 2.0)",
        ),
        # range
        pytest.param(
            "range(1,10)",
            CastResults(
                int=RangeSweep(start=1, stop=10, step=1),
                float=RangeSweep(start=1.0, stop=10.0, step=1.0),
                str=CastResults.error(
                    "ValueError while evaluating 'str(range(1,10))': Range can only be cast to int or float"
                ),
                bool=CastResults.error(
                    "ValueError while evaluating 'bool(range(1,10))': Range can only be cast to int or float"
                ),
            ),
            id="range(1,10)",
        ),
        pytest.param(
            "range(1.0,10.0)",
            CastResults(
                int=RangeSweep(start=1, stop=10, step=1),
                float=RangeSweep(start=1.0, stop=10.0, step=1.0),
                str=CastResults.error(
                    "ValueError while evaluating 'str(range(1.0,10.0))': Range can only be cast to int or float"
                ),
                bool=CastResults.error(
                    "ValueError while evaluating 'bool(range(1.0,10.0))': Range can only be cast to int or float"
                ),
            ),
            id="range(1.0,10.0)",
        ),
    ],
)
def test_cast_conversions(value: Any, expected_value: Any) -> None:
    for field in ("int", "float", "bool", "str"):
        cast_str = f"{field}({value})"
        expected = getattr(expected_value, field)
        if isinstance(expected, RaisesContext):
            with expected:
                parser.parse_rule(cast_str, "function")
        else:
            result = parser.parse_rule(cast_str, "function")
            assert eq(result, expected), f"{field} cast result mismatch"


@pytest.mark.parametrize(  # type: ignore
    "value,expected_value",
    [
        pytest.param("abs(10)", 10, id="abs(10)"),
        pytest.param("abs(-10)", 10, id="abs(-10)"),
        pytest.param("mul(abs(-10),2)", 20, id="mul(abs(-10),2)"),
    ],
)
def test_function(value: Any, expected_value: Any) -> None:
    functions = Functions()
    functions.register(name="abs", func=abs)
    functions.register(name="mul", func=lambda n, m: n * m)
    ret = OverridesParser(functions).parse_rule(value, "function")
    assert ret == expected_value


class F:
    @staticmethod
    def foo1(value: int) -> str:
        return f"{type(value).__name__}:{str(value)}"

    @staticmethod
    def foo2(x: Union[int, str], y: Union[int, str]) -> str:
        return f"{type(x).__name__}:{str(x)},{type(y).__name__}:{str(y)}"

    @staticmethod
    def range(start: int, stop: int, step: int = 1) -> str:
        return f"res:range(start={start},stop={stop},step={step})"

    @staticmethod
    def empty() -> int:
        return 10

    @staticmethod
    def sum(*args: int) -> int:
        return sum(args, 0)

    @staticmethod
    def sort(*args: int, reverse: bool = False) -> List[int]:
        if reverse:
            return list(reversed(sorted(args)))
        else:
            return list(sorted(args))


@pytest.mark.parametrize(  # type: ignore
    "func_name, func, value, expected",
    [
        pytest.param("foo_1", F.foo1, "foo_1(10)", "int:10", id="foo_1(10)"),
        pytest.param(
            "foo_1", F.foo1, "foo_1(value=10)", "int:10", id="foo_1(value=10)"
        ),
        pytest.param(
            "foo_2", F.foo2, "foo_2('10',10)", "str:10,int:10", id="foo_2('10',10)"
        ),
        pytest.param("empty", F.empty, "empty()", 10, id="empty()"),
        pytest.param("sum", F.sum, "sum()", 0, id="sum()"),
        pytest.param("sum", F.sum, "sum(1)", 1, id="sum(1)"),
        pytest.param("sum", F.sum, "sum(1,2,3)", 6, id="sum(1,2,3)"),
        pytest.param(
            "range",
            F.range,
            "range(10,20)",
            "res:range(start=10,stop=20,step=1)",
            id="range(10,20)",
        ),
        pytest.param(
            "range",
            F.range,
            "range(10,20,5)",
            "res:range(start=10,stop=20,step=5)",
            id="range(10,20,5)",
        ),
        pytest.param(
            "range",
            F.range,
            "range(10,20,step=5)",
            "res:range(start=10,stop=20,step=5)",
            id="range(10,20,step=5)",
        ),
        pytest.param(
            "range",
            F.range,
            "range(start=10,stop=20,step=5)",
            "res:range(start=10,stop=20,step=5)",
            id="range(start=10,stop=20,step=5)",
        ),
        pytest.param(
            "range",
            F.range,
            "range(step=5,start=10,stop=20)",
            "res:range(start=10,stop=20,step=5)",
            id="range(step=5,start=10,stop=20)",
        ),
        pytest.param(
            "range",
            F.range,
            "range(10,step=5,stop=20)",
            "res:range(start=10,stop=20,step=5)",
            id="range(10,step=5,stop=20)",
        ),
        pytest.param("sort", F.sort, "sort(10,1,5)", [1, 5, 10], id="sort(10,1,5)"),
        pytest.param(
            "sort",
            F.sort,
            "sort(10,1,5,reverse=true)",
            [10, 5, 1],
            id="sort(10,1,5,reverse=true)",
        ),
    ],
)
def test_eval(
    func_name: str, func: Callable[..., Any], value: str, expected: Any
) -> None:
    functions = Functions()
    functions.register(name=func_name, func=func)
    parser = OverridesParser(functions)
    assert parser.parse_rule(value, "function") == expected


@pytest.mark.parametrize(  # type: ignore
    "func_name, func, value, expected",
    [
        pytest.param(
            "empty",
            F.empty,
            "empty(100)",
            pytest.raises(
                HydraException, match=re.escape("too many positional arguments")
            ),
            id="empty(100)",
        ),
        pytest.param(
            "foo",
            F.foo1,
            "foo(true)",
            pytest.raises(
                HydraException,
                match=re.escape(
                    "TypeError while evaluating 'foo(true)':"
                    " mismatch type argument value: bool is incompatible with int"
                ),
            ),
            id="foo_1(true)",
        ),
        pytest.param(
            "foo",
            F.foo1,
            "foo(value=true)",
            pytest.raises(
                HydraException,
                match=re.escape(
                    "TypeError while evaluating 'foo(value=true)':"
                    " mismatch type argument value: bool is incompatible with int"
                ),
            ),
            id="foo_1(value:true)",
        ),
        pytest.param(
            "empty",
            F.foo1,
            "empty(no_such_name=10)",
            pytest.raises(
                HydraException,
                match=re.escape(
                    "TypeError while evaluating 'empty(no_such_name=10)': missing a required argument: 'value'"
                ),
            ),
            id="empty(no_such_name=10)",
        ),
        pytest.param(
            "empty",
            F.foo1,
            "empty(value=10,no_such_name=10)",
            pytest.raises(
                HydraException,
                match=re.escape(
                    "TypeError while evaluating 'empty(value=10,no_such_name=10)':"
                    " got an unexpected keyword argument 'no_such_name'"
                ),
            ),
            id="empty(value=10,no_such_name=10)",
        ),
        pytest.param(
            "sum",
            F.sum,
            "sum(true)",
            pytest.raises(
                HydraException,
                match=re.escape(
                    "TypeError while evaluating 'sum(true)':"
                    " mismatch type argument args[0]: bool is incompatible with int"
                ),
            ),
            id="sum(true)",
        ),
        pytest.param(
            "range",
            F.range,
            "range(start=10,20,1)",
            pytest.raises(
                HydraException,
                match=re.escape("positional argument follows keyword argument"),
            ),
            id="range(start=10,20,1)",
        ),
    ],
)
def test_eval_errors(
    func_name: str, func: Callable[..., Any], value: str, expected: Any
) -> None:
    functions = Functions()
    functions.register(name=func_name, func=func)
    parser = OverridesParser(functions)
    with expected:
        parser.parse_rule(value, "function")


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("glob(*)", Glob(include=["*"], exclude=[])),
        pytest.param("glob(include=*)", Glob(include=["*"], exclude=[])),
        pytest.param("glob(include=[*])", Glob(include=["*"], exclude=[])),
        pytest.param(
            "glob(include=[a*, b*], exclude=c*)",
            Glob(include=["a*", "b*"], exclude=["c*"]),
        ),
    ],
)
def test_glob(value: str, expected: Any) -> None:
    ret = parse_rule(value, "function")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "include,exclude,expected",
    [
        pytest.param(
            ["*"],
            [],
            ["the", "quick", "brown", "fox", "jumped", "under", "the", "lazy", "dog"],
            id="include=*",
        ),
        pytest.param(
            ["*"],
            ["quick", "under"],
            ["the", "brown", "fox", "jumped", "the", "lazy", "dog"],
            id="include=*, exclude=[quick,under]]",
        ),
        pytest.param(
            ["*"], ["*d*"], ["the", "quick", "brown", "fox", "the", "lazy"], id="=*"
        ),
        pytest.param(["t*"], [], ["the", "the"], id="=*"),
    ],
)
def test_glob_filter(
    include: List[str], exclude: List[str], expected: List[str]
) -> None:
    strings = ["the", "quick", "brown", "fox", "jumped", "under", "the", "lazy", "dog"]
    assert Glob(include=include, exclude=exclude).filter(strings) == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected_key,expected_value,expected_value_type",
    [
        pytest.param(
            "key= \tvalue \t", "key", "value", ValueType.ELEMENT, id="leading+trailing"
        ),
        pytest.param(
            "key=value \t 123",
            "key",
            "value \t 123",
            ValueType.ELEMENT,
            id="inside_primitive",
        ),
        pytest.param(
            "key='  foo,bar\t'",
            "key",
            QuotedString(text="  foo,bar\t", quote=Quote.single),
            ValueType.ELEMENT,
            id="inside_quoted_value_outer",
        ),
        pytest.param(
            "key='foo , \t\t bar'",
            "key",
            QuotedString(text="foo , \t\t bar", quote=Quote.single),
            ValueType.ELEMENT,
            id="inside_quoted_value_inter",
        ),
        pytest.param(
            "key=1 ,  2,\t\t3",
            "key",
            ChoiceSweep(list=[1, 2, 3], simple_form=True),
            ValueType.SIMPLE_CHOICE_SWEEP,
            id="around_commas",
        ),
        pytest.param(
            "key=choice\t(  1\t\t )",
            "key",
            ChoiceSweep(list=[1]),
            ValueType.CHOICE_SWEEP,
            id="function_one_arg",
        ),
        pytest.param(
            "key=choice(\t\t1,   2, \t 3 )",
            "key",
            ChoiceSweep(list=[1, 2, 3]),
            ValueType.CHOICE_SWEEP,
            id="function_many_args",
        ),
        pytest.param(
            "key=[1  ,\t2\t],[\t3\t   ,4  ]",
            "key",
            ChoiceSweep(list=[[1, 2], [3, 4]], simple_form=True),
            ValueType.SIMPLE_CHOICE_SWEEP,
            id="in_lists",
        ),
        pytest.param(
            "key=str(\t  [  1,\t2  ]\t   )",
            "key",
            ["1", "2"],
            ValueType.ELEMENT,
            id="mixed",
        ),
    ],
)
def test_whitespaces(
    value: str, expected_key: str, expected_value: Any, expected_value_type: ValueType
) -> None:
    ret = parse_rule(value, "override")
    expected = Override(
        input_line=value,
        type=OverrideType.CHANGE,
        key_or_group=expected_key,
        _value=expected_value,
        value_type=expected_value_type,
    )
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected_sweep_string_list, expected_sweep_encoded_list",
    [
        ("x=choice(1,2,3)", ["1", "2", "3"], [1, 2, 3]),
        ("x=choice('1', '2', '3')", ["1", "2", "3"], ["1", "2", "3"]),
        ("x=choice('a', 'b')", ["a", "b"], ["a", "b"]),
        (
            "x=choice(True, 'True', False, 'False', 'a', 1, 1.1, 2.0, 3, '1.5', '4')",
            ["True", "True", "False", "False", "a", "1", "1.1", "2.0", "3", "1.5", "4"],
            [True, "True", False, "False", "a", 1, 1.1, 2.0, 3, "1.5", "4"],
        ),
        (
            "x=range(1, 10)",
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (
            "x=choice([1,2,3], ['a', 'b'])",
            ["[1,2,3]", "['a','b']"],
            ["[1,2,3]", "['a','b']"],
        ),
        (
            "x=choice([1, 1.1, '2', 'a'], [True, False])",
            ["[1,1.1,'2','a']", "[True,False]"],
            ["[1,1.1,'2','a']", "[True,False]"],
        ),
    ],
)
def test_sweep_iterators(
    value: str,
    expected_sweep_string_list: List[str],
    expected_sweep_encoded_list: List[Any],
) -> None:
    ret = parser.parse_override(value)
    actual_sweep_string_list = [x for x in ret.sweep_string_iterator()]
    actual_sweep_encoded_list = [
        x for x in ret.sweep_iterator(transformer=Transformer.encode)
    ]
    assert actual_sweep_string_list == expected_sweep_string_list
    assert actual_sweep_encoded_list == expected_sweep_encoded_list
