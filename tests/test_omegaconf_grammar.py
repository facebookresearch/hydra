# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import math
from typing import Any, List, Tuple

import pytest
from omegaconf import OmegaConf

from hydra.errors import HydraException

from .test_overrides_parser import parse_rule

# Dummy assignments to allow copy-paste of `TEST_CONFIG_DATA` below from
# OmegaConf, and properly identify parsing error cases.
# (should be replaced by imports from OmegaConf in the future)
GrammarSyntaxError = HydraException
# The OmegaConf exceptions below cannot be identified at parsing time.
ConfigKeyError = GrammarTypeError = UnsupportedInterpolationType = None

# DO NOT EDIT `TEST_CONFIG_DATA`!
# It should be copied regularly from OmegaConf to ensure Hydra's grammar is able
# to parse similar expressions as OmegaConf's.
TEST_CONFIG_DATA: List[Tuple[str, Any, Any]] = [
    # Not interpolations (just building blocks for below).
    ("prim_str", "hi", ...),
    ("prim_str_space", "hello world", ...),
    ("test_str", "test", ...),
    ("test_str_partial", "st", ...),
    ("prim_list", [-1, "a", 1.1], ...),
    ("prim_dict", {"a": 0, "b": 1}, ...),
    ("FalsE", {"TruE": True}, ...),  # used to test keys with bool names
    ("None", {"True": 1}, ...),  # used to test keys with null-like names
    ("0", 42, ...),  # used to test keys with int names
    ("1", {"2": 1337}, ...),  # used to test dot-path with int keys
    # Special keywords.
    ("null", "${test:null}", None),
    ("true", "${test:TrUe}", True),
    ("false", "${test:falsE}", False),
    ("true_false", "${test:true_false}", "true_false"),
    # Integers.
    ("int", "${test:123}", 123),
    ("int_pos", "${test:+123}", 123),
    ("int_neg", "${test:-123}", -123),
    ("int_underscore", "${test:1_000}", 1000),
    ("int_bad_underscore_1", "${test:1_000_}", "1_000_"),
    ("int_bad_underscore_2", "${test:1__000}", "1__000"),
    ("int_bad_underscore_3", "${test:_1000}", "_1000"),
    ("int_bad_zero_start", "${test:007}", "007"),
    # Floats.
    ("float", "${test:1.1}", 1.1),
    ("float_no_int", "${test:.1}", 0.1),
    ("float_no_decimal", "${test:1.}", 1.0),
    ("float_plus", "${test:+1.01}", 1.01),
    ("float_minus", "${test:-.2}", -0.2),
    ("float_underscore", "${test:1.1_1}", 1.11),
    ("float_bad_1", "${test:1.+2}", "1.+2"),
    ("float_bad_2", r"${test:1\.2}", r"1\.2"),
    ("float_bad_3", "${test:1.2_}", "1.2_"),
    ("float_exp_1", "${test:-1e2}", -100.0),
    ("float_exp_2", "${test:+1E-2}", 0.01),
    ("float_exp_3", "${test:1_0e1_0}", 10e10),
    ("float_exp_4", "${test:1.07e+2}", 107.0),
    ("float_exp_5", "${test:1e+03}", 1000.0),
    ("float_exp_bad_1", "${test:e-2}", "e-2"),
    ("float_exp_bad_2", "${test:01e2}", "01e2"),
    ("float_inf", "${test:inf}", math.inf),
    ("float_plus_inf", "${test:+inf}", math.inf),
    ("float_minus_inf", "${test:-inf}", -math.inf),
    ("float_nan", "${test:nan}", math.nan),
    ("float_plus_nan", "${test:+nan}", math.nan),
    ("float_minus_nan", "${test:-nan}", math.nan),
    # Node interpolations.
    ("dict_access", "${prim_dict.a}", 0),
    ("list_access_1", "${prim_list.0}", -1),
    ("list_access_2", "${test:${prim_list.1},${prim_list.2}}", ["a", 1.1]),
    ("list_access_underscore", "${prim_list.1_000}", ConfigKeyError),  # "working"
    ("list_access_bad_negative", "${prim_list.-1}", GrammarSyntaxError),
    ("dict_access_list_like_1", "${0}", 42),
    ("dict_access_list_like_2", "${1.2}", 1337),
    ("bool_like_keys", "${FalsE.TruE}", True),
    ("null_like_key_ok", "${None.True}", 1),
    ("null_like_key_bad_case", "${null.True}", ConfigKeyError),
    ("null_like_key_quoted_1", "${'None'.'True'}", GrammarSyntaxError),
    ("null_like_key_quoted_2", "${'None.True'}", GrammarSyntaxError),
    ("dotpath_bad_type", "${prim_dict.${float}}", GrammarTypeError),
    # Resolver interpolations.
    ("no_args", "${test:}", []),
    ("space_in_args", "${test:a, b c}", ["a", "b c"]),
    ("list_as_input", "${test:[a, b], 0, [1.1]}", [["a", "b"], 0, [1.1]]),
    ("dict_as_input", "${test:{a: 1.1, b: b}}", {"a": 1.1, "b": "b"}),
    ("dict_as_input_quotes", "${test:{'a': 1.1, b: b}}", GrammarSyntaxError),
    ("dict_typo_colons", "${test:{a: 1.1, b:: b}}", {"a": 1.1, "b": ": b"}),
    ("dict_list_as_key", "${test:{[0]: 1}}", GrammarSyntaxError),
    ("missing_resolver", "${MiSsInG_ReSoLvEr:0}", UnsupportedInterpolationType),
    ("non_str_resolver", "${${bool}:}", GrammarTypeError),
    ("resolver_special", "${infnannulltruefalse:}", "ok"),
    # Env resolver (limited: more tests in `test_env_values_are_typed()`).
    ("env_int", "${env:OMEGACONF_TEST_ENV_INT}", 123),
    ("env_missing_str", "${env:OMEGACONF_TEST_MISSING,miss}", "miss"),
    ("env_missing_int", "${env:OMEGACONF_TEST_MISSING,123}", 123),
    ("env_missing_quoted_int", "${env:OMEGACONF_TEST_MISSING,'123'}", "123"),
    # Resolvers with special names (note: such resolvers are registered).
    ("bool_resolver_1", "${True:1,2,3}", ["True", 1, 2, 3]),
    ("bool_resolver_2", "${FALSE:1,2,3}", ["FALSE", 1, 2, 3]),
    ("null_resolver", "${null:1,2,3}", ["null", 1, 2, 3]),
    ("int_resolver_quoted", "${'0':1,2,3}", GrammarSyntaxError),
    ("int_resolver_noquote", "${0:1,2,3}", GrammarSyntaxError),
    ("float_resolver_quoted", "${'1.1':1,2,3}", GrammarSyntaxError),
    ("float_resolver_noquote", "${1.1:1,2,3}", GrammarSyntaxError),
    ("float_resolver_exp", "${1e1:1,2,3}", GrammarSyntaxError),
    # String interpolations (top-level).
    ("str_top_basic", "bonjour ${prim_str}", "bonjour hi"),
    ("str_top_quotes_single_1", "'bonjour ${prim_str}'", "'bonjour hi'"),
    (
        "str_top_quotes_single_2",
        "'Bonjour ${prim_str}', I said.",
        "'Bonjour hi', I said.",
    ),
    ("str_top_quotes_double_1", '"bonjour ${prim_str}"', '"bonjour hi"'),
    (
        "str_top_quotes_double_2",
        '"Bonjour ${prim_str}", I said.',
        '"Bonjour hi", I said.',
    ),
    ("str_top_missing_end_quote_single", "'${prim_str}", "'hi"),
    ("str_top_missing_end_quote_double", '"${prim_str}', '"hi'),
    ("str_top_missing_start_quote_double", '${prim_str}"', 'hi"'),
    ("str_top_missing_start_quote_single", "${prim_str}'", "hi'"),
    ("str_top_middle_quote_single", "I'd like ${prim_str}", "I'd like hi"),
    ("str_top_middle_quote_double", 'I"d like ${prim_str}', 'I"d like hi'),
    ("str_top_middle_quotes_single", "I like '${prim_str}'", "I like 'hi'"),
    ("str_top_middle_quotes_double", 'I like "${prim_str}"', 'I like "hi"'),
    ("str_top_any_char", "${prim_str} !@\\#$%^&*})][({,/?;", "hi !@\\#$%^&*})][({,/?;"),
    ("str_top_esc_inter", r"Esc: \${prim_str}", "Esc: ${prim_str}"),
    ("str_top_esc_inter_wrong_1", r"Wrong: $\{prim_str\}", r"Wrong: $\{prim_str\}"),
    ("str_top_esc_inter_wrong_2", r"Wrong: \${prim_str\}", r"Wrong: ${prim_str\}"),
    ("str_top_esc_backslash", r"Esc: \\${prim_str}", r"Esc: \hi"),
    ("str_top_quoted_braces_wrong", r"Wrong: \{${prim_str}\}", r"Wrong: \{hi\}"),
    ("str_top_leading_dollars", r"$$${prim_str}", "$$hi"),
    ("str_top_trailing_dollars", r"${prim_str}$$$$", "hi$$$$"),
    ("str_top_leading_escapes", r"\\\\\${prim_str}", r"\\${prim_str}"),
    ("str_top_middle_escapes", r"abc\\\\\${prim_str}", r"abc\\${prim_str}"),
    ("str_top_trailing_escapes", "${prim_str}" + "\\" * 5, "hi" + "\\" * 3),
    ("str_top_concat_interpolations", "${true}${float}", "True1.1"),
    # Quoted strings (within interpolations).
    ("str_quoted_single", "${test:'!@#$%^&*()[]:.,\"'}", '!@#$%^&*()[]:.,"'),
    ("str_quoted_double", '${test:"!@#$%^&*()[]:.,\'"}', "!@#$%^&*()[]:.,'"),
    ("str_quoted_outer_ws_single", "${test: '  a \t'}", "  a \t"),
    ("str_quoted_outer_ws_double", '${test: "  a \t"}', "  a \t"),
    ("str_quoted_int", "${test:'123'}", "123"),
    ("str_quoted_null", "${test:'null'}", "null"),
    ("str_quoted_bool", "${test:'truE', \"FalSe\"}", ["truE", "FalSe"]),
    ("str_quoted_list", "${test:'[a,b, c]'}", "[a,b, c]"),
    ("str_quoted_dict", '${test:"{a:b, c: d}"}', "{a:b, c: d}"),
    ("str_quoted_inter", "${test:'${null}'}", "None"),
    (
        "str_quoted_inter_nested",
        "${test:'${test:\"L=${prim_list}\"}'}",
        "L=[-1, 'a', 1.1]",
    ),
    ("str_quoted_nested", r"${test:'AB${test:\'CD${test:\\'EF\\'}GH\'}'}", "ABCDEFGH"),
    ("str_quoted_esc_single_1", r"${test:'ab\'cd\'\'${prim_str}'}", "ab'cd''hi"),
    ("str_quoted_esc_single_2", "${test:'\"\\\\\\\\\\${foo}\\ '}", r'"\${foo}\ '),
    ("str_quoted_esc_double_1", r'${test:"ab\"cd\"\"${prim_str}"}', 'ab"cd""hi'),
    ("str_quoted_esc_double_2", '${test:"\'\\\\\\\\\\${foo}\\ "}', r"'\${foo}\ "),
    ("str_quoted_backslash_noesc_single", r"${test:'a\b'}", r"a\b"),
    ("str_quoted_backslash_noesc_double", r'${test:"a\b"}', r"a\b"),
    ("str_quoted_concat_bad_1", '${test:"Hi "${prim_str}}', GrammarSyntaxError),
    ("str_quoted_concat_bad_2", "${test:'Hi''there'}", GrammarSyntaxError),
    ("str_quoted_too_many_1", "${test:''a'}", GrammarSyntaxError),
    ("str_quoted_too_many_2", "${test:'a''}", GrammarSyntaxError),
    ("str_quoted_too_many_3", "${test:''a''}", GrammarSyntaxError),
    # Unquoted strings (within interpolations).
    ("str_legal", "${test:a/-\\+.$*, \\\\}", ["a/-\\+.$*", "\\"]),
    ("str_illegal_1", "${test:a,=b}", GrammarSyntaxError),
    ("str_illegal_2", f"${{test:{chr(200)}}}", GrammarSyntaxError),
    ("str_illegal_3", f"${{test:{chr(129299)}}}", GrammarSyntaxError),
    ("str_dot", "${test:.}", "."),
    ("str_dollar", "${test:$}", "$"),
    ("str_colon", "${test::}", ":"),
    ("str_dollar_and_inter", "${test:$$${prim_str}}", "$$hi"),
    ("str_ws_1", "${test:hello world}", "hello world"),
    ("str_ws_2", "${test:a b\tc  \t\t  d}", "a b\tc  \t\t  d"),
    ("str_inter", "${test:hi_${prim_str_space}}", "hi_hello world"),
    ("str_esc_ws_1", r"${test:\ hello\ world\ }", " hello world "),
    ("str_esc_ws_2", "${test:\\ \\\t,\\\t}", [" \t", "\t"]),
    ("str_esc_comma", r"${test:hello\, world}", "hello, world"),
    ("str_esc_colon", r"${test:a\:b}", "a:b"),
    ("str_esc_equal", r"${test:a\=b}", "a=b"),
    ("str_esc_parentheses", r"${test:\(foo\)}", "(foo)"),
    ("str_esc_brackets", r"${test:\[foo\]}", "[foo]"),
    ("str_esc_braces", r"${test:\{foo\}}", "{foo}"),
    ("str_esc_backslash", r"${test:\\}", "\\"),
    ("str_backslash_noesc", r"${test:ab\cd}", r"ab\cd"),
    ("str_esc_illegal_1", r"${test:\#}", GrammarSyntaxError),
    ("str_esc_illegal_2", r"${test:\${foo\}}", GrammarSyntaxError),
    ("str_esc_illegal_3", "${test:\\'\\\"}", GrammarSyntaxError),
    # Whitespaces.
    ("ws_toplevel_1", "  \tab  ${prim_str} cd  \t", "  \tab  hi cd  \t"),
    ("ws_toplevel_2", "\t${test:foo}\t${float}\t${null}\t", "\tfoo\t1.1\tNone\t"),
    ("ws_inter_node_outer", "${ \tprim_dict.a  \t}", 0),
    ("ws_inter_node_around_dot", "${prim_dict .\ta}", 0),
    ("ws_inter_node_inside_id", "${prim _ dict.a}", GrammarSyntaxError),
    ("ws_inter_res_outer", "${\t test:foo\t  }", "foo"),
    ("ws_inter_res_around_colon", "${test\t  : \tfoo}", "foo"),
    ("ws_inter_res_inside_id", "${te st:foo}", GrammarSyntaxError),
    ("ws_inter_res_inside_args", "${test:f o o}", "f o o"),
    ("ws_list", "${test:[\t a,   b,  ''\t  ]}", ["a", "b", ""]),
    ("ws_dict", "${test:{\t a   : 1\t  , b:  \t''}}", {"a": 1, "b": ""}),
    ("ws_quoted_single", "${test:  \t'foo'\t }", "foo"),
    ("ws_quoted_double", '${test:  \t"foo"\t }', "foo"),
    # Lists and dictionaries.
    ("list", "${test:[0, 1]}", [0, 1]),
    (
        "dict",
        "${test:{x: 1, a: 'b', y: 1e2, null2: 0.1, true3: false, inf4: true}}",
        {"x": 1, "a": "b", "y": 100.0, "null2": 0.1, "true3": False, "inf4": True},
    ),
    (
        "dict_interpolation_key_forbidden",
        "${test:{${prim_str}: 0, ${null}: 1, ${int}: 2}}",
        GrammarSyntaxError,
    ),
    (
        "dict_quoted_key",
        "${test:{0: 1, 'a': 'b', 1.1: 1e2, null: 0.1, true: false, -inf: true}}",
        GrammarSyntaxError,
    ),
    ("dict_int_key", "${test:{0: 0}}", GrammarSyntaxError),
    ("dict_float_key", "${test:{1.1: 0}}", GrammarSyntaxError),
    ("dict_nan_key_1", "${test:{nan: 0}}", GrammarSyntaxError),
    ("dict_nan_key_2", "${test:{${test:nan}: 0}}", GrammarSyntaxError),
    ("dict_null_key", "${test:{null: 0}}", GrammarSyntaxError),
    ("dict_bool_key", "${test:{true: true, false: 'false'}}", GrammarSyntaxError),
    ("empty_dict_list", "${test:[],{}}", [[], {}]),
    (
        "structured_mixed",
        "${test:10,str,3.14,true,false,inf,[1,2,3], 'quoted', \"quoted\", 'a,b,c'}",
        [
            10,
            "str",
            3.14,
            True,
            False,
            math.inf,
            [1, 2, 3],
            "quoted",
            "quoted",
            "a,b,c",
        ],
    ),
    (
        "structured_deep",
        "${test:{null0: [0, 3.14, false], true1: {a: [0, 1, 2], b: {}}}}",
        {"null0": [0, 3.14, False], "true1": {"a": [0, 1, 2], "b": {}}},
    ),
    # Chained interpolations.
    ("null_chain", "${null}", None),
    ("true_chain", "${true}", True),
    ("int_chain", "${int}", 123),
    ("list_chain_bad_1", "${${prim_list}.0}", GrammarTypeError),
    ("dict_chain_bad_1", "${${prim_dict}.a}", GrammarTypeError),
    ("prim_list_copy", "${prim_list}", OmegaConf.create([-1, "a", 1.1])),
    ("prim_dict_copy", "${prim_dict}", OmegaConf.create({"a": 0, "b": 1})),
    ("list_chain", "${prim_list_copy.0}", -1),
    ("dict_chain", "${prim_dict_copy.a}", 0),
    # Nested interpolations.
    ("ref_prim_str", "prim_str", ...),
    ("nested_simple", "${${ref_prim_str}}", "hi"),
    ("plans", {"plan A": "awesome plan", "plan B": "crappy plan"}, ...),
    ("selected_plan", "plan A", ...),
    (
        "nested_dotted",
        r"I choose: ${plans.${selected_plan}}",
        "I choose: awesome plan",
    ),
    ("nested_deep", "${test:${${test:${ref_prim_str}}}}", "hi"),
    ("nested_resolver", "${${test_str}:a, b, c}", ["a", "b", "c"]),
    (
        "nested_resolver_combined_illegal",
        "${te${test_str_partial}:a, b, c}",
        GrammarSyntaxError,
    ),
    ("nested_args", "${test:${prim_str}, ${null}, ${int}}", ["hi", None, 123]),
    # Relative interpolations.
    (
        "relative",
        {"foo": 0, "one_dot": "${.foo}", "two_dots": "${..prim_dict.b}"},
        OmegaConf.create({"foo": 0, "one_dot": 0, "two_dots": 1}),
    ),
    ("relative_nested", "${test:${.relative.foo}}", 0),
    # Unmatched braces.
    ("missing_brace_1", "${test:${prim_str}", GrammarSyntaxError),
    ("missing_brace_2", "${${test:prim_str}", GrammarSyntaxError),
    ("extra_brace", "${test:${prim_str}}}", "hi}"),
]


@pytest.mark.parametrize(  # type: ignore
    "definition, is_exception",
    [
        # We only keep the `definition` field because we only care about the ability
        # to build the parse tree for the given expression, not resolve it.
        pytest.param(definition, expected is HydraException, id=key)
        for key, definition, expected in TEST_CONFIG_DATA
        # We also filter out expressions that are not direct interpolations because
        # Hydra's grammar is not meant to parse OmegaConf's top-level strings.
        if isinstance(definition, str)
        and definition.startswith("${")
        and definition.endswith("}")
        and key
        != "extra_brace"  # skip this one, it is valid in OmegaConf but not Hydra
    ],
)
def test_omegaconf_interpolations(definition: str, is_exception: bool) -> None:
    def run() -> None:
        parse_rule(value=definition, rule_name="interpolation")

    if is_exception:
        with pytest.raises(HydraException):
            run()
    else:
        run()
