# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Union

import pytest
from _pytest.python_api import RaisesContext

from hydra.core.override_parser.overrides_parser import (
    Cast,
    CastType,
    ChoiceSweep,
    FloatRange,
    IntervalSweep,
    Key,
    Override,
    OverridesParser,
    OverrideType,
    Quote,
    QuotedString,
    RangeSweep,
    Sort,
    Sweep,
    ValueType,
)
from hydra.errors import HydraException


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
        pytest.param("xyz_${a.b.c}", "xyz_${a.b.c}", id="value:str_interpolation"),
        pytest.param(
            "${env:USER,root}", "${env:USER,root}", id="value:custom_interpolation"
        ),
        pytest.param("c:\\foo\\a-b.txt", "c:\\foo\\a-b.txt", id="value:windows_path"),
        # null
        pytest.param("null", None, id="value:null"),
        # int
        pytest.param("1", 1, id="value:int:pos"),
        # float
        pytest.param("0.51", 0.51, id="value:float:positive"),
        pytest.param("10e0", 10.0, id="value:float:exp"),
        # bool
        pytest.param("true", True, id="value:bool"),
        pytest.param(".", ".", id="value:dot"),
        pytest.param("str(1)", "1", id="cast:str(1)"),
        pytest.param("float(10)", 10.0, id="cast:float(10)"),
        pytest.param("str('foo')", "foo", id="cast:str('foo')"),
        pytest.param("str([1])", ["1"], id="cast:str([1])"),
        pytest.param("str({a:10})", {"a": "10"}, id="cast:str({a:10})"),
    ],
)
def test_element(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "element")
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
            "1, 2, 3", ChoiceSweep(list=[1, 2, 3], simple_form=True), id="sweep:int_ws",
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
        pytest.param("sort([2,3,1])", [1, 2, 3], id="sort([3,2,1])"),
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
            "sort(10)",
            pytest.raises(
                HydraException, match=re.escape("mismatched input ')' expecting ','"),
            ),
            id="sort(10)",
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
                    "Error sorting: '<' not supported between instances of 'str' and 'int'"
                ),
            ),
            id="sort(3,2,str(1))",
        ),
    ],
)
def test_value(value: str, expected: Any) -> None:
    if isinstance(expected, RaisesContext):
        with expected:
            OverridesParser.parse_rule(value, "value")
    else:
        ret = OverridesParser.parse_rule(value, "value")
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
    ret = OverridesParser.parse_rule(value, "listValue")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("{}", {}, id="dict"),
        pytest.param("{a:b}", {"a": "b"}, id="dict"),
        pytest.param("{a:10}", {"a": 10}, id="dict"),
        pytest.param("{a:[a,10]}", {"a": ["a", 10]}, id="dict"),
        pytest.param("{a:[true,10]}", {"a": [True, 10]}, id="dict"),
        pytest.param("{a:10,b:20}}", {"a": 10, "b": 20}, id="dict"),
        pytest.param("{a:10,b:{}}}", {"a": 10, "b": {}}, id="dict"),
        pytest.param("{a:10,b:{c:[1,2]}}}", {"a": 10, "b": {"c": [1, 2]}}, id="dict"),
    ],
)
def test_dict_value(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "dictValue")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("choice(a)", ChoiceSweep(list=["a"]), id="sweep:choice(a)"),
        pytest.param(
            "choice(a,b)", ChoiceSweep(list=["a", "b"]), id="sweep:choice(a,b)",
        ),
        pytest.param(
            "choice (a,b)", ChoiceSweep(list=["a", "b"]), id="sweep:choice (a,b)",
        ),
        pytest.param(
            "choice( 10 , 20 )",
            ChoiceSweep(list=[10, 20]),
            id="sweep:choice( 10 , 20 )",
        ),
        pytest.param(
            "choice(list=[10,20])", ChoiceSweep(list=[10, 20]), id="sweep:choice:named",
        ),
        pytest.param(
            "choice(str(10))", ChoiceSweep(list=["10"]), id="choice(str(10))",
        ),
    ],
)
def test_choice_sweep(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "choiceSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("a,b", ChoiceSweep(list=["a", "b"], simple_form=True), id="a,b",),
        pytest.param(
            "a,10,3.14",
            ChoiceSweep(list=["a", 10, 3.14], simple_form=True),
            id="a,10,3.14",
        ),
        pytest.param(
            "a , b", ChoiceSweep(list=["a", "b"], simple_form=True), id="a , b",
        ),
    ],
)
def test_simple_choice_sweep(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "simpleChoiceSweep")
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
def test_range_sweep_parsing(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "rangeSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param(
            "interval(10,11)", IntervalSweep(start=10.0, end=11.0), id="interval(10,11)"
        ),
        pytest.param(
            "tag(log,interval(0.0,1.0))",
            IntervalSweep(start=0, end=1.0, tags={"log"}),
            id="tag(log,interval(0.0,1.0))",
        ),
        pytest.param(
            "interval (10,11)",
            IntervalSweep(start=10.0, end=11.0),
            id="interval (10,11)",
        ),
        pytest.param(
            "interval(2.72,3.14)",
            IntervalSweep(start=2.72, end=3.14),
            id="interval(2.72,3.14)",
        ),
        pytest.param(
            "interval(start=2.72,end=3.14)",
            IntervalSweep(start=2.72, end=3.14),
            id="interval(start=2.72,end=3.14)",
        ),
    ],
)
def test_interval_sweep(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "intervalSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "rule,value,expected",
    [
        # errors
        pytest.param(
            "primitive",
            " ",
            pytest.raises(
                HydraException, match=re.escape("mismatched input '<EOF>' expecting"),
            ),
            id="error:value:whitespace",
        ),
        pytest.param(
            "value",
            "[",
            pytest.raises(
                HydraException, match=re.escape("no viable alternative at input '['"),
            ),
            id="error:partial_list",
        ),
        pytest.param(
            "override",
            "key=[]aa",
            pytest.raises(
                HydraException,
                match=re.escape("extraneous input 'aa' expecting <EOF>"),
            ),
            id="error:left_overs",
        ),
        pytest.param(
            "override",
            "key=[1,2,3]'",
            pytest.raises(
                HydraException, match=re.escape("token recognition error at: '''"),
            ),
            id="error:left_overs",
        ),
        pytest.param(
            "key",
            "foo@",
            pytest.raises(
                HydraException, match=re.escape("missing {ID, DOT_PATH} at '<EOF>'")
            ),
            id="error:left_overs",
        ),
        pytest.param(
            "key",
            "foo@abc:",
            pytest.raises(
                HydraException, match=re.escape("missing {ID, DOT_PATH} at '<EOF>'")
            ),
            id="error:left_overs",
        ),
    ],
)
def test_parse_errors(rule: str, value: str, expected: Any) -> None:
    with expected:
        OverridesParser.parse_rule(value, rule)


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("abc", "abc", id="package"),
        pytest.param("abc.cde", "abc.cde", id="package"),
    ],
)
def test_package(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "package")
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
    ret = OverridesParser.parse_rule(value, "packageOrGroup")
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
    ret = OverridesParser.parse_rule(value, "key")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "prefix", [pytest.param("", id="none"), pytest.param(" ", id="ws")]
)
@pytest.mark.parametrize(  # type: ignore
    "suffix", [pytest.param("", id="none"), pytest.param(" ", id="ws")]
)
@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("a", "a", id="a"),
        pytest.param("/:+.$*=", "/:+.$*=", id="accepted_specials"),
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
        pytest.param("int('10')", 10, id="int('10')"),
    ],
)
def test_primitive(value: str, prefix: str, suffix: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(prefix + value + suffix, "primitive")
    if isinstance(ret, QuotedString):
        assert value == ret.with_quotes()

    assert eq(ret, expected)


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("10", 10, id="int"),
        pytest.param(" 10", 10, id="int"),
        pytest.param("10 ", 10, id="int"),
        pytest.param("3.14", 3.14, id="float"),
        pytest.param(" 3.14", 3.14, id="float"),
        pytest.param("3.14 ", 3.14, id="float"),
    ],
)
def test_number(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "number")
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
    ret = OverridesParser.parse_rule(value, "override")
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
            "key=value-true", "key", "value-true", ValueType.ELEMENT, id="id-bool",
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
            IntervalSweep(0.0, 1.0),
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
            IntervalSweep(0.0, 1.0, {"a", "b"}),
            ValueType.INTERVAL_SWEEP,
            id="interval:tags",
        ),
        pytest.param(
            "key=tag(tags=[a,b],sweep=interval(0,1))",
            "key",
            IntervalSweep(0.0, 1.0, {"a", "b"}),
            ValueType.INTERVAL_SWEEP,
            id="interval:tags:named",
        ),
        pytest.param(
            "key=str([1,2])", "key", ["1", "2"], ValueType.ELEMENT, id="casted_list",
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
    ret = OverridesParser.parse_rule(line, "override")
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
        (
            "~x",
            Override(
                type=OverrideType.DEL, key_or_group="x", value_type=None, _value=None,
            ),
        ),
        (
            "~x=10",
            Override(
                type=OverrideType.DEL,
                key_or_group="x",
                value_type=ValueType.ELEMENT,
                _value=10,
            ),
        ),
        (
            "~x=",
            Override(
                type=OverrideType.DEL,
                key_or_group="x",
                value_type=ValueType.ELEMENT,
                _value="",
            ),
        ),
    ],
)
def test_override_del(value: str, expected: Any) -> None:
    expected.input_line = value
    ret = OverridesParser.parse_rule(value, "override")
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
    parser = OverridesParser()
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
    ret = OverridesParser.parse_rule(override, "override")
    assert ret.get_key_element() == expected


