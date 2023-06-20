# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

from packaging import version
from pytest import mark, param, skip, xfail

from hydra._internal.config_loader_impl import ConfigLoaderImpl
from hydra._internal.core_plugins.bash_completion import BashCompletion
from hydra._internal.utils import create_config_search_path
from hydra.plugins.completion_plugin import DefaultCompletionPlugin
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


def is_expect_exists() -> bool:
    return shutil.which("expect") is not None


def is_fish_supported() -> bool:
    if shutil.which("fish") is None:
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
    if shutil.which("zsh") is None:
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


@mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_bash_completion_with_dot_in_path() -> None:
    process = subprocess.Popen(
        "tests/scripts/test_bash_dot_in_path.bash",
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"PATH": os.environ["PATH"]},
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


@mark.parametrize(
    "line_prefix",
    [param("", id="no_prefix"), param("dict.key1=val1 ", id="prefix")],
)
@mark.parametrize(
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
                "hydra/env=",
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
        param("gro", 2, ["group="], id="group"),
        param("group=di", 2, ["group=dict"], id="group"),
        param(
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
        param("group=", 2, ["group=dict", "group=list"], id="group"),
        param("group=dict group.dict=", 2, ["group.dict=true"], id="group"),
        param("group=dict group=", 2, ["group=dict", "group=list"], id="group"),
        param("group=dict group=", 2, ["group=dict", "group=list"], id="group"),
        param("+", 2, ["+group=", "+hydra", "+test_hydra/"], id="bare_plus"),
        param("+gro", 2, ["+group="], id="append_group_partial"),
        param("+group=di", 2, ["+group=dict"], id="append_group_partial_option"),
        param("+group=", 2, ["+group=dict", "+group=list"], id="group_append"),
        param(
            "group=dict +group=", 2, ["+group=dict", "+group=list"], id="group_append2"
        ),
        param("~gro", 2, ["~group"], id="delete_group_partial"),
        param("~group=di", 2, ["~group=dict"], id="delete_group_partial_option"),
        param("~group=", 2, ["~group=dict", "~group=list"], id="group_delete"),
        param(
            "group=dict ~group=", 2, ["~group=dict", "~group=list"], id="group_delete2"
        ),
        param("~", 2, ["~group", "~hydra", "~test_hydra/"], id="bare_tilde"),
        param("+test_hydra/lau", 2, ["+test_hydra/launcher="], id="nested_plus"),
        param(
            "+test_hydra/launcher=",
            2,
            ["+test_hydra/launcher=fairtask"],
            id="nested_plus_equal",
        ),
        param(
            "+test_hydra/launcher=fa",
            2,
            ["+test_hydra/launcher=fairtask"],
            id="nested_plus_equal_partial",
        ),
        param("~test_hydra/lau", 2, ["~test_hydra/launcher"], id="nested_tilde"),
        param(
            "~test_hydra/launcher=",
            2,
            ["~test_hydra/launcher=fairtask"],
            id="nested_tilde_equal",
        ),
        param(
            "~test_hydra/launcher=fa",
            2,
            ["~test_hydra/launcher=fairtask"],
            id="nested_tilde_equal_partial",
        ),
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

    @mark.skipif(
        not is_expect_exists(),
        reason="expect should be installed to run the expects tests",
    )
    @mark.parametrize("prog", [["python", "hydra/test_utils/completion.py"]])
    @mark.parametrize(
        "shell",
        ["bash", "fish", "zsh"],
    )
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
            skip("fish is not installed or the version is too old")
        if shell == "zsh" and not is_zsh_supported():
            skip("zsh is not installed or the version is too old")
        if shell in ("zsh", "fish") and any(
            word.startswith("~") for word in line.split(" ")
        ):
            xfail(f"{shell} treats words prefixed by the tilde symbol specially")

        # verify expect will be running the correct Python.
        # This preemptively detect a much harder to understand error from expect.
        ret = subprocess.check_output(
            ["python", "-c", "import sys; print(sys.executable)"],
            env={"PATH": os.environ["PATH"]},
        )
        assert os.path.realpath(ret.decode("utf-8").strip()) == os.path.realpath(
            sys.executable.strip()
        )

        verbose = os.environ.get("VERBOSE", "0") != "0"

        cmd = ["expect"]
        if verbose:
            cmd.append("-d")

        cmd.extend(
            [
                f"tests/scripts/test_{shell}_completion.exp",
                f"{' '.join(prog)}",
                f"line={line_prefix + line}",
                str(num_tabs),
            ]
        )

        cmd.extend(expected)
        if verbose:
            print("\nCOMMAND:\n" + " ".join(f"'{x}'" for x in cmd))

        subprocess.check_call(cmd)


@mark.parametrize(
    "line,expected",
    [
        param("", base_completion_list, id="empty_multirun"),
        param("gro", ["group="], id="group_name"),
        param("group", ["group="], id="group_eq"),
        param("group=", ["group=dict", "group=list"], id="group_options"),
        param("group=dic", ["group=dict"], id="group_option"),
        param("group=dict", ["group=dict"], id="group_option"),
        param("group=dict,list", [], id="multirun"),
        param(
            "group=dict dict.",
            ["dict.key1=", "dict.key2=", "dict.key3="],
            id="complete_node_from_group",
        ),
        param(
            "group=dict,list list.", ["list.0=", "list.1=", "list.2="], id="multirun"
        ),
        # Not currently supported.
        # This will actually take using the OverrideParser in some kind of partial parsing mode
        # because during typing there will be many overrides that are malformed.
        # Concretely group=dict, is not a valid override.
        # We can't just naively split on , because of things like: key=[1,2],[3,4]
        # Supporting this is likely a significant effort to extend the grammar to parse partial overrides
        param("group=dict,", ["group=dict,list"], id="multirun", marks=mark.xfail),
    ],
)
class TestMultirunCompletion:
    def test_completion_plugin_multirun(self, line: str, expected: List[str]) -> None:
        config_loader = create_config_loader()
        bc = DefaultCompletionPlugin(config_loader)
        ret = bc._query(config_name="config.yaml", line="--multirun " + line)
        assert ret == expected


@mark.parametrize(
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


@mark.parametrize(
    "line,expected",
    [
        ("", ["group=", "hydra", "test_hydra/"]),
        ("group=", ["group=dict", "group=list"]),
        ("group=d", ["group=dict"]),
        (
            "group=dict ",
            ["group.", "group=", "hydra", "hydra.", "test_hydra/", "toys."],
        ),
        ("group=dict toys.", ["toys.andy=", "toys.list.", "toys.slinky="]),
    ],
)
def test_missing_default_value(line: str, expected: List[str]) -> None:
    config_loader = create_config_loader()
    bc = DefaultCompletionPlugin(config_loader)
    ret = bc._query(config_name="missing_default", line=line)
    assert ret == expected


@mark.parametrize(
    "line,expected",
    [
        param(
            "",
            ["additional_group=", "group=", "hydra", "hydra.", "test_hydra/"],
            id="empty",
        ),
        param("group", ["group="], id="group"),
        param(
            "group=",
            ["group=dict", "group=file_opt", "group=list", "group=pkg_opt"],
            id="group_eq",
        ),
        param("add", ["additional_group="], id="add"),
        param("additional_group", ["additional_group="], id="additional_group"),
        param(
            "additional_group=",
            [
                "additional_group=file_opt_additional",
                "additional_group=pkg_opt_additional",
            ],
            id="additional_group_eq",
        ),
    ],
)
def test_searchpath_addition(line: str, expected: List[str]) -> None:
    config_loader = create_config_loader()
    bc = DefaultCompletionPlugin(config_loader)
    ret = bc._query(config_name="additional_searchpath", line=line)
    assert ret == expected


@mark.parametrize("relative", [True, False])
@mark.parametrize("line_prefix", ["", "dict.key1=val1 "])
@mark.parametrize(
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


@mark.parametrize("prefix", ["", " ", "\t", "/foo/bar", " /foo/bar/"])
@mark.parametrize(
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
@mark.parametrize(
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
    line = f"{app_prefix}{args_line}"
    result_line = BashCompletion.strip_python_or_app_name(line)
    assert result_line == args_line


@mark.skipif(sys.platform == "win32", reason="does not run on windows")
@mark.parametrize(
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
        skip("fish is not installed or the version is too old")
    cmd = [shell, script, "python hydra/test_utils/completion.py", comp_func]
    subprocess.check_call(cmd, env={"PATH": os.environ["PATH"]})
