# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import json
import runpy
import subprocess
from pathlib import Path

import pytest
import yaml
from test_docusaurus_standard import npm_project as npm_project

module = runpy.run_path(
    str(Path(__file__).parents[1] / "templates/dependency_audit.py")
)


@pytest.fixture
def project(tmp_path):
    (tmp_path / "package.json").write_text(
        json.dumps(
            {"packageManager": "pnpm@11.21.0", "dependencies": {"parent": "1.0.0"}}
        )
    )
    (tmp_path / "pnpm-workspace.yaml").write_text(
        "packages: ['.']\nminimumReleaseAge: 14400\nblockExoticSubdeps: true\n"
        "minimumReleaseAgeExclude: ['existing@1.0.0']\n"
    )
    lock = {
        "lockfileVersion": "9.0",
        "importers": {".": {}},
        "packages": {"parent@1.0.0": {}, "child@1.0.0": {}},
        "snapshots": {"parent@1.0.0": {"dependencies": {"child": "1.0.0"}}},
    }
    (tmp_path / "pnpm-lock.yaml").write_text(yaml.safe_dump(lock))
    return tmp_path


def upgrade(project):
    lock = yaml.safe_load((project / "pnpm-lock.yaml").read_bytes())
    lock["packages"].pop("child@1.0.0")
    lock["packages"]["child@1.0.1"] = {}
    lock["snapshots"]["parent@1.0.0"]["dependencies"]["child"] = "1.0.1"
    (project / "pnpm-lock.yaml").write_text(yaml.safe_dump(lock))


@pytest.mark.parametrize("fixture_name", ["project", "npm_project"])
def test_restore_removes_package_files_absent_from_snapshot(request, fixture_name):
    project = request.getfixturevalue(fixture_name)
    snapshot = module["valid_snapshot"](project)
    for name in ("package-lock.json", "pnpm-lock.yaml", "pnpm-workspace.yaml"):
        if name not in snapshot[1]:
            (project / name).write_text("{}")
    unrelated = project / "unrelated.txt"
    unrelated.write_text("preserve")

    module["restore_snapshot"](project, snapshot)

    assert module["valid_snapshot"](project) == snapshot
    for name in ("package-lock.json", "pnpm-lock.yaml", "pnpm-workspace.yaml"):
        assert (project / name).exists() == (name in snapshot[1])
    assert unrelated.read_text() == "preserve"


@pytest.mark.parametrize("fixture_name", ["project", "npm_project"])
@pytest.mark.parametrize(
    "filename",
    ["package.json", "package-lock.json", "pnpm-lock.yaml", "pnpm-workspace.yaml"],
)
@pytest.mark.parametrize("kind", ["directory", "symlink", "broken-symlink"])
def test_restore_rejects_unsafe_package_paths_before_writing(
    request, fixture_name, filename, kind
):
    project = request.getfixturevalue(fixture_name)
    snapshot = module["valid_snapshot"](project)
    target = project / filename
    target.unlink(missing_ok=True)
    sentinel = project / "sentinel"
    sentinel.write_text("preserve")
    if kind == "directory":
        target.mkdir()
    else:
        target.symlink_to(sentinel if kind == "symlink" else project / "missing")
    if filename != "package.json":
        (project / "package.json").write_text('{"changed": true}')
    manifest = (
        (project / "package.json").read_bytes() if filename != "package.json" else None
    )

    with pytest.raises(ValueError, match="unsafe package path"):
        module["restore_snapshot"](project, snapshot)

    assert sentinel.read_text() == "preserve"
    if manifest is not None:
        assert (project / "package.json").read_bytes() == manifest
    assert target.is_dir() if kind == "directory" else target.is_symlink()


def test_unused_exceptions_do_not_discard_a_resolved_patch(project):
    snapshot = module["valid_snapshot"](project)
    upgrade(project)
    policy = yaml.safe_load((project / "pnpm-workspace.yaml").read_bytes())
    policy["minimumReleaseAgeExclude"] += ["child@1.0.1", "unpublished@3.0.4"]
    (project / "pnpm-workspace.yaml").write_text(yaml.safe_dump(policy))
    notes = []
    assert not module["restore_invalid_state"](
        project, snapshot, notes, "Security fix", security_fix=True
    )
    assert "child@1.0.1" in module["valid_snapshot"](project)[3]["packages"]
    assert yaml.safe_load((project / "pnpm-workspace.yaml").read_bytes())[
        "minimumReleaseAgeExclude"
    ] == ["existing@1.0.0", "child@1.0.1"]
    assert "unpublished@3.0.4" in notes[0]


