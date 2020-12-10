# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import distutils.spawn
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List

import pytest
from packaging import version

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.core_plugins.bash_completion import BashCompletion
from hydra._internal.utils import create_config_search_path
from hydra.plugins.completion_plugin import DefaultCompletionPlugin
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


def is_expect_exists() -> bool:
    return distutils.spawn.find_executable("expect") is not None


def is_fish_supported() -> bool:
    if distutils.spawn.find_executable("fish") is None:
        return False

    proc = subprocess.run(
        ["fish", "--version"], stdout=subprocess.PIPE, encoding="utf-8"
    )
    matches = re.match(r".*version\s+(\d\.\d\.\d)(.*)", proc.stdout)
    if not matches:
        return False

    fish_version, git_version = matches.groups()

    # Release after 3.1.2 or git build after 3.1.2 contain space fix.
    if version.parse(fish_version) > version.parse("3.1.2"):
        return True
    elif version.parse(fish_version) >= version.parse("3.1.2") and git_version:
        return True
    else:
        return False


def is_zsh_supported() -> bool:
    if distutils.spawn.find_executable("zsh") is None:
        return False

    proc = subprocess.run(
        ["zsh", "--version"], stdout=subprocess.PIPE, encoding="utf-8"
    )
    matches = re.match(r"zsh\s+(\d\.\d(\.\d)?)", proc.stdout)
    if not matches:
        return False

    zsh_version = matches.groups()[0]

    # Support for Bash completion functions introduced in Zsh 4.2
    if version.parse(zsh_version) > version.parse("4.2"):
        return True
    else:
        return False