@pytest.mark.parametrize(  # type: ignore
    "override,expected,space_after_sep",
    [
        pytest.param("key=value", "value", False, id="str"),
        pytest.param("key='value'", "'value'", False, id="single_quoted"),
        pytest.param('key="value"', '"value"', False, id="double_quoted"),
        pytest.param("key='שלום'", "'שלום'", False, id="quoted_unicode",),
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
    ret = OverridesParser.parse_rule(override, "override")
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
    ret = OverridesParser.parse_rule(override, "override")
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
        pytest.param("a", {"a"}, id="tag"),
        pytest.param("a,b,c", {"a", "b", "c"}, id="tags"),
        pytest.param("tags=[]", set(), id="tags"),
        pytest.param("tags=[a,b,c]", {"a", "b", "c"}, id="tags"),
    ],
)
def test_tag_list(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "tagList")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        pytest.param("range(1,10)", RangeSweep(start=1, stop=10), id="range"),
        pytest.param("range(1,10,2)", RangeSweep(start=1, stop=10, step=2), id="range"),
        pytest.param(
            "tag(tag1,tag2,range(1,2))",
            RangeSweep(start=1, stop=2, tags={"tag1", "tag2"}),
            id="range",
        ),
        pytest.param(
            "str(choice(1,2))", ChoiceSweep(list=["1", "2"]), id="str(choice(1,2))",
        ),
        pytest.param(
            "sort(choice(2,1))", ChoiceSweep(list=[1, 2]), id="sort(choice(2,1))",
        ),
    ],
)
def test_sweep(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "sweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        pytest.param(
            "tag(choice(a,b))", ChoiceSweep(list=["a", "b"]), id="choice:no_tags",
        ),
        pytest.param(
            "tag (choice(a,b))", ChoiceSweep(list=["a", "b"]), id="choice:no_tags",
        ),
        pytest.param(
            "tag(tag1,tag2,choice(a,b))",
            ChoiceSweep(list=["a", "b"], tags={"tag1", "tag2"}),
            id="choice",
        ),
    ],
)
def test_tagged_choice_sweep(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "taggedChoiceSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        pytest.param(
            "tag(range(1,2))", RangeSweep(start=1, stop=2), id="range:no_tags",
        ),
        pytest.param(
            "tag(tag1,tag2,range(1,2))",
            RangeSweep(start=1, stop=2, tags={"tag1", "tag2"}),
            id="range",
        ),
        pytest.param(
            "tag (tag1,tag2,range(1,2))",
            RangeSweep(start=1, stop=2, tags={"tag1", "tag2"}),
            id="range",
        ),
    ],
)
def test_tagged_range_sweep(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "taggedRangeSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        pytest.param(
            "tag(interval(0,2))", IntervalSweep(start=0, end=2), id="interval:no_tags",
        ),
        pytest.param(
            "tag(tag1,tag2,interval(0,2))",
            IntervalSweep(start=0, end=2, tags={"tag1", "tag2"}),
            id="interval",
        ),
    ],
)
def test_tagged_interval_sweep(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "taggedIntervalSweep")
    assert ret == expected


