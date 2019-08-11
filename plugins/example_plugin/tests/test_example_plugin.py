# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
def test_example_plugin():
    from hydra_plugins.example_plugin import ExamplePlugin

    a = ExamplePlugin(10)
    assert a.add(20) == 30
