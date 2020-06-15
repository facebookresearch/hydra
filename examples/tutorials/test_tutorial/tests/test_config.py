# test_config.py 

import unittest
from hydra.experimental import compose, initialize

class FullUnitTest(unittest.TestCase):
    def test_config(self):
        conf_path = "../app/conf"
        initialize(config_path=conf_path)
        conf = compose("config.yaml")
        print(conf.pretty())
        pass