def create_config_loader() -> ConfigLoaderImpl:
    return ConfigLoaderImpl(
        config_search_path=create_config_search_path(
            search_path_dir=os.path.realpath("hydra/test_utils/configs/completion_test")
        )
    )


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestDotInPathCompletion:
    def test_bash_completion_with_dot_in_path(self) -> None:
        process = subprocess.Popen(
            "tests/scripts/test_bash_dot_in_path.bash",
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        assert stderr == b""
        assert stdout == b"TRUE\n"
        return


base_completion_list: List[str] = [
    "dict.",
    "dict_prefix=",
    "group=",
    "hydra",
    "hydra.",
    "list.",
    "list_prefix=",
    "test_hydra/",
]


@pytest.mark.parametrize(
    "line_prefix",
    [pytest.param("", id="no_prefix"), pytest.param("dict.key1=val1 ", id="prefix")],
)
@pytest.mark.parametrize(
    "line,num_tabs,expected",
    [
        ("", 2, base_completion_list),
        (" ", 2, base_completion_list),
        ("dict", 2, ["dict.", "dict_prefix="]),
        ("dict.", 3, ["dict.key1=", "dict.key2=", "dict.key3="]),
        ("dict.key", 2, ["dict.key1=", "dict.key2=", "dict.key3="]),
        ("dict.key1=", 2, ["dict.key1=val1"]),
        ("dict.key3=", 2, ["dict.key3="]),  # no value because dict.key3 is ???
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
        ("test_hydra/lau", 2, ["test_hydra/launcher="]),
        ("test_hydra/launcher=", 2, ["test_hydra/launcher=fairtask"]),
        ("test_hydra/launcher=fa", 2, ["test_hydra/launcher=fairtask"]),
        # loading groups
        pytest.param("gro", 2, ["group="], id="group"),
        pytest.param("group=di", 2, ["group=dict"], id="group"),
        pytest.param(
            "group=dict ",
            3,
            [
                "dict.",
                "dict_prefix=",
                "group.",
                "group=",
                "hydra",
                "hydra.",
                "list.",
                "list_prefix=",
                "test_hydra/",
                "toys.",
            ],
            id="group",
        ),
        pytest.param("group=", 2, ["group=dict", "group=list"], id="group"),
        pytest.param("group=dict group.dict=", 2, ["group.dict=true"], id="group"),
        pytest.param("group=dict group=", 2, ["group=dict", "group=list"], id="group"),
        pytest.param("group=dict group=", 2, ["group=dict", "group=list"], id="group"),
    ],
)
class TestRunCompletion:
    def test_completion_plugin(
        self, line_prefix: str, num_tabs: int, line: str, expected: List[str]
    ) -> None:
        config_loader = create_config_loader()
        bc = DefaultCompletionPlugin(config_loader)
        ret = bc._query(config_name="config.yaml", line=line_prefix + line)
        assert ret == expected

        ret = bc._query(
            config_name="config.yaml", line="--multirun " + line_prefix + line
        )
        assert ret == expected

    @pytest.mark.skipif(  # type: ignore
        not is_expect_exists(),
        reason="expect should be installed to run the expects tests",
    )
    @pytest.mark.parametrize(  # type: ignore
        "prog", [["python", "hydra/test_utils/completion.py"]]
    )
    @pytest.mark.parametrize("shell", ["bash", "fish", "zsh"])  # type: ignore
    def test_shell_integration(
        self,
        shell: str,
        prog: List[str],
        num_tabs: int,
        line_prefix: str,
        line: str,
        expected: List[str],
    ) -> None:
        if shell == "fish" and not is_fish_supported():
            pytest.skip("fish is not installed or the version is too old")
        if shell == "zsh" and not is_zsh_supported():
            pytest.skip("zsh is not installed or the version is too old")

        # verify expect will be running the correct Python.
        # This preemptively detect a much harder to understand error from expect.
        ret = subprocess.check_output(
            ["python", "-c", "import sys; print(sys.executable)"], env=os.environ
        )
        assert os.path.realpath(ret.decode("utf-8").strip()) == os.path.realpath(
            sys.executable.strip()
        )

        verbose = os.environ.get("VERBOSE", "0") != "0"

        line1 = "line={}".format(line_prefix + line)
        cmd = ["expect"]
        if verbose:
            cmd.append("-d")

        cmd.extend(
            [
                "tests/scripts/test_{}_completion.exp".format(shell),
                f"{' '.join(prog)}",
                line1,
                str(num_tabs),
            ]
        )

        if shell == "fish":
            # Fish will add a space to an unambiguous completion.
            expected = [x + " " if re.match(r".*=\w+$", x) else x for x in expected]

            # Exactly match token end. See
            # https://github.com/fish-shell/fish-shell/issues/6928
            expected = [re.escape(x) + "$" for x in expected]

        cmd.extend(expected)
        if verbose:
            print("\nCOMMAND:\n" + " ".join([f"'{x}'" for x in cmd]))
        subprocess.check_call(cmd)


@pytest.mark.parametrize(
    "line,expected",
    [
        pytest.param("", base_completion_list, id="empty_multirun"),
        pytest.param("gro", ["group="], id="group_name"),
        pytest.param("group", ["group="], id="group_eq"),
        pytest.param("group=", ["group=dict", "group=list"], id="group_options"),
        pytest.param("group=dic", ["group=dict"], id="group_option"),
        pytest.param("group=dict", ["group=dict"], id="group_option"),
        pytest.param("group=dict,list", [], id="multirun"),
        pytest.param(
            "group=dict dict.",
            ["dict.key1=", "dict.key2=", "dict.key3="],
            id="complete_node_from_group",
        ),
        pytest.param(
            "group=dict,list list.", ["list.0=", "list.1=", "list.2="], id="multirun"
        ),
        # Not currently supported.
        # This will actually take using the OverrideParser in some kind of partial parsing mode
        # because during typing there will be many overrides that are malformed.
        # Concretely group=dict, is not a valid override.
        # We can't just naively split on , because of things like: key=[1,2],[3,4]
        # Supporting this is likely a significant effort to extend the grammar to parse partial overrides
        pytest.param(
            "group=dict,", ["group=dict,list"], id="multirun", marks=pytest.mark.xfail
        ),
    ],
)
class TestMultirunCompletion:
    def test_completion_plugin_multirun(self, line: str, expected: List[str]) -> None:
        config_loader = create_config_loader()
        bc = DefaultCompletionPlugin(config_loader)
        ret = bc._query(config_name="config.yaml", line="--multirun " + line)
        assert ret == expected


@pytest.mark.parametrize(  # type: ignore
    "line,expected",
    [
        ("-c job", base_completion_list),
        ("-c hydra ", base_completion_list),
        ("-c all ", base_completion_list),
    ],
)
def test_with_flags(line: str, expected: List[str]) -> None:
    config_loader = create_config_loader()
    bc = DefaultCompletionPlugin(config_loader)
    ret = bc._query(config_name="config.yaml", line=line)
    assert ret == expected


@pytest.mark.parametrize("relative", [True, False])  # type: ignore
@pytest.mark.parametrize("line_prefix", ["", "dict.key1=val1 "])  # type: ignore
@pytest.mark.parametrize(  # type: ignore
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
    tmpdir: Path,
    files: List[str],
    line_prefix: str,
    key_eq: str,
    fname_prefix: str,
    expected: List[str],
    relative: bool,
) -> None:
    def create_files(in_files: List[str]) -> None:
        for f in in_files:
            path = Path(f)
            dirname = path.parent
            if str(dirname) != ".":
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

        ret = bc._query(config_name="config.yaml", line=probe)
        assert len(expected) == len(ret)
        for idx, file in enumerate(expected):
            assert key_eq + os.path.join(prefix, file) == ret[idx]
    finally:
        os.chdir(pwd)


@pytest.mark.parametrize(  # type: ignore
    "prefix", ["", " ", "\t", "/foo/bar", " /foo/bar/"]
)
@pytest.mark.parametrize(  # type: ignore
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
@pytest.mark.parametrize(  # type: ignore
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
def test_strip(
    prefix: str, app_prefix: str, args_line: str, args_line_index: int
) -> None:
    app_prefix = prefix + app_prefix
    if args_line:
        app_prefix = app_prefix + " "
    line = "{}{}".format(app_prefix, args_line)
    result_line = BashCompletion.strip_python_or_app_name(line)
    assert result_line == args_line


@pytest.mark.parametrize(  # type: ignore
    "shell,script,comp_func",
    [
        (
            "bash",
            "tests/scripts/test_bash_install_uninstall.sh",
            "hydra_bash_completion",
        ),
        (
            "fish",
            "tests/scripts/test_fish_install_uninstall.fish",
            "hydra_fish_completion",
        ),
    ],
)
def test_install_uninstall(shell: str, script: str, comp_func: str) -> None:
    if shell == "fish" and not is_fish_supported():
        pytest.skip("fish is not installed or the version is too old")
    cmd = [shell, script, "python hydra/test_utils/completion.py", comp_func]
    subprocess.check_call(cmd)