def test_used_only_exception_preserves_original_policy_and_lock(project):
    workspace = project / "pnpm-workspace.yaml"
    original = (
        "# Workspace policy rationale.\npackages: ['.']\n"
        "minimumReleaseAge: 14400 # Ten days.\nblockExoticSubdeps: true\n"
        "minimumReleaseAgeExclude: ['existing@1.0.0'] # Keep this comment.\n"
    )
    workspace.write_text(original)
    snapshot = module["valid_snapshot"](project)
    upgrade(project)
    upgraded_lock = (project / "pnpm-lock.yaml").read_bytes()
    policy = yaml.safe_load(workspace.read_bytes())
    policy["minimumReleaseAgeExclude"].append("child@1.0.1")
    workspace.write_text(yaml.safe_dump(policy))
    notes = []

    assert not module["restore_invalid_state"](
        project, snapshot, notes, "Security fix", security_fix=True
    )
    assert workspace.read_bytes() == (
        original.replace(
            "['existing@1.0.0']", "['existing@1.0.0', \"child@1.0.1\"]"
        ).encode()
    )
    repaired = module["valid_snapshot"](project)
    assert repaired is not None
    assert repaired[0] == snapshot[0]
    assert repaired[1]["pnpm-lock.yaml"] == upgraded_lock
    assert repaired[3]["packages"]["child@1.0.1"] == {
        "name": "child",
        "version": "1.0.1",
    }
    assert not notes


def test_invalid_reconstructed_policy_restores_snapshot(project, monkeypatch):
    workspace = project / "pnpm-workspace.yaml"
    original_policy = workspace.read_bytes()
    snapshot = module["valid_snapshot"](project)
    upgrade(project)
    policy = yaml.safe_load(workspace.read_bytes())
    policy["minimumReleaseAgeExclude"].append("child@1.0.1")
    workspace.write_text(yaml.safe_dump(policy))
    original_valid_snapshot = module["valid_snapshot"]
    calls = 0

    def reject_reconstructed_policy(directory):
        nonlocal calls
        calls += 1
        candidate = original_valid_snapshot(directory)
        return None if calls == 2 else candidate

    monkeypatch.setitem(
        module["restore_invalid_state"].__globals__,
        "valid_snapshot",
        reject_reconstructed_policy,
    )
    notes = []

    assert module["restore_invalid_state"](
        project, snapshot, notes, "Security fix", security_fix=True
    )
    assert workspace.read_bytes() == original_policy
    assert (project / "pnpm-lock.yaml").read_bytes() == snapshot[1]["pnpm-lock.yaml"]
    assert "reconstructed an invalid pnpm policy" in notes[0]


def test_shared_exclusion_anchor_restores_the_full_snapshot(project):
    workspace = project / "pnpm-workspace.yaml"
    original_policy = (
        "# Keep policy rationale.\npackages: ['.']\n"
        "minimumReleaseAge: 14400\nblockExoticSubdeps: true\n"
        "minimumReleaseAgeExclude: &pins ['existing@1.0.0']\n"
        "protectedPins: *pins\n"
    )
    workspace.write_text(original_policy)
    snapshot = module["valid_snapshot"](project)
    upgrade(project)
    policy = yaml.safe_load(original_policy)
    policy["minimumReleaseAgeExclude"] = policy["minimumReleaseAgeExclude"] + [
        "child@1.0.1"
    ]
    assert policy["protectedPins"] == ["existing@1.0.0"]
    workspace.write_text(yaml.safe_dump(policy))
    notes = []

    assert module["restore_invalid_state"](
        project, snapshot, notes, "Security fix", security_fix=True
    )
    for name, content in snapshot[1].items():
        assert (project / name).read_bytes() == content
    assert "restored" in notes[0]


def test_absent_exclusions_without_new_exception_accepts_lock_update(project):
    workspace = project / "pnpm-workspace.yaml"
    original_policy = (
        "# Keep policy rationale.\npackages: ['.']\n"
        "minimumReleaseAge: 14400\nblockExoticSubdeps: true\n"
    )
    workspace.write_text(original_policy)
    snapshot = module["valid_snapshot"](project)
    upgrade(project)
    policy = yaml.safe_load(original_policy)
    workspace.write_text(yaml.safe_dump(policy))
    upgraded_lock = (project / "pnpm-lock.yaml").read_bytes()
    notes = []

    assert not module["restore_invalid_state"](
        project, snapshot, notes, "Security fix", security_fix=True
    )
    assert workspace.read_bytes() == original_policy.encode()
    assert (project / "pnpm-lock.yaml").read_bytes() == upgraded_lock
    assert module["valid_snapshot"](project) is not None
    assert not notes


