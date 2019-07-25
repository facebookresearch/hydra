import subprocess
import sys
import tempfile
import shutil
import pytest
from omegaconf import OmegaConf
import re
from hydra import MissingConfigException
# noinspection PyUnresolvedReferences
from hydra.test_utils.utils import task_runner, sweep_runner, chdir_hydra_root, verify_dir_outputs

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
            app=dict(
                name='the nameless one',
            )
        )
        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_config_file__with_overide(task_runner):
    with task_runner(conf_dir='demos/3_config_file/',
                     conf_filename='config.yaml',
                     overrides=['app.name=morte']) as task:
        assert task.job_ret.cfg == dict(
            app=dict(
                name='morte',
            )
        )
        verify_dir_outputs(task.job_ret.working_dir, task.overrides)


def test_demos_compose__no_override(task_runner):
    with task_runner(conf_dir='demos/4_compose/conf') as task:
        assert task.job_ret.cfg == {}


def test_demos_compose__override_dataset(task_runner):
    with task_runner(conf_dir='demos/4_compose/conf',
                     overrides=['dataset=imagenet']) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            )
        )
        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_compose__override_dataset__wrong(task_runner):
    with pytest.raises(MissingConfigException) as ex:
        with task_runner(conf_dir='demos/4_compose/conf', overrides=['dataset=wrong_name']):
            pass
    assert sorted(ex.value.options) == sorted(['imagenet', 'cifar10'])


def test_demos_compose__override_all_configs(task_runner):
    with task_runner(conf_dir='demos/2_compose/conf',
                     overrides=['dataset=imagenet', 'model=resnet', 'optimizer=adam']) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            ),
            model=dict(
                type='resnet',
                num_layers=50,
                width=10
            ),
            optimizer=dict(
                type='adam',
                lr=0.1,
                beta=0.01
            ),
        )
        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_compose__override_all_configs(task_runner):
    with task_runner(conf_dir='demos/5_defaults/conf/', conf_filename='config.yaml') as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            ),
            model=dict(
                type='alexnet',
                num_layers=7
            ),
            optimizer=dict(
                type='nesterov',
                lr=0.001,
            ),
        )
        verify_dir_outputs(task.job_ret.working_dir)


def test_demos_defaults__override_all_configs_and_overrides(task_runner):
    with task_runner(conf_dir='demos/5_defaults/conf/',
                     conf_filename='config.yaml',
                     overrides=["dataset.name=foobar"]) as task:
        assert task.job_ret.cfg == dict(
            dataset=dict(
                name='foobar',
                path='/datasets/imagenet'
            ),
            model=dict(
                type='alexnet',
                num_layers=7
            ),
            optimizer=dict(
                type='nesterov',
                lr=0.001,
            ),
        )


@pytest.mark.parametrize('args,output_conf', [
    ([], OmegaConf.create()),
    (['abc=123', 'hello.a=456', 'hello.b=5671'], OmegaConf.create(dict(abc=123, hello=dict(a=456, b=5671)))),
])
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
        assert result.decode('utf-8') == "Working directory : {}\n".format(tempdir)
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
    ([], OmegaConf.create(dict(app=dict(name='the nameless one')))),
    (['app.name=morte'], OmegaConf.create(dict(app=dict(name='morte')))),
])
def test_demo_3_config_file(args, output_conf):
    cmd = [sys.executable, 'demos/3_config_file/config_file.py']
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == output_conf.pretty() + "\n"


@pytest.mark.parametrize('args,output_conf', [
    ([], OmegaConf.create()),
    (['dataset=imagenet'], OmegaConf.create(dict(dataset=dict(name='imagenet', path='/datasets/imagenet')))),
    (['dataset=imagenet', 'optimizer=adam', 'model=resnet'],
     OmegaConf.create(dict(
         dataset=dict(name='imagenet', path='/datasets/imagenet'),
         optimizer=dict(type='adam', lr=0.1, beta=0.01),
         model=dict(num_layers=50, type='resnet', width=10))
     )),
    (['dataset=imagenet', 'optimizer=adam', 'dataset.path=/imagenet2'],
     OmegaConf.create(dict(
         dataset=dict(name='imagenet', path='/imagenet2'),
         optimizer=dict(beta=0.01, lr=0.1, type='adam')
     )))
])
def test_demo_4_compose(args, output_conf):
    cmd = [sys.executable, 'demos/4_compose/compose.py']
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == output_conf.pretty() + "\n"


@pytest.mark.parametrize('args,output_conf', [
    ([], OmegaConf.create(dict(
        dataset=dict(name='imagenet', path='/datasets/imagenet'),
        optimizer=dict(type='nesterov', lr=0.001),
        model=dict(type='alexnet', num_layers=7),
    ))),
    (['dataset=cifar10'], OmegaConf.create(dict(
        dataset=dict(name='cifar10', path='/datasets/cifar10'),
        optimizer=dict(type='nesterov', lr=0.001),
        model=dict(type='alexnet', num_layers=7),
    )))
])
def test_demo_5_defaults(args, output_conf):
    cmd = [sys.executable, 'demos/5_defaults/defaults.py']
    cmd.extend(args)
    result = subprocess.check_output(cmd)
    assert result.decode('utf-8') == output_conf.pretty() + "\n"
