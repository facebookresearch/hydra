# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os

import nox

BASE = os.path.abspath(os.path.dirname(__file__))

DEFAULT_PYTHON_VERSIONS = ["2.7", "3.5", "3.6", "3.7"]

PYTHON_VERSIONS = os.environ.get(
    "NOX_PYTHON_VERSIONS", ",".join(DEFAULT_PYTHON_VERSIONS)
).split(",")

PLUGINS_INSTALL_COMMANDS = (["pip", "install"], ["pip", "install", "-e"])

# Allow limiting testing to specific plugins
# The list ['ALL'] indicates all plugins
PLUGINS = os.environ.get("PLUGINS", "ALL").split(",")

SILENT = os.environ.get("VERBOSE", "0") == "0"


def install_hydra(session, cmd):
    # clean install hydra
    session.chdir(BASE)
    session.run(*cmd, ".", silent=SILENT)


def install_pytest(session):
    session.install("pytest")
    # if session.python == "2.7":
    #     session.install("pytest")
    # else:
    #     session.install("pytest", "pytest_parallel")


def run_pytest(session, directory="."):
    session.run("pytest", directory, silent=False, *session.posargs)
    # if session.python == "2.7":
    #     session.run("pytest", silent=SILENT)
    # else:
    #     session.run("pytest", "--workers=30", silent=SILENT)


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
    out = session.run("python", setup_py, "--classifiers", silent=True).split("\n")
    pythons = filter(lambda line: "Programming Language :: Python" in line, out)
    return [p[len("Programming Language :: Python :: ") :] for p in pythons]


def get_plugin_python_version(session, plugin):
    return get_setup_python_versions(
        session, os.path.join(BASE, "plugins", plugin["path"], "setup.py")
    )


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize(
    "install_cmd",
    PLUGINS_INSTALL_COMMANDS,
    ids=[" ".join(x) for x in PLUGINS_INSTALL_COMMANDS],
)
@nox.parametrize("plugin", list_plugins(), ids=plugin_names())
def test_plugin(session, plugin, install_cmd):
    session.install("--upgrade", "setuptools", "pip")
    # Verify this plugin supports the python we are testing on, skip otherwise
    plugin_python_versions = get_plugin_python_version(session, plugin)
    if session.python not in plugin_python_versions:
        session.skip(
            "Not testing {} on Python {}, supports [{}]".format(
                plugin, session.python, ",".join(plugin_python_versions)
            )
        )

    install_hydra(session, install_cmd)
    plugin_enabled = {}
    all_plugins = get_all_plugins()
    # Install all plugins in session
    for plugin in all_plugins:
        cmd = list(install_cmd) + [os.path.join("plugins", plugin["path"])]
        pythons = get_plugin_python_version(session, plugin)
        plugin_enabled[plugin["path"]] = session.python in pythons
        if plugin_enabled[plugin["path"]]:
            session.run(*cmd, silent=SILENT)

    # Test that we can import Hydra
    session.run("python", "-c", "from hydra import main", silent=SILENT)

    # Test that we can import all installed plugins
    for plugin in all_plugins:
        # install all other plugins that are compatible with the current Python version
        if plugin_enabled[plugin["path"]]:
            session.run("python", "-c", "import {}".format(plugin["module"]))

    install_pytest(session)

    # Run Hydra tests
    run_pytest(session, "tests")

    # Run tests for current plugin
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


@nox.session
@nox.parametrize("py_ver", [2, 3])
def lint(session, py_ver):
    session.install("--upgrade", "setuptools", "pip")
    session.install("flake8", "flake8-copyright")
    session.run("pip", "install", "-e", ".", silent=SILENT)
    session.run("flake8", "--config", ".circleci/flake8_py{}.cfg".format(py_ver))

    session.install("black")
    # if this fails you need to format your code with black
    session.run("black", "--check", ".")


@nox.session(python=PYTHON_VERSIONS)
def test_jupyter_notebook(session):
    versions = copy.copy(DEFAULT_PYTHON_VERSIONS)
    versions.remove("2.7")
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