@pytest.mark.parametrize(
    "exclusions, expected",
    [
        (
            "minimumReleaseAgeExclude:\n# Keep the migration exceptions.\n"
            "- 'existing@1.0.0' # Existing rationale.\n",
            "minimumReleaseAgeExclude:\n# Keep the migration exceptions.\n"
            "- 'existing@1.0.0' # Existing rationale.\n- child@1.0.1\n",
        ),
        (
            "minimumReleaseAgeExclude:\n  - 'existing@1.0.0'\n",
            "minimumReleaseAgeExclude:\n  - 'existing@1.0.0'\n  - child@1.0.1\n",
        ),
        (
            "minimumReleaseAgeExclude:\n- 'existing@1.0.0'",
            "minimumReleaseAgeExclude:\n- 'existing@1.0.0'\n- child@1.0.1\n",
        ),
        (
            "minimumReleaseAgeExclude: &exclusions\n- 'existing@1.0.0'\n",
            "minimumReleaseAgeExclude: &exclusions\n- 'existing@1.0.0'\n- child@1.0.1\n",
        ),
        (
            "shared: &exclusions ['existing@1.0.0']\n"
            "minimumReleaseAgeExclude: *exclusions # Keep shared settings unchanged.\n",
            "shared: &exclusions ['existing@1.0.0']\n"
            'minimumReleaseAgeExclude: ["existing@1.0.0", "child@1.0.1"] # Keep shared settings unchanged.\n',
        ),
        (
            "minimumReleaseAgeExclude: ['existing@1.0.0'] # Keep this comment.\n",
            "minimumReleaseAgeExclude: ['existing@1.0.0', \"child@1.0.1\"] # Keep this comment.\n",
        ),
        (
            "minimumReleaseAgeExclude: ['existing@1.0.0',] # Keep this comment.\n",
            "minimumReleaseAgeExclude: ['existing@1.0.0', \"child@1.0.1\"] # Keep this comment.\n",
        ),
        (
            "minimumReleaseAgeExclude: [\n"
            "  'existing@1.0.0', # Existing rationale.\n"
            "] # Keep this comment.\n",
            "minimumReleaseAgeExclude: [\n"
            "  'existing@1.0.0', # Existing rationale.\n"
            ' "child@1.0.1"] # Keep this comment.\n',
        ),
        (
            "minimumReleaseAgeExclude: []\n",
            'minimumReleaseAgeExclude: ["child@1.0.1"]\n',
        ),
        ("", "minimumReleaseAgeExclude:\n- child@1.0.1\n"),
    ],
)
def test_pruning_preserves_original_policy_comments_and_formatting(
    project, exclusions, expected
):
    workspace = project / "pnpm-workspace.yaml"
    prefix = (
        "# Workspace policy rationale.\npackages: ['.']\n"
        "minimumReleaseAge: 14400 # Ten days.\nblockExoticSubdeps: true\n"
    )
    workspace.write_text(prefix + exclusions)
    snapshot = module["valid_snapshot"](project)
    upgrade(project)
    policy = yaml.safe_load(workspace.read_text())
    policy["minimumReleaseAgeExclude"] = policy.get("minimumReleaseAgeExclude", []) + [
        "child@1.0.1",
        "unpublished@3.0.4",
    ]
    # Model pnpm rewriting the proposal before pruning its unused exclusion.
    workspace.write_text(yaml.safe_dump(policy))
    notes = []
    assert not module["restore_invalid_state"](
        project, snapshot, notes, "Security fix", security_fix=True
    )
    assert workspace.read_text() == prefix + expected
    assert "child@1.0.1" in module["valid_snapshot"](project)[3]["packages"]
    assert "unpublished@3.0.4" in notes[0]


