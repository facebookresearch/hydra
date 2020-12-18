# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pytest import mark, param

from hydra._internal.grammar.utils import escape_special_characters


@mark.parametrize(  # type: ignore
    ("s", "expected"),
    [
        param("abc", "abc", id="no_esc"),
        param("\\", "\\\\", id="esc_backslash"),
        param("\\\\\\", "\\\\\\\\\\\\", id="esc_backslash_x3"),
        param("()", "\\(\\)", id="esc_parentheses"),
        param("[]", "\\[\\]", id="esc_brackets"),
        param("{}", "\\{\\}", id="esc_braces"),
        param(":=,", "\\:\\=\\,", id="esc_symbols"),
        param("  \t", "\\ \\ \\\t", id="esc_ws"),
        param(
            "ab\\(cd{ef}[gh]): ij,kl\t",
            "ab\\\\\\(cd\\{ef\\}\\[gh\\]\\)\\:\\ ij\\,kl\\\t",
            id="esc_mixed",
        ),
    ],
)
def test_escape_special_characters(s: str, expected: str) -> None:
    escaped = escape_special_characters(s)
    assert escaped == expected
