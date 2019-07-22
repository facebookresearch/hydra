import os

import nox

BASE = os.path.abspath(os.path.dirname(__file__))


def plugin_names():
    return sorted(os.listdir(os.path.join(BASE, 'plugins')))


def clean_all(session):
    session.chdir(os.path.join(BASE))
    session.run('python', 'setup.py', 'clean')


def clean_and_install_hydra(session):
    session.chdir(os.path.join(BASE))
    session.run('python', 'setup.py', 'clean', 'install')


def nox_test_hydra_core():
    default_versions = [
        '2.7',
        '3.6'
    ]
    python_versions = os.environ.get("HYDRA_CORE_PYTHON_VERSIONS",
                                     ','.join(default_versions)).split(',')

    @nox.session(python=python_versions)
    def test_core(session):
        session.install('--upgrade', 'setuptools', 'pip')
        clean_and_install_hydra(session)
        session.install('pytest')
        session.run('pytest')


def nox_test_plugins():
    default_versions = ['3.6']
    python_versions = os.environ.get("HYDRA_PLUGINS_PYTHON_VERSIONS",
                                     ','.join(default_versions)).split(',')

    # different installation commands for plugins
    plugins_install_commands = (
        ('pip', 'install', '.'),
        ('pip', 'install', '-e', '.'),
    )

    @nox.session(python=python_versions)
    @nox.parametrize('plugin_name', plugin_names())
    @nox.parametrize('install_cmd', plugins_install_commands)
    def test_plugins(session, plugin_name, install_cmd):
        session.install('--upgrade', 'setuptools', 'pip')
        clean_and_install_hydra(session)

        all_plugins = [(plugin, 'hydra_plugins.' + plugin) for plugin in plugin_names()]
        # Install all plugins in session
        for plugin in all_plugins:
            session.chdir(os.path.join(BASE, "plugins", plugin[0]))
            session.run(*install_cmd)

        # Test that we can import Hydra
        session.run('python', '-c', 'from hydra import Hydra')
        # Test that we can import all installed plugins
        for plugin in all_plugins:
            session.run('python', '-c', 'import {}'.format(plugin[1]))

        # Run tests for current plugin
        session.chdir(os.path.join(BASE, "plugins", plugin_name))
        session.install('pytest')
        session.run('pytest')


nox_test_hydra_core()
nox_test_plugins()
