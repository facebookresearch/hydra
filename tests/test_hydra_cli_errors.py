# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from pathlib import Path
from typing import Any

import pytest

from hydra.test_utils.test_utils import (
    chdir_hydra_root,
    normalize_newlines,
    run_with_error,
)

chdir_hydra_root()


@pytest.mark.parametrize(  # type:ignore
    "override,expected",
    [
        pytest.param(
            "+key=int(",
            "no viable alternative at input 'int('",
            id="parse_error_in_function",
        ),
        pytest.param(
            "+key=sort()",
            """Error parsing override '+key=sort()'
ValueError while evaluating 'sort()': empty sort input""",
            id="empty_sort",
        ),
        pytest.param(
            "key=sort(interval(1,10))",
            """Error parsing override 'key=sort(interval(1,10))'
TypeError while evaluating 'sort(interval(1,10))': mismatch type argument args[0]""",
            id="sort_interval",
        ),
        pytest.param(
            "+key=choice()",
            """Error parsing override '+key=choice()'
ValueError while evaluating 'choice()': empty choice is not legal""",
            id="empty choice",
        ),
        pytest.param(
            ["+key=choice(choice(a,b))", "-m"],
            """Error parsing override '+key=choice(choice(a,b))'
ValueError while evaluating 'choice(choice(a,b))': nesting choices is not supported
See https://hydra.cc/docs/next/advanced/override_grammar/basic for details

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
""",
            id="empty choice",
        ),
        pytest.param(
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
