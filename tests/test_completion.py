# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra._internal.config_loader import ConfigLoader
from hydra.plugins import CompletionPlugin
from hydra._internal.core_plugins import BashCompletion
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.test_utils.test_utils import create_search_path

chdir_hydra_root()


@pytest.mark.parametrize(
    "line, index, expected",
    [
        ("", None, ["dict.", "dict_prefix=", "hydra.", "list.", "list_prefix="]),
        ("dict", None, ["dict.", "dict_prefix="]),
        ("dict.", None, ["dict.key1=", "dict.key2="]),
        ("dict.key", None, ["dict.key1=", "dict.key2="]),
        ("dict.key1=", None, ["dict.key1=val1"])
        # ("dict.key1", None, ["=val1"]),
        # ("dict.key2", None, ["=val2"]),
        # ("list1", None, [".0", ".1"]),
        # ("list1.0", None, ["=aa"]),
        # ("list1.1", None, ["=bb"]),
        # test completion of:
        # list
        # dict
        # thing after =
        # test top level dict and top level list
        # all of the above with an index of a word one before last.
    ],
)
def test_completion(line, index, expected):
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["tests/configs/completion_test"]),
        strict_cfg=False,
        config_file="config.yaml",
    )

    ret = CompletionPlugin._complete(
        config_loader=config_loader, line=line, index=index
    )
    assert ret == expected


@pytest.mark.parametrize("app_suffix", ["", " "])
@pytest.mark.parametrize(
    "app_prefix",
    [
        "python foo.py",
        "hydra_app",
        "python  foo.py",
        "python demos/hydra_app/example/hydra_app/main.py",
        "/miniconda3/envs/hydra36/bin/python foo.py",
    ],
)
@pytest.mark.parametrize(
    "args_line, args_line_index",
    [
        ("", None),
        ("foo=bar", None),
        ("foo=bar bar=baz0", None),
        ("", 0),
        ("foo=bar", 3),
        ("foo=bar bar=baz0", 3),
        ("dict.", 0),
        ("dict.", 5),
    ],
)
def test_strip(app_prefix, app_suffix, args_line, args_line_index):
    if args_line:
        app_prefix = app_prefix + " "
    app_prefix = app_prefix + app_suffix
    line = "{}{}".format(app_prefix, args_line)
    index = len(app_prefix) + args_line_index if args_line_index is not None else None
    result_line, result_index = BashCompletion.strip_python_or_app_name(line, index)
    assert result_line == args_line
    assert result_index == args_line_index
