# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import json
import subprocess
import threading
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import analyze_hydra_projects as analyzer
import pytest


def row(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "analysis_version": 2,
        "analyzed_at": "2026-07-30T00:00:00+00:00",
        "repo": "example/project",
        "url": "https://github.com/example/project",
        "stars": 42,
        "status": "ok",
        "tree_sha": "a" * 40,
        "fork": False,
        "archived": False,
        "analysis_complete": True,
        "root_dependency_declared": False,
        "readme_hydra_status": "none",
        "documentation_files_with_hydra": [],
        "documentation_hydra_evidence": [],
        "version_evidence": [],
    }
    value.update(overrides)
    return value


def declaration(path: str, scope: str) -> dict[str, str]:
    return {
        "kind": "declaration",
        "path": path,
        "scope": scope,
        "requirement": "hydra-core>=1.3",
    }


def valid_ai_result() -> dict[str, Any]:
    return {
        "repo": "example/project",
        "analyzed_commit": "a" * 40,
        "project_name": "Example",
        "project_url": "https://github.com/example/project",
        "project_subpath": None,
        "category": "application",
        "domains": ["machine_learning"],
        "relationships": ["uses"],
        "reach": "core",
        "origin": "native",
        "maintenance": "active",
        "classification": "confirmed",
        "confidence": "high",
        "summary": "Hydra configures the main application.",
        "evidence": [
            {
                "kind": "code",
                "url": (
                    f"https://github.com/example/project/blob/{'a' * 40}/app.py#L10"
                ),
                "path": "app.py",
                "line": 10,
                "claim": "The main entry point uses @hydra.main.",
            }
        ],
        "disposition": "include",
        "rationale": "Hydra is part of normal application use.",
        "unresolved_questions": [],
    }


CODEX_USAGE_EVENT = json.dumps(
    {
        "type": "turn.completed",
        "usage": {
            "input_tokens": 17068,
            "cached_input_tokens": 1000,
            "cache_write_input_tokens": 200,
            "output_tokens": 50,
            "reasoning_output_tokens": 20,
        },
    }
)


def test_user_documentation_excludes_project_history_and_agent_files() -> None:
    assert analyzer.is_user_documentation_path("README.md")
    assert analyzer.is_user_documentation_path("docs/configuration.md")
    assert analyzer.is_user_documentation_path("website/docs/intro.md")
    assert analyzer.is_user_documentation_path("guides/hydra_usage.md")
    assert not analyzer.is_user_documentation_path("CHANGELOG.md")
    assert not analyzer.is_user_documentation_path("docs/CHANGELOG.md")
    assert not analyzer.is_user_documentation_path("AGENTS.md")
    assert not analyzer.is_user_documentation_path(".github/README.md")


def test_github_metadata_readme_is_not_user_documentation() -> None:
    candidate = row(
        readme_path=".github/README.md",
        readme_hydra_status="documented",
    )
    assert analyzer.user_documentation_paths(candidate) == []


def test_unrelated_hydra_mention_in_user_docs_is_not_documentation() -> None:
    candidate = row(
        documentation_files_with_hydra=["docs/hardware.md"],
        documentation_hydra_evidence=[
            {
                "kind": "mentioned",
                "path": "docs/hardware.md",
                "line": 10,
                "text": "Firmware 1.117.3-hydra",
            }
        ],
    )
    assert analyzer.user_documentation_paths(candidate) == []
    assert analyzer.route_repository(candidate)[0] == "exclude_obvious"


