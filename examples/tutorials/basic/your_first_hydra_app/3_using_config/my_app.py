# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest
from omegaconf import DictConfig, MissingMandatoryValue, open_dict

import hydra


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    assert cfg.node.loompa == 10  # attribute style access
    assert cfg["node"]["loompa"] == 10  # dictionary style access
    assert cfg.node.zippity == 10  # Variable interpolation
    assert type(cfg.node.zippity) == int  # Variable interpolation inherits the type
    assert cfg.node.do == "oompa 10"  # string interpolation

    # Accessing a field that is not in the config results in an exception:
    with pytest.raises(AttributeError):
        cfg.new_field = 10

    # you can enable config field addition in a context with open_dict:
    with open_dict(cfg):
        cfg.new_field = 10
    assert cfg.new_field == 10

    # You can check if a field is present in the config:
    assert "new_field" in cfg  # dictionary style
    assert hasattr(cfg, "new_field")  # attribute style

    # Accessing a field marked as missing ('???') raises in an exception
    with pytest.raises(MissingMandatoryValue):
        cfg.node.waldo


if __name__ == "__main__":
    my_app()