@pytest.mark.parametrize("failure", [None, "exit", "invalid"])
def test_fresh_security_resolution_is_isolated_and_restores_failures(
    project, monkeypatch, failure
):
    snapshot = module["valid_snapshot"](project)
    commands = []

    def invoke(command, *, cwd, **kwargs):
        args = command[5:]
        commands.append(args)
        if args[0] == "audit":
            return subprocess.CompletedProcess(command, 1, "5 advisories remain", "")
        assert not (cwd / "pnpm-lock.yaml").exists()
        assert "--ignore-scripts" in args and "--force" not in args
        assert "--config.optimistic-repeat-install=false" in args
        modules = Path(args[args.index("--modules-dir") + 1])
        assert modules != cwd / "node_modules"
        assert Path(args[args.index("--virtual-store-dir") + 1]) == modules / ".pnpm"
        (cwd / "pnpm-lock.yaml").write_bytes(snapshot[1]["pnpm-lock.yaml"])
        if failure == "invalid":
            (cwd / "pnpm-lock.yaml").write_text("[")
        else:
            upgrade(project)
        return subprocess.CompletedProcess(command, int(failure == "exit"), "", "")

    monkeypatch.setattr(subprocess, "run", invoke)
    notes = []
    result = module["fix_security"](project, float("inf"), notes)
    assert result.returncode == (1 if failure else 0)
    assert len(commands) == 2
    if failure:
        assert (project / "pnpm-lock.yaml").read_bytes() == snapshot[1][
            "pnpm-lock.yaml"
        ]
        assert "regeneration failed" in notes[0]
    else:
        assert "child@1.0.1" in module["valid_snapshot"](project)[3]["packages"]
        assert "Regenerated" in notes[0]


def test_weakened_policy_prevents_fresh_resolution(project, monkeypatch):
    commands = []

    def invoke(command, *, cwd, **kwargs):
        commands.append(command)
        policy = yaml.safe_load((cwd / "pnpm-workspace.yaml").read_bytes())
        policy["blockExoticSubdeps"] = False
        (cwd / "pnpm-workspace.yaml").write_text(yaml.safe_dump(policy))
        return subprocess.CompletedProcess(command, 1, "", "")

    monkeypatch.setattr(subprocess, "run", invoke)
    module["fix_security"](project, float("inf"))
    assert len(commands) == 1


@pytest.mark.parametrize(
    "status",
    [
        "unpublished",
        "blocked",
        "compatible",
        "unavailable",
        "malformed",
        "invalid-json",
        "invalid-error",
        "mutated-policy",
        "no-patch",
        "unrelated",
        "missing-constraint",
        "unavailable-intersection",
    ],
)
def test_patch_publication_and_parent_constraints_are_reported(
    project, monkeypatch, status
):
    detail = {
        "patchedRange": None if status == "no-patch" else ">=2.0.0",
        "nodes": ["child@0.9.0" if status == "unrelated" else "child@1.0.0"],
        "title": "Example",
        "severity": "high",
        "url": "https://github.com/advisories/example",
        "range": "<2.0.0",
    }
    data = {
        "package_manager": "pnpm",
        "metadata": {"vulnerabilities": {"high": 1}},
        "vulnerabilities": {"child": {"via": [detail], "fixAvailable": True}},
    }
    commands = []

    def invoke(command, **kwargs):
        args = command[5:]
        commands.append(args)
        value, code = ["2.0.0"], 0
        if args[1] == "child@>=2.0.0":
            if status == "unpublished":
                value, code = {"error": {"code": "ERR_PNPM_PACKAGE_NOT_FOUND"}}, 1
            elif status == "unavailable":
                value, code = {"error": {"code": "ETIMEDOUT"}}, 1
            elif status == "invalid-json":
                return subprocess.CompletedProcess(command, 0, "{", "")
            elif status == "invalid-error":
                value, code = {"error": "invalid metadata"}, 1
            elif status == "mutated-policy":
                policy = yaml.safe_load((project / "pnpm-workspace.yaml").read_bytes())
                policy["blockExoticSubdeps"] = False
                (project / "pnpm-workspace.yaml").write_text(yaml.safe_dump(policy))
        elif args[1] == "parent@1.0.0":
            value = {
                "dependencies": None
                if status == "malformed"
                else {}
                if status == "missing-constraint"
                else {"child": "^1.0.0" if status == "blocked" else ">=1.0.0"}
            }
        elif args[1] == "child@^1.0.0 >=2.0.0":
            value, code = {"error": {"code": "ERR_PNPM_NO_MATCHING_VERSION"}}, 1
        elif args[1] == "child@>=1.0.0 >=2.0.0":
            if status == "unavailable-intersection":
                value, code = {"error": {"code": "ETIMEDOUT"}}, 1
            else:
                value = "2.0.0"
        return subprocess.CompletedProcess(command, code, json.dumps(value), "")

    monkeypatch.setattr(subprocess, "run", invoke)
    snapshot = module["valid_snapshot"](project)
    cache = {}
    notes = []
    for _ in range(2):
        module["describe_pnpm_fixes"](
            project, data, snapshot[1], notes, float("inf"), cache
        )
    expected = {
        "unpublished": "No published stable patch",
        "blocked": "`parent@1.0.0` requires `child ^1.0.0`",
        "compatible": "No checked parent constraint excludes",
        "unavailable": "Could not verify publication",
        "malformed": "Parent compatibility could not be fully verified",
        "invalid-json": "Could not verify publication",
        "invalid-error": "Could not verify publication",
        "mutated-policy": "Could not verify publication",
        "no-patch": "No patched version declared",
        "unrelated": "No checked parent constraint excludes",
        "missing-constraint": "Parent compatibility could not be fully verified",
        "unavailable-intersection": "Parent compatibility could not be fully verified",
    }
    assert isinstance(detail["fixStatus"], str)
    assert expected[status] in detail["fixStatus"]
    assert data["vulnerabilities"]["child"]["fixAvailable"] == (
        status
        not in (
            "unpublished",
            "unavailable",
            "invalid-json",
            "invalid-error",
            "mutated-policy",
            "no-patch",
        )
    )
    assert expected[status] in module["format_remaining_audit"](data, snapshot[3])
    assert (
        len(commands)
        == {
            "unpublished": 1,
            "blocked": 3,
            "compatible": 3,
            "unavailable": 1,
            "malformed": 2,
            "invalid-json": 1,
            "invalid-error": 1,
            "mutated-policy": 1,
            "no-patch": 0,
            "unrelated": 1,
            "missing-constraint": 2,
            "unavailable-intersection": 3,
        }[status]
    )
    assert module["valid_snapshot"](project)[:2] == snapshot[:2]
    if status == "mutated-policy":
        assert len(notes) == 1 and "restored" in notes[0]


