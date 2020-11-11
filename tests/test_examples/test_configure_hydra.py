# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from pathlib import Path
from textwrap import dedent
from typing import Any

from hydra.test_utils.test_utils import (
    assert_text_same,
    chdir_hydra_root,
    get_run_output,
)

chdir_hydra_root()


def test_custom_help(tmpdir: Path) -> None:
    result, _err = get_run_output(
        [
            "examples/configure_hydra/custom_help/my_app.py",
            "hydra.run.dir=" + str(tmpdir),
            "--help",
        ]
    )
    expected = dedent(
        """\
            == AwesomeApp ==

            This is AwesomeApp!
            You can choose a db driver by appending
            == Configuration groups ==
            Compose your configuration from those groups (db=mysql)

            db: mysql, postgresql


            == Config ==
            This is the config generated for this run.
            You can override everything, for example:
            python my_app.py db.user=foo db.pass=bar
            -------
            db:
              driver: mysql
              user: omry
              pass: secret

            -------

            Powered by Hydra (https://hydra.cc)
            Use --hydra-help to view Hydra specific help
"""
    )
    assert_text_same(from_line=expected, to_line=result)


def test_job_name_no_config_override(tmpdir: Path) -> None:
    cmd = [
        "examples/configure_hydra/job_name/no_config_file_override.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert result == "no_config_file_override"


def test_job_name_with_config_override(tmpdir: Path) -> None:
    cmd = [
        "examples/configure_hydra/job_name/with_config_file_override.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert result == "name_from_config_file"


def test_logging(tmpdir: Path) -> None:
    cmd = [
        "examples/configure_hydra/logging/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
    ]
    result, _err = get_run_output(cmd)
    assert result == "[INFO] - Info level message"


def test_disabling_logging(tmpdir: Path) -> None:
    cmd = [
        "examples/configure_hydra/logging/my_app.py",
        "hydra.run.dir=" + str(tmpdir),
        "hydra/job_logging=none",
        "hydra/hydra_logging=none",
    ]
    result, _err = get_run_output(cmd)
    assert result == ""


def test_workdir_config(monkeypatch: Any, tmpdir: Path) -> None:
    script = str(Path("examples/configure_hydra/workdir/my_app.py").absolute())
    monkeypatch.chdir(tmpdir)
    result, _err = get_run_output([script])
    assert Path(result) == Path(tmpdir) / "run_dir"

    result, _err = get_run_output(
        [script, "--multirun", "hydra/hydra_logging=disabled"]
    )
    assert Path(result) == Path(tmpdir) / "sweep_dir" / "0"


def test_workdir_override(monkeypatch: Any, tmpdir: Path) -> None:
    script = str(Path("examples/configure_hydra/workdir/my_app.py").absolute())
    monkeypatch.chdir(tmpdir)
    result, _err = get_run_output([script, "hydra.run.dir=blah"])
    assert Path(result) == Path(tmpdir) / "blah"