@pytest.mark.parametrize(
    ("candidate", "expected"),
    [
        (
            row(
                root_dependency_declared=True,
                version_evidence=[declaration("requirements.txt", "root")],
                readme_path="README.md",
                readme_hydra_status="documented",
            ),
            "documented",
        ),
        (
            row(
                documentation_files_with_hydra=["docs/tutorial.md"],
                documentation_hydra_evidence=[
                    {
                        "kind": "documented",
                        "path": "docs/tutorial.md",
                        "line": 5,
                        "text": "Use Hydra to run the tutorial.",
                    }
                ],
                version_evidence=[
                    {
                        "kind": "lock",
                        "path": "uv.lock",
                        "scope": "root",
                    }
                ],
            ),
            "documented",
        ),
        (
            row(
                root_dependency_declared=True,
                version_evidence=[declaration("requirements.txt", "root")],
            ),
            "verify_usage",
        ),
        (
            row(
                version_evidence=[
                    declaration("packages/training/requirements.txt", "workspace")
                ]
            ),
            "review_component",
        ),
        (
            row(
                version_evidence=[
                    declaration("vendor/tool/requirements.txt", "vendored")
                ]
            ),
            "review_lineage",
        ),
        (
            row(
                version_evidence=[
                    {
                        "kind": "lock",
                        "path": "examples/uv.lock",
                        "scope": "example_or_test",
                    }
                ]
            ),
            "exclude_obvious",
        ),
        (row(), "exclude_obvious"),
        (row(analysis_complete=False), "insufficient"),
        (row(status="error"), "insufficient"),
    ],
)
def test_mechanical_routes(candidate: dict[str, object], expected: str) -> None:
    route, _ = analyzer.route_repository(candidate)
    assert route == expected


def test_explicit_repository_is_always_a_seed() -> None:
    routing = analyzer.routing_record(row(status="error"), explicit_seed=True)
    assert routing["review_queue"] == "seed"
    assert routing["mechanical_route"] == "insufficient"


def test_latest_crawl_row_wins(tmp_path: Path) -> None:
    source = tmp_path / "crawl.ndjson"
    source.write_text(
        '{"repo":"example/project","status":"error"}\n'
        '{"repo":"example/project","status":"ok","stars":10}\n',
        encoding="utf-8",
    )
    assert analyzer.read_latest_rows(source)["example/project"]["status"] == "ok"


def test_evidence_pack_keeps_only_user_documentation() -> None:
    candidate = row(
        documentation_hydra_evidence=[
            {
                "kind": "documented",
                "path": "CHANGELOG.md",
                "line": 1,
                "text": "Added Hydra",
            },
            {
                "kind": "documented",
                "path": "docs/configuration.md",
                "line": 12,
                "text": "Run with Hydra",
            },
        ]
    )
    routing = analyzer.routing_record(candidate)
    pack = analyzer.build_evidence_pack(candidate, routing)
    assert pack["user_documentation_evidence"] == [
        {
            "kind": "documented",
            "path": "docs/configuration.md",
            "line": 12,
            "text": "Run with Hydra",
        }
    ]


def test_ai_result_requires_commit_pinned_line_evidence() -> None:
    result = valid_ai_result()
    analyzer.validate_ai_result(result, "example/project")
    result["evidence"][0]["url"] = (
        "https://github.com/example/project/blob/main/app.py#L10"
    )
    with pytest.raises(analyzer.AIExecutionError, match="commit-pinned"):
        analyzer.validate_ai_result(result, "example/project")


def test_ai_result_must_match_crawl_revision() -> None:
    result = valid_ai_result()
    with pytest.raises(analyzer.AIExecutionError, match="does not match crawl"):
        analyzer.validate_ai_result(result, "example/project", "b" * 40)

    result["analyzed_commit"] = "b" * 40
    with pytest.raises(analyzer.AIExecutionError, match="URL revision"):
        analyzer.validate_ai_result(result, "example/project", "b" * 40)


def test_non_confirmed_inclusion_is_rejected() -> None:
    result = valid_ai_result()
    result["classification"] = "incidental"
    with pytest.raises(analyzer.AIExecutionError, match="requires confirmed"):
        analyzer.validate_ai_result(result, "example/project")


@pytest.mark.parametrize(
    "domains",
    [
        [],
        ["machine learning"],
        ["machine_learning", "machine_learning"],
        ["unknown", "machine_learning"],
    ],
)
def test_invalid_project_domains_are_rejected(domains: list[str]) -> None:
    result = valid_ai_result()
    result["domains"] = domains
    with pytest.raises(analyzer.AIExecutionError, match="domain"):
        analyzer.validate_ai_result(result, "example/project")


def test_supported_none_classification_is_valid() -> None:
    result = valid_ai_result()
    result.update(
        {
            "classification": "none",
            "relationships": [],
            "reach": "none",
            "origin": "unknown",
            "disposition": "exclude",
        }
    )
    analyzer.validate_ai_result(result, "example/project")


