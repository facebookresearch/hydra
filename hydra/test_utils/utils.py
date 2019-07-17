import copy
import logging
import os
import tempfile

import pytest
import shutil
from omegaconf import OmegaConf

from hydra import Hydra

log = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def task_runner():
    class TaskTestFunction:
        def __init__(self):
            self.temp_dir = None
            self.overrides = None
            self.hydra = None
            self.job_ret = None

        def __call__(self, cfg):
            log.info("Hello from run")
            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append("hydra.run.dir={}".format(self.temp_dir))
            self.job_ret = self.hydra.run(overrides=overrides)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir)

    def _(conf_dir, conf_filename=None, overrides=[]):
        task = TaskTestFunction()
        hydra = Hydra(task_name="task",
                      conf_dir=conf_dir,
                      conf_filename=conf_filename,
                      task_function=task,
                      verbose=None)

        task.hydra = hydra
        task.overrides = overrides
        return task

    return _


@pytest.fixture(scope="function")
def sweep_runner():
    class SweepTaskFunction:
        def __init__(self):
            self.temp_dir = None
            self.cfg = None
            self.overrides = None
            self.hydra = None
            self.sweeps = None

            self.all_configs = None

        def __call__(self, cfg):
            log.info("Hello from sweep")
            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append("hydra.sweep.dir={}".format(self.temp_dir))
            self.returns = self.hydra.sweep(overrides=overrides)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir)

    def _(conf_dir, conf_filename=None, overrides=[]):
        sweep = SweepTaskFunction()
        hydra = Hydra(task_name="task",
                      conf_dir=conf_dir,
                      conf_filename=conf_filename,
                      task_function=sweep,
                      verbose=None)

        sweep.hydra = hydra
        sweep.overrides = overrides
        return sweep

    return _


def chdir_hydra_root():
    cur = os.getcwd()
    max_up = 4
    target = 'ATTRIBUTION'
    while not os.path.exists(os.path.join(cur, target)) and max_up > 0:
        cur = os.path.relpath(os.path.join(cur, ".."))
        max_up = max_up - 1
    if max_up == 0:
        raise IOError("Could not find {} in parents of {}".format(target, os.getcwd()))
    os.chdir(cur)


def verify_dir_outputs(d, overrides=[]):
    assert os.path.exists(os.path.join(d, 'task.log'))
    assert os.path.exists(os.path.join(d, 'config.yaml'))
    assert os.path.exists(os.path.join(d, 'overrides.yaml'))
    # TODO: reactivate after OmegaConf but is fixed:
    # https://github.com/omry/omegaconf/issues/25
    # assert OmegaConf.load(os.path.join(d, 'overrides.yaml')) == OmegaConf.from_dotlist(overrides)
