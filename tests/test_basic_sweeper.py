# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import sys
from textwrap import dedent
from typing import Any, List, Optional

from pytest import mark, param

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.core_plugins.basic_sweeper import BasicSweeper
from hydra._internal.utils import create_config_search_path
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.test_utils.test_utils import assert_multiline_regex_search, run_process


@mark.parametrize(
    "args,max_batch_size,expected",
    [
        param(["x=10"], None, [[["x=10"]]], id="simple"),
        param(["x=10,20"], None, [[["x=10"], ["x=20"]]], id="split_1d"),
        param(["x=[10,20]"], None, [[["x=[10,20]"]]], id="not_split_yaml_list"),
        param(
            ["x=[a,b,c],[d,e,f]"],
            None,
            [[["x=[a,b,c]"], ["x=[d,e,f]"]]],
            id="list_of_lists",
        ),
        param(
            ["a=1,2", "b=10,11"],
            None,
            [[["a=1", "b=10"], ["a=1", "b=11"], ["a=2", "b=10"], ["a=2", "b=11"]]],
            id="no_batching",
        ),
        param(
            ["a=1,2", "b=10,11"],
            1,
            [
                [["a=1", "b=10"]],
                [["a=1", "b=11"]],
                [["a=2", "b=10"]],
                [["a=2", "b=11"]],
            ],
            id="batches_of_1",
        ),
        param(
            ["a=1,2", "b=10,11"],
            2,
            [[["a=1", "b=10"], ["a=1", "b=11"]], [["a=2", "b=10"], ["a=2", "b=11"]]],
            id="batches_of_2",
        ),
        param(["a=range(0,3)"], None, [[["a=0"], ["a=1"], ["a=2"]]], id="range"),
        param(["a=range(3)"], None, [[["a=0"], ["a=1"], ["a=2"]]], id="range_no_start"),
        param(["a=1,2,3", "a=20"], None, [[["a=20"]]], id="override_same_key1"),
        param(
            ["a=2", "a=10,20"], None, [[["a=10"], ["a=20"]]], id="override_same_key2"
        ),
        param(
            ["a=1,2,3", "a=10,20"],
            None,
            [[["a=10"], ["a=20"]]],
            id="override_same_key3",
        ),
        param(["a={x:1},{x:2}"], None, [[["a={x:1}"], ["a={x:2}"]]], id="dicts"),
        param(
            ["a={x:1},{x:2}", "+a={y:10},{y:20}"],
            None,
            [
                [
                    ["a={x:1}", "+a={y:10}"],
                    ["a={x:1}", "+a={y:20}"],
                    ["a={x:2}", "+a={y:10}"],
                    ["a={x:2}", "+a={y:20}"],
                ]
            ],
            id="dicts_multiple_with_plus",
        ),
        param(
            ["a={x:1},{x:2}", "a={y:10},{y:20}"],
            None,
            [
                [
                    ["a={x:1}", "a={y:10}"],
                    ["a={x:1}", "a={y:20}"],
                    ["a={x:2}", "a={y:10}"],
                    ["a={x:2}", "a={y:20}"],
                ]
            ],
            id="dicts_multiple",
        ),
        param(["a=1,2,3", "a={x:1}"], None, [[["a={x:1}"]]], id="override_with_dict1"),
        param(
            ["a=1,2,3", "a={x:1},{x:2}"],
            None,
            [[["a={x:1}"], ["a={x:2}"]]],
            id="override_with_dict2",
        ),
        param(
            ["a={x:1}", "a=1,2,3"],
            None,
            [[["a=1"], ["a=2"], ["a=3"]]],
            id="override_with_dict3",
        ),
        param(["a={x:1},{x:2}", "a=1"], None, [[["a=1"]]], id="override_with_dict4"),
    ],
)
def test_split(
    args: List[str], max_batch_size: Optional[int], expected: List[List[List[str]]]
) -> None:

    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    parser = OverridesParser.create(config_loader)
    ret = BasicSweeper.split_arguments(
        parser.parse_overrides(args), max_batch_size=max_batch_size
    )
    lret = [list(x) for x in ret]
    assert lret == expected


@mark.parametrize(
    "args,expected",
    [
        param(["a=1", "b=2", "a=3"], ["b=2", "a=3"], id="simple_override"),
        param(["a=1,2", "a=3,4"], ["a=3,4"], id="override_split"),
        param(
            ["a=1", "b=2", "+a={x:10}", "+a={y:20}"],
            ["a=1", "b=2", "+a={x:10}", "+a={y:20}"],
            id="override_plus",
        ),
        param(
            ["a=1", "b=2", "a={x:10}", "a={y:20}"],
            ["b=2", "a={x:10}", "a={y:20}"],
            id="override_plus",
        ),
        param(["a={x:1}", "a={y:2}"], ["a={x:1}", "a={y:2}"], id="override_dict"),
        param(
            ["a=1,2", "+a={x:10},{y:20}", "a=3,4"],
            ["+a={x:10},{y:20}", "a=3,4"],
            id="override_mixed",
        ),
        param(["a=1,2", "a={x:10},{y:20}", "a=3,4"], ["a=3,4"], id="override_mixed"),
        param(["+a=xx,yy", "+a=[zz]"], ["+a=[zz]"], id="override_plus_list"),
    ],
)
def test_simplify(args: List[str], expected: List[str]) -> None:
    config_loader = ConfigLoaderImpl(config_search_path=create_config_search_path(None))
    parser = OverridesParser.create(config_loader)
    overrides = parser.parse_overrides(args)
    simplified = BasicSweeper.simplify_overrides(overrides)
    expected_overrides = parser.parse_overrides(expected)
    assert simplified == expected_overrides


def test_partial_failure(
    tmpdir: Any,
) -> None:
    cmd = [
        sys.executable,
        "-Werror",
        "tests/test_apps/app_can_fail/my_app.py",
        "--multirun",
        "+divisor=1,0",
        f'hydra.run.dir="{str(tmpdir)}"',
        "hydra.job.chdir=True",
        "hydra.hydra_logging.formatters.simple.format='[HYDRA] %(message)s'",
    ]
    out, err = run_process(cmd=cmd, print_error=False, raise_exception=False)

    expected_out_regex = re.escape(
        dedent(
            """
            [HYDRA] Launching 2 jobs locally
            [HYDRA] \t#0 : +divisor=1
            val=1.0
            [HYDRA] \t#1 : +divisor=0
            """
        ).strip()
    )

    assert_multiline_regex_search(expected_out_regex, out)

    expected_err_regex = dedent(
        r"""
        Error executing job with overrides: \['\+divisor=0'\](
        )?
        Traceback \(most recent call last\):
          File ".*my_app\.py", line 9, in my_app
            val = 1 / cfg\.divisor(
                  ~~\^~~~~~~~~~~~~)?
        ZeroDivisionError: division by zero

        Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace\.
        """
    ).strip()

    assert_multiline_regex_search(expected_err_regex, err)