@pytest.mark.parametrize("direct_override", [False, True])
def test_parent_can_use_an_older_patch_than_the_latest_registry_match(
    project, monkeypatch, direct_override
):
    if direct_override:
        workspace = project / "pnpm-workspace.yaml"
        policy = yaml.safe_load(workspace.read_bytes())
        policy["overrides"] = {"child": "^2.0.0"}
        workspace.write_text(yaml.safe_dump(policy))
        lockfile = project / "pnpm-lock.yaml"
        lock = yaml.safe_load(lockfile.read_bytes())
        lock["snapshots"] = {}
        lockfile.write_text(yaml.safe_dump(lock))
    detail = {"patchedRange": ">=2.0.0", "nodes": ["child@1.0.0"]}
    data = {"package_manager": "pnpm", "vulnerabilities": {"child": {"via": [detail]}}}
    responses = {
        "child@>=2.0.0": "3.0.0",
        "parent@1.0.0": {"dependencies": {"child": "^1.0.0 || ^2.0.0"}},
        "child@^1.0.0 >=2.0.0": [],
        "child@^2.0.0 >=2.0.0": "2.1.0",
    }

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(
            command, 0, json.dumps(responses[command[6]]), ""
        ),
    )
    module["describe_pnpm_fixes"](
        project, data, module["valid_snapshot"](project)[1], [], float("inf"), {}
    )
    assert "Published patch: `child@2.1.0`" in detail["fixStatus"]
    assert "No checked parent constraint excludes" in detail["fixStatus"]
    assert detail["fixVersion"] == "2.1.0"


