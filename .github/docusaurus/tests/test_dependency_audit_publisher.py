# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parents[2] / "workflows/dependency-audit.yml"
if not WORKFLOW_PATH.exists():
    WORKFLOW_PATH = Path(__file__).parents[1] / "templates/dependency-audit.yml"
WORKFLOW = yaml.safe_load(WORKFLOW_PATH.read_text())
PUBLISH = WORKFLOW["jobs"]["pull-request"]["steps"][-1]


@pytest.mark.parametrize("existing", [False, True])
@pytest.mark.parametrize("changes", [False, True])
@pytest.mark.parametrize("passed", [False, True])
@pytest.mark.parametrize("draft", [False, True])
@pytest.mark.parametrize("failure", [None, "view", "draft", "edit"])
def test_publication_preserves_reports_and_signals_failed_validation(
    tmp_path, existing, changes, passed, draft, failure
):
    cli = tmp_path / "mock-cli"
    cli.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "from pathlib import Path\n"
        "tool, args = Path(sys.argv[0]).name, sys.argv[1:]\n"
        "with open(os.environ['COMMAND_LOG'], 'a') as log:\n"
        "    log.write(json.dumps([tool, *args]) + '\\n')\n"
        "if tool == 'git' and args[0] == 'rev-parse':\n"
        "    sys.exit(1)\n"
        "if tool == 'git' and args[0] == 'diff':\n"
        "    sys.exit(int(os.environ['HAS_CHANGES']))\n"
        "if tool == 'gh' and args[:2] == ['pr', 'list']:\n"
        "    print(os.environ['PR_NUMBER'])\n"
        "if tool == 'gh' and args[:2] == ['pr', 'view']:\n"
        "    if os.environ['API_FAILURE'] == 'view': sys.exit(1)\n"
        "    print(os.environ['IS_DRAFT'])\n"
        "if tool == 'gh' and args[:2] == ['pr', 'ready']:\n"
        "    if os.environ['API_FAILURE'] == 'draft': sys.exit(1)\n"
        "if tool == 'gh' and args[:2] == ['pr', 'edit']:\n"
        "    if os.environ['API_FAILURE'] == 'edit': sys.exit(1)\n"
    )
    cli.chmod(0o755)
    for tool in ("git", "gh"):
        (tmp_path / tool).symlink_to(cli)
    project = tmp_path / "website"
    project.mkdir()
    for filename in ("package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml"):
        (project / filename).write_text("{}")
    report = "## Production build\n\nFailed; manual repair required.\n"
    (tmp_path / "dependency-audit-pr.md").write_text(report)
    command_log = tmp_path / "commands.jsonl"
    result = subprocess.run(
        ["bash", "-c", PUBLISH["run"]],
        cwd=tmp_path,
        env={
            **os.environ,
            **PUBLISH["env"],
            "PATH": f"{tmp_path}:{os.environ['PATH']}",
            "NPM_PROJECT": "website",
            "BASE_BRANCH": "main",
            "RUNNER_TEMP": str(tmp_path),
            "COMMAND_LOG": str(command_log),
            "HAS_CHANGES": str(int(changes)),
            "PR_NUMBER": "42" if existing else "",
            "VALIDATION_PASSED": str(passed).lower(),
            "IS_DRAFT": str(draft).lower(),
            "API_FAILURE": failure or "",
        },
        capture_output=True,
        text=True,
    )
    inspect_draft = existing and changes and not passed
    view_failed = inspect_draft and failure == "view"
    convert_draft = inspect_draft and not draft and not view_failed
    draft_failed = convert_draft and failure == "draft"
    blocked = view_failed or draft_failed
    edit_failed = existing and changes and not blocked and failure == "edit"
    assert result.returncode == (1 if not passed or blocked or edit_failed else 0), (
        result.stderr
    )
    commands = [json.loads(line) for line in command_log.read_text().splitlines()]
    commits = [command for command in commands if command[:2] == ["git", "commit"]]
    assert commits == (
        [
            [
                "git",
                "commit",
                "-m",
                "Documentation dependency audit and upgrades",
            ]
        ]
        if changes and not blocked
        else []
    )
    writes = [
        command
        for command in commands
        if command[:2] == ["gh", "pr"] and command[2] in ("create", "edit")
    ]
    assert len(writes) == int(changes and not blocked)
    if writes:
        assert writes[0][2] == ("edit" if existing else "create")
        assert ("--draft" in writes[0]) == (not existing and not passed)
        assert writes[0][writes[0].index("--title") + 1] == (
            "Docusaurus maintenance: security audit and dependency upgrades"
        )
    assert (tmp_path / "dependency-audit-pr.md").read_text().startswith(report)
    draft_commands = [
        command for command in commands if command[:3] == ["gh", "pr", "ready"]
    ]
    assert draft_commands == (
        [["gh", "pr", "ready", "42", "--undo"]] if convert_draft else []
    )
    inspections = [
        command for command in commands if command[:3] == ["gh", "pr", "view"]
    ]
    assert len(inspections) == int(inspect_draft)
    pushes = [command for command in commands if command[:2] == ["git", "push"]]
    assert len(pushes) == int(changes and not blocked)
    if pushes and draft_commands:
        assert commands.index(draft_commands[0]) < commands.index(pushes[0])
