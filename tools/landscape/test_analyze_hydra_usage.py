# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from argparse import Namespace
from pathlib import Path

import analyze_hydra_usage as analyzer
from pytest import MonkeyPatch, raises


def entry(path: str, *, size: int = 100) -> dict[str, object]:
    return {"path": path, "sha": f"sha-{path}", "size": size, "type": "blob"}


def args(**overrides: object) -> Namespace:
    values: dict[str, object] = {
        "max_declaration_manifests": 200,
        "max_lock_files": 25,
        "max_markdown_files": 100,
        "max_file_bytes": 1_000_000,
        "workers": 2,
        "no_code_search": False,
    }
    values.update(overrides)
    return Namespace(**values)


class FakeClient:
    def __init__(
        self,
        entries: list[dict[str, object]],
        texts: dict[str, str],
        searches: dict[str, tuple[list[dict[str, object]], int, bool]] | None = None,
    ) -> None:
        self.entries = entries
        self.texts = texts
        self.searches = searches or {}

    def get_tree(self, repo: analyzer.Repository) -> dict[str, object]:
        return {"sha": "tree-sha", "tree": self.entries, "truncated": False}

    def get_blob_text(
        self,
        repo: analyzer.Repository,
        path: str,
        sha: str,
        revision: str,
        max_bytes: int,
    ) -> str:
        assert revision == "tree-sha"
        text = self.texts[path]
        if len(text.encode()) > max_bytes:
            raise analyzer.BlobTooLarge(f"{path} exceeds --max-file-bytes={max_bytes}")
        return text

    def search_code(
        self, repo: analyzer.Repository, query: str
    ) -> tuple[list[dict[str, object]], int, bool]:
        return self.searches[query]


REPO = analyzer.Repository(
    full_name="example/project",
    stars=42,
    default_branch="main",
    fork=False,
    archived=False,
    html_url="https://github.com/example/project",
)


def test_raw_blob_fetch_uses_scanned_revision(monkeypatch: MonkeyPatch) -> None:
    urls = []

    class Response:
        headers = {"Content-Length": "7"}

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self, size: int) -> bytes:
            assert size == 101
            return b"content"

    def fake_urlopen(request: analyzer.Request, timeout: float) -> Response:
        urls.append(request.full_url)
        return Response()

    monkeypatch.setattr(analyzer, "urlopen", fake_urlopen)
    client = analyzer.GitHubClient(token=None, timeout=30, blob_source="raw")

    assert (
        client.get_blob_text(
            REPO, "docs/usage.md", "blob-sha", "tree-sha", max_bytes=100
        )
        == "content"
    )
    assert urls == [
        "https://raw.githubusercontent.com/example/project/tree-sha/docs/usage.md"
    ]


def test_api_blob_fetch_uses_scanned_revision(monkeypatch: MonkeyPatch) -> None:
    requests = []
    client = analyzer.GitHubClient(token=None, timeout=30, blob_source="api")

    class Response:
        headers = {"Content-Length": "7"}

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self, size: int) -> bytes:
            assert size == 101
            return b"content"

    def fake_urlopen(request: analyzer.Request, timeout: float) -> Response:
        requests.append(request)
        return Response()

    monkeypatch.setattr(analyzer, "urlopen", fake_urlopen)
    assert (
        client.get_blob_text(
            REPO,
            "docs/usage guide.md",
            "moving-blob-sha",
            "tree-sha",
            max_bytes=100,
        )
        == "content"
    )
    assert [request.full_url for request in requests] == [
        "https://api.github.com/repos/example/project/contents/"
        "docs/usage%20guide.md?ref=tree-sha"
    ]
    assert requests[0].get_header("Accept") == "application/vnd.github.raw+json"


