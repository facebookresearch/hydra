import pytest
from hydra.utils import fullname
from hydra._internal import Plugins
from hydra.plugins import Plugin, Launcher, Sweeper, SearchPathPlugin
from hydra.utils import get_class

launchers = [
    "hydra._internal.core_plugins.basic_launcher.BasicLauncher",
    "hydra_plugins.fairtask.fairtask_launcher.FAIRTaskLauncher",
    "hydra_plugins.submitit.submitit_launcher.SubmititLauncher",
]
sweepers = ["hydra._internal.core_plugins.basic_sweeper.BasicSweeper"]
search_path_plugins = [
    "hydra_plugins.fair_cluster.fair_cluster_defaults.FAIRClusterDefaults"
]


@pytest.mark.parametrize(
    "plugin_type, expected",
    [
        (Launcher, launchers),
        (Sweeper, sweepers),
        (SearchPathPlugin, search_path_plugins),
        (Plugin, launchers + sweepers + search_path_plugins),
    ],
)
def test_discover(plugin_type, expected):
    plugins = Plugins.discover(plugin_type)
    plugins = sorted(plugins, key=lambda x: fullname(x))
    expected_classes = [get_class(x) for x in sorted(expected)]
    assert plugins == expected_classes