def test_codex_usage_is_extracted_and_formatted() -> None:
    usage = analyzer.extract_codex_usage(
        f'{{"type":"turn.started"}}\nnot json\n{CODEX_USAGE_EVENT}\n'
    )
    assert usage == {
        "input_tokens": 17068,
        "cached_input_tokens": 1000,
        "cache_write_input_tokens": 200,
        "output_tokens": 50,
        "reasoning_output_tokens": 20,
        "total_tokens": 17118,
    }


def test_model_resolution_and_api_cost_estimate(tmp_path: Path) -> None:
    (tmp_path / "config.toml").write_text('model = "gpt-5.6-sol"\n', encoding="utf-8")
    assert analyzer.resolve_codex_model(None, codex_home=tmp_path) == "gpt-5.6-sol"
    usage = analyzer.extract_codex_usage(CODEX_USAGE_EVENT)
    cost = analyzer.api_cost_estimate("gpt-5.6-sol", usage)
    assert cost == 0.08259
    assert analyzer.format_api_cost(cost) == "$0.0826"
    assert analyzer.api_cost_estimate("gpt-5.6-terra", usage) == 0.033036
    assert analyzer.api_cost_estimate("gpt-5.6-luna", usage) == 0.003304
    assert analyzer.api_cost_estimate("unknown-model", usage) is None
    assert analyzer.format_api_cost(None) == "unavailable"


def test_default_model_and_reasoning_effort() -> None:
    args = analyzer.parse_args([])
    assert args.model == "gpt-5.6-terra"
    assert args.reasoning_effort == "medium"


def test_overwrite_preserves_results_and_advances_through_batches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "crawl.ndjson"
    output = tmp_path / "analysis.ndjson"
    routing = tmp_path / "routing.ndjson"
    source.write_text(
        "\n".join(
            json.dumps(
                row(
                    repo=repo,
                    stars=10,
                    tree_sha=f"tree-{index}",
                    root_dependency_declared=True,
                    version_evidence=[declaration("requirements.txt", "root")],
                )
            )
            for index, repo in enumerate(("example/one", "example/two"), 1)
        )
        + "\n",
        encoding="utf-8",
    )
    output.write_text(
        "\n".join(
            json.dumps(
                {
                    "analysis_version": analyzer.ANALYSIS_VERSION,
                    "analyzed_at": analyzed_at,
                    "repo": repo,
                    "source_tree_sha": "old-tree",
                    "status": "ok",
                }
            )
            for repo, analyzed_at in (
                ("example/one", "2026-01-01T00:00:00+00:00"),
                ("example/two", "2026-01-02T00:00:00+00:00"),
                ("example/unselected", "2026-01-03T00:00:00+00:00"),
            )
        )
        + "\n",
        encoding="utf-8",
    )
    analyzed: list[str] = []

    def fake_run_codex(
        candidate: dict[str, Any], *args: object, **kwargs: object
    ) -> tuple[dict[str, Any], dict[str, int], float]:
        analyzed.append(str(candidate["repo"]))
        result = valid_ai_result()
        result["repo"] = candidate["repo"]
        result["project_url"] = candidate["url"]
        return result, {}, 0.1

    monkeypatch.setattr(analyzer, "run_codex", fake_run_codex)
    arguments = [
        "--input",
        str(source),
        "--routing-out",
        str(routing),
        "--out",
        str(output),
        "--min-stars",
        "0",
        "--ai",
        "--overwrite",
        "--batch-size",
        "1",
    ]
    assert analyzer.main(arguments) == 0
    assert analyzer.main(arguments) == 0

    results = analyzer.read_latest_rows(output)
    assert analyzed == ["example/one", "example/two"]
    assert set(results) == {"example/one", "example/two", "example/unselected"}
    assert results["example/one"]["source_tree_sha"] == "tree-1"
    assert results["example/two"]["source_tree_sha"] == "tree-2"
    assert results["example/unselected"]["source_tree_sha"] == "old-tree"


