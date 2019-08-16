# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Utilities used by tests
"""
import copy
import logging
import os
import shutil
import string
import subprocess
import sys
import tempfile

import pytest
import six
from omegaconf import OmegaConf

from hydra.internal.hydra import Hydra

# CircleCI does not have the environment variable USER, breaking the tests.
os.environ["USER"] = "test_user"

# pylint: disable=C0103
log = logging.getLogger(__name__)


def strip_node(cfg, key):
    """
    Removes a key from a config, key is in dot.notation.
    Nodes that are becoming empty after removing the element inside them will also be removed.
    :param cfg: config node
    :param key: key to strip
    """
    fragments = key.split(".")
    while cfg.select(key) is not None:
        c = cfg
        for f in fragments[0:-1]:
            c = c[f]
        del c[fragments.pop(-1)]
        if c:
            break
        key = ".".join(fragments)


@pytest.fixture(scope="function")
def task_runner():
    """
    Task runner fixture
    """

    class TaskTestFunction:
        """
        Context function
        """

        def __init__(self):
            self.temp_dir = None
            self.overrides = None
            self.hydra = None
            self.job_ret = None

        def __call__(self, cfg):
            """
            Actual function being exectured by Hydra
            """

            log.info("Hello from run")
            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append("hydra.run.dir={}".format(self.temp_dir))
            self.job_ret = self.hydra.run(overrides=overrides)
            strip_node(self.job_ret.cfg, "hydra.run.dir")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir)

    def _(conf_dir, conf_filename=None, overrides=None, strict=False):
        task = TaskTestFunction()
        hydra = Hydra(
            task_name="task",
            conf_dir=conf_dir,
            conf_filename=conf_filename,
            task_function=task,
            verbose=None,
            strict=strict,
        )

        task.hydra = hydra
        task.overrides = overrides or []
        return task

    return _


@pytest.fixture(scope="function")
def sweep_runner():
    """
    Sweep runner fixture
    """

    class SweepTaskFunction:
        """
        Context function
        """

        def __init__(self):
            self.temp_dir = None
            self.cfg = None
            self.overrides = None
            self.hydra = None
            self.sweeps = None
            self.returns = None

            self.all_configs = None

        def __call__(self, cfg):
            """
            Actual function being exectured by Hydra
            """
            log.info("Hello from sweep")
            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append("hydra.sweep.dir={}".format(self.temp_dir))
            self.returns = self.hydra.multirun(overrides=overrides)
            flat = [item for sublist in self.returns for item in sublist]
            for ret in flat:
                strip_node(ret.cfg, "hydra.sweep.dir")

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir)

    def _(conf_dir, conf_filename=None, overrides=None, strict=False):
        sweep = SweepTaskFunction()
        hydra = Hydra(
            task_name="task",
            conf_dir=conf_dir,
            conf_filename=conf_filename,
            task_function=sweep,
            verbose=None,
            strict=strict,
        )

        sweep.hydra = hydra
        sweep.overrides = overrides or []
        return sweep

    return _


def chdir_hydra_root():
    """
    Chage the cwd to the root of the hydra project.
    used from unit tests to make them runnable from anywhere in the tree.
    """
    cur = os.getcwd()
    max_up = 4
    target = "ATTRIBUTION"
    while not os.path.exists(os.path.join(cur, target)) and max_up > 0:
        cur = os.path.relpath(os.path.join(cur, ".."))
        max_up = max_up - 1
    if max_up == 0:
        raise IOError("Could not find {} in parents of {}".format(target, os.getcwd()))
    os.chdir(cur)


def verify_dir_outputs(d, overrides=None):
    """
    Verify that directory output makes sense
    """
    assert os.path.exists(os.path.join(d, "task.log"))
    assert os.path.exists(os.path.join(d, "config.yaml"))
    assert os.path.exists(os.path.join(d, "overrides.yaml"))
    assert OmegaConf.load(os.path.join(d, "overrides.yaml")) == OmegaConf.create(
        overrides or []
    )


def integration_test(
    tmpdir,
    task_config,
    hydra_config,
    overrides,
    prints,
    expected_outputs,
    filename="task.py",
):
    if isinstance(prints, str):
        prints = [prints]
    if isinstance(expected_outputs, str):
        expected_outputs = [expected_outputs]
    if isinstance(task_config, (list, dict)):
        task_config = OmegaConf.create(task_config)
    if isinstance(hydra_config, (list, dict)):
        hydra_config = OmegaConf.create(hydra_config)

    s = string.Template(
        """
import hydra
from hydra.internal.utils import HydraConfig
import os

@hydra.main($CONFIG_PATH)
def experiment(_cfg):
    $PRINTS

if __name__ == "__main__":
    experiment()
"""
    )
    print_code = ""
    for p in prints:
        print_code += "print({});".format(p)

    config_path = ""
    if task_config is not None:
        cfg_file = str(tmpdir / "config.yaml")
        task_config.save(cfg_file)
        config_path = "config_path='{}'".format("config.yaml")

    if hydra_config is not None:
        cfg_file = tmpdir / ".hydra"
        cfg_file.mkdir()
        hydra_config.save(str(cfg_file / "hydra.yaml"))

    code = s.substitute(PRINTS=print_code, CONFIG_PATH=config_path)

    task_file = tmpdir / filename
    task_file.write_text(six.u(str(code)), encoding="utf-8")
    cmd = [sys.executable, str(task_file)]
    cmd.extend(overrides)
    orig_dir = os.getcwd()
    try:
        os.chdir(str(tmpdir))
        result = subprocess.check_output(cmd)
        outputs = result.decode("utf-8").splitlines()
        assert len(outputs) == len(expected_outputs)
        for idx in range(len(outputs)):
            assert outputs[idx] == expected_outputs[idx]
    finally:
        os.chdir(orig_dir)
