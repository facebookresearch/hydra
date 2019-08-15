# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

import nox

BASE = os.path.abspath(os.path.dirname(__file__))

DEFAULT_PYTHON_VERSIONS = ["2.7", "3.5", "3.6", "3.7"]

PYTHON_VERSIONS = os.environ.get(
    "NOX_PYTHON_VERSIONS", ",".join(DEFAULT_PYTHON_VERSIONS)
).split(",")

PLUGINS_INSTALL_COMMANDS = (
    # TODO: enable after october when https://github.com/pypa/pip/pull/6770 is public
    # ["pip", "install", "."],
    ["pip", "install", "-e", "."],
)


def install_hydra(session):
    # clean install hydra
    session.chdir(BASE)
    # TODO: This would better be 'pip install .'
    # but until https://github.com/pypa/pip/pull/6770 is public this is too slow.
    session.run("pip", "install", "-e", ".", silent=True)


def install_pytest(session):
    if session.python == "2.7":
        session.install("pytest")
    else:
        session.install("pytest", "pytest_parallel")


def run_pytest(session):
    session.run("pytest", silent=True)
    # if session.python == "2.7":
    #     session.run("pytest", silent=True)
    # else:
    #     session.run("pytest", "--workers=30", silent=True)


def plugin_names():
    return sorted(os.listdir(os.path.join(BASE, "plugins")))


def get_all_plugins():
    return [(plugin, "hydra_plugins." + plugin) for plugin in plugin_names()]


@nox.session(python=PYTHON_VERSIONS)
def test_core(session):
    session.install("--upgrade", "setuptools", "pip")
    install_hydra(session)
    install_pytest(session)
    run_pytest(session)


def get_python_versions(session, setup_py):
    out = session.run("python", setup_py, "--classifiers", silent=True).split("\n")
    pythons = filter(lambda line: "Programming Language :: Python" in line, out)
    return [p[len("Programming Language :: Python :: ") :] for p in pythons]


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize(
    "install_cmd",
    PLUGINS_INSTALL_COMMANDS,
    ids=[" ".join(x) for x in PLUGINS_INSTALL_COMMANDS],
)
@nox.parametrize("plugin", plugin_names(), ids=plugin_names())
def test_plugin(session, plugin, install_cmd):
    session.install("--upgrade", "setuptools", "pip")

    # Verify this plugin supports the python we are testing on, skip otherwise
    plugin_python_versions = get_python_versions(
        session, os.path.join(BASE, "plugins", plugin, "setup.py")
    )
    if session.python not in plugin_python_versions:
        session.skip(
            "Not testing {} on Python {}, supports [{}]".format(
                plugin, session.python, ",".join(plugin_python_versions)
            )
        )

    install_hydra(session)

    all_plugins = get_all_plugins()
    # Install all plugins in session
    for a_plugin in all_plugins:
        cmd = list(install_cmd) + [os.path.join("plugins", a_plugin[0])]
        session.run(*cmd, silent=True)

    # Test that we can import Hydra
    session.run("python", "-c", "from hydra import Hydra", silent=True)

    # Test that we can import all installed plugins
    for a_plugin in all_plugins:
        session.run("python", "-c", "import {}".format(a_plugin[1]))

    install_pytest(session)

    # Run Hydra tests
    run_pytest(session)

    # Run tests for current plugin
    session.chdir(os.path.join(BASE, "plugins", plugin))
    run_pytest(session)


# code coverage runs with python 3.6
@nox.session(python="3.6")
def coverage(session):
    session.install("--upgrade", "setuptools", "pip")
    session.install("coverage", "pytest")
    session.run("pip", "install", "-e", ".", silent=True)
    # Install all plugins in session
    for plugin in get_all_plugins():
        session.run(
            "pip", "install", "-e", os.path.join("plugins", plugin[0]), silent=True
        )

    session.run("coverage", "erase")
    session.run("coverage", "run", "--append", "-m", "pytest", silent=True)
    for plugin in plugin_names():
        plugin_python_versions = get_python_versions(
            session, os.path.join(BASE, "plugins", plugin, "setup.py")
        )
        if session.python not in plugin_python_versions:
            continue

        session.run(
            "coverage",
            "run",
            "--append",
            "-m",
            "pytest",
            os.path.join("plugins", plugin),
            silent=True,
        )

    # Increase the fail_under as coverage improves
    session.run("coverage", "report", "--fail-under=80")

    session.run("coverage", "erase")


@nox.session
@nox.parametrize("py_ver", [2, 3])
def lint(session, py_ver):
    session.install("--upgrade", "setuptools", "pip")
    session.install("flake8")
    session.run("pip", "install", "-e", ".", silent=True)
    session.run("flake8", "--config", ".circleci/flake8_py{}.cfg".format(py_ver))

    session.install("black")
    # if this fails you need to format your code with black
    session.run("black", "--check", ".")
