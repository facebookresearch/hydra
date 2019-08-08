import re
import shutil
import subprocess
import sys
import tempfile

import pytest
from omegaconf import OmegaConf

from hydra.errors import MissingConfigException
from hydra.test_utils.test_utils import chdir_hydra_root, verify_dir_outputs

chdir_hydra_root()


def test_missing_conf_dir(task_runner):
    with pytest.raises(IOError):
        with task_runner(conf_dir='not_found'):
            pass


def test_missing_conf_file(task_runner):
    with pytest.raises(IOError):
        with task_runner(conf_dir='.', conf_filename='not_found'):
            pass


def test_demos_minimal__no_overrides(task_runner):
    with task_runner(conf_dir='demos/0_minimal/') as task:
        assert task.job_ret.cfg == {}


def test_demos_minimal__with_overrides(task_runner):
    with task_runner(conf_dir='demos/0_minimal/',
                     overrides=['abc=123', 'a.b=1', 'a.a=2']) as task:
        assert task.job_ret.cfg == dict(abc=123, a=dict(b=1, a=2))
        verify_dir_outputs(task.job_ret.working_dir, task.overrides)


def test_demos_config_file__no_overrides(task_runner):
    with task_runner(conf_dir='demos/3_config_file/',
                     conf_filename='config.yaml') as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            )
        )

        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_config_file__with_overide(task_runner):
    with task_runner(conf_dir='demos/3_config_file/',
                     conf_filename='config.yaml',
                     overrides=['dataset.path=/datasets/imagenet2']) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet2'
            )
        )
        verify_dir_outputs(task.job_ret.working_dir, task.overrides)


def test_demos_config_splitting(task_runner):
    with task_runner(conf_dir='demos/4_config_splitting/conf',
                     conf_filename='config.yaml') as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            ),
            optimizer=dict(
                lr=0.001,
                type='nesterov'
            )
        )
        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_config_groups__override_dataset__wrong(task_runner):
    with pytest.raises(MissingConfigException) as ex:
        with task_runner(conf_dir='demos/5_config_groups/conf', overrides=['optimizer=wrong_name']):
            pass
    assert sorted(ex.value.options) == sorted(['adam', 'nesterov'])


def test_demos_config_groups__override_all_configs(task_runner):
    with task_runner(conf_dir='demos/5_config_groups/conf',
                     overrides=['optimizer=adam', 'optimizer.lr=10']) as task:
        assert task.job_ret.cfg == dict(
            optimizer=dict(
                type='adam',
                lr=10,
                beta=0.01
            ),
        )
        verify_dir_outputs(task.job_ret.working_dir, overrides=task.overrides)


@pytest.mark.parametrize(
    'args,output_conf', [
        ([], OmegaConf.create()), ([
                                       'abc=123', 'hello.a=456', 'hello.b=5671'], OmegaConf.create(
            dict(
                abc=123, hello=dict(
                    a=456, b=5671)))), ])
def test_demo_0_minimal(args, output_conf):
    cmd = [sys.executable, 'demos/0_minimal/minimal.py']
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == output_conf.pretty() + "\n"


def test_demo_1_workdir():
    cmd = [sys.executable, 'demos/1_working_directory/working_directory.py']
    try:
        tempdir = tempfile.mkdtemp()
        cmd.extend(['hydra.run.dir={}'.format(tempdir)])
        result = subprocess.check_output(cmd)
        assert result.decode(
            'utf-8') == "Working directory : {}\n".format(tempdir)
    finally:
        shutil.rmtree(tempdir)


@pytest.mark.parametrize('args,expected', [
    ([], ['Info level message']),
    (['-v' '__main__'], ['Info level message', 'Debug level message']),
])
def test_demo_2_logging(args, expected):
    cmd = [sys.executable, 'demos/2_logging/logging_example.py']
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    lines = result.decode('utf-8').splitlines()
    assert len(lines) == len(expected)
    for i in range(len(lines)):
        assert re.findall(expected[i], lines[i])


@pytest.mark.parametrize('args,output_conf', [
    ([], OmegaConf.create(dict(dataset=dict(name='imagenet', path='/datasets/imagenet')))),
    (['dataset.path=abc'], OmegaConf.create(dict(dataset=dict(name='imagenet', path='abc')))),
])
def test_demo_3_config_file(args, output_conf):
    cmd = [sys.executable, 'demos/3_config_file/config_file.py']
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == output_conf.pretty() + "\n"


@pytest.mark.parametrize('filename, args, expected_name', [
    ('no_config_file_override.py', [], 'no_config_file_override'),
    ('no_config_file_override.py', ['hydra.name=overridden_name'], 'overridden_name'),
    ('with_config_file_override.py', [], 'name_from_config_file'),
    ('with_config_file_override.py', ['hydra.name=overridden_name'], 'overridden_name'),
])
def test_demo_99_task_name(filename, args, expected_name):
    cmd = [
        sys.executable,
        'demos/99_hydra_configuration/task_name/' +
        filename]
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == expected_name + "\n"