@pytest.mark.parametrize("metadata", ["published", "unavailable", "mutated", "blocked"])
def test_security_resolution_uses_verified_published_patch(
    project, monkeypatch, metadata
):
    lockfile = project / "pnpm-lock.yaml"
    lock = yaml.safe_load(lockfile.read_bytes())
    lock["packages"] = {"parent@1.0.0": {}, "child@4.2.0": {}}
    lock["snapshots"]["parent@1.0.0"]["dependencies"]["child"] = "4.2.0"
    lockfile.write_text(yaml.safe_dump(lock))
    before = module["valid_snapshot"](project)
    workspace = project / "pnpm-workspace.yaml"
    commands = []
    response = {
        "metadata": {"vulnerabilities": {"high": 1}},
        "advisories": {
            "example": {
                "module_name": "child",
                "severity": "high",
                "title": "Example",
                "url": "https://github.com/advisories/example",
                "vulnerable_versions": "<=4.2.0",
                "patched_versions": ">=4.2.1",
                "findings": [{"version": "4.2.0"}],
            }
        },
    }

    def invoke(command, *, cwd, **kwargs):
        args = command[5:]
        commands.append(args)
        if args[:2] == ["audit", "--fix=update"]:
            policy = yaml.safe_load(workspace.read_bytes())
            policy["minimumReleaseAgeExclude"].append("child@4.2.1")
            workspace.write_text(yaml.safe_dump(policy))
            return subprocess.CompletedProcess(command, 1, "remaining findings", "")
        if args[:2] == ["audit", "--json"]:
            return subprocess.CompletedProcess(command, 1, json.dumps(response), "")
        if args[0] == "view":
            value, code = ["4.3.0"], 0
            if args[1] == "child@>=4.2.1" and metadata == "unavailable":
                value, code = {"error": {"code": "ETIMEDOUT"}}, 1
            elif args[1] == "child@>=4.2.1" and metadata == "mutated":
                policy = yaml.safe_load(workspace.read_bytes())
                policy["blockExoticSubdeps"] = False
                workspace.write_text(yaml.safe_dump(policy))
            elif args[1] == "parent@1.0.0":
                value = {
                    "dependencies": {
                        "child": "~4.2.0" if metadata == "blocked" else "^4.1.1"
                    }
                }
            elif args[1] == "child@~4.2.0 >=4.2.1":
                value = []
            return subprocess.CompletedProcess(command, code, json.dumps(value), "")
        assert args[0] == "install" and "--ignore-scripts" in args
        exclusions = yaml.safe_load(workspace.read_bytes())["minimumReleaseAgeExclude"]
        assert "child@4.2.1" not in exclusions
        assert ("child@4.3.0" in exclusions) == (metadata == "published")
        version = "4.3.0" if metadata == "published" else "4.2.0"
        proposed = yaml.safe_load(before[1]["pnpm-lock.yaml"])
        proposed["packages"] = {"parent@1.0.0": {}, f"child@{version}": {}}
        proposed["snapshots"]["parent@1.0.0"]["dependencies"]["child"] = version
        lockfile.write_text(yaml.safe_dump(proposed))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", invoke)
    notes = []
    initial_audit = {
        "package_manager": "pnpm",
        "vulnerabilities": {
            "child": {"via": [{"patchedRange": ">=4.2.1", "nodes": ["child@4.2.0"]}]}
        },
    }
    result = module["fix_security"](project, float("inf"), notes, before=initial_audit)
    assert result.returncode == 0
    assert not module["restore_invalid_state"](
        project, before, notes, "Security fix", security_fix=True
    )
    expected = ["existing@1.0.0"] + (["child@4.3.0"] if metadata == "published" else [])
    assert (
        yaml.safe_load(workspace.read_bytes())["minimumReleaseAgeExclude"] == expected
    )
    assert yaml.safe_load(workspace.read_bytes())["blockExoticSubdeps"] is True
    assert commands.index(
        ["audit", "--fix=update", "--audit-level", "info", "--ignore-scripts"]
    ) < next(i for i, args in enumerate(commands) if args[0] == "install")


@pytest.mark.parametrize("constraint", ["1.0.0", "^1.0.0", ">=2.0.0", "unavailable"])
def test_report_identifies_preserved_local_override_blocker(
    project, monkeypatch, constraint
):
    workspace = project / "pnpm-workspace.yaml"
    policy = yaml.safe_load(workspace.read_bytes())
    policy["overrides"] = {"child": constraint}
    workspace.write_text(yaml.safe_dump(policy))
    snapshot = module["valid_snapshot"](project)
    detail = {
        "patchedRange": ">=2.0.0",
        "nodes": ["child@1.0.0"],
        "title": "Example",
        "severity": "high",
        "url": "https://github.com/advisories/example",
        "range": "<2.0.0",
    }
    data = {
        "package_manager": "pnpm",
        "metadata": {"vulnerabilities": {"high": 1}},
        "vulnerabilities": {"child": {"via": [detail], "fixAvailable": True}},
    }

    def invoke(command, **kwargs):
        package = command[6]
        value, code = ["2.0.0"], 0
        if package == "parent@1.0.0":
            value = {"dependencies": {"child": ">=1.0.0"}}
        elif package in ("child@1.0.0 >=2.0.0", "child@^1.0.0 >=2.0.0"):
            value = []
        elif package == "child@unavailable >=2.0.0":
            value, code = {"error": {"code": "ETIMEDOUT"}}, 1
        return subprocess.CompletedProcess(command, code, json.dumps(value), "")

    monkeypatch.setattr(subprocess, "run", invoke)
    module["describe_pnpm_fixes"](project, data, snapshot[1], [], float("inf"), {})
    report = module["format_remaining_audit"](data, snapshot[3])
    assert "child@2.0.0" in report
    if constraint in ("1.0.0", "^1.0.0"):
        assert "Blocked by retained override" in report
        assert "pnpm-workspace.yaml" in report and "overrides.child" in report
        assert f"`{constraint}`" in report
    elif constraint == "unavailable":
        assert "Could not verify" in report and "override" in report
    else:
        assert "Blocked by retained override" not in report
    assert module["valid_snapshot"](project) == snapshot


