#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

"""Analyze how dependent GitHub repositories use and document Hydra.

The analyzer reads repositories from the enriched github-to-sqlite database,
visits them in descending star order, and appends one JSON object per repository
to an NDJSON file. It distinguishes root dependencies from nested examples,
records partial coverage explicitly, and searches Markdown beyond the main
README. Rerunning the same command skips completed repositories.

Set GITHUB_TOKEN (or GH_TOKEN) to avoid GitHub's unauthenticated API limit.
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import re
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.10
    import tomli as tomllib  # type: ignore[missing-import]

UTC = timezone.utc

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
WORK_ROOT = REPO_ROOT / "temp" / "hydra-dependents"
DEFAULT_DB = WORK_ROOT / "github-to-sqlite-hydra.db"
DEFAULT_OUT = WORK_ROOT / "hydra-usage-analysis-v2.ndjson"
ANALYSIS_VERSION = 2
USER_AGENT = "hydra-landscape-analysis/1.0"
LOCK_FILES = {"pipfile.lock", "poetry.lock", "pdm.lock", "uv.lock"}
EXACT_MANIFESTS = {
    "environment.yml",
    "environment.yaml",
    "pipfile",
    "pipfile.lock",
    "poetry.lock",
    "pdm.lock",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
    "uv.lock",
}
MARKDOWN_SUFFIXES = {".md", ".mdx"}
README_RE = re.compile(r"^readme(?:\.[^/]+)?$", re.IGNORECASE)
NON_USER_DOCUMENT_NAMES = {
    "agents.md",
    "claude.md",
    "code_of_conduct.md",
    "contributing.md",
    "history.md",
    "license.md",
    "news.md",
    "release.md",
    "releases.md",
    "security.md",
}
NON_USER_DOCUMENT_PARTS = {
    ".github",
    "changelog",
    "changelogs",
    "changes",
    "news",
    "release",
    "releases",
    "vendor",
    "vendored",
    "third_party",
    "third-party",
}
HYDRA_NAME_RE = re.compile(r"(?<![\w.-])hydra[-_.]core(?![\w.-])", re.IGNORECASE)
HYDRA_MENTION_RE = re.compile(r"\bhydra\b", re.IGNORECASE)
STRONG_DOCUMENTATION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"hydra[-_.]core",
        r"hydra\.cc",
        r"github\.com/facebookresearch/hydra",
        r"@hydra\.main",
        r"\b(?:from|import)\s+hydra\b",
        r"\bhydra\.(?:compose|initialize|initialize_config_dir|initialize_config_module)\b",
        r"\bhydra\s+(?:configuration|config|framework)\b",
        r"\bhydra\b.{0,50}\b(?:config\w*|framework|multirun|sweep\w*)\b",
        r"\b(?:config\w*|framework|multirun|sweep\w*)\b.{0,50}\bhydra\b",
    )
]
REQUIREMENT_SUFFIX_RE = re.compile(
    r"""
    ^\s*
    (?P<specifier>
        (?:
            (?:===|==|~=|!=|<=|>=|<|>|\^|~)\s*[^,;\s'"\]}]+
            (?:\s*,\s*(?:===|==|~=|!=|<=|>=|<|>)\s*[^,;\s'"\]}]+)*
        )
        | \*
    )?
    """,
    re.VERBOSE,
)


class RepositoryUnavailable(Exception):
    """The repository or its default branch cannot be read."""


class BlobUnavailable(Exception):
    """A file disappeared or became unreadable after listing the tree."""


class BlobTooLarge(BlobUnavailable):
    """A file exceeds the configured read limit."""


class SearchUnavailable(Exception):
    """GitHub code search could not be used for this repository."""


@dataclass(frozen=True)
class Repository:
    full_name: str
    stars: int | None
    default_branch: str
    fork: bool
    archived: bool
    html_url: str


class GitHubReader(Protocol):
    def get_tree(self, repo: Repository) -> dict[str, Any]:
        raise NotImplementedError

    def get_blob_text(
        self,
        repo: Repository,
        path: str,
        sha: str,
        revision: str,
        max_bytes: int,
    ) -> str:
        raise NotImplementedError

    def search_code(
        self, repo: Repository, query: str
    ) -> tuple[list[dict[str, Any]], int, bool]:
        raise NotImplementedError


class GitHubClient:
    def __init__(self, token: str | None, timeout: float, blob_source: str) -> None:
        self.token = token
        self.timeout = timeout
        self.blob_source = blob_source
        self.requests = 0
        self.raw_requests = 0

    def get_json(self, path: str) -> dict[str, Any]:
        url = f"https://api.github.com{path}"
        delay = 2.0
        for attempt in range(6):
            headers = {
                "Accept": "application/vnd.github+json",
                "User-Agent": USER_AGENT,
                "X-GitHub-Api-Version": "2022-11-28",
            }
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            request = Request(url, headers=headers)
            try:
                self.requests += 1
                with urlopen(request, timeout=self.timeout) as response:
                    return json.load(response)
            except HTTPError as error:
                remaining = error.headers.get("X-RateLimit-Remaining")
                if error.code == 404:
                    raise RepositoryUnavailable(
                        f"GitHub returned 404 for {path}"
                    ) from error
                retry_after = error.headers.get("Retry-After")
                if error.code == 403 and (remaining == "0" or retry_after is not None):
                    if retry_after is not None:
                        wait = float(retry_after)
                    else:
                        reset = int(error.headers.get("X-RateLimit-Reset", "0"))
                        wait = max(reset - int(time.time()) + 1, 1)
                    print(
                        f"GitHub rate limit reached; waiting {wait:g}s",
                        file=sys.stderr,
                    )
                    time.sleep(wait)
                    continue
                if error.code != 429 and error.code < 500:
                    raise
                if attempt == 5:
                    raise
                wait = float(retry_after) if retry_after else delay
                print(
                    f"GitHub returned HTTP {error.code}; retrying in {wait:g}s",
                    file=sys.stderr,
                )
                time.sleep(wait)
                delay = min(delay * 2, 60)
            except URLError:
                if attempt == 5:
                    raise
                time.sleep(delay)
                delay = min(delay * 2, 60)
        raise AssertionError("retry loop exhausted")

    def get_tree(self, repo: Repository) -> dict[str, Any]:
        branch = quote(repo.default_branch, safe="")
        return self.get_json(f"/repos/{repo.full_name}/git/trees/{branch}?recursive=1")

    def get_bounded_text(
        self, request: Request, path: str, max_bytes: int, *, api: bool
    ) -> str:
        delay = 2.0
        for attempt in range(6):
            try:
                if api:
                    self.requests += 1
                else:
                    self.raw_requests += 1
                with urlopen(request, timeout=self.timeout) as response:
                    content_length = response.headers.get("Content-Length")
                    if content_length is not None and int(content_length) > max_bytes:
                        raise BlobTooLarge(
                            f"{path} exceeds --max-file-bytes={max_bytes}"
                        )
                    raw = response.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raise BlobTooLarge(f"{path} exceeds --max-file-bytes={max_bytes}")
                return raw.decode("utf-8", errors="replace")
            except HTTPError as error:
                if error.code == 404:
                    raise BlobUnavailable(f"GitHub returned 404 for {path}") from error
                remaining = error.headers.get("X-RateLimit-Remaining")
                retry_after = error.headers.get("Retry-After")
                if (
                    api
                    and error.code == 403
                    and (remaining == "0" or retry_after is not None)
                ):
                    if retry_after is not None:
                        wait = float(retry_after)
                    else:
                        reset = int(error.headers.get("X-RateLimit-Reset", "0"))
                        wait = max(reset - int(time.time()) + 1, 1)
                    print(
                        f"GitHub rate limit reached; waiting {wait:g}s",
                        file=sys.stderr,
                    )
                    time.sleep(wait)
                    continue
                if error.code != 429 and error.code < 500:
                    raise
                if attempt == 5:
                    raise
                wait = float(retry_after) if retry_after else delay
                time.sleep(wait)
                delay = min(delay * 2, 60)
            except URLError:
                if attempt == 5:
                    raise
                time.sleep(delay)
                delay = min(delay * 2, 60)
        raise AssertionError("retry loop exhausted")

    def get_raw_text(
        self, repo: Repository, path: str, revision: str, max_bytes: int
    ) -> str:
        encoded_revision = quote(revision, safe="")
        encoded_path = quote(path, safe="/")
        url = (
            f"https://raw.githubusercontent.com/{repo.full_name}/"
            f"{encoded_revision}/{encoded_path}"
        )
        request = Request(url, headers={"User-Agent": USER_AGENT})
        return self.get_bounded_text(request, path, max_bytes, api=False)

    def get_blob_text(
        self,
        repo: Repository,
        path: str,
        sha: str,
        revision: str,
        max_bytes: int,
    ) -> str:
        if self.blob_source == "raw":
            return self.get_raw_text(repo, path, revision, max_bytes)
        encoded_path = quote(path, safe="/")
        encoded_revision = quote(revision, safe="")
        url = (
            f"https://api.github.com/repos/{repo.full_name}/contents/{encoded_path}"
            f"?ref={encoded_revision}"
        )
        headers = {
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return self.get_bounded_text(
            Request(url, headers=headers), path, max_bytes, api=True
        )

    def search_code(
        self, repo: Repository, query: str
    ) -> tuple[list[dict[str, Any]], int, bool]:
        if not self.token:
            raise SearchUnavailable("GITHUB_TOKEN/GH_TOKEN is required")
        parameters = urlencode({"q": f"{query} repo:{repo.full_name}", "per_page": 100})
        try:
            data = self.get_json(f"/search/code?{parameters}")
        except (HTTPError, RepositoryUnavailable) as error:
            raise SearchUnavailable(str(error)) from error
        items = data.get("items", [])
        if not isinstance(items, list):
            raise SearchUnavailable("GitHub code search returned no item list")
        return (
            items,
            int(data.get("total_count", len(items))),
            bool(data.get("incomplete_results")),
        )


def edit_distance_at_most(left: str, right: str, limit: int) -> bool:
    if abs(len(left) - len(right)) > limit:
        return False
    previous = list(range(len(right) + 1))
    for row, left_character in enumerate(left, 1):
        current = [row]
        for column, right_character in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (left_character != right_character),
                )
            )
        if min(current) > limit:
            return False
        previous = current
    return previous[-1] <= limit


def resembles_requirements_file(name: str) -> bool:
    suffix = PurePosixPath(name).suffix
    if suffix not in {"", ".in", ".txt", ".yaml", ".yml"}:
        return False
    prefix = re.split(r"[-_.]", name, maxsplit=1)[0]
    return edit_distance_at_most(prefix, "requirements", 2)


def is_manifest(path: str) -> bool:
    pure = PurePosixPath(path)
    name = pure.name.lower()
    parent_names = {part.lower() for part in pure.parts[:-1]}
    dependency_directory_file = bool(
        parent_names & {"dependency", "dependencies", "deps", "requirements"}
    ) and pure.suffix.lower() in {".in", ".txt", ".yaml", ".yml"}
    return (
        name in EXACT_MANIFESTS
        or resembles_requirements_file(name)
        or dependency_directory_file
        or (
            name.startswith("environment")
            and PurePosixPath(name).suffix in {".yaml", ".yml"}
        )
    )


def is_markdown(path: str) -> bool:
    return PurePosixPath(path).suffix.lower() in MARKDOWN_SUFFIXES


def path_scope(path: str) -> str:
    parts = tuple(part.lower() for part in PurePosixPath(path).parts)
    if len(parts) == 1:
        return "root"
    if any(
        part in {"ext", "external", "third_party", "third-party", "vendor", "vendored"}
        for part in parts[:-1]
    ):
        return "vendored"
    if any(part in {"doc", "docs", "documentation"} for part in parts[:-1]):
        return "docs"
    if any(
        part
        in {
            "demo",
            "demos",
            "example",
            "examples",
            "test",
            "tests",
            "tutorial",
            "tutorials",
        }
        for part in parts[:-1]
    ):
        return "example_or_test"
    return "workspace"


def path_priority(path: str) -> tuple[int, int, int, str]:
    pure = PurePosixPath(path)
    scope_rank = {
        "root": 0,
        "workspace": 1,
        "docs": 2,
        "example_or_test": 3,
        "vendored": 4,
    }[path_scope(path)]
    return (scope_rank, len(pure.parts), len(path), path.lower())


def is_user_documentation_path(path: str) -> bool:
    pure = PurePosixPath(path)
    parts = tuple(part.lower() for part in pure.parts)
    name = pure.name.lower()
    stem = pure.stem.lower()
    if name in NON_USER_DOCUMENT_NAMES:
        return False
    if any(part in NON_USER_DOCUMENT_PARTS for part in parts[:-1]):
        return False
    if "changelog" in stem or stem.startswith("release"):
        return False
    if name.startswith("readme"):
        return True
    if any(part in {"doc", "docs", "documentation"} for part in parts[:-1]):
        return True
    return any(
        marker in stem
        for marker in (
            "config",
            "getting_started",
            "getting-started",
            "guide",
            "tutorial",
            "usage",
        )
    )


def select_readme(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = []
    for entry in entries:
        path = PurePosixPath(entry.get("path", ""))
        if entry.get("type") != "blob" or not README_RE.match(path.name):
            continue
        parts = tuple(part.lower() for part in path.parts)
        if len(parts) == 1:
            rank = 1
        elif len(parts) == 2 and parts[0] == ".github":
            rank = 0
        elif len(parts) == 2 and parts[0] in {"doc", "docs"}:
            rank = 2
        else:
            continue
        candidates.append((rank, len(entry["path"]), entry["path"].lower(), entry))
    winner = min(candidates, key=lambda candidate: candidate[:3], default=None)
    return winner[3] if winner is not None else None


def select_manifests(
    entries: list[dict[str, Any]],
    max_declarations: int,
    max_locks: int,
    max_file_bytes: int,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    candidates = [
        entry
        for entry in entries
        if entry.get("type") == "blob" and is_manifest(entry.get("path", ""))
    ]
    candidates.sort(key=lambda item: path_priority(item["path"]))
    declarations = [
        entry
        for entry in candidates
        if PurePosixPath(entry["path"]).name.lower() not in LOCK_FILES
    ]
    locks = [
        entry
        for entry in candidates
        if PurePosixPath(entry["path"]).name.lower() in LOCK_FILES
    ]
    eligible_declarations = [
        entry for entry in declarations if int(entry.get("size", 0)) <= max_file_bytes
    ]
    eligible_locks = [
        entry for entry in locks if int(entry.get("size", 0)) <= max_file_bytes
    ]
    selected_declarations = eligible_declarations[:max_declarations]
    selected_locks = eligible_locks[:max_locks]
    selected = selected_declarations + selected_locks
    return selected, {
        "declaration_candidates": len(declarations),
        "declaration_files_omitted": len(declarations) - len(selected_declarations),
        "declaration_files_size_skipped": len(declarations)
        - len(eligible_declarations),
        "lock_candidates": len(locks),
        "lock_files_omitted": len(locks) - len(selected_locks),
        "lock_files_size_skipped": len(locks) - len(eligible_locks),
    }


def select_markdown(
    entries: list[dict[str, Any]],
    readme: dict[str, Any] | None,
    max_files: int,
    max_file_bytes: int,
) -> tuple[list[dict[str, Any]], int, int]:
    candidates = [
        entry
        for entry in entries
        if entry.get("type") == "blob" and is_markdown(entry.get("path", ""))
    ]
    eligible = [
        entry for entry in candidates if int(entry.get("size", 0)) <= max_file_bytes
    ]
    readme_path = readme["path"] if readme is not None else None
    eligible.sort(
        key=lambda item: (
            item["path"] != readme_path,
            *path_priority(item["path"]),
        )
    )
    selected = eligible[:max_files]
    return selected, len(candidates) - len(selected), len(candidates) - len(eligible)


def clean_requirement(value: str) -> str:
    value = value.strip().strip(",")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()


def requirement_for_version(value: str) -> str:
    value = value.strip()
    if value == "*":
        return "hydra-core"
    if re.match(r"^\d", value):
        value = f"=={value}"
    return f"hydra-core{value}"


def requirement_for_dependency_table(value: dict[str, Any]) -> str:
    version = value.get("version")
    if isinstance(version, str):
        return requirement_for_version(version)
    for key in ("git", "url", "path"):
        reference = value.get(key)
        if not isinstance(reference, str):
            continue
        if key == "git" and not reference.startswith("git+"):
            reference = f"git+{reference}"
        if key == "git":
            revision = next(
                (
                    value.get(revision_key)
                    for revision_key in ("rev", "tag", "branch")
                    if isinstance(value.get(revision_key), str)
                ),
                None,
            )
            if revision is not None:
                reference = f"{reference}@{revision}"
        return f"hydra-core @ {reference}"
    return "hydra-core"


def normalize_locked_version(value: str) -> str:
    return re.sub(r"^==\s*", "", value.strip())


def specifier_from_requirement(requirement: str) -> str | None:
    match = HYDRA_NAME_RE.search(requirement)
    if not match:
        return None
    suffix = requirement[match.end() :]
    suffix = re.sub(r"^\s*\[[^\]]+\]", "", suffix)
    match = REQUIREMENT_SUFFIX_RE.match(suffix)
    if not match:
        return None
    specifier = match.group("specifier")
    return re.sub(r"\s+", "", specifier) if specifier else None


def requirement_from_line(line: str) -> str | None:
    if line.lstrip().startswith("#"):
        return None
    active_line = re.split(r"\s+#", line, maxsplit=1)[0]
    stripped = active_line.lstrip()
    if re.match(r"^-\s+", stripped):
        active_line = stripped[1:].lstrip()
        stripped = active_line
    editable = re.match(r"^(?:-e|--editable)(?:\s+|=)(.+)$", stripped)
    editable_reference = None
    if editable is not None:
        editable_reference = editable.group(1).strip()
        active_line = editable_reference
    elif stripped.startswith("-"):
        return None
    match = HYDRA_NAME_RE.search(active_line)
    if not match:
        return None
    package = "hydra-core"
    if editable_reference is not None:
        return f"{package} @ {editable_reference}"
    suffix = active_line[match.end() :].strip()
    if suffix.startswith("=") and not suffix.startswith(("==", "=>")):
        value = suffix[1:].strip().rstrip(",")
        if value.startswith("{"):
            version_match = re.search(
                r"""version\s*=\s*['"]([^'"]+)['"]""", value, re.IGNORECASE
            )
            return f"{package}{version_match.group(1)}" if version_match else package
        value = clean_requirement(value)
        if re.fullmatch(r"\d+(?:\.\d+)*(?:[A-Za-z0-9_.+-]*)", value):
            value = f"=={value}"
        return f"{package}{value}" if value != "*" else package
    suffix = re.split(r"""[;'"\}]""", suffix, maxsplit=1)[0].strip()
    if suffix.startswith("=") and not suffix.startswith("=="):
        suffix = f"={suffix}"
    return f"{package}{suffix}"


def add_evidence(
    evidence: list[dict[str, Any]],
    *,
    path: str,
    kind: str,
    requirement: str | None = None,
    resolved_version: str | None = None,
    source: str,
) -> None:
    item: dict[str, Any] = {
        "path": path,
        "scope": path_scope(path),
        "kind": kind,
        "source": source,
    }
    if requirement is not None:
        requirement = clean_requirement(requirement)
        item["requirement"] = requirement
        item["specifier"] = specifier_from_requirement(requirement)
    if resolved_version is not None:
        item["resolved_version"] = str(resolved_version).strip()
    if item not in evidence:
        evidence.append(item)


def walk_dependency_tables(
    value: Any, path: str, evidence: list[dict[str, Any]], file_path: str
) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if str(key).lower().replace("_", "-") == "hydra-core":
                if isinstance(child, str):
                    requirement = requirement_for_version(child)
                elif isinstance(child, dict):
                    requirement = requirement_for_dependency_table(child)
                else:
                    requirement = "hydra-core"
                add_evidence(
                    evidence,
                    path=file_path,
                    kind="declaration",
                    requirement=requirement,
                    source=child_path,
                )
            walk_dependency_tables(child, child_path, evidence, file_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            if isinstance(child, str) and HYDRA_NAME_RE.search(child):
                add_evidence(
                    evidence,
                    path=file_path,
                    kind="declaration",
                    requirement=child,
                    source=child_path,
                )
            else:
                walk_dependency_tables(child, child_path, evidence, file_path)


def find_dependency_tables(
    value: Any, path: str, evidence: list[dict[str, Any]], file_path: str
) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            normalized_key = str(key).lower().replace("_", "-")
            if "dependenc" in normalized_key:
                walk_dependency_tables(child, child_path, evidence, file_path)
            else:
                find_dependency_tables(child, child_path, evidence, file_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            find_dependency_tables(child, f"{path}[{index}]", evidence, file_path)


def parse_toml(path: str, text: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return evidence

    if PurePosixPath(path).name.lower() in LOCK_FILES:
        packages = data.get("package", [])
        if isinstance(packages, list):
            for index, package in enumerate(packages):
                if not isinstance(package, dict):
                    continue
                name = str(package.get("name", "")).lower().replace("_", "-")
                if name == "hydra-core" and package.get("version") is not None:
                    add_evidence(
                        evidence,
                        path=path,
                        kind="lock",
                        resolved_version=normalize_locked_version(
                            str(package["version"])
                        ),
                        source=f"package[{index}]",
                    )
        return evidence

    project = data.get("project", {})
    if isinstance(project, dict):
        for key in ("dependencies", "optional-dependencies"):
            if key in project:
                walk_dependency_tables(project[key], f"project.{key}", evidence, path)
    dependency_groups = data.get("dependency-groups")
    if dependency_groups is not None:
        walk_dependency_tables(dependency_groups, "dependency-groups", evidence, path)
    for key in ("packages", "dev-packages"):
        if key in data:
            walk_dependency_tables(data[key], key, evidence, path)
    tool = data.get("tool", {})
    if isinstance(tool, dict):
        find_dependency_tables(tool, "tool", evidence, path)
    return evidence


def parse_pipfile_lock(path: str, text: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return evidence
    for section in ("default", "develop"):
        dependencies = data.get(section, {})
        if not isinstance(dependencies, dict):
            continue
        for name, value in dependencies.items():
            if name.lower().replace("_", "-") != "hydra-core":
                continue
            version = value.get("version") if isinstance(value, dict) else value
            add_evidence(
                evidence,
                path=path,
                kind="lock",
                resolved_version=(
                    normalize_locked_version(str(version))
                    if version is not None
                    else None
                ),
                source=section,
            )
    return evidence


def parse_setup_cfg(path: str, text: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    parser = configparser.ConfigParser(interpolation=None)
    try:
        parser.read_string(text)
    except configparser.Error:
        return evidence
    for section in parser.sections():
        normalized_section = section.lower()
        requirement_section = "require" in normalized_section
        if not requirement_section and normalized_section not in {
            "options",
            "metadata",
        }:
            continue
        for option, value in parser.items(section):
            if not requirement_section and "require" not in option:
                continue
            for line in value.splitlines():
                requirement = requirement_from_line(line)
                if requirement is not None:
                    add_evidence(
                        evidence,
                        path=path,
                        kind="declaration",
                        requirement=requirement,
                        source=f"{section}.{option}",
                    )
    return evidence


def parse_manifest(path: str, text: str) -> list[dict[str, Any]]:
    name = PurePosixPath(path).name.lower()
    if name.endswith(".toml") or name in {
        "pipfile",
        "poetry.lock",
        "pdm.lock",
        "uv.lock",
    }:
        return parse_toml(path, text)
    if name == "pipfile.lock":
        return parse_pipfile_lock(path, text)
    if name == "setup.cfg":
        return parse_setup_cfg(path, text)

    evidence: list[dict[str, Any]] = []
    kind = "lock" if name in LOCK_FILES else "declaration"
    for line_number, line in enumerate(text.splitlines(), 1):
        requirement = requirement_from_line(line)
        if requirement is None:
            continue
        if any(item.get("source") == f"line:{line_number}" for item in evidence):
            continue
        add_evidence(
            evidence,
            path=path,
            kind=kind,
            requirement=requirement,
            source=f"line:{line_number}",
        )
    return evidence


def document_hydra_evidence(path: str, text: str) -> list[dict[str, Any]]:
    evidence = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not HYDRA_MENTION_RE.search(line):
            continue
        compact = re.sub(r"\s+", " ", line).strip()
        kind = (
            "documented"
            if any(pattern.search(compact) for pattern in STRONG_DOCUMENTATION_PATTERNS)
            else "mentioned"
        )
        evidence.append(
            {
                "path": path,
                "line": line_number,
                "kind": kind,
                "text": compact[:240],
            }
        )
    return evidence


def evidence_status(evidence: list[dict[str, Any]]) -> str:
    if any(item["kind"] == "documented" for item in evidence):
        return "documented"
    return "mentioned" if evidence else "none"


def analyze_readme(path: str | None, text: str | None) -> dict[str, Any]:
    if path is None or text is None:
        return {
            "readme_path": path,
            "readme_hydra_status": "missing",
            "hydra_documented_in_readme": False,
            "readme_hydra_snippets": [],
        }
    evidence = document_hydra_evidence(path, text)
    status = evidence_status(evidence)
    return {
        "readme_path": path,
        "readme_hydra_status": status,
        "hydra_documented_in_readme": status == "documented",
        "readme_hydra_snippets": [
            {"line": item["line"], "kind": item["kind"], "text": item["text"]}
            for item in evidence[:5]
        ],
    }


def analyze_documentation(
    documents: dict[str, str], readme_path: str | None
) -> dict[str, Any]:
    evidence = []
    files_with_hydra = []
    other_files_with_hydra = []
    other_evidence = []
    for path, text in sorted(documents.items()):
        file_evidence = document_hydra_evidence(path, text)
        if not file_evidence:
            continue
        files_with_hydra.append(path)
        evidence.extend(file_evidence)
        if path != readme_path:
            other_files_with_hydra.append(path)
            other_evidence.extend(file_evidence)
    status = evidence_status(evidence)
    other_status = evidence_status(other_evidence)
    evidence.sort(
        key=lambda item: (
            not (
                item["kind"] == "documented"
                and is_user_documentation_path(item["path"])
            ),
            item["kind"] != "documented",
            item["path"],
            item["line"],
        )
    )
    return {
        "documentation_hydra_status": status,
        "hydra_documented_in_markdown": status == "documented",
        "documentation_files_with_hydra": files_with_hydra,
        "documentation_hydra_evidence": evidence[:50],
        "other_markdown_hydra_status": other_status,
        "other_markdown_files_with_hydra": other_files_with_hydra,
    }


def load_repositories(args: argparse.Namespace) -> list[Repository]:
    connection = sqlite3.connect(args.db)
    connection.row_factory = sqlite3.Row
    clauses = []
    parameters: list[Any] = []
    if args.min_stars is not None:
        clauses.append("coalesce(stargazers_count, 0) >= ?")
        parameters.append(args.min_stars)
    if args.skip_forks:
        clauses.append("not fork")
    if args.skip_archived:
        clauses.append("not archived")
    if args.repo:
        placeholders = ",".join("?" for _ in args.repo)
        clauses.append(f"full_name in ({placeholders})")
        parameters.extend(args.repo)
    where = f"where {' and '.join(clauses)}" if clauses else ""
    rows = connection.execute(
        f"""
        select full_name, stargazers_count, default_branch, fork, archived, html_url
        from repos
        {where}
        order by coalesce(stargazers_count, 0) desc, full_name
        """,
        parameters,
    ).fetchall()
    connection.close()

    if args.repo:
        found = {row["full_name"] for row in rows}
        missing = sorted(set(args.repo) - found)
        if missing:
            raise SystemExit(
                f"Repositories not found in database: {', '.join(missing)}"
            )
    if args.limit is not None:
        rows = rows[: args.limit]
    return [
        Repository(
            full_name=row["full_name"],
            stars=row["stargazers_count"],
            default_branch=row["default_branch"] or "main",
            fork=bool(row["fork"]),
            archived=bool(row["archived"]),
            html_url=row["html_url"],
        )
        for row in rows
    ]


def completed_repositories(path: Path) -> set[str]:
    completed = set()
    if not path.exists():
        return completed
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise SystemExit(
                    f"{path}:{line_number}: invalid JSON: {error}"
                ) from error
            if row.get("analysis_version") == ANALYSIS_VERSION and row.get(
                "status"
            ) in {"ok", "unavailable"}:
                completed.add(row["repo"])
    return completed


def fetch_entries(
    client: GitHubReader,
    repo: Repository,
    entries: list[dict[str, Any]],
    workers: int,
    revision: str,
    max_file_bytes: int,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    unique_entries = {entry["path"]: entry for entry in entries}
    texts: dict[str, str] = {}
    failures: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                client.get_blob_text,
                repo,
                entry["path"],
                entry.get("sha", ""),
                revision,
                max_file_bytes,
            ): entry["path"]
            for entry in unique_entries.values()
        }
        for future in as_completed(futures):
            path = futures[future]
            try:
                texts[path] = future.result()
            except (
                BlobUnavailable,
                HTTPError,
                URLError,
                OSError,
                ValueError,
            ) as error:
                failures.append({"path": path, "error": str(error)})
    failures.sort(key=lambda item: item["path"])
    return texts, failures


def search_for_paths(
    client: GitHubReader,
    repo: Repository,
    query: str,
    predicate: Callable[[str], bool],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    try:
        items, total_count, incomplete_results = client.search_code(repo, query)
    except SearchUnavailable as error:
        return [], {
            "status": "unavailable",
            "query": query,
            "error": str(error),
        }
    entries = [
        {"path": item["path"], "sha": item.get("sha", ""), "type": "blob"}
        for item in items
        if predicate(item["path"])
    ]
    return entries, {
        "status": (
            "complete"
            if total_count <= len(items) and not incomplete_results
            else "partial"
        ),
        "query": query,
        "total_count": total_count,
        "results_returned": len(items),
        "incomplete_results": incomplete_results,
        "matching_paths": len(entries),
    }


def analyze_repository(
    client: GitHubReader, repo: Repository, args: argparse.Namespace
) -> dict[str, Any]:
    started = time.monotonic()
    tree = client.get_tree(repo)
    revision = str(tree["sha"])
    entries = tree.get("tree", [])
    if not isinstance(entries, list):
        raise ValueError("GitHub tree response has no tree list")

    readme = select_readme(entries)
    manifests, manifest_inventory = select_manifests(
        entries,
        args.max_declaration_manifests,
        args.max_lock_files,
        args.max_file_bytes,
    )
    markdown, markdown_files_omitted, markdown_files_size_skipped = select_markdown(
        entries, readme, args.max_markdown_files, args.max_file_bytes
    )
    selected_markdown_paths = {entry["path"] for entry in markdown}
    readme_size_skipped = bool(
        readme is not None
        and readme["path"] not in selected_markdown_paths
        and int(readme.get("size", 0)) > args.max_file_bytes
    )
    extra_readme = (
        [readme]
        if readme is not None
        and readme["path"] not in selected_markdown_paths
        and not readme_size_skipped
        else []
    )
    texts, files_failed = fetch_entries(
        client,
        repo,
        manifests + markdown + extra_readme,
        args.workers,
        revision,
        args.max_file_bytes,
    )

    evidence: list[dict[str, Any]] = []
    for entry in manifests:
        if entry["path"] in texts:
            items = parse_manifest(entry["path"], texts[entry["path"]])
            for item in items:
                item["discovery"] = "tree_scan"
            evidence.extend(items)

    omitted_manifests = (
        manifest_inventory["declaration_files_omitted"]
        + manifest_inventory["lock_files_omitted"]
    )
    manifest_search_needed = (
        not evidence or omitted_manifests > 0 or bool(tree.get("truncated"))
    )
    manifest_search: dict[str, Any] = {"status": "not_needed"}
    search_manifest_entries: list[dict[str, Any]] = []
    if manifest_search_needed and not args.no_code_search:
        search_manifest_entries, manifest_search = search_for_paths(
            client, repo, "hydra-core", is_manifest
        )
        already_scanned = {entry["path"] for entry in manifests}
        search_manifest_entries = [
            entry
            for entry in search_manifest_entries
            if entry["path"] not in already_scanned
        ]
        supplemental_texts, supplemental_failures = fetch_entries(
            client,
            repo,
            search_manifest_entries,
            args.workers,
            revision,
            args.max_file_bytes,
        )
        texts.update(supplemental_texts)
        files_failed.extend(supplemental_failures)
        for entry in search_manifest_entries:
            if entry["path"] in supplemental_texts:
                items = parse_manifest(entry["path"], supplemental_texts[entry["path"]])
                for item in items:
                    item["discovery"] = "code_search"
                evidence.extend(items)
    elif manifest_search_needed:
        manifest_search = {"status": "disabled"}

    markdown_search_needed = markdown_files_omitted > 0 or bool(tree.get("truncated"))
    markdown_search: dict[str, Any] = {"status": "not_needed"}
    search_markdown_entries: list[dict[str, Any]] = []
    if markdown_search_needed and not args.no_code_search:
        searches = []
        entries_by_path = {}
        for extension in ("md", "mdx"):
            entries, search = search_for_paths(
                client, repo, f"hydra extension:{extension}", is_markdown
            )
            searches.append(search)
            for entry in entries:
                entries_by_path[entry["path"]] = entry
        search_markdown_entries = list(entries_by_path.values())
        statuses = {search["status"] for search in searches}
        markdown_search = {
            "status": (
                "complete"
                if statuses == {"complete"}
                else "unavailable"
                if statuses == {"unavailable"}
                else "partial"
            ),
            "queries": searches,
        }
        already_scanned = {entry["path"] for entry in markdown + extra_readme}
        search_markdown_entries = [
            entry
            for entry in search_markdown_entries
            if entry["path"] not in already_scanned
        ]
        supplemental_texts, supplemental_failures = fetch_entries(
            client,
            repo,
            search_markdown_entries,
            args.workers,
            revision,
            args.max_file_bytes,
        )
        texts.update(supplemental_texts)
        files_failed.extend(supplemental_failures)
    elif markdown_search_needed:
        markdown_search = {"status": "disabled"}

    manifest_paths = {entry["path"] for entry in manifests + search_manifest_entries}
    markdown_paths = {
        entry["path"] for entry in markdown + extra_readme + search_markdown_entries
    }
    manifest_failures = {
        item["path"] for item in files_failed if item["path"] in manifest_paths
    }
    known_lock_paths = {
        entry["path"]
        for entry in manifests + search_manifest_entries
        if PurePosixPath(entry["path"]).name.lower() in LOCK_FILES
    }
    lock_failures = manifest_failures & known_lock_paths
    declaration_failures = manifest_failures - known_lock_paths
    markdown_failures = {
        item["path"] for item in files_failed if item["path"] in markdown_paths
    }

    declaration_files_omitted = manifest_inventory["declaration_files_omitted"]
    lock_files_omitted = manifest_inventory["lock_files_omitted"]
    if not evidence and manifest_search.get("status") in {
        "disabled",
        "unavailable",
    }:
        declaration_coverage = "recognized_files_only"
    elif manifest_inventory["declaration_files_size_skipped"] > 0:
        declaration_coverage = "partial"
    elif (
        declaration_files_omitted == 0
        and not tree.get("truncated")
        and not declaration_failures
    ):
        declaration_coverage = "complete"
    elif manifest_search.get("status") == "complete" and not declaration_failures:
        declaration_coverage = "search_completed"
    else:
        declaration_coverage = "partial"

    lock_coverage = (
        "complete"
        if lock_files_omitted == 0 and not tree.get("truncated") and not lock_failures
        else "partial"
    )
    if lock_coverage == "partial" or declaration_coverage in {
        "partial",
        "recognized_files_only",
    }:
        manifest_coverage = "partial"
    elif declaration_coverage == "search_completed":
        manifest_coverage = "search_completed"
    else:
        manifest_coverage = "complete"

    if markdown_files_size_skipped > 0 or readme_size_skipped:
        markdown_coverage = "partial"
    elif (
        markdown_files_omitted == 0
        and not tree.get("truncated")
        and not markdown_failures
    ):
        markdown_coverage = "complete"
    elif markdown_search.get("status") == "complete" and not markdown_failures:
        markdown_coverage = "search_completed"
    else:
        markdown_coverage = "partial"

    documents = {path: text for path, text in texts.items() if path in markdown_paths}
    readme_path = readme["path"] if readme is not None else None
    readme_result = analyze_readme(
        readme_path, documents.get(readme_path) if readme_path else None
    )
    documentation_result = analyze_documentation(documents, readme_path)

    declarations = [item for item in evidence if item["kind"] == "declaration"]
    declared_specifiers = sorted(
        {item["specifier"] for item in declarations if item.get("specifier")}
    )
    root_declared_specifiers = sorted(
        {
            item["specifier"]
            for item in declarations
            if item["scope"] == "root" and item.get("specifier")
        }
    )
    locked_versions = sorted(
        {
            item["resolved_version"]
            for item in evidence
            if item["kind"] == "lock" and item.get("resolved_version")
        }
    )
    files_failed.sort(key=lambda item: item["path"])
    result = {
        "analysis_version": ANALYSIS_VERSION,
        "analyzed_at": datetime.now(UTC).isoformat(),
        "repo": repo.full_name,
        "url": repo.html_url,
        "stars": repo.stars,
        "default_branch": repo.default_branch,
        "fork": repo.fork,
        "archived": repo.archived,
        "status": "ok",
        "tree_sha": tree.get("sha"),
        "tree_truncated": bool(tree.get("truncated")),
        "analysis_complete": manifest_coverage in {"complete", "search_completed"}
        and markdown_coverage in {"complete", "search_completed"},
        "manifest_coverage": manifest_coverage,
        "declaration_coverage": declaration_coverage,
        "lock_coverage": lock_coverage,
        "manifest_inventory": manifest_inventory,
        "manifest_search": manifest_search,
        "manifest_files_scanned": sorted(
            path for path in manifest_paths if path in texts
        ),
        "manifest_files_omitted": omitted_manifests,
        "markdown_coverage": markdown_coverage,
        "markdown_search": markdown_search,
        "markdown_files_scanned": sorted(
            path for path in markdown_paths if path in texts
        ),
        "markdown_files_omitted": markdown_files_omitted,
        "markdown_files_size_skipped": markdown_files_size_skipped,
        "readme_size_skipped": readme_size_skipped,
        "files_failed": files_failed,
        "direct_dependency_declared": bool(declarations),
        "root_dependency_declared": any(
            item["scope"] == "root" for item in declarations
        ),
        "nested_dependency_declared": any(
            item["scope"] != "root" for item in declarations
        ),
        "declaration_scopes": sorted({item["scope"] for item in declarations}),
        "declared_specifiers": declared_specifiers,
        "root_declared_specifiers": root_declared_specifiers,
        "locked_versions": locked_versions,
        "version_evidence": evidence,
        **readme_result,
        **documentation_result,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    return result


def unavailable_result(repo: Repository, error: Exception) -> dict[str, Any]:
    return {
        "analysis_version": ANALYSIS_VERSION,
        "analyzed_at": datetime.now(UTC).isoformat(),
        "repo": repo.full_name,
        "url": repo.html_url,
        "stars": repo.stars,
        "default_branch": repo.default_branch,
        "fork": repo.fork,
        "archived": repo.archived,
        "status": "unavailable",
        "error": str(error),
    }


def error_result(repo: Repository, error: Exception) -> dict[str, Any]:
    return {
        "analysis_version": ANALYSIS_VERSION,
        "analyzed_at": datetime.now(UTC).isoformat(),
        "repo": repo.full_name,
        "url": repo.html_url,
        "stars": repo.stars,
        "default_branch": repo.default_branch,
        "fork": repo.fork,
        "archived": repo.archived,
        "status": "error",
        "error_type": type(error).__name__,
        "error": str(error),
    }


def compact_values(values: list[str], limit: int = 3) -> str:
    if not values:
        return "-"
    displayed = ", ".join(values[:limit])
    omitted = max(0, len(values) - limit)
    return f"{displayed} (+{omitted})" if omitted else displayed


def format_progress(index: int, total: int, result: dict[str, Any]) -> str:
    prefix = (
        f"{index}/{total} {result['repo']}: {result['status']} "
        f"stars={result.get('stars') or 0}"
    )
    if result["status"] != "ok":
        return f"{prefix} error={result.get('error', '-')}"

    declared = compact_values(result["declared_specifiers"])
    if result["direct_dependency_declared"] and declared == "-":
        declared = "unpinned"
    return (
        f"{prefix} declared={declared} "
        f"scopes={compact_values(result['declaration_scopes'])} "
        f"root={'yes' if result['root_dependency_declared'] else 'no'} "
        f"nested={'yes' if result['nested_dependency_declared'] else 'no'} "
        f"locked={compact_values(result['locked_versions'])} "
        f"readme={result['readme_hydra_status']} "
        f"docs={result['other_markdown_hydra_status']} "
        f"coverage={result['manifest_coverage']}/{result['markdown_coverage']} "
        f"manifests={len(result['manifest_files_scanned'])} "
        f"markdown={len(result['markdown_files_scanned'])} "
        f"evidence={len(result['version_evidence'])} "
        f"failed_files={len(result['files_failed'])} "
        f"elapsed={result['elapsed_seconds']:g}s"
    )


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--repo",
        action="append",
        help="Analyze only this owner/repository (repeatable)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the star-sorted candidate set before resume filtering",
    )
    parser.add_argument("--min-stars", type=int)
    parser.add_argument("--skip-forks", action="store_true")
    parser.add_argument("--skip-archived", action="store_true")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the output instead of resuming it",
    )
    parser.add_argument("--max-declaration-manifests", type=int, default=200)
    parser.add_argument("--max-lock-files", type=int, default=25)
    parser.add_argument("--max-markdown-files", type=int, default=100)
    parser.add_argument("--max-file-bytes", type=int, default=1_000_000)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--no-code-search",
        action="store_true",
        help="Disable GitHub code-search fallbacks for partial scans",
    )
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--delay", type=float, default=0.1)
    parser.add_argument(
        "--blob-source",
        choices=("raw", "api"),
        default="raw",
        help="Fetch file contents from raw.githubusercontent.com or the REST API",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")
    repositories = load_repositories(args)
    completed = set() if args.overwrite else completed_repositories(args.out)
    pending = [repo for repo in repositories if repo.full_name not in completed]
    completed_count = len(repositories) - len(pending)
    print(
        f"selected={len(repositories)} completed={completed_count} "
        f"pending={len(pending)} output={args.out}",
        file=sys.stderr,
    )
    if not pending:
        return 0

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print(
            "Warning: GITHUB_TOKEN/GH_TOKEN is unset; GitHub allows only 60 "
            "unauthenticated requests per hour and code search is unavailable.",
            file=sys.stderr,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    client = GitHubClient(
        token=token, timeout=args.timeout, blob_source=args.blob_source
    )
    output_mode = "w" if args.overwrite else "a"
    with args.out.open(output_mode, encoding="utf-8") as output:
        for index, repo in enumerate(pending, 1):
            try:
                result = analyze_repository(client, repo, args)
            except RepositoryUnavailable as error:
                result = unavailable_result(repo, error)
            except (HTTPError, URLError, OSError, ValueError) as error:
                result = error_result(repo, error)
            output.write(json.dumps(result, sort_keys=True) + "\n")
            output.flush()
            print(
                format_progress(completed_count + index, len(repositories), result),
                file=sys.stderr,
                flush=True,
            )
            if index != len(pending) and args.delay:
                time.sleep(args.delay)
    print(
        f"GitHub API requests: {client.requests}; raw file requests: "
        f"{client.raw_requests}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
