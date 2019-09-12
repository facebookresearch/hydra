# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra._internal.config_loader import ConfigLoader
from hydra.plugins import CompletionPlugin
from hydra._internal.core_plugins import BashCompletion
from hydra.test_utils.test_utils import chdir_hydra_root
from hydra.test_utils.test_utils import create_search_path
import hydra

chdir_hydra_root()

# TODO: decide if to filter items added in current line from completion suggestions
# TODO: integration test with expect?
@pytest.mark.parametrize("line_prefix", ["", "dict.key1=val1 "])
@pytest.mark.parametrize(
    "line, index, expected",
    [
        (
            "",
            None,
            [
                "dict.",
                "dict_prefix=",
                "group=",
                "hydra.",
                "hydra/",
                "list.",
                "list_prefix=",
            ],
        ),
        ("dict", None, ["dict.", "dict_prefix="]),
        ("dict.", None, ["dict.key1=", "dict.key2="]),
        ("dict.key", None, ["dict.key1=", "dict.key2="]),
        ("dict.key1=", None, ["dict.key1=val1"]),
        ("list", None, ["list.", "list_prefix="]),
        ("list.", None, ["list.0=", "list.1="]),
        ("gro", None, ["group="]),
        (
            "hydra/",
            None,
            [
                "hydra/hydra_logging=",
                "hydra/job_logging=",
                "hydra/launcher=",
                "hydra/output=",
                "hydra/sweeper=",
            ],
        ),
        ("hydra/lau", None, ["hydra/launcher="]),
        ("hydra/launcher=", None, ["hydra/launcher=basic", "hydra/launcher=fairtask"]),
        ("hydra/launcher=ba", None, ["hydra/launcher=basic"]),
        ("./", None, []),
        # TODO: handle case of common prefix in groups and config like in optimizer
        # in demos/5_config_groups/defaults.py
    ],
)
def test_completion(line_prefix, line, index, expected):
    config_loader = ConfigLoader(
        config_search_path=create_search_path(["tests/configs/completion_test"]),
        strict_cfg=False,
        config_file="config.yaml",
    )
    if index is not None:
        index += len(line_prefix)
    bc = CompletionPlugin(config_loader)
    ret = bc._query(line=line_prefix + line)
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


@hydra.main(config_path="configs/completion_test/config.yaml")
def run_cli(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    run_cli()