#  TODO: is this still needed after cleanup?
# @pytest.mark.parametrize(  # type: ignore
#     "value, expected",
#     [
#         pytest.param(
#             "sort(1,2,3)",
#             Sort(
#                 list_or_sweep=ChoiceSweep(simple_form=True, list=[1, 2, 3], tags=set()),
#                 reverse=False,
#             ),
#             id="sort:choice:simple",
#         ),
#         pytest.param(
#             "sort(choice(1,2,3))",
#             Sort(
#                 list_or_sweep=ChoiceSweep(
#                      list=[1, 2, 3], tags=set()
#                 ),
#                 reverse=False,
#             ),
#             id="sort:choice",
#         ),
#         pytest.param(
#             "sort(range(10,1))",
#             Sort(list_or_sweep=RangeSweep(start=10, stop=1), reverse=False),
#             id="sort:range",
#         ),
#     ],
# )
# def test_sweep_sort(value: str, expected: str) -> None:
#     ret = OverridesParser.parse_rule(value, "sweepSort")
#     assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        # list
        pytest.param(
            "sort([1,2,3])",
            Sort(list_or_sweep=[1, 2, 3], reverse=False),
            id="sort:list",
        ),
        pytest.param(
            "sort(list=[1,2,3])",
            Sort(list_or_sweep=[1, 2, 3], reverse=False),
            id="sort:list:named",
        ),
        pytest.param(
            "sort(list=[])",
            Sort(list_or_sweep=[], reverse=False),
            id="sort:list:named:empty",
        ),
        pytest.param(
            "sort(list=[1,2,3], reverse=True)",
            Sort(list_or_sweep=[1, 2, 3], reverse=True),
            id="sort:list:named:rev",
        ),
        # simple choice sweep
        pytest.param(
            "sort(1,2,3)",
            Sort(
                list_or_sweep=ChoiceSweep(simple_form=True, list=[1, 2, 3], tags=set()),
                reverse=False,
            ),
            id="sort:choice:simple",
        ),
        pytest.param(
            "sort(1,2,3,reverse=True)",
            Sort(
                list_or_sweep=ChoiceSweep(simple_form=True, list=[1, 2, 3], tags=set()),
                reverse=True,
            ),
            id="sort:choice:simple:rev",
        ),
        # choice sweep
        pytest.param(
            "sort(choice(1,2,3))",
            Sort(list_or_sweep=ChoiceSweep(list=[1, 2, 3], tags=set()), reverse=False,),
            id="sort:choice",
        ),
        pytest.param(
            "sort(choice(1,2,3), reverse=True)",
            Sort(list_or_sweep=ChoiceSweep(list=[1, 2, 3], tags=set()), reverse=True,),
            id="sort:choice:rev",
        ),
        pytest.param(
            "sort(tag(a,b,choice(1,2,3)), reverse=True)",
            Sort(
                list_or_sweep=ChoiceSweep(list=[1, 2, 3], tags={"a", "b"}),
                reverse=True,
            ),
            id="sort:tag:choice:rev",
        ),
        # range sweep
        pytest.param(
            "sort(float(range(10,1))))",
            Sort(list_or_sweep=RangeSweep(start=10.0, stop=1.0), reverse=False),
            id="sort:float:range",
        ),
        pytest.param(
            "sort(range(10,1))",
            Sort(list_or_sweep=RangeSweep(start=10, stop=1), reverse=False),
            id="sort:range",
        ),
        pytest.param(
            "sort(tag(a,b,range(1,10,2)), reverse=True)",
            Sort(
                list_or_sweep=RangeSweep(start=1, stop=10, step=2, tags={"a", "b"}),
                reverse=True,
            ),
            id="rev_sort:tag:range",
        ),
    ],
)
def test_sort(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "sort")
    assert ret == expected


