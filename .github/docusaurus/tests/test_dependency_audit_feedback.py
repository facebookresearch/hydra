import hashlib
import json
import subprocess
import sys

import pytest
import yaml
from test_docusaurus_standard import audit_module, fake_npm
from test_docusaurus_standard import npm_project as npm_project
from test_docusaurus_standard import pnpm_project as pnpm_project


@pytest.mark.parametrize("exit_code", [0, 1])
def test_command_logs_include_successful_output_and_warnings(
    npm_project, monkeypatch, capsys, exit_code
):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(
            command, exit_code, "build output", "build warning"
        ),
    )
    audit_module["run"](npm_project, "run", "build")
    output = capsys.readouterr().out
    assert "build output" in output and "build warning" in output


@pytest.mark.parametrize("install,build", [(0, 0), (1, 0), (0, 1)])
def test_validation_output_and_dependency_fingerprints(
    npm_project, monkeypatch, install, build
):
    fake_npm(monkeypatch, install=install, build=build)
    validation = {}
    report = audit_module["prepare"](npm_project, validation=validation)
    assert validation["passed"] == (install == build == 0)
    for name in ("package.json", "package-lock.json"):
        assert hashlib.sha256((npm_project / name).read_bytes()).hexdigest() in report


@pytest.mark.parametrize("build", [0, 1])
def test_cli_exports_validation_status_without_preventing_report_publication(
    npm_project, monkeypatch, build
):
    fake_npm(monkeypatch, build=build)
    monkeypatch.chdir(npm_project.parent)
    report = npm_project / "report.md"
    output = npm_project / "github-output"
    output.write_text("existing=value\n")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dependency_audit.py",
            "--directory",
            npm_project.name,
            "--report",
            str(report),
            "--github-output",
            str(output),
        ],
    )
    audit_module["main"]()
    assert report.exists()
    assert output.read_text() == (
        f"existing=value\nvalidation_passed={'true' if build == 0 else 'false'}\n"
    )


@pytest.mark.parametrize("pnpm", [False, True])
def test_all_locked_version_changes_include_transitives_additions_and_removals(pnpm):
    old = {
        "packages": {
            "node_modules/leaf": {"version": "1.0.0"},
            "node_modules/gone": {"version": "1.0.0"},
        }
    }
    new = {
        "packages": {
            "node_modules/leaf": {"version": "1.1.0"},
            "node_modules/nested/node_modules/leaf": {"version": "1.0.0"},
            "node_modules/new": {"version": "2.0.0"},
        }
    }
    if pnpm:
        old = {
            "packages": {
                "leaf@1.0.0": {"name": "leaf", "version": "1.0.0"},
                "gone@1.0.0": {"name": "gone", "version": "1.0.0"},
            }
        }
        new = {
            "packages": {
                "leaf@1.0.0": {"name": "leaf", "version": "1.0.0"},
                "leaf@1.1.0": {"name": "leaf", "version": "1.1.0"},
                "new@2.0.0": {"name": "new", "version": "2.0.0"},
            }
        }
    assert audit_module["locked_changes"](old, new) == [
        "- gone: `1.0.0` → `not installed`",
        "- leaf: `1.0.0` → `1.0.0, 1.1.0`",
        "- new: `not installed` → `2.0.0`",
    ]


def test_report_includes_non_advisory_transitive_upgrade(pnpm_project, monkeypatch):
    lockfile = pnpm_project / "pnpm-lock.yaml"
    lock = yaml.safe_load(lockfile.read_bytes())
    lock["packages"]["leaf@1.0.0"] = {}
    lockfile.write_text(yaml.safe_dump(lock))

    def invoke(command, **kwargs):
        args = command[5:]
        stdout = ""
        if args[:2] == ["audit", "--json"]:
            stdout = json.dumps(
                {"metadata": {"vulnerabilities": {"total": 0}}, "advisories": {}}
            )
        elif args[0] == "view":
            stdout = '"1.0.0"'
        elif "--lockfile-only" in args:
            candidate = yaml.safe_load(lockfile.read_bytes())
            candidate["packages"].pop("leaf@1.0.0", None)
            candidate["packages"]["leaf@1.0.1"] = {}
            lockfile.write_text(yaml.safe_dump(candidate))
        return subprocess.CompletedProcess(command, 0, stdout, "")

    monkeypatch.setattr(subprocess, "run", invoke)
    report = audit_module["prepare"](pnpm_project)
    assert "- leaf: `1.0.0` → `1.0.1`" in report
