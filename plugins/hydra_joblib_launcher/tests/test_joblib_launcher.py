# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, cast

from hydra.core.plugins import Plugins
from hydra.core.utils import JobReturn
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import (
    TSweepRunner,
    chdir_plugin_root,
    run_python_script,
)
from omegaconf import OmegaConf
from pytest import mark

from hydra_plugins.hydra_joblib_launcher.joblib_launcher import JoblibLauncher

chdir_plugin_root()


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert JoblibLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@mark.parametrize("launcher_name, overrides", [("joblib", [])])
class TestJoblibLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    """

    pass


@mark.parametrize(
    "task_launcher_cfg, extra_flags",
    [
        # joblib with process-based backend (default)
        (
            {},
            [
                "-m",
                "hydra/job_logging=hydra_debug",
                "hydra/job_logging=disabled",
                "hydra/launcher=joblib",
            ],
        )
    ],
)
class TestJoblibLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass


def test_example_app(hydra_sweep_runner: TSweepRunner, tmpdir: Any) -> None:
    with hydra_sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=".",
        config_name="config",
        overrides=["task=1,2,3,4", f"hydra.sweep.dir={tmpdir}"],
    ) as sweep:
        overrides = {("task=1",), ("task=2",), ("task=3",), ("task=4",)}

        assert sweep.returns is not None and len(sweep.returns[0]) == 4
        for ret in sweep.returns[0]:
            assert tuple(ret.overrides) in overrides


def test_example_app_loads_its_config(tmp_path: Path) -> None:
    stdout, _stderr = run_python_script(
        [
            "example/my_app.py",
            "--multirun",
            "task=1,2",
            f'hydra.sweep.dir="{tmp_path}"',
            "hydra.launcher.n_jobs=1",
        ],
    )

    assert "Joblib.Parallel" in stdout
    assert (tmp_path / "0" / "my_app.log").exists()
    assert (tmp_path / "1" / "my_app.log").exists()


def test_inner_max_num_threads_configures_loky_backend(
    hydra_sweep_runner: TSweepRunner, monkeypatch: Any
) -> None:
    from hydra_plugins.hydra_joblib_launcher import _core

    calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
    real_parallel_backend = _core.parallel_backend

    @contextmanager
    def spy_parallel_backend(*args: Any, **kwargs: Any) -> Iterator[None]:
        calls.append((args, kwargs))
        with real_parallel_backend(*args, **kwargs):
            yield

    monkeypatch.setattr(_core, "parallel_backend", spy_parallel_backend)

    with hydra_sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=".",
        config_name="config",
        overrides=[
            "hydra.launcher.n_jobs=1",
            "hydra.launcher.inner_max_num_threads=2",
        ],
    ) as sweep:
        assert sweep.returns is not None and len(sweep.returns[0]) == 1

    assert calls == [(("loky",), {"n_jobs": 1, "inner_max_num_threads": 2})]


def test_inner_max_num_threads_does_not_require_n_jobs(
    monkeypatch: Any, tmp_path: Path
) -> None:
    from hydra_plugins.hydra_joblib_launcher import _core

    backend_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
    parallel_calls: list[dict[str, Any]] = []

    @contextmanager
    def spy_parallel_backend(*args: Any, **kwargs: Any) -> Iterator[None]:
        backend_calls.append((args, kwargs))
        yield

    class FakeParallel:
        def __init__(self, **kwargs: Any) -> None:
            parallel_calls.append(kwargs)

        def __call__(self, calls: Any) -> list[JobReturn]:
            return [JobReturn()]

    monkeypatch.setattr(_core, "parallel_backend", spy_parallel_backend)
    monkeypatch.setattr(_core, "Parallel", FakeParallel)

    launcher = JoblibLauncher(inner_max_num_threads=2)
    launcher.config = OmegaConf.create(
        {
            "hydra": {
                "hydra_logging": None,
                "verbose": False,
                "sweep": {"dir": str(tmp_path)},
            }
        }
    )
    launcher.task_function = cast(Any, lambda cfg: None)
    launcher.hydra_context = cast(Any, object())

    _core.launch(launcher=launcher, job_overrides=[[]], initial_job_idx=0)

    assert backend_calls == [(("loky",), {"inner_max_num_threads": 2})]
    assert parallel_calls == [{}]


@mark.parametrize(
    "overrides",
    [
        "hydra.launcher.batch_size=1",
        "hydra.launcher.max_nbytes=10000",
        "hydra.launcher.max_nbytes=1M",
        "hydra.launcher.pre_dispatch=all",
        "hydra.launcher.pre_dispatch=10",
        "hydra.launcher.pre_dispatch=3*n_jobs",
    ],
)
def test_example_app_launcher_overrides(
    hydra_sweep_runner: TSweepRunner, overrides: str
) -> None:
    with hydra_sweep_runner(
        calling_file="example/my_app.py",
        calling_module=None,
        task_function=None,
        config_path=".",
        config_name="config",
        overrides=[overrides],
    ) as sweep:
        assert sweep.returns is not None and len(sweep.returns[0]) == 1
