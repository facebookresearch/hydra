# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import functools
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Union

import nox
from nox import Session
from nox.logger import logger

BASE = os.path.abspath(os.path.dirname(__file__))

DEFAULT_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11"]
DEFAULT_OS_NAMES = ["Linux", "MacOS", "Windows"]

PYTHON_VERSIONS = os.environ.get(
    "NOX_PYTHON_VERSIONS", ",".join(DEFAULT_PYTHON_VERSIONS)
).split(",")

INSTALL_EDITABLE_MODE = os.environ.get("INSTALL_EDITABLE_MODE", 0)

INSTALL_COMMAND = (
    ["pip", "install", "-e"] if INSTALL_EDITABLE_MODE else ["pip", "install"]
)

# Allow limiting testing to specific plugins
# The list ['ALL'] indicates all plugins
PLUGINS = os.environ.get("PLUGINS", "ALL").split(",")
SKIP_PLUGINS = os.environ.get("SKIP_PLUGINS", "")

SKIP_CORE_TESTS = os.environ.get("SKIP_CORE_TESTS", "0") != "0"
USE_OMEGACONF_DEV_VERSION = os.environ.get("USE_OMEGACONF_DEV_VERSION", "0") != "0"
FIX = os.environ.get("FIX", "0") == "1"
VERBOSE = os.environ.get("VERBOSE", "0")
SILENT = VERBOSE == "0"

nox.options.error_on_missing_interpreters = True


@dataclass
class Plugin:
    name: str
    abspath: str
    module: str
    source_dir: str
    dir_name: str
    setup_py: str
    classifiers: List[str]


def get_current_os() -> str:
    current_os = platform.system()
    if current_os == "Darwin":
        current_os = "MacOS"
    return current_os


print(f"Operating system\t:\t{get_current_os()}")
print(f"NOX_PYTHON_VERSIONS\t:\t{PYTHON_VERSIONS}")
print(f"PLUGINS\t\t\t:\t{PLUGINS}")
print(f"SKIP_PLUGINS\t\t\t:\t{SKIP_PLUGINS}")
print(f"SKIP_CORE_TESTS\t\t:\t{SKIP_CORE_TESTS}")
print(f"FIX\t\t\t:\t{FIX}")
print(f"VERBOSE\t\t\t:\t{VERBOSE}")
print(f"INSTALL_EDITABLE_MODE\t:\t{INSTALL_EDITABLE_MODE}")
print(f"USE_OMEGACONF_DEV_VERSION\t:\t{USE_OMEGACONF_DEV_VERSION}")


def _upgrade_basic(session: Session) -> None:
    session.install("--upgrade", "pip", silent=SILENT)
    session.install("--upgrade", "setuptools", silent=SILENT)


def find_dirs(path: str) -> Iterator[str]:
    for file in os.listdir(path):
        fullname = os.path.join(path, file)
        if os.path.isdir(fullname):
            yield fullname


def print_installed_package_version(session: Session, package_name: str) -> None:
    pip_list: str = session.run("pip", "list", silent=True)
    for line in pip_list.split("\n"):
        if package_name in line:
            print(f"Installed {package_name} version: {line}")


def install_hydra(session: Session, cmd: List[str]) -> None:
    # needed for build
    session.install("read-version", silent=SILENT)
    # clean install hydra
    session.chdir(BASE)
    if USE_OMEGACONF_DEV_VERSION:
        session.install("--pre", "omegaconf", silent=SILENT)
    session.run(*cmd, ".", silent=SILENT)
    print_installed_package_version(session, "omegaconf")
    if not SILENT:
        session.install("pipdeptree", silent=SILENT)
        session.run("pipdeptree", "-p", "hydra-core")


def install_selected_plugins(
    session: Session,
    install_cmd: List[str],
    selected_plugins: List[Plugin],
) -> None:
    for plugin in selected_plugins:
        install_plugin(session, install_cmd, plugin)
    # Test that we can import Hydra
    session.run("python", "-c", "from hydra import main", silent=SILENT)


def install_plugin(session: Session, install_cmd: List[str], plugin: Plugin) -> None:
    maybe_install_torch(session, plugin)
    cmd = install_cmd + [plugin.abspath]
    session.run(*cmd, silent=SILENT)
    if not SILENT:
        session.run("pipdeptree", "-p", plugin.name)
    # Test that we can import all installed plugins
    session.run("python", "-c", f"import {plugin.module}")


