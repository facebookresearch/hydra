from hydra import ConfigLoader


def test_override_run_dir_without_hydra_cfg():
    config_loader = ConfigLoader(conf_dir='.', conf_filename=None)
    hydra_cfg = config_loader.load_hydra_cfg(['hydra.run.dir=abc'])
    assert hydra_cfg.hydra.run.dir == 'abc'


def test_override_run_dir_with_hydra_cfg():
    config_loader = ConfigLoader(conf_dir='demos/99_hydra_configuration/workdir/', conf_filename=None)
    hydra_cfg = config_loader.load_hydra_cfg(['hydra.run.dir=abc'])
    assert hydra_cfg.hydra.run.dir == 'abc'
