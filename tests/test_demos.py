import pytest

from hydra import MissingConfigException
# noinspection PyUnresolvedReferences
from tests.utils import task_runner, sweep_runner


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
        assert task.cfg == {}


def test_demos_minimal__with_overrides(task_runner):
    with task_runner(conf_dir='demos/0_minimal/',
                     overrides=['abc=123', 'a.b=1', 'a.a=2']) as task:
        assert task.cfg == dict(abc=123, a=dict(b=1, a=2))


def test_demos_config_file__no_overrides(task_runner):
    with task_runner(conf_dir='demos/3_config_file/',
                     conf_filename='config.yaml') as task:
        assert task.cfg == dict(
            app=dict(
                name='the nameless one',
            )
        )


def test_demos_config_file__with_overide(task_runner):
    with task_runner(conf_dir='demos/3_config_file/',
                     conf_filename='config.yaml',
                     overrides=['app.name=morte']) as task:
        assert task.cfg == dict(
            app=dict(
                name='morte',
            )
        )


def test_demos_compose__no_override(task_runner):
    with task_runner(conf_dir='demos/4_compose/conf') as task:
        assert task.cfg == {}


def test_demos_compose__override_dataset(task_runner):
    with task_runner(conf_dir='demos/4_compose/conf',
                     overrides=['dataset=imagenet']) as task:
        assert task.cfg == dict(
            dataset=dict(
                name='imagenet',
                path='/datasets/imagenet'
            )
        )


def test_demos_compose__override_dataset__wrong(task_runner):
    with pytest.raises(MissingConfigException) as ex:
        with task_runner(conf_dir='demos/4_compose/conf', overrides=['dataset=wrong_name']):
            pass
    assert sorted(ex.value.options) == sorted(['imagenet', 'cifar10'])


def test_demos_compose__override_all_configs(task_runner):
    with task_runner(conf_dir='demos/2_compose/conf',
                     overrides=['dataset=imagenet', 'model=resnet', 'optimizer=adam']) as task:
        assert task.cfg == dict(
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


def test_demos_compose__override_all_configs(task_runner):
    with task_runner(conf_dir='demos/5_defaults/conf/', conf_filename='config.yaml') as task:
        assert task.cfg == dict(
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


def test_demos_defaults__override_all_configs_and_overrides(task_runner):
    with task_runner(conf_dir='demos/5_defaults/conf/',
                     conf_filename='config.yaml',
                     overrides=["dataset.name=foobar"]) as task:
        assert task.cfg == dict(
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


def test_demos_sweep(sweep_runner):
    sweep = sweep_runner(conf_dir='demos/6_sweep/conf/',
                         conf_filename='config.yaml',
                         overrides=['hydra.launcher.queue=local', 'hydra.no_workers=false'])
    with sweep:
        # TODO: improve testing of sweep.
        # 1. are all sweeps executed (and once)?
        pass