def maybe_install_torch(session: Session, plugin: Plugin) -> None:
    if plugin_requires_torch(plugin):
        install_cpu_torch(session)
        print_installed_package_version(session, "torch")


def plugin_requires_torch(plugin: Plugin) -> bool:
    """Determine whether the given plugin depends on pytorch as a requirement"""
    return '"torch"' in Path(plugin.setup_py).read_text()


def install_cpu_torch(session: Session) -> None:
    """
    Install the CPU version of pytorch.
    This is a much smaller download size than the normal version `torch` package hosted on pypi.
    The smaller download prevents our CI jobs from timing out.
    """
    session.install(
        "torch", "--extra-index-url", "https://download.pytorch.org/whl/cpu"
    )


def pytest_args(*args: str) -> List[str]:
    ret = ["pytest"]
    ret.extend(args)
    return ret


def run_pytest(session: Session, directory: str = ".", *args: str) -> None:
    pytest_cmd = pytest_args(directory, *args)
    # silent=False to enable some output on CI
    # (otherwise we risk no-output timeout)
    session.run(*pytest_cmd, silent=False)


def get_setup_python_versions(classifiers: List[str]) -> List[str]:
    pythons = filter(lambda line: "Programming Language :: Python" in line, classifiers)
    return [p[len("Programming Language :: Python :: ") :] for p in pythons]


def session_python_as_tuple(session: Session) -> Tuple[int, int]:
    major_str, minor_str = session.python.split(".")
    major, minor = int(major_str), int(minor_str)
    return major, minor


def get_plugin_os_names(classifiers: List[str]) -> List[str]:
    oses = list(filter(lambda line: "Operating System" in line, classifiers))
    if len(oses) == 0:
        # No Os is specified so all oses are supported
        return DEFAULT_OS_NAMES
    if len(oses) == 1 and oses[0] == "Operating System :: OS Independent":
        # All oses are supported
        return DEFAULT_OS_NAMES
    else:
        return [p.split("::")[-1].strip() for p in oses]


@functools.lru_cache()
def list_plugins(directory: str) -> List[Plugin]:
    blacklist = [".isort.cfg", "examples"]
    _plugin_directories = [
        x
        for x in sorted(os.listdir(os.path.join(BASE, directory)))
        if x not in blacklist
    ]

    # Install bootstrap deps in base python environment
    subprocess.check_output(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "read-version",  # needed to read data from setup.py
            "toml",  # so read-version can read pyproject.toml
        ],
    )

    plugins: List[Plugin] = []
    for dir_name in _plugin_directories:
        abspath = os.path.join(BASE, directory, dir_name)
        setup_py = os.path.join(abspath, "setup.py")
        name_and_classifiers: List[str] = subprocess.check_output(
            [sys.executable, setup_py, "--name", "--classifiers"],
            text=True,
        ).splitlines()
        name, classifiers = name_and_classifiers[0], name_and_classifiers[1:]

        if "hydra_plugins" in os.listdir(abspath):
            module = "hydra_plugins." + dir_name
            source_dir = "hydra_plugins"
        else:
            module = dir_name
            source_dir = dir_name

        plugins.append(
            Plugin(
                name=name,
                abspath=abspath,
                source_dir=source_dir,
                module=module,
                dir_name=dir_name,
                setup_py=setup_py,
                classifiers=classifiers,
            )
        )
    return plugins


def select_plugins_under_directory(session: Session, directory: str) -> List[Plugin]:
    """
    Select all plugins under the current directory that should be tested in this session.
    """
    plugins_under_directory: List[Plugin] = list_plugins(directory)
    selected_plugins = [
        plugin
        for plugin in plugins_under_directory
        if is_plugin_compatible(session, plugin)
    ]

    if len(selected_plugins) == 0:
        logger.warn("No plugins selected")

    return selected_plugins


