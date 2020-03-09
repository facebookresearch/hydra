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
SKIP_CORE_TESTS = "0"

# Allow limiting testing to specific plugins
# The list ['ALL'] indicates all plugins
PLUGINS = os.environ.get("PLUGINS", "ALL").split(",")
SKIP_CORE_TESTS = os.environ.get("SKIP_CORE_TESTS", SKIP_CORE_TESTS) != "0"

SILENT = os.environ.get("VERBOSE", "0") == "0"


def find_python_files(folder):
    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            if filename.endswith(".py"):
                yield os.path.join(root, filename)


def install_hydra(session, cmd):
    # clean install hydra
    session.chdir(BASE)
    session.run(*cmd, ".", silent=SILENT)


def pytest_args(session, *args):
    ret = ["pytest"]
    ret.extend(args)
    if len(session.posargs) > 0:
        ret.extend(session.posargs)
    return ret


def run_pytest(session, directory="."):
    pytest_cmd = pytest_args(session, directory)
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


def get_current_os() -> str:
    current_os = platform.system()
    if current_os == "Darwin":
        current_os = "MacOS"
    return current_os


def select_plugins(session):
    """
    Select all plugins that should be tested in this session.
    Considers the current Python version and operating systems against the supported ones,
    as well as the user plugins selection (via the PLUGINS environment variable).
    """

    assert session.python is not None, "Session python version is not specified"

    example_plugins = [
        {"name": x, "path": "examples/{}".format(x)}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins/examples")))
    ]
    plugins = [
        {"name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins")))
        if x != "examples"
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


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    session.install("--upgrade", "setuptools", "pip", silent=SILENT)
    session.run("pip", "install", "-r", "requirements/dev.txt", silent=SILENT)
    session.run("pip", "install", "-e", ".", silent=SILENT)
    session.run("flake8", "--config", ".circleci/flake8_py3.cfg")

    session.install("black")
    # if this fails you need to format your code with black
    session.run("black", "--check", ".", silent=SILENT)

    session.run("isort", "--check", ".", silent=SILENT)

    # Mypy
    session.run("mypy", ".", "--strict", silent=SILENT)

    # Mypy for plugins
    for plugin in select_plugins(session):
        session.run(
            "mypy", os.path.join("plugins", plugin["path"]), "--strict", silent=SILENT
        )

    # Mypy for examples
    for pyfie in find_python_files("examples"):
        session.run("mypy", pyfie, "--strict", silent=SILENT)


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize(
    "install_cmd",
    PLUGINS_INSTALL_COMMANDS,
    ids=[" ".join(x) for x in PLUGINS_INSTALL_COMMANDS],
)
def test_core(session, install_cmd):
    session.install("--upgrade", "setuptools", "pip")
    install_hydra(session, install_cmd)
    session.install("pytest")
    run_pytest(session, "tests")

    # test discovery_test_plugin
    run_pytest(session, "tests/test_plugins/discovery_test_plugin")

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
    session.install("--upgrade", "setuptools", "pip")
    session.install("pytest")
    install_hydra(session, install_cmd)
    selected_plugin = select_plugins(session)
    # Install all supported plugins in session
    for plugin in selected_plugin:
        cmd = list(install_cmd) + [os.path.join("plugins", plugin["path"])]
        session.run(*cmd, silent=SILENT)

    # Test that we can import Hydra
    session.run("python", "-c", "from hydra import main", silent=SILENT)

    # Test that we can import all installed plugins
    for plugin in selected_plugin:
        session.run("python", "-c", "import {}".format(plugin["module"]))

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

    session.install("--upgrade", "setuptools", "pip")
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
def test_jupyter_notebook(session):
    versions = copy.copy(DEFAULT_PYTHON_VERSIONS)
    if session.python not in versions:
        session.skip(
            f"Not testing Jupyter notebook on Python {session.python}, supports [{','.join(versions)}]"
        )
    session.install("--upgrade", "setuptools", "pip")
    session.install("jupyter", "nbval")
    install_hydra(session, ["pip", "install", "-e"])
    session.run(
        *pytest_args(
            session, "--nbval", "examples/notebook/hydra_notebook_example.ipynb"
        ),
        silent=SILENT,
    )
