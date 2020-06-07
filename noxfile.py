# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import copy
import os
import platform
from typing import List

import nox
from nox.logger import logger

BASE = os.path.abspath(os.path.dirname(__file__))

DEFAULT_PYTHON_VERSIONS = ["3.6", "3.7", "3.8"]
DEFAULT_OS_NAMES = ["Linux", "MacOS", "Windows"]

PYTHON_VERSIONS = os.environ.get(
    "NOX_PYTHON_VERSIONS", ",".join(DEFAULT_PYTHON_VERSIONS)
).split(",")

PLUGINS_INSTALL_COMMANDS = (["pip", "install"], ["pip", "install", "-e"])

# Allow limiting testing to specific plugins
# The list ['ALL'] indicates all plugins
PLUGINS = os.environ.get("PLUGINS", "ALL").split(",")

SKIP_CORE_TESTS = "0"
SKIP_CORE_TESTS = os.environ.get("SKIP_CORE_TESTS", SKIP_CORE_TESTS) != "0"
FIX = os.environ.get("FIX", "0") == "1"
VERBOSE = os.environ.get("VERBOSE", "0")
SILENT = VERBOSE == "0"


def get_current_os() -> str:
    current_os = platform.system()
    if current_os == "Darwin":
        current_os = "MacOS"
    return current_os


print(f"Operating system\t:\t{get_current_os()}")
print(f"NOX_PYTHON_VERSIONS\t:\t{PYTHON_VERSIONS}")
print(f"PLUGINS\t\t\t:\t{PLUGINS}")
print(f"SKIP_CORE_TESTS\t\t:\t{SKIP_CORE_TESTS}")
print(f"FIX\t\t\t:\t{FIX}")
print(f"VERBOSE\t\t\t:\t{VERBOSE}")


def _upgrade_basic(session):
    session.run(
        "python",
        "-m",
        "pip",
        "install",
        "--upgrade",
        "setuptools",
        "pip",
        silent=SILENT,
    )


def find_python_files(folder):
    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            if filename.endswith(".py"):
                yield os.path.join(root, filename)


def install_hydra(session, cmd):
    # clean install hydra
    session.chdir(BASE)
    session.run(*cmd, ".", silent=SILENT)
    session.install("pipdeptree", silent=SILENT)
    session.run("pipdeptree", "-p", "hydra-core")


def pytest_args(session, *args):
    ret = ["pytest", "-Werror"]
    ret.extend(args)
    if len(session.posargs) > 0:
        ret.extend(session.posargs)
    return ret


def run_pytest(session, directory=".", *args):
    pytest_cmd = pytest_args(session, directory, *args)
    session.run(*pytest_cmd, silent=SILENT)


def get_setup_python_versions(classifiers):
    pythons = filter(lambda line: "Programming Language :: Python" in line, classifiers)
    return [p[len("Programming Language :: Python :: ") :] for p in pythons]


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


def select_plugins(session):
    """
    Select all plugins that should be tested in this session.
    Considers the current Python version and operating systems against the supported ones,
    as well as the user plugins selection (via the PLUGINS environment variable).
    """

    assert session.python is not None, "Session python version is not specified"
    blacklist = [".isort.cfg"]
    example_plugins = [
        {"name": x, "path": "examples/{}".format(x)}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins/examples")))
        if x not in blacklist
    ]
    plugins = [
        {"name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins")))
        if x != "examples"
        if x not in blacklist
    ]
    available_plugins = plugins + example_plugins

    ret = []
    skipped = []
    for plugin in available_plugins:
        if not (plugin["name"] in PLUGINS or PLUGINS == ["ALL"]):
            skipped.append(f"Deselecting {plugin['name']}: User request")
            continue

        setup_py = os.path.join(BASE, "plugins", plugin["path"], "setup.py")
        classifiers = session.run(
            "python", setup_py, "--classifiers", silent=True
        ).splitlines()

        plugin_python_versions = get_setup_python_versions(classifiers)
        python_supported = session.python in plugin_python_versions

        plugin_os_names = get_plugin_os_names(classifiers)
        os_supported = get_current_os() in plugin_os_names

        if not python_supported:
            py_str = ", ".join(plugin_python_versions)
            skipped.append(
                f"Deselecting {plugin['name']} : Incompatible Python {session.python}. Supports [{py_str}]"
            )
            continue

        # Verify this plugin supports the OS we are testing on, skip otherwise
        if not os_supported:
            os_str = ", ".join(plugin_os_names)
            skipped.append(
                f"Deselecting {plugin['name']}: Incompatible OS {get_current_os()}. Supports [{os_str}]"
            )
            continue

        ret.append(
            {
                "name": plugin["name"],
                "path": plugin["path"],
                "module": "hydra_plugins." + plugin["name"],
            }
        )

    for msg in skipped:
        logger.warn(msg)

    if len(ret) == 0:
        logger.warn("No plugins selected")
    return ret


def install_lint_deps(session):
    _upgrade_basic(session)
    session.run("pip", "install", "-r", "requirements/dev.txt", silent=SILENT)
    session.run("pip", "install", "-e", ".", silent=SILENT)
    session.install("black")


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    install_lint_deps(session)
    session.run("black", "--check", ".", silent=SILENT)
    session.run(
        "isort",
        "--check",
        "--diff",
        ".",
        "--skip=plugins",
        "--skip=.nox",
        silent=SILENT,
    )
    session.run("mypy", ".", "--strict", silent=SILENT)
    session.run("flake8", "--config", ".flake8")
    # Mypy for examples
    for pyfie in find_python_files("examples"):
        session.run("mypy", pyfie, "--strict", silent=SILENT)