def is_plugin_compatible(session: Session, plugin: Plugin) -> bool:
    """
    Considers the current Python version and operating systems against the supported ones,
    as well as the user plugins selection (via the PLUGINS and SKIP_PLUGINS environment variables).
    """
    assert session.python is not None, "Session python version is not specified"

    if (
        not (plugin.dir_name in PLUGINS or PLUGINS == ["ALL"])
        or plugin.dir_name in SKIP_PLUGINS
    ):
        logger.warn(f"Deselecting {plugin.dir_name}: User request")
        return False

    plugin_python_versions = get_setup_python_versions(plugin.classifiers)
    python_supported = session.python in plugin_python_versions

    plugin_os_names = get_plugin_os_names(plugin.classifiers)
    os_supported = get_current_os() in plugin_os_names

    if not python_supported:
        py_str = ", ".join(plugin_python_versions)
        logger.warn(
            f"Deselecting {plugin.dir_name} : Incompatible Python {session.python}. Supports [{py_str}]"
        )
        return False

    # Verify this plugin supports the OS we are testing on, skip otherwise
    if not os_supported:
        os_str = ", ".join(plugin_os_names)
        logger.warn(
            f"Deselecting {plugin.dir_name}: Incompatible OS {get_current_os()}. Supports [{os_str}]"
        )
        return False

    return True


def install_dev_deps(session: Session) -> None:
    session.run("pip", "install", "-r", "requirements/dev.txt", silent=SILENT)


def _black_cmd() -> List[str]:
    black = ["black", "."]
    if not FIX:
        black += ["--check"]
    return black


def _isort_cmd() -> List[str]:
    isort = ["isort", "."]
    if not FIX:
        isort += ["--check", "--diff"]
    return isort


def _mypy_cmd(strict: bool, python_version: Optional[str] = "3.7") -> List[str]:
    mypy = [
        "mypy",
        "--install-types",
        "--non-interactive",
        "--config-file",
        f"{BASE}/.mypy.ini",
    ]
    if strict:
        mypy.append("--strict")
    if python_version is not None:
        mypy.append(f"--python-version={python_version}")
    return mypy


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
def lint(session: Session) -> None:
    if session_python_as_tuple(session) <= (3, 6):
        session.skip(f"Skipping session {session.name} as python >= 3.7 is required")
    _upgrade_basic(session)
    install_dev_deps(session)
    install_hydra(session, ["pip", "install", "-e"])

    apps = _get_standalone_apps_dirs()
    session.log("Installing standalone apps")
    for subdir in apps:
        session.chdir(str(subdir))
        session.run(*_black_cmd(), silent=SILENT)
        session.run(*_isort_cmd(), silent=SILENT)
        session.chdir(BASE)

    session.run(*_black_cmd(), silent=SILENT)

    skiplist = apps + [
        ".git",
        "website",
        "plugins",
        "tools",
        ".nox",
        "hydra/grammar/gen",
        "tools/configen/example/gen",
        "tools/configen/tests/test_modules/expected",
        "temp",
        "build",
        "contrib",
    ]
    isort = _isort_cmd() + [f"--skip={skip}" for skip in skiplist]

    session.run(*isort, silent=SILENT)

    session.run(
        *_mypy_cmd(strict=True),
        ".",
        "--exclude=^examples/",
        "--exclude=^tests/standalone_apps/",
        "--exclude=^tests/test_apps/",
        "--exclude=^tools/",
        "--exclude=^plugins/",
        silent=SILENT,
    )
    session.run("flake8", "--config", ".flake8")
    session.run("yamllint", "--strict", ".")

    mypy_check_subdirs = [
        "examples/advanced",
        "examples/configure_hydra",
        "examples/patterns",
        "examples/instantiate",
        "examples/tutorials/basic/your_first_hydra_app",
        "examples/tutorials/basic/running_your_hydra_app",
        "examples/tutorials/structured_configs",
        "tests/standalone_apps",
        "tests/test_apps",
    ]
    for sdir in mypy_check_subdirs:
        dirs = find_dirs(path=sdir)
        for d in dirs:
            session.run(
                *_mypy_cmd(strict=True),
                d,
                silent=SILENT,
            )

    for sdir in ["tools"]:
        dirs = find_dirs(path=sdir)
        for d in dirs:
            session.run(
                *_mypy_cmd(strict=False),  # no --strict flag for tools
                d,
                silent=SILENT,
            )

    # lint example plugins
    lint_plugins_in_dir(session=session, directory="examples/plugins")

    # bandit static security analysis
    session.run("bandit", "--exclude", "./.nox/**", "-ll", "-r", ".", silent=SILENT)