# TODO: add shuffle example
@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        pytest.param(
            "sort([1,2,3])",
            Sort(list_or_sweep=[1, 2, 3], reverse=False),
            id="sort:list",
        ),
    ],
)
def test_ordering(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "ordering")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "cast_type",
    [
        pytest.param(CastType.INT, id="int-cast"),
        pytest.param(CastType.FLOAT, id="float-cast"),
        pytest.param(CastType.BOOL, id="bool-cast"),
        pytest.param(CastType.STR, id="str-cast"),
    ],
)
@pytest.mark.parametrize(  # type: ignore
    "value,expected_value",
    [
        pytest.param("x", "x", id="str"),
        pytest.param("10", 10, id="int"),
        pytest.param("3.14", 3.14, id="float"),
        pytest.param("true", True, id="bool"),
        pytest.param(
            "a,b", ChoiceSweep(simple_form=True, list=["a", "b"]), id="choice"
        ),
        pytest.param("choice(a,b)", ChoiceSweep(list=["a", "b"]), id="choice",),
        pytest.param("range(1,20,2)", RangeSweep(start=1, stop=20, step=2), id="range"),
        pytest.param(
            "interval(0.0,1.0)", IntervalSweep(start=0.0, end=1.0), id="interval"
        ),
        pytest.param("[a,b,c]", ["a", "b", "c"], id="list"),
        pytest.param("{a:10,b:20}", {"a": 10, "b": 20}, id="dict"),
    ],
)
def test_cast(value: str, expected_value: Any, cast_type: CastType) -> None:
    def cast(v: Any) -> str:
        if cast_type == CastType.INT:
            return f"int({v})"
        elif cast_type == CastType.FLOAT:
            return f"float({v})"
        elif cast_type == CastType.BOOL:
            return f"bool({v})"
        elif cast_type == CastType.STR:
            return f"str({v})"
        else:
            assert False

    cast_str = cast(value)
    ret1 = OverridesParser.parse_rule(cast_str, "cast")
    assert ret1 == Cast(cast_type=cast_type, value=expected_value, input_line=cast_str)


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
                    "Error evaluating `int(inf)` : cannot convert float infinity to integer"
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
                    "Error evaluating `int(nan)` : cannot convert float NaN to integer"
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
                    "Error evaluating `int('')` : invalid literal for int() with base 10: ''"
                ),
                float=CastResults.error(
                    "Error evaluating `float('')` : could not convert string to float: ''"
                ),
                str="",
                bool=CastResults.error(
                    "Error evaluating `bool('')` : Cannot cast '' to bool"
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
                    "Error evaluating `bool('10')` : Cannot cast '10' to bool"
                ),
            ),
            id="'10'",
        ),
        pytest.param(
            "'10.0'",
            CastResults(
                int=CastResults.error(
                    "Error evaluating `int('10.0')` : invalid literal for int() with base 10: '10.0'"
                ),
                float=10.0,
                str="10.0",
                bool=CastResults.error(
                    "Error evaluating `bool('10.0')` : Cannot cast '10.0' to bool"
                ),
            ),
            id="'10.0'",
        ),
        pytest.param(
            "'true'",
            CastResults(
                int=CastResults.error(
                    "Error evaluating `int('true')` : invalid literal for int() with base 10: 'true'"
                ),
                float=CastResults.error(
                    "Error evaluating `float('true')` : could not convert string to float: 'true'"
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
                    "Error evaluating `int('false')` : invalid literal for int() with base 10: 'false'"
                ),
                float=CastResults.error(
                    "Error evaluating `float('false')` : could not convert string to float: 'false'"
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
                    "Error evaluating `int('[1,2,3]')` : invalid literal for int() with base 10: '[1,2,3]'"
                ),
                float=CastResults.error(
                    "Error evaluating `float('[1,2,3]')` : could not convert string to float: '[1,2,3]'"
                ),
                str="[1,2,3]",
                bool=CastResults.error(
                    "Error evaluating `bool('[1,2,3]')` : Cannot cast '[1,2,3]' to bool"
                ),
            ),
            id="'[1,2,3]'",
        ),
        pytest.param(
            "'{a:10}'",
            CastResults(
                int=CastResults.error(
                    "Error evaluating `int('{a:10}')` : invalid literal for int() with base 10: '{a:10}'"
                ),
                float=CastResults.error(
                    "Error evaluating `float('{a:10}')` : could not convert string to float: '{a:10}'"
                ),
                str="{a:10}",
                bool=CastResults.error(
                    "Error evaluating `bool('{a:10}')` : Cannot cast '{a:10}' to bool"
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
                    "Error evaluating `int([a,1])` : invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "Error evaluating `float([a,1])` : could not convert string to float: 'a'"
                ),
                str=["a", "1"],
                bool=CastResults.error(
                    "Error evaluating `bool([a,1])` : Cannot cast 'a' to bool"
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
                    "Error evaluating `int({a:10,b:xyz})` : invalid literal for int() with base 10: 'xyz'"
                ),
                float=CastResults.error(
                    "Error evaluating `float({a:10,b:xyz})` : could not convert string to float: 'xyz'"
                ),
                str={"a": "10", "b": "xyz"},
                bool=CastResults.error(
                    "Error evaluating `bool({a:10,b:xyz})` : Cannot cast 'xyz' to bool"
                ),
            ),
            id="{a:10,b:xyz}",
        ),
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
            "choice(a,b)",
            CastResults(
                int=CastResults.error(
                    "Error evaluating `int(choice(a,b))` : invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "Error evaluating `float(choice(a,b))` : could not convert string to float: 'a'"
                ),
                str=ChoiceSweep(list=["a", "b"]),
                bool=CastResults.error(
                    "Error evaluating `bool(choice(a,b))` : Cannot cast 'a' to bool"
                ),
            ),
            id="choice(a,b)",
        ),
        pytest.param(
            "choice(1,a)",
            CastResults(
                int=CastResults.error(
                    "Error evaluating `int(choice(1,a))` : invalid literal for int() with base 10: 'a'"
                ),
                float=CastResults.error(
                    "Error evaluating `float(choice(1,a))` : could not convert string to float: 'a'"
                ),
                str=ChoiceSweep(list=["1", "a"]),
                bool=CastResults.error(
                    "Error evaluating `bool(choice(1,a))` : Cannot cast 'a' to bool"
                ),
            ),
            id="choice(1,a)",
        ),
        pytest.param(
            "interval(1.0, 2.0)",
            CastResults(
                int=CastResults.error(
                    "Intervals are always interpreted as floating-point intervals and cannot be casted"
                ),
                float=CastResults.error(
                    "Intervals are always interpreted as floating-point intervals and cannot be casted"
                ),
                str=CastResults.error(
                    "Intervals are always interpreted as floating-point intervals and cannot be casted"
                ),
                bool=CastResults.error(
                    "Intervals are always interpreted as floating-point intervals and cannot be casted"
                ),
            ),
            id="interval(1.0, 2.0)",
        ),
        pytest.param(
            "range(1,10)",
            CastResults(
                int=RangeSweep(start=1, stop=10, step=1),
                float=RangeSweep(start=1.0, stop=10.0, step=1.0),
                str=CastResults.error("Range can only be casted to int or float"),
                bool=CastResults.error("Range can only be casted to int or float"),
            ),
            id="range(1,10)",
        ),
        pytest.param(
            "range(1.0,10.0)",
            CastResults(
                int=RangeSweep(start=1, stop=10, step=1),
                float=RangeSweep(start=1.0, stop=10.0, step=1.0),
                str=CastResults.error("Range can only be casted to int or float"),
                bool=CastResults.error("Range can only be casted to int or float"),
            ),
            id="range(1.0,10.0)",
        ),
    ],
)
def test_cast_conversions(value: Any, expected_value: Any) -> None:
    for cast_type in (CastType.INT, CastType.FLOAT, CastType.BOOL, CastType.STR):
        field = cast_type.name.lower()
        cast_str = f"{field}({value})"
        ret = OverridesParser.parse_rule(cast_str, "cast")
        expected = getattr(expected_value, field)
        if isinstance(expected, RaisesContext):
            with expected:
                ret.convert()
        else:
            result = ret.convert()
            assert eq(result, expected), f"{field} cast result mismatch"
            assert type(result) == type(
                expected
            ), f"{field}({value}) cast type mismatch"
