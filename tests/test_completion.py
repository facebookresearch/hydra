# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import distutils.spawn
import os
import subprocess

import pytest

from hydra._internal.config_loader import ConfigLoader
from hydra._internal.core_plugins import BashCompletion
from hydra._internal.pathlib import Path
from hydra.plugins.completion_plugin import DefaultCompletionPlugin
from hydra.test_utils.test_utils import chdir_hydra_root, create_search_path

chdir_hydra_root()


def is_expect_exists():
    return distutils.spawn.find_executable("expect") is not None


def create_config_loader():
    return ConfigLoader(
        config_search_path=create_search_path(
            ["hydra/test_utils/configs/completion_test"], abspath=True
        )
    )


base_completion_list = [
    "dict.",
    "dict_prefix=",
    "group=",
    "hydra.",
    "hydra/",
    "list.",
    "list_prefix=",
]


@pytest.mark.parametrize("line_prefix", ["", "dict.key1=val1 ", "-r "])
@pytest.mark.parametrize(
    "line,num_tabs,expected",
    [
        ("", 2, base_completion_list),
        (" ", 2, base_completion_list),
        ("dict", 2, ["dict.", "dict_prefix="]),
        ("dict.", 3, ["dict.key1=", "dict.key2=", "dict.key3="]),
        ("dict.key", 2, ["dict.key1=", "dict.key2=", "dict.key3="]),
        ("dict.key1=", 2, ["dict.key1=val1"]),
        ("dict.key3=", 2, []),  # no matches because value is ??? (missing)
        ("list", 2, ["list.", "list_prefix="]),
        ("list.", 2, ["list.0=", "list.1=", "list.2="]),
        (
            "hydra/",
            3,
            [
                "hydra/help=",
                "hydra/hydra_help=",
                "hydra/hydra_logging=",
                "hydra/job_logging=",
                "hydra/launcher=",
                "hydra/output=",
                "hydra/sweeper=",
            ],
        ),
        ("hydra/lau", 2, ["hydra/launcher="]),
        ("hydra/launcher=", 2, ["hydra/launcher=basic", "hydra/launcher=fairtask"]),
        ("hydra/launcher=ba", 2, ["hydra/launcher=basic"]),
        # loading groups
        ("gro", 2, ["group="]),
        ("group=di", 2, ["group=dict"]),
        (
            "group=dict ",
            3,
            [
                "dict.",
                "dict_prefix=",
                "group.",
                "group=",
                "hydra.",
                "hydra/",
                "list.",
                "list_prefix=",
                "toys.",
            ],
        ),
        ("group=", 2, ["group=dict", "group=list"]),
        ("group=dict group.dict=", 2, ["group.dict=true"]),
        ("group=dict group=", 2, ["group=dict", "group=list"]),
    ],
)
class TestCompletion:
    def test_completion_plugin(self, line_prefix, num_tabs, line, expected):
        config_loader = create_config_loader()
        bc = DefaultCompletionPlugin(config_loader)
        ret = bc._query(config_file="config.yaml", line=line_prefix + line)
        assert ret == expected

    @pytest.mark.skipif(
        not is_expect_exists(),
        reason="expect should be installed to run the expects tests",
    )
    @pytest.mark.parametrize("prog", ["python hydra/test_utils/completion.py"])
    @pytest.mark.parametrize("shell", ["bash"])
    def test_shell_integration(
        self, shell, prog, num_tabs, line_prefix, line, expected
    ):
        line1 = "line={}".format(line_prefix + line)
        cmd = [
            "expect",
            # "-d",  # Uncomment for debug prints from expect
            "tests/expect/test_{}_completion.exp".format(shell),
            prog,
            line1,
            str(num_tabs),
        ]
        cmd.extend(expected)
        print(" ".join(["'{}'".format(x) for x in cmd]))
        subprocess.check_call(cmd)


@pytest.mark.parametrize(
    "line,expected",
    [
        ("-c job", base_completion_list),
        ("-c hydra ", base_completion_list),
        ("-c all ", base_completion_list),
    ],
)
def test_with_flags(line, expected):
    config_loader = create_config_loader()
    bc = DefaultCompletionPlugin(config_loader)
    ret = bc._query(config_file="config.yaml", line=line)
    assert ret == expected


@pytest.mark.parametrize("relative", [True, False])
@pytest.mark.parametrize("line_prefix", ["", "dict.key1=val1 "])
@pytest.mark.parametrize(
    "key_eq, fname_prefix, files, expected",
    [
        ("abc=", "", ["foo.txt"], ["foo.txt"]),
        ("abc=", "fo", ["foo.txt"], ["foo.txt"]),
        ("abc=", "foo.txt", ["foo.txt"], ["foo.txt"]),
        ("abc=", "foo", ["foo1.txt", "foo2.txt"], ["foo1.txt", "foo2.txt"]),
        ("abc=", "foo1", ["foo1.txt", "foo2.txt"], ["foo1.txt"]),
        ("abc=", "foo/bar", [], []),
    ],
)
def test_file_completion(
    tmpdir, files, line_prefix, key_eq, fname_prefix, expected, relative
):
    def create_files(in_files):
        for f in in_files:
            dirname = os.path.dirname(f)
            if dirname != "":
                Path.mkdir(dirname, parents=True)
            Path(f).touch(exist_ok=True)

    config_loader = create_config_loader()
    try:
        pwd = os.getcwd()
        os.chdir(str(tmpdir))
        create_files(files)
        bc = DefaultCompletionPlugin(config_loader)
        probe = line_prefix + key_eq
        if relative:
            prefix = "." + os.path.sep
            probe += prefix + fname_prefix
        else:
            prefix = os.path.realpath(".")
            probe += os.path.join(prefix, fname_prefix)

        ret = bc._query(config_file="config.yaml", line=probe)
        assert len(expected) == len(ret)
        for idx, file in enumerate(expected):
            assert key_eq + os.path.join(prefix, file) == ret[idx]
    finally:
        os.chdir(pwd)


@pytest.mark.parametrize("prefix", ["", " ", "\t", "/foo/bar", " /foo/bar/"])
@pytest.mark.parametrize(
    "app_prefix",
    [
        "python foo.py",
        "hydra_app",
        "hydra_app ",
        "hy1-_=ra_app",
        "foo.par",
        "f_o-o1=2.par",
        "python  foo.py",
        "python tutorials/hydra_app/example/hydra_app/main.py",
        "python foo.py",
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
def test_strip(prefix, app_prefix, args_line, args_line_index):
    app_prefix = prefix + app_prefix
    if args_line:
        app_prefix = app_prefix + " "
    line = "{}{}".format(app_prefix, args_line)
    result_line = BashCompletion.strip_python_or_app_name(line)
    assert result_line == args_line