def test_blob_fetch_stops_at_byte_limit(monkeypatch: MonkeyPatch) -> None:
    class Response:
        headers: dict[str, str] = {}

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self, size: int) -> bytes:
            assert size == 11
            return b"x" * size

    monkeypatch.setattr(analyzer, "urlopen", lambda *args, **kwargs: Response())
    client = analyzer.GitHubClient(token=None, timeout=30, blob_source="raw")

    with raises(analyzer.BlobTooLarge):
        client.get_blob_text(REPO, "README.md", "blob-sha", "tree-sha", max_bytes=10)


def test_pyproject_declarations_do_not_match_unrelated_tool_text() -> None:
    evidence = analyzer.parse_manifest(
        "pyproject.toml",
        """
[project]
dependencies = ["hydra-core>=1.3,<1.5", "other"]

[tool.poetry.dependencies]
hydra-core = "^1.2"

[tool.poetry.group.test.dependencies]
hydra-core = "1.3.2"

[tool.unrelated]
description = "mentions hydra-core but is not a dependency"
""",
    )
    assert [item["specifier"] for item in evidence] == [
        ">=1.3,<1.5",
        "^1.2",
        "==1.3.2",
    ]


def test_pyproject_preserves_structured_poetry_direct_reference() -> None:
    evidence = analyzer.parse_manifest(
        "pyproject.toml",
        """
[tool.poetry.dependencies]
hydra-core = {git = "https://github.com/facebookresearch/hydra.git", tag = "v1.1.0"}
""",
    )
    assert evidence[0]["requirement"] == (
        "hydra-core @ git+https://github.com/facebookresearch/hydra.git@v1.1.0"
    )
    assert evidence[0]["specifier"] is None


def test_pyproject_parses_top_level_dependency_groups() -> None:
    evidence = analyzer.parse_manifest(
        "pyproject.toml",
        """
[dependency-groups]
dev = ["hydra-core>=1.3"]
""",
    )
    assert len(evidence) == 1
    assert evidence[0]["requirement"] == "hydra-core>=1.3"
    assert evidence[0]["specifier"] == ">=1.3"
    assert evidence[0]["source"] == "dependency-groups.dev[0]"


def test_lock_versions_are_normalized() -> None:
    poetry = analyzer.parse_manifest(
        "poetry.lock",
        """
[[package]]
name = "hydra-core"
version = "1.3.2"
""",
    )
    pipfile = analyzer.parse_manifest(
        "Pipfile.lock",
        '{"default": {"hydra-core": {"version": "==1.3.2"}}}',
    )
    assert poetry[0]["resolved_version"] == "1.3.2"
    assert pipfile[0]["resolved_version"] == "1.3.2"


def test_nonstandard_requirement_file_names_are_recognized() -> None:
    assert analyzer.is_manifest("requirements/base.txt")
    assert analyzer.is_manifest("requirements_gpu.yml")
    assert analyzer.is_manifest("CVPR-2024/reqirements.txt")


def test_setup_cfg_optional_extra_is_a_declaration() -> None:
    evidence = analyzer.parse_setup_cfg(
        "setup.cfg",
        """
[options.extras_require]
training =
    hydra-core>=1.3
""",
    )
    assert evidence[0]["specifier"] == ">=1.3"
    assert evidence[0]["source"] == "options.extras_require.training"


def test_requirements_parser_ignores_comments_and_preserves_extras() -> None:
    evidence = analyzer.parse_manifest(
        "requirements.txt",
        """
# hydra-core==1.1
hydra-core[all]==1.3.2
""",
    )
    assert len(evidence) == 1
    assert evidence[0]["requirement"] == "hydra-core[all]==1.3.2"
    assert evidence[0]["specifier"] == "==1.3.2"


def test_requirements_parser_ignores_dependency_in_inline_comment() -> None:
    evidence = analyzer.parse_manifest(
        "requirements.txt",
        "requests>=2  # hydra-core==1.1\n",
    )
    assert evidence == []


def test_requirements_parser_ignores_pip_option_lines() -> None:
    evidence = analyzer.parse_manifest(
        "requirements.txt",
        """
-r requirements/hydra-core.txt
--requirement=requirements/hydra-core.txt
-c constraints/hydra-core.txt
--constraint=constraints/hydra-core.txt
--find-links https://example.com/hydra-core/
""",
    )
    assert evidence == []