@pytest.mark.parametrize("shared_patch", [False, True])
def test_patch_candidate_must_satisfy_every_affected_parent(
    project, monkeypatch, shared_patch
):
    detail = {"patchedRange": ">=2.0.0", "nodes": ["child@1.0.0"]}
    data = {"package_manager": "pnpm", "vulnerabilities": {"child": {"via": [detail]}}}
    files = module["valid_snapshot"](project)[1]
    lock = yaml.safe_load(files["pnpm-lock.yaml"])
    lock["snapshots"]["other-parent@1.0.0"] = {"dependencies": {"child": "1.0.0"}}
    files["pnpm-lock.yaml"] = yaml.safe_dump(lock).encode()
    responses = {
        "child@>=2.0.0": ["2.1.0", "3.1.0"],
        "parent@1.0.0": {"dependencies": {"child": "^2.0.0 || ^3.0.0"}},
        "other-parent@1.0.0": {"dependencies": {"child": "^3.0.0"}},
        "child@^2.0.0 >=2.0.0": ["2.1.0"],
        "child@^3.0.0 >=2.0.0": ["3.1.0"],
    }
    if not shared_patch:
        responses["parent@1.0.0"] = {"dependencies": {"child": "^2.0.0"}}
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(
            command, 0, json.dumps(responses[command[6]]), ""
        ),
    )
    module["describe_pnpm_fixes"](project, data, files, [], float("inf"), {})
    assert data["vulnerabilities"]["child"]["fixAvailable"] is True
    if shared_patch:
        assert "Published patch: `child@3.1.0`" in detail["fixStatus"]
        assert "No checked parent constraint excludes" in detail["fixStatus"]
    else:
        assert (
            "no single patch satisfies all checked parent constraints"
            in detail["fixStatus"]
        )
        assert "Published patch:" not in detail["fixStatus"]


@pytest.mark.parametrize(
    "metadata",
    [
        "published",
        "unavailable",
        "still-vulnerable",
        "overlapping-advisory",
        "missing-initial",
        "unrelated-target",
    ],
)
@pytest.mark.parametrize("already_locked", [False, True, "peer"])
def test_security_resolution_retains_verified_already_applied_patch(
    project, monkeypatch, metadata, already_locked
):
    workspace = project / "pnpm-workspace.yaml"
    lockfile = project / "pnpm-lock.yaml"
    if already_locked:
        lock = yaml.safe_load(lockfile.read_bytes())
        parent = (
            "parent@1.0.0(peer@1.0.0)"
            if already_locked == "peer"
            else "other-parent@1.0.0"
        )
        lock["packages"].update({parent: {}, "child@1.0.1": {}})
        lock["snapshots"][parent] = {"dependencies": {"child": "1.0.1"}}
        lockfile.write_text(yaml.safe_dump(lock))
    before = module["valid_snapshot"](project)
    initial_audit = {
        "package_manager": "pnpm",
        "vulnerabilities": {
            "child": {
                "via": [
                    {
                        "patchedRange": (
                            None
                            if metadata == "still-vulnerable"
                            else ">=2.0.0"
                            if metadata == "unrelated-target"
                            else ">=1.0.1"
                        ),
                        "nodes": ["child@1.0.0"],
                    }
                ]
            }
        },
    }
    retained = metadata in ("published", "overlapping-advisory")
    if metadata == "overlapping-advisory":
        initial_audit["vulnerabilities"]["child"]["via"].append(
            {"patchedRange": None, "nodes": ["child@1.0.0"]}
        )

    def invoke(command, **kwargs):
        args = command[5:]
        if args[:2] == ["audit", "--fix=update"]:
            upgrade(project)
            policy = yaml.safe_load(workspace.read_bytes())
            policy["minimumReleaseAgeExclude"].append("child@1.0.1")
            workspace.write_text(yaml.safe_dump(policy))
            return subprocess.CompletedProcess(command, 1, "remaining findings", "")
        if args[:2] == ["audit", "--json"]:
            affected = (
                "child"
                if metadata in ("still-vulnerable", "overlapping-advisory")
                else "other"
            )
            response = {
                "metadata": {"vulnerabilities": {"high": 1}},
                "advisories": {
                    "example": {
                        "module_name": affected,
                        "severity": "high",
                        "title": "Example",
                        "url": "https://github.com/advisories/example",
                        "vulnerable_versions": "<=1.0.1",
                        "patched_versions": "<0.0.0",
                        "findings": [{"version": "1.0.1"}],
                    }
                },
            }
            return subprocess.CompletedProcess(command, 1, json.dumps(response), "")
        if args[0] == "view":
            value, code = "1.0.1", 0
            if args[1] in ("parent@1.0.0", "other-parent@1.0.0"):
                value = {"dependencies": {"child": "^1.0.0"}}
            elif metadata == "unavailable":
                value, code = {"error": {"code": "ETIMEDOUT"}}, 1
            elif metadata == "unrelated-target":
                value = "2.0.0" if args[1] == "child@>=2.0.0" else []
            return subprocess.CompletedProcess(command, code, json.dumps(value), "")
        assert args[0] == "install"
        exclusions = yaml.safe_load(workspace.read_bytes())["minimumReleaseAgeExclude"]
        assert ("child@1.0.1" in exclusions) == retained
        lockfile.write_bytes(before[1]["pnpm-lock.yaml"])
        if retained:
            upgrade(project)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", invoke)
    assert (
        module["fix_security"](
            project,
            float("inf"),
            [],
            before="Initial audit unavailable"
            if metadata == "missing-initial"
            else initial_audit,
        ).returncode
        == 0
    )
    assert not module["restore_invalid_state"](
        project, before, [], "Security fix", security_fix=True
    )
    locked = yaml.safe_load(lockfile.read_bytes())
    version = locked["snapshots"]["parent@1.0.0"]["dependencies"]["child"]
    assert version == ("1.0.1" if retained else "1.0.0")
    assert (
        "child@1.0.1"
        in yaml.safe_load(workspace.read_bytes())["minimumReleaseAgeExclude"]
    ) == retained