@nox.session(python=PYTHON_VERSIONS)
def lint_plugins(session):

    install_cmd = ["pip", "install", "-e"]
    install_hydra(session, install_cmd)
    plugins = select_plugins(session)

    # plugin linting requires the plugins and their dependencies to be installed
    _install_plugins(session, plugins, install_cmd)

    install_lint_deps(session)

    session.run("flake8", "--config", ".flake8", "plugins")
    # Mypy for plugins
    for plugin in plugins:
        session.chdir(os.path.join("plugins", plugin["path"]))
        blackcmd = ["black", "."]
        isortcmd = ["isort", "."]
        if not FIX:
            blackcmd += ["--check"]
            isortcmd += ["--check", "--diff"]
        session.run(*blackcmd, silent=SILENT)
        session.run(*isortcmd, silent=SILENT)
        session.chdir(BASE)

    session.run("mypy", ".", "--strict", silent=SILENT)


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize(
    "install_cmd",
    PLUGINS_INSTALL_COMMANDS,
    ids=[" ".join(x) for x in PLUGINS_INSTALL_COMMANDS],
)
def test_core(session, install_cmd):
    _upgrade_basic(session)
    install_hydra(session, install_cmd)
    session.install("pytest")
    run_pytest(session, "tests")

    # test discovery_test_plugin
    run_pytest(session, "tests/test_plugins/discovery_test_plugin", "--noconftest")

    # run namespace config loader tests
    run_pytest(session, "tests/test_plugins/namespace_pkg_config_source_test")

    # Install and test example app
    session.run(*install_cmd, "examples/advanced/hydra_app_example", silent=SILENT)
    run_pytest(session, "examples/advanced/hydra_app_example")


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize(
    "install_cmd",
    PLUGINS_INSTALL_COMMANDS,
    ids=[" ".join(x) for x in PLUGINS_INSTALL_COMMANDS],
)
def test_plugins(session, install_cmd):
    _upgrade_basic(session)
    session.install("pytest")
    install_hydra(session, install_cmd)
    selected_plugin = select_plugins(session)
    for plugin in selected_plugin:
        cmd = list(install_cmd) + [os.path.join("plugins", plugin["path"])]
        session.run(*cmd, silent=SILENT)

    # Test that we can import Hydra
    session.run("python", "-c", "from hydra import main", silent=SILENT)

    # Test that we can import all installed plugins
    for plugin in selected_plugin:
        session.run("python", "-c", f"import {plugin['module']}")

    # Run Hydra tests to verify installed plugins did not break anything
    if not SKIP_CORE_TESTS:
        run_pytest(session, "tests")
    else:
        session.log("Skipping Hydra core tests")

    # Run tests for all installed plugins
    for plugin in selected_plugin:
        # install all other plugins that are compatible with the current Python version
        session.chdir(os.path.join(BASE, "plugins", plugin["path"]))
        run_pytest(session)


@nox.session(python="3.8")
def coverage(session):
    coverage_env = {
        "COVERAGE_HOME": BASE,
        "COVERAGE_FILE": f"{BASE}/.coverage",
        "COVERAGE_RCFILE": f"{BASE}/.coveragerc",
    }

    _upgrade_basic(session)
    session.install("coverage", "pytest")
    session.run("pip", "install", "-e", ".", silent=SILENT)
    session.run("coverage", "erase")

    selected_plugins = select_plugins(session)
    for plugin in selected_plugins:
        session.run(
            "pip",
            "install",
            "-e",
            os.path.join("plugins", plugin["path"]),
            silent=SILENT,
        )

    session.run("coverage", "erase", env=coverage_env)
    # run plugin coverage
    for plugin in selected_plugins:
        session.chdir(os.path.join("plugins", plugin["path"]))
        cov_args = ["coverage", "run", "--append", "-m"]
        cov_args.extend(pytest_args(session))
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
        *pytest_args(session),
    )

    # Increase the fail_under as coverage improves
    session.run("coverage", "report", "--fail-under=80", env=coverage_env)
    session.run("coverage", "erase", env=coverage_env)


@nox.session(python=PYTHON_VERSIONS)
def test_jupyter_notebooks(session):
    versions = copy.copy(DEFAULT_PYTHON_VERSIONS)
    if session.python not in versions:
        session.skip(
            f"Not testing Jupyter notebook on Python {session.python}, supports [{','.join(versions)}]"
        )
    # pyzmq 19.0.1 has installation issues on Windows
    session.install("jupyter", "nbval", "pyzmq==19.0.0")
    install_hydra(session, ["pip", "install", "-e"])
    args = pytest_args(
        session, "--nbval", "examples/notebook/hydra_notebook_example.ipynb"
    )
    # Jupyter notebook test on Windows yield warnings
    args = [x for x in args if x != "-Werror"]
    session.run(*args, silent=SILENT)

    args = pytest_args(session, "--nbval", "examples/notebook/%run_test.ipynb")
    args = [x for x in args if x != "-Werror"]
    session.run(*args, silent=SILENT)


def _install_plugins(session, plugins, install_cmd):
    for plugin in plugins:
        cmd = install_cmd + [os.path.join("plugins", plugin["path"])]
        session.run(*cmd, silent=SILENT)