def test_requirements_parser_preserves_editable_dependency() -> None:
    evidence = analyzer.parse_manifest(
        "requirements.txt",
        (
            "-e git+https://github.com/facebookresearch/"
            "hydra.git@v1.1.0#egg=hydra-core\n"
        ),
    )
    assert len(evidence) == 1
    assert evidence[0]["requirement"] == (
        "hydra-core @ git+https://github.com/facebookresearch/"
        "hydra.git@v1.1.0#egg=hydra-core"
    )
    assert evidence[0]["specifier"] is None


def test_environment_yaml_parser_preserves_conda_list_items() -> None:
    evidence = analyzer.parse_manifest(
        "environment.yml",
        """
dependencies:
  - python=3.11
  - hydra-core=1.3.2
""",
    )
    assert len(evidence) == 1
    assert evidence[0]["requirement"] == "hydra-core==1.3.2"
    assert evidence[0]["specifier"] == "==1.3.2"


def test_setup_py_parser_ignores_commented_dependency() -> None:
    evidence = analyzer.parse_manifest(
        "setup.py",
        """
# "hydra-core==1.1",
install_requires=["hydra-core[all]>=1.3"],
""",
    )
    assert len(evidence) == 1
    assert evidence[0]["requirement"] == "hydra-core[all]>=1.3"
    assert evidence[0]["specifier"] == ">=1.3"


def test_main_readme_uses_github_location_precedence() -> None:
    entries = [
        entry("docs/README.md"),
        entry("README.md"),
        entry(".github/README.md"),
        entry("subpackage/README.md"),
    ]
    readme = analyzer.select_readme(entries)
    assert readme is not None
    assert readme["path"] == ".github/README.md"

    case_tie = [entry("README.md"), entry("readme.md")]
    readme = analyzer.select_readme(case_tie)
    assert readme is not None
    assert readme["path"] == "README.md"


def test_non_markdown_readme_is_fetched_and_analyzed() -> None:
    entries = [entry("README.rst")]
    client = FakeClient(
        entries,
        {"README.rst": "This project uses Hydra for configuration."},
        searches={"hydra-core": ([], 0, False)},
    )

    result = analyzer.analyze_repository(client, REPO, args())

    assert result["readme_path"] == "README.rst"
    assert result["readme_hydra_status"] == "documented"
    assert result["hydra_documented_in_readme"] is True
    assert result["markdown_files_scanned"] == ["README.rst"]
    assert result["readme_size_skipped"] is False
    assert result["markdown_coverage"] == "complete"


def test_oversized_non_markdown_readme_keeps_coverage_partial() -> None:
    entries = [entry("README.rst", size=2_000)]
    client = FakeClient(
        entries,
        {},
        searches={"hydra-core": ([], 0, False)},
    )

    result = analyzer.analyze_repository(client, REPO, args(max_file_bytes=1_000))

    assert result["readme_path"] == "README.rst"
    assert result["readme_size_skipped"] is True
    assert result["markdown_coverage"] == "partial"


def test_manifest_caps_are_split_and_reported() -> None:
    entries = [
        entry("uv.lock"),
        entry("a/uv.lock"),
        entry("requirements.txt"),
        entry("a/requirements.txt"),
        entry("b/requirements.txt"),
    ]
    selected, inventory = analyzer.select_manifests(entries, 2, 1, 1_000_000)
    assert [item["path"] for item in selected] == [
        "requirements.txt",
        "a/requirements.txt",
        "uv.lock",
    ]
    assert inventory == {
        "declaration_candidates": 3,
        "declaration_files_omitted": 1,
        "declaration_files_size_skipped": 0,
        "lock_candidates": 2,
        "lock_files_omitted": 1,
        "lock_files_size_skipped": 0,
    }


