# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import json
from pathlib import Path

import build_public_landscape as landscape
import pytest


def included_decision(**overrides: object) -> dict[str, object]:
    decision: dict[str, object] = {
        "repo": "example/project",
        "decision": "include",
        "group": "good_hydra_usage",
        "feature_candidate": True,
        "decided_at": "2026-08-10",
        "listing": {
            "name": "Example",
            "url": "https://github.com/example/project",
            "description": "An example Hydra application.",
            "kind": "application",
            "type": "Application",
            "tags": ["robotics", "simulation"],
            "relationships": ["integrates"],
        },
    }
    decision.update(overrides)
    return decision


def test_build_project_maps_canonical_decision_fields() -> None:
    assert landscape.build_project(included_decision()) == {
        "repository": "example/project",
        "name": "Example",
        "url": "https://github.com/example/project",
        "description": "An example Hydra application.",
        "kind": "application",
        "type": "Application",
        "tags": ["robotics", "simulation"],
        "relationships": ["integrates"],
        "group": "good_hydra_usage",
        "featureCandidate": True,
        "reviewedAt": "2026-08-10",
    }


def test_build_payload_omits_excluded_decisions() -> None:
    payload = landscape.build_payload(
        [
            {"repo": "example/excluded", "decision": "exclude"},
            included_decision(),
        ]
    )

    assert payload["schemaVersion"] == 2
    assert [project["repository"] for project in payload["projects"]] == [
        "example/project"
    ]


def test_featured_project_requires_good_hydra_usage() -> None:
    with pytest.raises(ValueError, match="must have good Hydra usage"):
        landscape.build_project(included_decision(group="powered_by_hydra"))


def test_excluded_decision_cannot_contain_a_listing() -> None:
    with pytest.raises(ValueError, match="must not contain a listing"):
        landscape.build_payload(
            [
                {
                    "repo": "example/excluded",
                    "decision": "exclude",
                    "listing": {},
                }
            ]
        )


def test_check_mode_rejects_stale_generated_output(tmp_path: Path) -> None:
    decisions = tmp_path / "decisions.json"
    decisions.write_text(json.dumps([included_decision()]) + "\n", encoding="utf-8")
    output = tmp_path / "landscape.json"

    assert landscape.main(["--decisions", str(decisions), "--out", str(output)]) == 0
    assert (
        landscape.main(["--decisions", str(decisions), "--out", str(output), "--check"])
        == 0
    )

    output.write_text("{}\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="is stale"):
        landscape.main(["--decisions", str(decisions), "--out", str(output), "--check"])
