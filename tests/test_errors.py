# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pickle

from hydra.errors import MissingConfigException


def test_pickle_missing_config_exception() -> None:
    exception = MissingConfigException("msg", "filename", ["option1", "option2"])
    x = pickle.dumps(exception)
    loaded = pickle.loads(x)  # nosec
    assert isinstance(loaded, MissingConfigException)
    assert loaded.args == ("msg",)
    assert loaded.missing_cfg_file == "filename"
    assert loaded.options == ["option1", "option2"]