def test_size_skipped_manifests_keep_coverage_partial() -> None:
    entries = [
        entry("pyproject.toml"),
        entry("requirements.txt", size=2_000),
        entry("uv.lock", size=2_000),
        entry("README.md"),
    ]
    client = FakeClient(
        entries,
        {
            "pyproject.toml": '[project]\ndependencies=["hydra-core>=1.3"]',
            "README.md": "Nothing about the configuration framework.",
        },
        searches={"hydra-core": ([], 0, False)},
    )
    result = analyzer.analyze_repository(client, REPO, args(max_file_bytes=1_000))
    assert result["manifest_inventory"] == {
        "declaration_candidates": 2,
        "declaration_files_omitted": 1,
        "declaration_files_size_skipped": 1,
        "lock_candidates": 1,
        "lock_files_omitted": 1,
        "lock_files_size_skipped": 1,
    }
    assert result["declaration_coverage"] == "partial"
    assert result["lock_coverage"] == "partial"
    assert result["manifest_coverage"] == "partial"


def test_size_skipped_markdown_keeps_coverage_partial() -> None:
    entries = [entry("README.md"), entry("docs/usage.mdx", size=2_000)]
    client = FakeClient(
        entries,
        {"README.md": "Nothing about the configuration framework."},
        searches={
            "hydra-core": ([], 0, False),
            "hydra extension:md": ([], 0, False),
            "hydra extension:mdx": ([], 0, False),
        },
    )
    result = analyzer.analyze_repository(client, REPO, args(max_file_bytes=1_000))
    assert result["markdown_files_omitted"] == 1
    assert result["markdown_files_size_skipped"] == 1
    assert result["markdown_coverage"] == "partial"


def test_code_search_fallbacks_respect_file_size_limit() -> None:
    entries = [entry("README.md", size=5)]
    client = FakeClient(
        entries,
        {
            "README.md": "None.",
            "deep/requirements.txt": "hydra-core==1.3.2",
            "docs/usage.md": "This project uses Hydra for configuration.",
        },
        searches={
            "hydra-core": (
                [{"path": "deep/requirements.txt", "sha": "manifest-sha"}],
                1,
                False,
            ),
            "hydra extension:md": (
                [{"path": "docs/usage.md", "sha": "documentation-sha"}],
                1,
                False,
            ),
            "hydra extension:mdx": ([], 0, False),
        },
    )

    result = analyzer.analyze_repository(
        client,
        REPO,
        args(max_markdown_files=0, max_file_bytes=10),
    )

    assert result["direct_dependency_declared"] is False
    assert result["manifest_coverage"] == "partial"
    assert result["markdown_coverage"] == "partial"
    assert [item["path"] for item in result["files_failed"]] == [
        "deep/requirements.txt",
        "docs/usage.md",
    ]


def test_documented_user_evidence_is_preserved_past_output_cap() -> None:
    changelog = "\n".join(f"Hydra config change {index}" for index in range(60))
    result = analyzer.analyze_documentation(
        {
            "CHANGELOG.md": changelog,
            "docs/usage.md": "This project uses Hydra for configuration.",
        },
        None,
    )
    assert result["documentation_hydra_evidence"][0]["path"] == "docs/usage.md"
    assert result["documentation_hydra_evidence"][0]["kind"] == "documented"


def test_documentation_recognizes_current_hydra_repository_url() -> None:
    result = analyzer.analyze_documentation(
        {"README.md": ("See https://github.com/hydra-ecosystem/hydra for details.")},
        None,
    )
    assert result["documentation_hydra_evidence"][0]["kind"] == "documented"


