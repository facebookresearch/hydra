import tempfile

import pytest
from omegaconf import OmegaConf

from hydra import ConfigLoader
from hydra.test_utils.utils import chdir_hydra_root
from hydra.errors import MissingConfigException

chdir_hydra_root()


def test_override_run_dir_without_hydra_cfg():
    config_loader = ConfigLoader(conf_dir='.', conf_filename=None)
    hydra_cfg = config_loader.load_hydra_cfg(['hydra.run.dir=abc'])
    assert hydra_cfg.hydra.run.dir == 'abc'


def test_override_run_dir_with_hydra_cfg():
    config_loader = ConfigLoader(conf_dir='demos/99_hydra_configuration/workdir/', conf_filename=None)
    hydra_cfg = config_loader.load_hydra_cfg(['hydra.run.dir=abc'])
    assert hydra_cfg.hydra.run.dir == 'abc'


def test_conf_dir_not_directory():
    with tempfile.NamedTemporaryFile() as f:
        config_loader = ConfigLoader(conf_dir=f.name, conf_filename=None)
        with pytest.raises(IOError):
            config_loader.load_hydra_cfg()


def test_load_configuration():
    config_loader = ConfigLoader(conf_dir='demos/3_config_file', conf_filename='config.yaml')
    cfg = config_loader.load_configuration(overrides=['abc=123'])
    assert cfg['task_cfg'] == OmegaConf.create(dict(abc=123, dataset=dict(name='imagenet', path='/datasets/imagenet')))


def test_load_with_missing_default():
    config_loader = ConfigLoader(conf_dir='tests/configs', conf_filename='missing-default.yaml')
    with pytest.raises(MissingConfigException):
        config_loader.load_configuration()


def test_load_with_missing_optional_default():
    config_loader = ConfigLoader(conf_dir='tests/configs', conf_filename='missing-optional-default.yaml')
    cfg = config_loader.load_configuration()
    assert cfg['task_cfg'] == {}


def test_load_with_optional_default():
    config_loader = ConfigLoader(conf_dir='tests/configs', conf_filename='optional-default.yaml')
    cfg = config_loader.load_configuration()
    assert cfg['task_cfg'] == dict(foo=10)


def test_load_changing_group_in_default():
    config_loader = ConfigLoader(conf_dir='tests/configs', conf_filename='optional-default.yaml')
    cfg = config_loader.load_configuration(['group1=file2'])
    assert cfg['task_cfg'] == dict(foo=20)


def test_load_adding_group_not_in_default():
    config_loader = ConfigLoader(conf_dir='tests/configs', conf_filename='optional-default.yaml')
    cfg = config_loader.load_configuration(['group2=file1'])
    assert cfg['task_cfg'] == dict(foo=10, bar=100)


def test_load_history():
    config_loader = ConfigLoader(conf_dir='tests/configs', conf_filename='missing-optional-default.yaml')
    config_loader.load_configuration()
    assert config_loader.get_load_history() == [('pkg://hydra.default_conf/hydra.yaml', True),
                                                ('pkg://hydra.default_conf/hydra_logging.yaml', True),
                                                ('pkg://hydra.default_conf/task_logging.yaml', True),
                                                ('tests/configs/missing-optional-default.yaml', True),
                                                ('tests/configs/foo/missing.yaml', False)]
