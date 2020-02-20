# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import copy
import os
import platform
from typing import List

import nox

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

SILENT = os.environ.get("VERBOSE", "0") == "0"


def find_python_files(folder):
    for root, folders, files in os.walk(folder,):
        for filename in folders + files:
            if filename.endswith(".py"):
                yield os.path.join(root, filename)


def install_hydra(session, cmd):
    # clean install hydra
    session.chdir(BASE)
    session.run(*cmd, ".", silent=SILENT)


def install_pytest(session):
    session.install("pytest")
    # session.install("pytest", "pytest_parallel")


def run_pytest(session, directory="."):
    if len(session.posargs) == 0:
        session.run("pytest", directory, silent=False)
    else:
        session.run("pytest", *session.posargs, silent=False)
    # session.run("pytest", "--workers=30", silent=SILENT)


def plugin_names():
    return [x["name"] for x in list_plugins()]


def list_plugins():
    example_plugins = [
        {"name": x, "path": "examples/{}".format(x)}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins/examples")))
    ]
    plugins = [
        {"name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins")))
        if x != "examples"
    ]
    return plugins + example_plugins


def get_all_plugins():
    return [
        {
            "name": plugin["name"],
            "path": plugin["path"],
            "module": "hydra_plugins." + plugin["name"],
        }
        for plugin in list_plugins()
        if plugin["name"] in PLUGINS or PLUGINS == ["ALL"]
    ]


def test_example_app(session, install_cmd):
    # Install and test example app
    session.run(*install_cmd, "examples/advanced/hydra_app_example", silent=SILENT)
    session.run(
        "pytest", "examples/advanced/hydra_app_example", silent=SILENT, *session.posargs
    )


@nox.session
def lint(session):
    session.install("--upgrade", "setuptools", "pip")
    # needed for isort to properly identify pytest as third party
    session.install("pytest")
    session.install(
        "mypy",
        "flake8",
        "flake8-copyright",
        "git+git://github.com/timothycrosley/isort.git@c54b3dd4620f9b3e7ac127c583ecb029fb90f1b7",
    )
    session.run("pip", "install", "-e", ".", silent=SILENT)
    session.run("flake8", "--config", ".circleci/flake8_py3.cfg")

    session.install("black")
    # if this fails you need to format your code with black
    session.run("black", "--check", ".")

    session.run("isort", "--check", ".")

    # Mypy
    session.run("mypy", ".", "--strict")

    # Mypy for plugins
    for plugin in get_all_plugins():
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
    install_pytest(session)
    run_pytest(session, "tests")

    test_example_app(session, install_cmd)


def get_setup_python_versions(session, setup_py):
    out = session.run("python", setup_py, "--classifiers", silent=True).splitlines()
    pythons = filter(lambda line: "Programming Language :: Python" in line, out)
    return [p[len("Programming Language :: Python :: ") :] for p in pythons]


def get_plugin_python_version(session, plugin):
    return get_setup_python_versions(
        session, os.path.join(BASE, "plugins", plugin["path"], "setup.py")
    )


def get_plugin_os_names(session: nox.session, plugin: str) -> List[str]:
    setup_py = os.path.join(BASE, "plugins", plugin["path"], "setup.py")
    out = session.run("python", setup_py, "--classifiers", silent=True).splitlines()
    oses = list(filter(lambda line: "Operating System" in line, out))
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


def check_if_os_supports_plugin(session: nox.session, plugin: str) -> bool:
    """Check if the given plugin is supported for the current OS"""
    current_os = get_current_os()
    plugin_os_names = get_plugin_os_names(session, plugin)
    return current_os in plugin_os_names


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize(
    "install_cmd",
    PLUGINS_INSTALL_COMMANDS,
    ids=[" ".join(x) for x in PLUGINS_INSTALL_COMMANDS],
)
def test_plugins(session, install_cmd):
    session.install("--upgrade", "setuptools", "pip")
    install_pytest(session)
    install_hydra(session, install_cmd)
    plugin_enabled = {}
    all_plugins = get_all_plugins()
    # Install all supported plugins in session
    for plugin in all_plugins:
        # Verify this plugin supports the python we are testing on, skip otherwise
        plugin_python_versions = get_plugin_python_version(session, plugin)
        plugin_enabled[plugin["path"]] = session.python in plugin_python_versions
        if not plugin_enabled[plugin["path"]]:
            py_str = ",".join(plugin_python_versions)
            session.log(
                f"Not testing {plugin['name']} on Python {session.python}, supports [{py_str}]"
            )
            continue

        # Verify this plugin supports the OS we are testing on, skip otherwise
        plugin_enabled[plugin["path"]] = check_if_os_supports_plugin(session, plugin)
        if not plugin_enabled[plugin["path"]]:
            os_str = ",".join(get_plugin_os_names(session, plugin))
            session.log(
                f"Not testing {plugin['name']} on OS {get_current_os()}, supports [{os_str}]"
            )
            continue

        cmd = list(install_cmd) + [os.path.join("plugins", plugin["path"])]
        session.run(*cmd, silent=SILENT)

    # Test that we can import Hydra
    session.run("python", "-c", "from hydra import main", silent=SILENT)

    # Test that we can import all installed plugins
    for plugin in all_plugins:
        # install all other plugins that are compatible with the current Python version
        if plugin_enabled[plugin["path"]]:
            session.run("python", "-c", "import {}".format(plugin["module"]))

    # Run Hydra tests to verify installed plugins did not break anything
    run_pytest(session, "tests")

    # Run tests for all installed plugins
    for plugin in all_plugins:
        # install all other plugins that are compatible with the current Python version
        if plugin_enabled[plugin["path"]]:
            session.chdir(os.path.join(BASE, "plugins", plugin["path"]))
            run_pytest(session)


# code coverage runs with python 3.6
@nox.session(python="3.6")
def coverage(session):
    session.install("--upgrade", "setuptools", "pip")
    session.install("coverage", "pytest")
    session.run("pip", "install", "-e", ".", silent=SILENT)
    # Install all plugins in session
    for plugin in get_all_plugins():
        if check_if_os_supports_plugin(session, plugin):
            session.run(
                "pip",
                "install",
                "-e",
                os.path.join("plugins", plugin["path"]),
                silent=SILENT,
            )

    session.run("coverage", "erase")
    session.run("coverage", "run", "--append", "-m", "pytest", silent=SILENT)
    for plugin in list_plugins():
        plugin_python_versions = get_plugin_python_version(session, plugin)
        if session.python not in plugin_python_versions:
            continue
        if not check_if_os_supports_plugin(session, plugin):
            continue

        session.run(
            "coverage",
            "run",
            "--append",
            "-m",
            "pytest",
            os.path.join("plugins", plugin["path"]),
            silent=SILENT,
        )

    # Increase the fail_under as coverage improves
    session.run("coverage", "report", "--fail-under=80")

    session.run("coverage", "erase")


@nox.session(python=PYTHON_VERSIONS)
def test_jupyter_notebook(session):
    versions = copy.copy(DEFAULT_PYTHON_VERSIONS)
    if session.python not in versions:
        session.skip(
            "Not testing Jupyter notebook on Python {}, supports [{}]".format(
                session.python, ",".join(versions)
            )
        )
    session.install("--upgrade", "setuptools", "pip")
    session.install("jupyter", "nbval")
    install_hydra(session, ["pip", "install", "-e"])
    session.run(
        "pytest",
        "--nbval",
        "examples/notebook/hydra_notebook_example.ipynb",
        silent=SILENT,
    )
