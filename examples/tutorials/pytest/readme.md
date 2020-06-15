See discussion in issue [#591](https://github.com/facebookresearch/hydra/issues/591#issuecomment-643856511).  Merge this into [#676](https://github.com/facebookresearch/hydra/issues/676).
```bash
$ tree .
.
├── app
│   ├── __init__.py
│   └── conf
│       └── config.yaml
└── tests
    ├── __init__.py
    └── test_sample.py

3 directories, 4 files
$ cd tests
$ pytest -q test_sample.py 
.                                                                                                [100%]
1 passed in 0.56s
(base) LP-VLIU-OSX:tests vliu$ cat test_sample.py 
import unittest
from hydra.experimental import compose, initialize

class FullUnitTest(unittest.TestCase):
    def test_config(self):
        initialize(config_dir="../app/conf")
        conf = compose("config.yaml")
        print(conf.pretty())
        pass
$
```

