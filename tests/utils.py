import pytest
import tempfile
from hydra import Hydra
import shutil
import copy
import logging
import os

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
            # executed by hydra
            # arbitrary return value
            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append(f"hydra.run_dir={self.temp_dir}")
            self.job_ret = self.hydra.run(overrides=overrides)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir)

    def _(conf_dir, conf_filename=None, overrides=[]):
        task = TaskTestFunction()
        hydra = Hydra(task_name="test-task",
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
            # arbitrary return value
            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append(f"hydra.sweep.dir={self.temp_dir}")
            self.returns = self.hydra.sweep(overrides=overrides)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir)

    def _(conf_dir, conf_filename=None, overrides=[]):
        sweep = SweepTaskFunction()
        hydra = Hydra(task_name="test-sweep",
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
    max_up = 3
    target = 'setup.py'
    while not os.path.exists(os.path.join(cur, target)) and max_up > 0:
        cur = os.path.relpath(os.path.join(cur, ".."))
        max_up = max_up - 1
    if max_up == 0:
        raise IOError("Could not find {} in parents of {}".format(target, os.getcwd()))
    os.chdir(cur)