def lint_plugins_in_dir(session: Session, directory: str) -> None:
    plugins = select_plugins_under_directory(session, directory)
    for plugin in plugins:
        lint_plugin(session, plugin)


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
@nox.parametrize("plugin", list_plugins("plugins"), ids=[p.name for p in list_plugins("plugins")])  # type: ignore
def lint_plugins(session: Session, plugin: Plugin) -> None:
    if session_python_as_tuple(session) <= (3, 6):
        session.skip(f"Skipping session {session.name} as python >= 3.7 is required")
    if not is_plugin_compatible(session, plugin):
        session.skip(f"Skipping session {session.name}")
    _upgrade_basic(session)
    lint_plugin(session, plugin)


def lint_plugin(session: Session, plugin: Plugin) -> None:
    install_cmd = ["pip", "install"]
    install_hydra(session, install_cmd)

    # plugin linting requires the plugin and its dependencies to be installed
    install_plugin(session=session, install_cmd=install_cmd, plugin=plugin)

    install_dev_deps(session)

    session.run("flake8", "--config", ".flake8", plugin.abspath)
    path = plugin.abspath
    source_dir = plugin.source_dir
    session.chdir(path)
    session.run(*_black_cmd(), silent=SILENT)
    session.run(*_isort_cmd(), silent=SILENT)
    session.chdir(BASE)

    files = []
    for file in ["tests", "example"]:
        abs = os.path.join(path, file)
        if os.path.exists(abs):
            files.append(abs)

    # Mypy for plugin
    session.run(
        *_mypy_cmd(
            strict=True,
            # Don't pass --python-version flag when linting plugins, as mypy may
            # report syntax errors if the passed --python-version is different
            # from the python version that was used to install the plugin's
            # dependencies.
            python_version=None,
        ),
        "--follow-imports=silent",
        f"{path}/{source_dir}",
        *files,
        silent=SILENT,
    )


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
def test_tools(session: Session) -> None:
    _upgrade_basic(session)
    install_cmd = ["pip", "install"]
    session.install("pytest")
    install_hydra(session, install_cmd)

    tools = [
        x
        for x in sorted(os.listdir(os.path.join(BASE, "tools")))
        if not os.path.isfile(x)
    ]

    for tool in tools:
        tool_path = os.path.join("tools", tool)
        session.chdir(BASE)
        if (Path(tool_path) / "setup.py").exists():
            cmd = list(install_cmd) + ["-e", tool_path]
            session.run(*cmd, silent=SILENT)
            session.run("pytest", tool_path)

    session.chdir(BASE)


def _get_standalone_apps_dirs() -> List[Union[str, Path]]:
    standalone_apps_dir = Path(f"{BASE}/tests/standalone_apps")
    apps: List[Union[str, Path]] = [
        standalone_apps_dir / subdir for subdir in os.listdir(standalone_apps_dir)
    ]
    apps.append(f"{BASE}/examples/advanced/hydra_app_example")
    return apps


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
def test_core(session: Session) -> None:
    _upgrade_basic(session)
    install_hydra(session, INSTALL_COMMAND)
    session.install("pytest")

    if not SKIP_CORE_TESTS:
        run_pytest(
            session,
            "build_helpers",
            "tests",
            "-W ignore:pkg_resources is deprecated as an API:DeprecationWarning",
            *session.posargs,
        )
    else:
        session.log("Skipping Hydra core tests")

    apps = _get_standalone_apps_dirs()
    session.log("Testing standalone apps")
    for subdir in apps:
        session.chdir(subdir)
        session.run(*INSTALL_COMMAND, ".", silent=SILENT)
        run_pytest(session, ".")

    session.chdir(BASE)

    selected_plugins = select_plugins_under_directory(session, "examples/plugins")
    install_selected_plugins(
        session=session, install_cmd=INSTALL_COMMAND, selected_plugins=selected_plugins
    )
    test_selected_plugins(
        session,
        selected_plugins=selected_plugins,
    )


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
def test_plugins_vs_core(session: Session) -> None:
    _upgrade_basic(session)
    session.install("pytest")
    install_hydra(session, INSTALL_COMMAND)

    # install all plugins compatible with the current Python version
    selected_plugins = select_plugins_under_directory(session, "plugins")
    install_selected_plugins(
        session=session, install_cmd=INSTALL_COMMAND, selected_plugins=selected_plugins
    )

    # Run Hydra tests to verify installed plugins did not break anything
    if not SKIP_CORE_TESTS:
        # exclude test_completion for plugins tests.
        # 1. It's tested during normal core tests.
        # 2. it's somewhat fragile and tend to timeout in mac.
        # 3. it's expensive and it's not worth the cost to run it for plugins as well.
        run_pytest(session, "tests", "--ignore=tests/test_completion.py")
    else:
        session.log("Skipping Hydra core tests")


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
@nox.parametrize("plugin", list_plugins("plugins"), ids=[p.name for p in list_plugins("plugins")])  # type: ignore
def test_plugins(session: Session, plugin: Plugin) -> None:
    _upgrade_basic(session)
    session.install("pytest")
    install_hydra(session, INSTALL_COMMAND)
    if not is_plugin_compatible(session, plugin):
        session.skip(f"Skipping session {session.name}")
    else:
        install_selected_plugins(
            session=session, install_cmd=INSTALL_COMMAND, selected_plugins=[plugin]
        )
        test_selected_plugins(
            session=session,
            selected_plugins=[plugin],
        )