def test_repository_analysis_separates_scopes_and_scans_other_markdown() -> None:
    entries = [
        entry("README.md"),
        entry("docs/usage.md"),
        entry("pyproject.toml"),
        entry("examples/setup.py"),
        entry("vendor/requirements.txt"),
    ]
    client = FakeClient(
        entries,
        {
            "README.md": "No configuration framework is named here.",
            "docs/usage.md": "This project uses Hydra for configuration.",
            "pyproject.toml": '[project]\ndependencies=["hydra-core>=1.3"]',
            "examples/setup.py": 'install_requires=["hydra-core==1.1"]',
            "vendor/requirements.txt": "hydra-core\n",
        },
    )
    result = analyzer.analyze_repository(client, REPO, args())
    assert result["root_dependency_declared"] is True
    assert result["nested_dependency_declared"] is True
    assert result["declaration_scopes"] == [
        "example_or_test",
        "root",
        "vendored",
    ]
    assert result["readme_hydra_status"] == "none"
    assert result["other_markdown_hydra_status"] == "documented"
    assert result["other_markdown_files_with_hydra"] == ["docs/usage.md"]
    assert result["manifest_coverage"] == "complete"
    assert result["markdown_coverage"] == "complete"
    assert result["tree_sha"] == "tree-sha"


def test_code_search_recovers_omitted_manifest() -> None:
    entries = [
        entry("requirements.txt"),
        entry("deep/requirements.txt"),
        entry("README.md"),
    ]
    client = FakeClient(
        entries,
        {
            "requirements.txt": "other-package\n",
            "deep/requirements.txt": "hydra-core==1.3.2\n",
            "README.md": "Nothing about the configuration framework.",
        },
        searches={
            "hydra-core": (
                [
                    {
                        "path": "deep/requirements.txt",
                        "sha": "sha-deep/requirements.txt",
                    }
                ],
                1,
                False,
            )
        },
    )
    result = analyzer.analyze_repository(
        client, REPO, args(max_declaration_manifests=1)
    )
    assert result["declared_specifiers"] == ["==1.3.2"]
    assert result["version_evidence"][0]["discovery"] == "code_search"
    assert result["manifest_coverage"] == "search_completed"
    assert result["analysis_complete"] is True


def test_code_search_recovers_omitted_mdx_documentation() -> None:
    entries = [entry("README.md"), entry("docs/hydra.mdx")]
    client = FakeClient(
        entries,
        {
            "README.md": "No configuration framework is named here.",
            "docs/hydra.mdx": "This project uses Hydra for configuration.",
        },
        searches={
            "hydra-core": ([], 0, False),
            "hydra extension:md": ([], 0, False),
            "hydra extension:mdx": (
                [
                    {
                        "path": "docs/hydra.mdx",
                        "sha": "sha-docs/hydra.mdx",
                    }
                ],
                1,
                False,
            ),
        },
    )
    result = analyzer.analyze_repository(client, REPO, args(max_markdown_files=1))
    assert result["other_markdown_hydra_status"] == "documented"
    assert result["markdown_files_scanned"] == ["README.md", "docs/hydra.mdx"]
    assert result["markdown_search"]["status"] == "complete"


def test_omitted_lock_files_remain_partial_after_code_search() -> None:
    entries = [entry("uv.lock"), entry("nested/uv.lock"), entry("README.md")]
    lock = '[[package]]\nname = "other"\nversion = "1.0"\n'
    client = FakeClient(
        entries,
        {
            "uv.lock": lock,
            "nested/uv.lock": lock,
            "README.md": "Nothing about the configuration framework.",
        },
        searches={"hydra-core": ([], 0, False)},
    )
    result = analyzer.analyze_repository(client, REPO, args(max_lock_files=1))
    assert result["declaration_coverage"] == "complete"
    assert result["lock_coverage"] == "partial"
    assert result["manifest_coverage"] == "partial"
    assert result["analysis_complete"] is False


def test_completed_rows_must_match_current_analysis_version(tmp_path: Path) -> None:
    output = tmp_path / "results.ndjson"
    output.write_text(
        '{"repo":"old/project","status":"ok"}\n'
        f'{{"analysis_version":{analyzer.ANALYSIS_VERSION},'
        '"repo":"new/project","status":"ok"}\n'
    )
    assert analyzer.completed_repositories(output) == {"new/project"}
