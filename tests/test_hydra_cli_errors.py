# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from pathlib import Path
from typing import Any

from hydra.test_utils.test_utils import (
    chdir_hydra_root,
    normalize_newlines,
    run_with_error,
)

from pytest import mark, param

chdir_hydra_root()


@mark.parametrize(
    "override,expected",
    [
        param(
            "+key=int(",
            """Error when parsing index: 1, string: +key=int( out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_parse_error_in_0', '+key=int(', 'hydra.mode=RUN'].
no viable alternative at input 'int('""",
            id="parse_error_in_function",
        ),
        param(
            "+key=sort()",
            """Error when parsing index: 1, string: +key=sort() out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_empty_sort_0', '+key=sort()', 'hydra.mode=RUN'].
Error parsing override '+key=sort()'
ValueError while evaluating 'sort()': empty sort input""",
            id="empty_sort",
        ),
        param(
            "key=sort(interval(1,10))",
            """Error when parsing index: 1, string: key=sort(interval(1,10)) out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_sort_interval_0', 'key=sort(interval(1,10))', 'hydra.mode=RUN'].
Error parsing override 'key=sort(interval(1,10))'
TypeError while evaluating 'sort(interval(1,10))': mismatch type argument args[0]""",
            id="sort_interval",
        ),
        param(
            "+key=choice()",
            """Error when parsing index: 1, string: +key=choice() out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_empty_choice0_0', '+key=choice()', 'hydra.mode=RUN'].
Error parsing override '+key=choice()'
ValueError while evaluating 'choice()': empty choice is not legal""",
            id="empty choice",
        ),
        param(
            "+key=extend_list(1, 2, 3)",
            """Error when parsing index: 1, string: +key=extend_list(1, 2, 3) out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_plus_key_extend0', '+key=extend_list(1, 2, 3)', 'hydra.mode=RUN'].
Error parsing override '+key=extend_list(1, 2, 3)'
Trying to use override symbols when extending a list""",
            id="plus key extend_list",
        ),
        param(
            "key={inner_key=extend_list(1, 2, 3)}",
            """Error when parsing index: 1, string: key={inner_key=extend_list(1, 2, 3)} out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_embedded_extend0', 'key={inner_key=extend_list(1, 2, 3)}', 'hydra.mode=RUN']. 
no viable alternative at input '{inner_key='
See https://hydra.cc/docs/1.2/advanced/override_grammar/basic for details

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.""",
            id="embedded extend_list",
        ),
        param(
            ["+key=choice(choice(a,b))", "-m"],
            """Error when parsing index: 1, string: +key=choice(choice(a,b)) out of ['hydra.sweep.dir=/tmp/pytest-of-runner/pytest-0/test_cli_error_empty_choice1_0', '+key=choice(choice(a,b))', 'hydra.mode=MULTIRUN'].
Error parsing override '+key=choice(choice(a,b))'
ValueError while evaluating 'choice(choice(a,b))': nesting choices is not supported
See https://hydra.cc/docs/1.2/advanced/override_grammar/basic for details

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
""",
            id="empty choice",
        ),
        param(
            "--config-dir=/dir/not/found",
            f"""Additional config directory '{Path('/dir/not/found').absolute()}' not found

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
""",
            id="config_dir_not_found",
        ),
    ],
)
def test_cli_error(tmpdir: Any, monkeypatch: Any, override: Any, expected: str) -> None:
    monkeypatch.chdir("tests/test_apps/app_without_config/")
    if isinstance(override, str):
        override = [override]
    cmd = ["my_app.py", "hydra.sweep.dir=" + str(tmpdir)] + override
    ret = normalize_newlines(run_with_error(cmd))
    assert (
        re.search("^" + re.escape(normalize_newlines(expected.strip())), ret)
        is not None
    ), (
        f"Result:"
        f"\n---"
        f"\n{ret}"
        f"\n---"
        f"\nDid not match expected:"
        f"\n---"
        f"\n{expected}"
        f"\n---"
    )
