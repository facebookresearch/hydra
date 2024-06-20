# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import codecs
import logging
import os
import re
import shutil
import subprocess
from functools import partial
from os.path import abspath, dirname, exists, isdir, join
from pathlib import Path
from typing import List, Optional

from setuptools import Command
from setuptools.command import build_py, develop, sdist

log = logging.getLogger(__name__)

def find_version(*file_paths: str) -> str:
    """Find the version number from the specified file."""
    with codecs.open(os.path.join(*file_paths), "r", "utf-8") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def matches(patterns: List[str], string: str) -> bool:
    """Check if the string matches any of the given patterns."""
    string = string.replace("\\", "/")
    return any(re.match(pattern, string) for pattern in patterns)

def find_files(
    root: str,
    rbase: str,
    include_files: List[str],
    include_dirs: List[str],
    excludes: List[str],
    scan_exclude: List[str],
) -> List[str]:
    """Recursively find files and directories matching the given patterns."""
    files = []
    scan_root = os.path.join(root, rbase)
    with os.scandir(scan_root) as it:
        for entry in it:
            path = os.path.join(rbase, entry.name)
            if matches(scan_exclude, path):
                continue

            if entry.is_dir():
                if matches(include_dirs, path):
                    if not matches(excludes, path):
                        files.append(path)
                else:
                    ret = find_files(
                        root=root,
                        rbase=path,
                        include_files=include_files,
                        include_dirs=include_dirs,
                        excludes=excludes,
                        scan_exclude=scan_exclude,
                    )
                    files.extend(ret)
            else:
                if matches(include_files, path) and not matches(excludes, path):
                    files.append(path)

    return files

def find(
    root: str,
    include_files: List[str],
    include_dirs: List[str],
    excludes: List[str],
    scan_exclude: Optional[List[str]] = None,
) -> List[str]:
    """Find all files and directories matching the given patterns starting from the root."""
    if scan_exclude is None:
        scan_exclude = []
    return find_files(
        root=root,
        rbase="",
        include_files=include_files,
        include_dirs=include_dirs,
        excludes=excludes,
        scan_exclude=scan_exclude,
    )

class CleanCommand(Command):
    """
    Custom command to clean out generated and junk files.
    """

    description = "Cleans out generated and junk files we don't want in the repo"
    user_options: List[str] = []

    def run(self) -> None:
        files = find(
            ".",
            include_files=["^hydra/grammar/gen/.*"],
            include_dirs=[
                "\\.egg-info$",
                "^.pytest_cache$",
                ".*/__pycache__$",
                ".*/multirun$",
                ".*/outputs$",
                "^build$",
            ],
            scan_exclude=["^.git$", "^.nox/.*$", "^website/.*$"],
            excludes=[".*\\.gitignore$"],
        )

        if self.dry_run:
            print("Would clean up the following files and dirs")
            print("\n".join(files))
        else:
            for f in files:
                if exists(f):
                    if isdir(f):
                        shutil.rmtree(f, ignore_errors=True)
                    else:
                        os.unlink(f)

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

def run_antlr(cmd: Command) -> None:
    """Run the ANTLR command to generate parsers."""
    try:
        log.info("Generating parsers with antlr4")
        cmd.run_command("antlr")
    except OSError as e:
        if e.errno == errno.ENOENT:
            msg = f"| Unable to generate parsers: {e} |"
            msg = "=" * len(msg) + "\n" + msg + "\n" + "=" * len(msg)
            log.critical(msg)
            exit(1)
        else:
            raise

class BuildPyCommand(build_py.build_py):
    def run(self) -> None:
        if not self.dry_run:
            self.run_command("clean")
            run_antlr(self)
        build_py.build_py.run(self)

class DevelopCommand(develop.develop):
    def run(self) -> None:
        if not self.dry_run:
            run_antlr(self)
        develop.develop.run(self)

class SDistCommand(sdist.sdist):
    def run(self) -> None:
        if not self.dry_run:
            self.run_command("clean")
            run_antlr(self)
        sdist.sdist.run(self)

class ANTLRCommand(Command):
    """
    Generate parsers using ANTLR.
    """

    description = "Run ANTLR"
    user_options: List[str] = []

    def run(self) -> None:
        """Run the ANTLR command to generate parsers."""
        root_dir = abspath(dirname(__file__))
        project_root = abspath(dirname(root_dir))
        grammars = [
            "hydra/grammar/OverrideLexer.g4",
            "hydra/grammar/OverrideParser.g4",
        ]
        for grammar in grammars:
            command = [
                "java",
                "-jar",
                join(root_dir, "bin/antlr-4.11.1-complete.jar"),
                "-Dlanguage=Python3",
                "-o",
                join(project_root, "hydra/grammar/gen/"),
                "-Xexact-output-dir",
                "-visitor",
                join(project_root, grammar),
            ]

            log.info(f"Generating parser for Python3: {command}")

            subprocess.check_call(command)

            log.info("Replacing imports of antlr4 in generated parsers")
            self._fix_imports()

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def _fix_imports(self) -> None:
        """Fix imports in the generated parsers to use the vendored antlr4."""
        build_dir = Path(__file__).parent.absolute()
        project_root = build_dir.parent
        lib = "antlr4"
        pkgname = 'omegaconf.vendor'

        replacements = [
            partial(
                re.compile(rf'(^\s*)import {lib}\n', flags=re.M).sub,
                rf'\1from {pkgname} import {lib}\n'
            ),
            partial(
                re.compile(rf'(^\s*)from {lib}(\.|\s+)', flags=re.M).sub,
                rf'\1from {pkgname}.{lib}\2'
            ),
        ]

        path = project_root / "hydra" / "grammar" / "gen"
        for item in path.iterdir():
            if item.is_file() and item.name.endswith(".py"):
                text = item.read_text('utf8')
                for replacement in replacements:
                    text = replacement(text)
                item.write_text(text, 'utf8')
