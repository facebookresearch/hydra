# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra_plugins.fair_cluster import FAIRClusterDefaults
from omegaconf import OmegaConf, DictConfig, ListConfig, Config, BaseNode

from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin
from hydra._internal import pathlib

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import integration_test


def test_discovery():
    launchers = Plugins.discover(SearchPathPlugin)
    # discovered plugins are actually different class objects, compare by name
    assert FAIRClusterDefaults.__name__ in [x.__name__ for x in launchers]


# TODO: this can be a function in OmegaConf
def overlaps(query, cfg):
    if isinstance(query, DictConfig):
        if not isinstance(cfg, DictConfig):
            return False
        for k, v in query.items(resolve=False):
            if k in cfg:
                cv = cfg.get_node(k)
                if isinstance(cv, BaseNode):
                    cv = cv.value()
                if isinstance(cv, Config):
                    if not overlaps(v, cv):
                        return False
                else:
                    if v != cv:
                        return False
            else:
                return False
    elif isinstance(query, ListConfig):
        if not isinstance(cfg, ListConfig):
            return False
        for idx, item in enumerate(query):
            cv = cfg.get_node(idx)
            if isinstance(cv, BaseNode):
                cv = cv.value()
            if isinstance(item, Config):
                if not overlaps(item, cv):
                    return False
            else:
                if item != cv:
                    return False
    return True


def test_fair_cluster(tmpdir):
    task_config = OmegaConf.create()
    overrides = []
    prints = "HydraConfig().pretty()"
    expected_outputs = None
    output = integration_test(tmpdir, task_config, overrides, prints, expected_outputs)
    path = (
        pathlib.Path(__file__)
        / "../../hydra_plugins/fair_cluster/conf/hydra/output/default.yaml"
    )
    expected = OmegaConf.load(str(path))

    actual = OmegaConf.create(str(output))
    assert overlaps(expected, actual)
