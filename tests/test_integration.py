import importlib

import pytest
from omegaconf import OmegaConf

from hydra.test_utils.test_utils import integration_test
# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


def create_hydra_launcher_config():
    return OmegaConf.create({'hydra': {
        'hydra_logging': {
            'root': {
                'level': 'ERROR'
            }
        },
        'launcher': {
            'class': 'hydra_plugins.fairtask.FAIRTaskLauncher',
            'params': {
                'no_workers': True,
                'queue': 'local',
                'queues': {
                    'local': {
                        'class': 'fairtask.local.LocalQueueConfig',
                        'params': {
                            'num_workers': 2
                        }
                    }
                }
            }
        }
    }})


@pytest.mark.parametrize('task_config, overrides, filename, expected_name', [
    # TODO : once submitit local queue is fixed activate testss here.
    (None, [], 'no_config.py', 'no_config'),
    (None, ['hydra.name=overridden_name'], 'no_config.py', 'overridden_name'),
    (
            OmegaConf.create(dict(hydra=dict(name='name_from_config_file'))),
            [],
            'with_config.py',
            'name_from_config_file'
    ),
    (
            OmegaConf.create(dict(hydra=dict(name='name_from_config_file'))),
            ['hydra.name=overridden_name'],
            'with_config.py',
            'overridden_name'
    ),
])
@pytest.mark.parametrize('hydra_config, extra_flags, plugin_module', [
    (None, [], None),
    (create_hydra_launcher_config(), ['-s'], 'hydra_plugins.fairtask')
])
def test_task_name(tmpdir,
                   task_config,
                   overrides,
                   filename,
                   expected_name,
                   hydra_config,
                   extra_flags,
                   plugin_module):
    if plugin_module is not None:
        try:
            importlib.import_module(plugin_module)
        except ImportError:
            pytest.skip("Plugin {} not installed".format(plugin_module))

    overrides = extra_flags + overrides
    cfg = OmegaConf.merge(hydra_config or OmegaConf.create(), task_config or OmegaConf.create())
    integration_test(tmpdir,
                     task_config=cfg,
                     overrides=overrides,
                     prints="JobRuntime().get('name')",
                     expected_outputs=expected_name,
                     filename=filename)

# TODO:
# Add tests for customizing workdir
# Port more tests to integration tests.
# Maybe making integration tests more comprehensive (testing output directory content fo
#
