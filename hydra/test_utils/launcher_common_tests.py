# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Common test functions testing launchers
"""
import copy
from pathlib import Path
from typing import List, Set

import pytest
from omegaconf import DictConfig, OmegaConf

from hydra.test_utils.test_utils import (
    TSweepRunner,
    integration_test,
    verify_dir_outputs,
)


@pytest.mark.usefixtures("restore_singletons")
class LauncherTestSuite:
    def test_sweep_1_job(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str],
    ) -> None:
        sweep_1_job(
            sweep_runner,
            overrides=["hydra/launcher=" + launcher_name, "hydra.sweep.dir=."]
            + overrides,
        )

    def test_sweep_2_jobs(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str]
    ) -> None:
        sweep_2_jobs(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_not_sweeping_hydra_overrides(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str]
    ) -> None:
        not_sweeping_hydra_overrides(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_sweep_1_job_strict(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str]
    ) -> None:
        sweep_1_job(
            sweep_runner,
            strict=True,
            overrides=["hydra/launcher=" + launcher_name] + overrides,
        )

    def test_sweep_1_job_strict_and_bad_key(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str]
    ) -> None:
        # Ideally this would be KeyError, This can't be more specific because some launcher plugins
        # like submitit raises a different exception on job failure and not the underlying exception.
        with pytest.raises(Exception):
            sweep_1_job(
                sweep_runner,
                strict=True,
                overrides=["hydra/launcher=" + launcher_name, "boo=bar"] + overrides,
            )

    def test_sweep_2_optimizers(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str]
    ) -> None:
        sweep_two_config_groups(
            sweep_runner, overrides=["hydra/launcher=" + launcher_name] + overrides
        )

    def test_sweep_over_unspecified_mandatory_default(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str],
    ) -> None:
        base_overrides = ["hydra/launcher=" + launcher_name, "group1=file1,file2"]
        sweep = sweep_runner(
            calling_file=None,
            calling_module="hydra.test_utils.a_module",
            task_function=None,
            config_path="configs",
            config_name="unspecified_mandatory_default",
            overrides=base_overrides + overrides,
            strict=True,
        )
        expected_overrides = [["group1=file1"], ["group1=file2"]]
        expected_conf = [OmegaConf.create({"foo": 10}), OmegaConf.create({"foo": 20})]
        with sweep:
            assert sweep.returns is not None
            assert len(sweep.returns[0]) == 2
            for i in range(2):
                job_ret = sweep.returns[0][i]
                assert job_ret.overrides == expected_overrides[i]
                assert job_ret.cfg == expected_conf[i]
                verify_dir_outputs(job_ret, job_ret.overrides)

    def test_sweep_and_override(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str]
    ) -> None:
        """
        Tests that we can override things in the configs merged in only during the sweep config construction
        db.user=someone does not exist db_conf.yaml, and is only appear when we merge in db=mysql or db=postgresql.
        This presents a tricky situation when operating in strict mode, this tests verifies it's handled correctly.
        """
        base_overrides = [
            "hydra/launcher=" + launcher_name,
            "db=mysql,postgresql",
            "db.user=someone",
        ]
        sweep = sweep_runner(
            calling_file=None,
            calling_module="hydra.test_utils.a_module",
            task_function=None,
            config_path="configs",
            config_name="db_conf.yaml",
            overrides=base_overrides + overrides,
            strict=True,
        )
        expected_overrides = [
            ["db=mysql", "db.user=someone"],
            ["db=postgresql", "db.user=someone"],
        ]
        expected_conf = [
            {"db": {"driver": "mysql", "password": "secret", "user": "someone"}},
            {
                "db": {
                    "user": "someone",
                    "driver": "postgresql",
                    "password": "drowssap",
                    "timeout": 10,
                }
            },
        ]
        with sweep:
            assert sweep.returns is not None
            assert len(sweep.returns[0]) == 2
            for i in range(2):
                job_ret = sweep.returns[0][i]
                assert job_ret.overrides == expected_overrides[i]
                assert job_ret.cfg == expected_conf[i]
                verify_dir_outputs(job_ret, job_ret.overrides)


@pytest.mark.usefixtures("restore_singletons")
class BatchedSweeperTestSuite:
    def test_sweep_2_jobs_2_batches(
        self, sweep_runner: TSweepRunner, launcher_name: str, overrides: List[str],
    ) -> None:
        job_overrides = ["group1=file1,file2", "bar=100,200,300"]
        hydra_overrides = ["hydra/launcher=" + launcher_name]
        overrides.extend(job_overrides)
        overrides.extend(hydra_overrides)
        sweep = sweep_runner(
            calling_file=None,
            calling_module="hydra.test_utils.a_module",
            task_function=None,
            config_path="configs",
            config_name="compose.yaml",
            overrides=overrides,
            strict=True,
        )
        expected_overrides = [
            ["group1=file1", "bar=100"],
            ["group1=file1", "bar=200"],
            ["group1=file1", "bar=300"],
            ["group1=file2", "bar=100"],
            ["group1=file2", "bar=200"],
            ["group1=file2", "bar=300"],
        ]

        expected_conf = [
            {"foo": 10, "bar": 100},
            {"foo": 10, "bar": 200},
            {"foo": 10, "bar": 300},
            {"foo": 20, "bar": 100},
            {"foo": 20, "bar": 200},
            {"foo": 20, "bar": 300},
        ]

        dirs: Set[str] = set()
        with sweep:

            temp_dir = sweep.temp_dir
            assert temp_dir is not None
            multirun_cfg_path = Path(temp_dir) / "multirun.yaml"
            assert multirun_cfg_path.exists()
            multirun_cfg = OmegaConf.load(multirun_cfg_path)
            assert multirun_cfg.hydra.overrides.task == job_overrides

            assert sweep.returns is not None
            # expecting 3 batches of 2
            assert len(sweep.returns) == 3
            for batch in sweep.returns:
                assert len(batch) == 2

            flat = [rt for batch in sweep.returns for rt in batch]
            assert len(flat) == 6  # with a total of 6 jobs
            for idx, job_ret in enumerate(flat):
                assert job_ret.overrides == expected_overrides[idx]
                assert job_ret.cfg == expected_conf[idx]
                dirs.add(job_ret.working_dir)
                verify_dir_outputs(job_ret, job_ret.overrides)
        assert len(dirs) == 6  # and a total of 6 unique output directories


def sweep_1_job(
    sweep_runner: TSweepRunner, overrides: List[str], strict: bool = False
) -> None:
    """
    Runs a sweep with one job
    """
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        task_function=None,
        config_path="configs",
        config_name="compose.yaml",
        overrides=overrides,
        strict=strict,
    )

    with sweep:
        assert sweep.returns is not None
        job_ret = sweep.returns[0]
        assert len(job_ret) == 1
        assert job_ret[0].overrides == []
        assert job_ret[0].cfg == {"foo": 10, "bar": 100}
        assert job_ret[0].hydra_cfg.hydra.job.name == "a_module", (
            "Unexpected job name: " + job_ret[0].hydra_cfg.hydra.job.name
        )
        verify_dir_outputs(sweep.returns[0][0])


def sweep_2_jobs(sweep_runner: TSweepRunner, overrides: List[str]) -> None:
    """
    Runs a sweep with two jobs
    """
    overrides.append("a=0,1")
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        task_function=None,
        config_path="configs/compose.yaml",
        config_name=None,
        overrides=overrides,
    )
    base = OmegaConf.create({"foo": 10, "bar": 100, "a": 0})

    with sweep:
        assert sweep.temp_dir is not None
        assert sweep.returns is not None
        temp_dir = Path(sweep.temp_dir)
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            expected_conf = OmegaConf.merge(
                base, OmegaConf.from_dotlist(job_ret.overrides)
            )
            assert job_ret.overrides == [f"a={i}"]
            assert job_ret.cfg == expected_conf
            assert job_ret.hydra_cfg.hydra.job.name == "a_module", (
                "Unexpected job name: " + job_ret.hydra_cfg.hydra.job.name
            )
            verify_dir_outputs(job_ret, job_ret.overrides)
            path = temp_dir / str(i)
            lst = [x for x in temp_dir.iterdir() if x.is_dir()]
            assert path.exists(), f"'{path}' does not exist, dirs: {lst}"


def not_sweeping_hydra_overrides(
    sweep_runner: TSweepRunner, overrides: List[str]
) -> None:
    """
    Runs a sweep with two jobs
    """
    overrides.extend(["a=0,1", "hydra.verbose=true,false"])
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        task_function=None,
        config_path="configs",
        config_name="compose.yaml",
        overrides=overrides,
        strict=None,
    )
    base = OmegaConf.create({"foo": 10, "bar": 100})

    with sweep:
        assert sweep.returns is not None
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            expected_conf = OmegaConf.merge(
                base, OmegaConf.from_dotlist(job_ret.overrides)
            )
            assert job_ret.overrides == [f"a={i}"]
            assert job_ret.cfg == expected_conf
            verify_dir_outputs(job_ret, job_ret.overrides)


def sweep_two_config_groups(sweep_runner: TSweepRunner, overrides: List[str]) -> None:
    """
    Make sure that optimizers=adam,nesterov is interpreted correctly
    """
    overrides = copy.deepcopy(overrides)
    overrides.extend(["group1=file1,file2"])
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        task_function=None,
        config_path="configs",
        config_name="compose",
        overrides=overrides,
    )
    expected_overrides = [["group1=file1"], ["group1=file2"]]
    expected_conf = [
        OmegaConf.create({"foo": 10, "bar": 100}),
        OmegaConf.create({"foo": 20, "bar": 100}),
    ]
    with sweep:
        assert sweep.returns is not None
        assert len(sweep.returns[0]) == 2
        for i in range(2):
            job_ret = sweep.returns[0][i]
            assert job_ret.overrides == expected_overrides[i]
            assert job_ret.cfg == expected_conf[i]
            verify_dir_outputs(job_ret, job_ret.overrides)


@pytest.mark.usefixtures("restore_singletons")
class IntegrationTestSuite:
    @pytest.mark.parametrize(  # type: ignore
        "task_config, overrides, filename, expected_name",
        [
            pytest.param(None, [], "no_config.py", "no_config", id="no_config"),
            pytest.param(
                None,
                ["hydra.job.name=overridden_name"],
                "no_config.py",
                "overridden_name",
                id="different_filename",
            ),
            pytest.param(
                {"hydra": {"job": {"name": "name_from_config_file"}}},
                [],
                "with_config.py",
                "name_from_config_file",
                id="different_filename_and_config_file_name_override",
            ),
            pytest.param(
                {"hydra": {"job": {"name": "name_from_config_file"}}},
                ["hydra.job.name=overridden_name"],
                "with_config.py",
                "overridden_name",
                id="different_filename_and_config_file_name_override_and_command_line_override",
            ),
        ],
    )
    def test_custom_task_name(
        self,
        tmpdir: Path,
        task_config: DictConfig,
        overrides: List[str],
        filename: str,
        expected_name: str,
        task_launcher_cfg: DictConfig,
        extra_flags: List[str],
    ) -> None:
        overrides = extra_flags + overrides
        task_launcher_cfg = OmegaConf.create(task_launcher_cfg or {})  # type: ignore
        task_config = OmegaConf.create(task_config or {})  # type: ignore
        cfg = OmegaConf.merge(task_launcher_cfg, task_config)
        assert isinstance(cfg, DictConfig)
        integration_test(
            tmpdir=tmpdir,
            task_config=cfg,
            overrides=overrides,
            prints="HydraConfig.get().job.name",
            expected_outputs=expected_name,
            filename=filename,
        )

    @pytest.mark.parametrize(  # type: ignore
        "task_config, overrides, expected_dir",
        [
            pytest.param(
                {
                    "hydra": {
                        "sweep": {
                            "dir": "task_cfg",
                            "subdir": "task_cfg_${hydra.job.num}",
                        }
                    }
                },
                [],
                "task_cfg/task_cfg_0",
                id="sweep_dir_config_override",
            ),
            pytest.param(
                {},
                [
                    "hydra.sweep.dir=cli_dir",
                    "hydra.sweep.subdir=cli_dir_${hydra.job.num}",
                ],
                "cli_dir/cli_dir_0",
                id="sweep_dir_cli_override",
            ),
            pytest.param(
                {
                    "hydra": {
                        "sweep": {
                            "dir": "task_cfg",
                            "subdir": "task_cfg_${hydra.job.num}",
                        }
                    }
                },
                [
                    "hydra.sweep.dir=cli_dir",
                    "hydra.sweep.subdir=cli_dir_${hydra.job.num}",
                ],
                "cli_dir/cli_dir_0",
                id="sweep_dir_cli_overridding_config",
            ),
            pytest.param(
                {
                    "hydra": {
                        "sweep": {
                            "dir": "hydra_cfg",
                            "subdir": "${hydra.job.override_dirname}",
                        }
                    },
                    "a": "hello",
                    "b": 20,
                },
                ["a=1", "b=2"],
                "hydra_cfg/a=1,b=2",
                id="subdir:override_dirname",
            ),
            pytest.param(
                # Test override_dirname integration
                {
                    "hydra": {
                        "sweep": {
                            "dir": "hydra_cfg",
                            "subdir": "${hydra.job.override_dirname}",
                        },
                        "job": {
                            "config": {
                                "override_dirname": {
                                    "kv_sep": "_",
                                    "item_sep": "+",
                                    "exclude_keys": ["seed"],
                                }
                            }
                        },
                    },
                    "a": "hello",
                    "b": 20,
                    "seed": "???",
                },
                ["a=1", "b=2", "seed=10"],
                "hydra_cfg/a_1+b_2",
                id="subdir:custom_override_dirname",
            ),
        ],
    )
    def test_custom_sweeper_run_workdir(
        self,
        tmpdir: Path,
        task_config: str,
        overrides: List[str],
        expected_dir: str,
        task_launcher_cfg: DictConfig,
        extra_flags: List[str],
    ) -> None:
        overrides = extra_flags + overrides
        task_launcher_cfg = OmegaConf.create(task_launcher_cfg or {})  # type: ignore
        task_config = OmegaConf.create(task_config or {})  # type: ignore
        cfg = OmegaConf.merge(task_launcher_cfg, task_config)
        assert isinstance(cfg, DictConfig)
        integration_test(
            tmpdir=tmpdir,
            task_config=cfg,
            overrides=overrides,
            prints="os.getcwd()",
            expected_outputs=str(tmpdir / expected_dir),
        )

    def test_get_orig_dir_multirun(
        self, tmpdir: Path, task_launcher_cfg: DictConfig, extra_flags: List[str]
    ) -> None:
        overrides = extra_flags
        task_launcher_cfg = OmegaConf.create(task_launcher_cfg or {})  # type: ignore
        task_config = OmegaConf.create()
        cfg = OmegaConf.merge(task_launcher_cfg, task_config)
        assert isinstance(cfg, DictConfig)
        integration_test(
            tmpdir=tmpdir,
            task_config=cfg,
            overrides=overrides,
            prints="hydra.utils.get_original_cwd()",
            expected_outputs=str(tmpdir),
        )

    def test_to_absolute_path_multirun(
        self, tmpdir: Path, task_launcher_cfg: DictConfig, extra_flags: List[str],
    ) -> None:
        expected_dir = "cli_dir/cli_dir_0"
        overrides = extra_flags + [
            "hydra.sweep.dir=cli_dir",
            "hydra.sweep.subdir=cli_dir_${hydra.job.num}",
        ]
        task_launcher_cfg = OmegaConf.create(task_launcher_cfg or {})  # type: ignore
        task_config = OmegaConf.create()
        cfg = OmegaConf.merge(task_launcher_cfg, task_config)
        assert isinstance(cfg, DictConfig)
        path = str(Path("/foo/bar").absolute())
        integration_test(
            tmpdir=tmpdir,
            task_config=cfg,
            overrides=overrides,
            prints="hydra.utils.to_absolute_path('/foo/bar')",
            expected_outputs=path,
        )
        outputs = [str(tmpdir / "foo/bar"), str(tmpdir / expected_dir)]
        integration_test(
            tmpdir=tmpdir,
            task_config=cfg,
            overrides=overrides,
            prints=["hydra.utils.to_absolute_path('foo/bar')", "os.getcwd()"],
            expected_outputs=outputs,
        )
