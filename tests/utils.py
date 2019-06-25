import pytest
import tempfile
from hydra import Hydra
import shutil
import copy


class TaskTestFunction:
    def __init__(self):
        self.temp_dir = None
        self.cfg = None
        self.overrides = None
        self.hydra = None

    def __call__(self, cfg):
        # executed by hydra
        self.cfg = cfg

    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        overrides = copy.deepcopy(self.overrides)
        overrides.append(f"hydra.run_dir={self.temp_dir}")
        self.hydra.run(overrides=overrides)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.temp_dir)


@pytest.fixture(scope="function")
def task_runner():
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