def test_selected_plugins(session: Session, selected_plugins: List[Plugin]) -> None:
    # Run tests for all installed plugins
    for plugin in selected_plugins:
        session.chdir(plugin.abspath)
        run_pytest(session)


@nox.session(python="3.8")  # type: ignore
def coverage(session: Session) -> None:
    _upgrade_basic(session)
    coverage_env = {
        "COVERAGE_HOME": BASE,
        "COVERAGE_FILE": f"{BASE}/.coverage",
        "COVERAGE_RCFILE": f"{BASE}/.coveragerc",
    }

    session.install("coverage", "pytest")
    install_hydra(session, ["pip", "install", "-e"])
    session.run("coverage", "erase", env=coverage_env)

    for directory in ["plugins", "examples/plugins"]:
        selected_plugins = select_plugins_under_directory(session, directory)
        for plugin in selected_plugins:
            session.run(
                "pip",
                "install",
                "-e",
                plugin.abspath,
                silent=SILENT,
            )

        # run plugin coverage
        for plugin in selected_plugins:
            session.chdir(plugin.abspath)
            cov_args = ["coverage", "run", "--append", "-m"]
            cov_args.extend(pytest_args())
            session.run(*cov_args, silent=SILENT, env=coverage_env)
            session.chdir(BASE)

    # run hydra-core coverage
    session.run(
        "coverage",
        "run",
        "--append",
        "-m",
        silent=SILENT,
        env=coverage_env,
        *pytest_args(),
    )

    # Increase the fail_under as coverage improves
    session.run("coverage", "report", "--fail-under=80", env=coverage_env)
    session.run("coverage", "erase", env=coverage_env)


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
def test_jupyter_notebooks(session: Session) -> None:
    _upgrade_basic(session)
    versions = copy.copy(DEFAULT_PYTHON_VERSIONS)
    if session.python not in versions:
        session.skip(
            f"Not testing Jupyter notebook on Python {session.python}, supports [{','.join(versions)}]"
        )

    session.install("jupyter", "nbval", "pyzmq", "pytest")
    if platform.system() == "Windows":
        session.install("pywin32")

    install_hydra(session, ["pip", "install", "-e"])
    args = pytest_args(
        "--nbval",
        "-W ignore::DeprecationWarning",
        "-W ignore::ResourceWarning",
        "-W ignore::pytest.PytestAssertRewriteWarning",
        "examples/jupyter_notebooks/compose_configs_in_notebook.ipynb",
    )
    session.run(*args, silent=SILENT)

    notebooks_dir = Path("tests/jupyter")
    for notebook in [
        file for file in notebooks_dir.iterdir() if str(file).endswith(".ipynb")
    ]:
        args = pytest_args(
            "--nbval",
            "-W ignore::DeprecationWarning",
            "-W ignore::ResourceWarning",
            "-W ignore::pytest.PytestAssertRewriteWarning",
            str(notebook),
        )
        args = [x for x in args if x != "-Werror"]
        session.run(*args, silent=SILENT)


@nox.session(python=PYTHON_VERSIONS)  # type: ignore
def benchmark(session: Session) -> None:
    _upgrade_basic(session)
    install_dev_deps(session)
    install_hydra(session, INSTALL_COMMAND)
    session.install("pytest")
    run_pytest(session, "build_helpers", "tests/benchmark.py", *session.posargs)
