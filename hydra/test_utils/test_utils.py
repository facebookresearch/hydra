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
from contextlib import contextmanager

import pytest
import six
from omegaconf import OmegaConf

from hydra._internal.config_search_path import ConfigSearchPath
from hydra._internal.hydra import Hydra
from hydra.plugins.common.utils import JobReturn

# CircleCI does not have the environment variable USER, breaking the tests.
os.environ["USER"] = "test_user"

log = logging.getLogger(__name__)


@contextmanager
def does_not_raise(enter_result=None):
    yield enter_result


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
            Actual function being executed by Hydra
            """

            return 100

        def __enter__(self):
            self.temp_dir = tempfile.mkdtemp()
            overrides = copy.deepcopy(self.overrides)
            overrides.append("hydra.run.dir={}".format(self.temp_dir))
            self.job_ret = self.hydra.run(overrides=overrides)
            strip_node(self.job_ret.cfg, "hydra.run.dir")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # release log file handles
            logging.shutdown()
            shutil.rmtree(self.temp_dir)

    def _(calling_file, calling_module, config_path, overrides=None, strict=False):
        task = TaskTestFunction()
        hydra = Hydra(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path=config_path,
            task_function=task,
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
            self.hydra = None
            self.sweeps = None
            self.returns = None

        def __call__(self, cfg):
            """
            Actual function being executed by Hydra
            """
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

    def _(calling_file, calling_module, config_path, overrides=None, strict=False):
        sweep = SweepTaskFunction()
        hydra = Hydra(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path=config_path,
            task_function=sweep,
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


def verify_dir_outputs(job_return, overrides=None):
    """
    Verify that directory output makes sense
    """
    assert isinstance(job_return, JobReturn)
    assert os.path.exists(
        os.path.join(job_return.working_dir, job_return.task_name + ".log")
    )

    hydra_dir = os.path.join(
        job_return.working_dir, job_return.hydra_cfg.hydra.output_subdir
    )
    assert os.path.exists(os.path.join(hydra_dir, "config.yaml"))
    assert os.path.exists(os.path.join(hydra_dir, "overrides.yaml"))
    assert OmegaConf.load(
        os.path.join(hydra_dir, "overrides.yaml")
    ) == OmegaConf.create(overrides or [])


def integration_test(
    tmpdir, task_config, overrides, prints, expected_outputs, filename="task.py"
):
    if isinstance(prints, str):
        prints = [prints]
    if isinstance(expected_outputs, str):
        expected_outputs = [expected_outputs]
    if isinstance(task_config, (list, dict)):
        task_config = OmegaConf.create(task_config)

    s = string.Template(
        """import hydra
import os
from hydra.plugins.common.utils import HydraConfig

@hydra.main($CONFIG_PATH)
def experiment(cfg):
    with open("$OUTPUT_FILE", "w") as f:
        $PRINTS

if __name__ == "__main__":
    experiment()
"""
    )

    print_code = ""
    if prints is None or len(prints) == 0:
        print_code = "pass"
    else:
        for p in prints:
            print_code += 'f.write({} + "\\\n")'.format(p)

    config_path = ""
    if task_config is not None:
        cfg_file = tmpdir / "config.yaml"
        task_config.save(str(cfg_file))
        config_path = "config_path='{}'".format("config.yaml")
    output_file = str(tmpdir / "output.txt")
    # replace Windows path separator \ with an escaped version \\
    output_file = output_file.replace("\\", "\\\\")
    code = s.substitute(
        PRINTS=print_code, CONFIG_PATH=config_path, OUTPUT_FILE=output_file
    )
    task_file = tmpdir / filename
    task_file.write_text(six.u(str(code)), encoding="utf-8")
    cmd = [sys.executable, str(task_file)]
    cmd.extend(overrides)
    orig_dir = os.getcwd()
    try:
        os.chdir(str(tmpdir))
        subprocess.check_call(cmd)

        with open(output_file, "r") as f:
            file_str = f.read()
            output = str.splitlines(file_str)

        if expected_outputs is not None:
            assert len(output) == len(expected_outputs)
            for idx in range(len(output)):
                assert output[idx] == expected_outputs[idx]
        # some tests are parsing the file output for more specialized testing.
        return file_str
    finally:
        os.chdir(orig_dir)


def create_search_path(search_path=[], abspath=False):
    csp = ConfigSearchPath()
    csp.append("hydra", "pkg://hydra.conf")
    for sp in search_path:
        csp.append("test", sp if not abspath else os.path.realpath(sp))
    return csp
