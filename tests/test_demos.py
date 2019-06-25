# noinspection PyUnresolvedReferences
from tests.utils import task_runner


def test_demos_0_minimal__no_overrides(task_runner):
    with task_runner(conf_dir='demos/0_minimal/') as task:
        assert task.cfg == {}


def test_demos_0_minimal__with_overrides(task_runner):
    with task_runner(conf_dir='demos/0_minimal/',
                     overrides=["abc=123", "a.b=1", "a.a=2"]) as task:
        assert task.cfg == dict(abc=123, a=dict(b=1, a=2))


def test_demos_1_config_file__no_overrides(task_runner):
    with task_runner(conf_dir='demos/1_config_file/',
                     conf_filename='config.yaml') as task:
        assert task.cfg == dict(
            best_app=dict(
                name='with_config_file',
                model="foo",
                dataset='bar'
            )
        )


def test_demos_1_config_file__with_overide(task_runner):
    with task_runner(conf_dir='demos/1_config_file/',
                     conf_filename='config.yaml',
                     overrides=['best_app.name=and_with_overrides!']) as task:
        assert task.cfg == dict(
            best_app=dict(
                name='and_with_overrides!',
                model="foo",
                dataset='bar'
            )
        )