def test_repointed_existing_patch_retains_its_used_exception(project):
    lockfile = project / "pnpm-lock.yaml"
    lock = yaml.safe_load(lockfile.read_bytes())
    lock["packages"]["child@1.0.1"] = {}
    lockfile.write_text(yaml.safe_dump(lock))
    before = module["valid_snapshot"](project)
    upgrade(project)
    workspace = project / "pnpm-workspace.yaml"
    policy = yaml.safe_load(workspace.read_bytes())
    policy["minimumReleaseAgeExclude"].append("child@1.0.1")
    workspace.write_text(yaml.safe_dump(policy))
    assert not module["restore_invalid_state"](
        project, before, [], "Security fix", security_fix=True
    )
    assert yaml.safe_load(workspace.read_bytes())["minimumReleaseAgeExclude"] == [
        "existing@1.0.0",
        "child@1.0.1",
    ]


def test_peer_context_change_is_not_a_new_security_target(project):
    before = module["valid_snapshot"](project)
    lockfile = project / "pnpm-lock.yaml"
    lock = yaml.safe_load(lockfile.read_bytes())
    lock["snapshots"]["parent@1.0.0(peer@2.0.0)"] = lock["snapshots"].pop(
        "parent@1.0.0"
    )
    lockfile.write_text(yaml.safe_dump(lock))
    assert (
        module["changed_pnpm_targets"](before[1], module["valid_snapshot"](project)[1])
        == set()
    )


@pytest.mark.parametrize(
    "selector,name",
    [
        ("child@<2", "child"),
        ("parent@1>child", "child"),
        ("parent@>=1>child@<2", "child"),
        ("@scope/parent@1>@scope/child@<2", "@scope/child"),
    ],
)
def test_qualified_override_requires_manual_compatibility_review(
    project, monkeypatch, selector, name
):
    workspace = project / "pnpm-workspace.yaml"
    policy = yaml.safe_load(workspace.read_bytes())
    policy["overrides"] = {selector: "1.0.0"}
    workspace.write_text(yaml.safe_dump(policy))
    snapshot = module["valid_snapshot"](project)
    detail = {"patchedRange": ">=2.0.0", "nodes": [f"{name}@1.0.0"]}
    data = {"package_manager": "pnpm", "vulnerabilities": {name: {"via": [detail]}}}

    def invoke(command, **kwargs):
        value = (
            {"dependencies": {name: ">=1.0.0"}}
            if command[6] == "parent@1.0.0"
            else "2.0.0"
        )
        return subprocess.CompletedProcess(command, 0, json.dumps(value), "")

    monkeypatch.setattr(subprocess, "run", invoke)
    module["describe_pnpm_fixes"](project, data, snapshot[1], [], float("inf"), {})
    assert "fixVersion" not in detail
    assert f"overrides.{selector}` = `1.0.0`" in detail["fixStatus"]
    assert "manual" in detail["fixStatus"]
    assert "No checked parent constraint excludes" not in detail["fixStatus"]
    assert module["valid_snapshot"](project) == snapshot
