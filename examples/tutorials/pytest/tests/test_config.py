# test_config.py 

import unittest
from hydra.experimental import compose, initialize

class FullUnitTest(unittest.TestCase):
    def test_config(self):
        initialize(config_dir="../app/conf")
        conf = compose("config.yaml",strict=False)
        print(conf.pretty())
        pass