def test_successful_result_persists_usage_cost_and_elapsed_time() -> None:
    candidate = row()
    routing = analyzer.routing_record(candidate, explicit_seed=True)
    usage = analyzer.extract_codex_usage(CODEX_USAGE_EVENT)
    result = analyzer.successful_result(
        candidate,
        routing,
        valid_ai_result(),
        usage,
        12.345,
        "gpt-5.6-terra",
        "medium",
        0.033036,
    )
    assert result["codex_usage"] == usage
    assert result["codex_model"] == "gpt-5.6-terra"
    assert result["codex_reasoning_effort"] == "medium"
    assert result["api_cost_estimate_usd"] == 0.033036
    assert result["api_pricing_source"].endswith("/gpt-5.6-terra")
    assert result["elapsed_seconds"] == 12.345


def test_run_codex_uses_structured_output_and_validates_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        captured["command"] = command
        captured["input"] = kwargs["input"]
        output_index = command.index("--output-last-message") + 1
        Path(command[output_index]).write_text(
            json.dumps(valid_ai_result()), encoding="utf-8"
        )
        return SimpleNamespace(
            returncode=0,
            stdout=CODEX_USAGE_EVENT,
            stderr="",
        )

    monkeypatch.setattr(analyzer.shutil, "which", lambda _: "/usr/bin/codex")
    monkeypatch.setattr(analyzer.subprocess, "run", fake_run)
    candidate = row()
    routing = analyzer.routing_record(candidate, explicit_seed=True)
    result, usage, elapsed_seconds = analyzer.run_codex(
        candidate,
        routing,
        codex_bin="codex",
        model="gpt-5.6-terra",
        reasoning_effort="medium",
        timeout=30,
        progress_interval=30,
    )
    assert result["classification"] == "confirmed"
    assert usage["total_tokens"] == 17118
    assert elapsed_seconds >= 0
    assert "--json" in captured["command"]
    assert "--sandbox" in captured["command"]
    assert "read-only" in captured["command"]
    assert "--output-schema" in captured["command"]
    assert captured["command"][captured["command"].index("--model") + 1] == (
        "gpt-5.6-terra"
    )
    assert 'model_reasoning_effort="medium"' in captured["command"]
    assert "untrusted repository content" in captured["input"]
    assert f"Pinned crawl revision: {'a' * 40}" in captured["input"]


def test_run_codex_reports_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args: object, **kwargs: object) -> None:
        raise subprocess.TimeoutExpired(cmd="codex", timeout=1)

    monkeypatch.setattr(analyzer.shutil, "which", lambda _: "/usr/bin/codex")
    monkeypatch.setattr(analyzer.subprocess, "run", fake_run)
    candidate = row()
    routing = analyzer.routing_record(candidate, explicit_seed=True)
    with pytest.raises(analyzer.AIExecutionError, match="timed out"):
        analyzer.run_codex(
            candidate,
            routing,
            codex_bin="codex",
            model=None,
            reasoning_effort="medium",
            timeout=1,
            progress_interval=30,
        )


def test_run_codex_reports_periodic_progress(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    progress_reported = threading.Event()
    render_project_status = analyzer.render_project_status

    def record_progress(message: str, *, final: bool) -> None:
        render_project_status(message, final=final)
        progress_reported.set()

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        output_index = command.index("--output-last-message") + 1
        assert progress_reported.wait(timeout=1)
        Path(command[output_index]).write_text(
            json.dumps(valid_ai_result()), encoding="utf-8"
        )
        return SimpleNamespace(
            returncode=0,
            stdout=CODEX_USAGE_EVENT,
            stderr="",
        )

    monkeypatch.setattr(analyzer.shutil, "which", lambda _: "/usr/bin/codex")
    monkeypatch.setattr(analyzer.subprocess, "run", fake_run)
    monkeypatch.setattr(analyzer, "render_project_status", record_progress)
    candidate = row()
    routing = analyzer.routing_record(candidate, explicit_seed=True)
    analyzer.run_codex(
        candidate,
        routing,
        codex_bin="codex",
        model=None,
        reasoning_effort="medium",
        timeout=30,
        progress_interval=0.01,
    )
    assert "example/project: Codex still running elapsed=" in capsys.readouterr().err
