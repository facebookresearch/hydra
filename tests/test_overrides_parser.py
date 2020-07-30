# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
import re
from typing import Any, List

import pytest

from hydra.core.override_parser.overrides_parser import (
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
    ValueType,
)
from hydra.errors import HydraException


def eq(item1: Any, item2: Any) -> bool:
    if isinstance(item1, float) and isinstance(item2, float):
        return item1 == item2 or math.isnan(item1) and math.isnan(item2)
    else:
        return item1 == item2  # type: ignore


# element:
#       primitive
#     | listValue
#     | dictValue
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
            "1,2,3", ChoiceSweep(choices=[1, 2, 3], simple_form=True), id="sweep:int"
        ),
        pytest.param(
            "1, 2, 3",
            ChoiceSweep(choices=[1, 2, 3], simple_form=True),
            id="sweep:int_ws",
        ),
        pytest.param(
            "${a}, ${b}, ${c}",
            ChoiceSweep(choices=["${a}", "${b}", "${c}"], simple_form=True),
            id="sweep:interpolations",
        ),
        pytest.param(
            "[a,b],[c,d]",
            ChoiceSweep(choices=[["a", "b"], ["c", "d"]], simple_form=True),
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
    ],
)
def test_value(value: str, expected: Any) -> None:
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
        pytest.param(
            "choice(a)",
            ChoiceSweep(choices=["a"], simple_form=False),
            id="sweep:choice(a)",
        ),
        pytest.param(
            "choice(a,b)",
            ChoiceSweep(choices=["a", "b"], simple_form=False),
            id="sweep:choice(a,b)",
        ),
        pytest.param(
            "choice( 10 , 20 )",
            ChoiceSweep(choices=[10, 20], simple_form=False),
            id="sweep:choice( 10 , 20 )",
        ),
    ],
)
def test_choice_sweep_parsing(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "choiceSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param(
            "a,b",
            ChoiceSweep(choices=["a", "b"], simple_form=True),
            id="sweep:choice(a)",
        ),
        pytest.param(
            "a , b",
            ChoiceSweep(choices=["a", "b"], simple_form=True),
            id="sweep:choice(a)",
        ),
    ],
)
def test_simple_choice_sweep_parsing(value: str, expected: Any) -> None:
    ret = OverridesParser.parse_rule(value, "simpleChoiceSweep")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value,expected",
    [
        pytest.param("range(10,11)", RangeSweep(start=10, stop=11, step=1), id="ints"),
        pytest.param(
            "range(1,10,2)", RangeSweep(start=1, stop=10, step=2), id="ints_with_ste"
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
            "interval(10,11)", IntervalSweep(start=10.0, end=11.0), id="ints_autocast"
        ),
        pytest.param(
            "interval(2.72,3.14)", IntervalSweep(start=2.72, end=3.14), id="floats",
        ),
    ],
)
def test_interval_sweep_parsing(value: str, expected: Any) -> None:
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
    "value,expected_key,expected_value,expected_value_type,tags",
    [
        pytest.param(
            "key=value", "key", "value", ValueType.ELEMENT, set(), id="simple_value"
        ),
        pytest.param(
            "key='1,2,3'",
            "key",
            QuotedString(text="1,2,3", quote=Quote.single),
            ValueType.ELEMENT,
            set(),
            id="simple_value",
        ),
        pytest.param(
            "key='שלום'",
            "key",
            QuotedString(text="שלום", quote=Quote.single),
            ValueType.ELEMENT,
            set(),
            id="unicode",
        ),
        pytest.param(
            "key=value-123", "key", "value-123", ValueType.ELEMENT, set(), id="id-int"
        ),
        pytest.param(
            "key=value-1.0", "key", "value-1.0", ValueType.ELEMENT, set(), id="id-float"
        ),
        pytest.param(
            "key=value-true",
            "key",
            "value-true",
            ValueType.ELEMENT,
            set(),
            id="id-bool",
        ),
        pytest.param("key=", "key", "", ValueType.ELEMENT, set(), id="empty_value"),
        pytest.param(
            "key='foo,bar'",
            "key",
            QuotedString(text="foo,bar", quote=Quote.single),
            ValueType.ELEMENT,
            set(),
            id="quoted_value",
        ),
        pytest.param(
            "key='foo , bar'",
            "key",
            QuotedString(text="foo , bar", quote=Quote.single),
            ValueType.ELEMENT,
            set(),
            id="quoted_value",
        ),
        pytest.param(
            "key=1,2,3",
            "key",
            [1, 2, 3],
            ValueType.SIMPLE_CHOICE_SWEEP,
            set(),
            id="choice_sweep",
        ),
        pytest.param(
            "key=choice(1)",
            "key",
            [1],
            ValueType.CHOICE_SWEEP,
            set(),
            id="choice_sweep_1_element",
        ),
        pytest.param(
            "key=choice(1,2,3)",
            "key",
            [1, 2, 3],
            ValueType.CHOICE_SWEEP,
            set(),
            id="choice_sweep",
        ),
        pytest.param(
            "key=[1,2],[3,4]",
            "key",
            [[1, 2], [3, 4]],
            ValueType.SIMPLE_CHOICE_SWEEP,
            set(),
            id="choice_sweep",
        ),
        pytest.param(
            "key=choice([1,2],[3,4])",
            "key",
            [[1, 2], [3, 4]],
            ValueType.CHOICE_SWEEP,
            set(),
            id="choice_sweep",
        ),
        pytest.param(
            "key=range(0,2)",
            "key",
            range(0, 2),
            ValueType.RANGE_SWEEP,
            set(),
            id="range_sweep",
        ),
        pytest.param(
            "key=range(1,5,2)",
            "key",
            range(1, 5, 2),
            ValueType.RANGE_SWEEP,
            set(),
            id="range_sweep",
        ),
        pytest.param(
            "key=range(10.0, 11.0)",
            "key",
            FloatRange(10, 11.0, 1),
            ValueType.RANGE_SWEEP,
            set(),
            id="range_sweep",
        ),
        pytest.param(
            "key=interval(0,1)",
            "key",
            IntervalSweep(0.0, 1.0),
            ValueType.INTERVAL_SWEEP,
            set(),
            id="range_sweep",
        ),
        # tags
        pytest.param(
            "key=tag(a,b,choice([1,2],[3,4]))",
            "key",
            [[1, 2], [3, 4]],
            ValueType.CHOICE_SWEEP,
            {"a", "b"},
            id="choice_sweep:tags",
        ),
        pytest.param(
            "key=tag(a,b,interval(0,1))",
            "key",
            IntervalSweep(0.0, 1.0, {"a", "b"}),
            ValueType.INTERVAL_SWEEP,
            {"a", "b"},
            id="range_sweep:tags",
        ),
        pytest.param(
            "key=tag(a,b,interval(0,1))",
            "key",
            IntervalSweep(0.0, 1.0, {"a", "b"}),
            ValueType.INTERVAL_SWEEP,
            {"a", "b"},
            id="range_sweep:tags",
        ),
    ],
)
def test_parse_override(
    prefix: str,
    value: str,
    override_type: OverrideType,
    expected_key: str,
    expected_value: Any,
    expected_value_type: ValueType,
    tags: Any,
) -> None:
    line = prefix + value
    ret = OverridesParser.parse_rule(line, "override")
    expected = Override(
        input_line=line,
        type=override_type,
        key_or_group=expected_key,
        _value=expected_value,
        value_type=expected_value_type,
        tags=tags,
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
            _value=["a", "b", "c"],
            input_line=overrides[2],
        ),
        Override(
            type=OverrideType.CHANGE,
            key_or_group="z",
            value_type=ValueType.CHOICE_SWEEP,
            _value=["a", "b", "c"],
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
    assert ret.get_value_element(space_after_sep=space_after_sep) == expected


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
    ],
)
def test_tag_list(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "tagList")
    assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "value, expected",
    [
        pytest.param(
            "choice(a,b)",
            ChoiceSweep(choices=["a", "b"], simple_form=False),
            id="choice",
        ),
        pytest.param("range(1,10)", RangeSweep(start=1, stop=10), id="range"),
        pytest.param("range(1,10,2)", RangeSweep(start=1, stop=10, step=2), id="range"),
        pytest.param(
            "interval(0,3.14)", IntervalSweep(start=0, end=3.14), id="interval"
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
            "tag(choice(a,b))",
            ChoiceSweep(simple_form=False, choices=["a", "b"]),
            id="choice:no_tags",
        ),
        pytest.param(
            "tag(tag1,tag2,choice(a,b))",
            ChoiceSweep(simple_form=False, choices=["a", "b"], tags={"tag1", "tag2"}),
            id="choice",
        ),
        pytest.param(
            "tag(range(1,2))", RangeSweep(start=1, stop=2), id="range:no_tags",
        ),
        pytest.param(
            "tag(tag1,tag2,range(1,2))",
            RangeSweep(start=1, stop=2, tags={"tag1", "tag2"}),
            id="range",
        ),
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
def test_tagged_sweep(value: str, expected: str) -> None:
    ret = OverridesParser.parse_rule(value, "taggedSweep")
    assert ret == expected
