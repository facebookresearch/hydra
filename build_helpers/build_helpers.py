# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import codecs
import distutils.log
import errno
import os
import re
import shutil
import subprocess
from os.path import abspath, basename, dirname, exists, isdir, join
from typing import List, Optional

from setuptools import Command
from setuptools.command import build_py, develop, sdist  # type: ignore


def find_version(*file_paths: str) -> str:
    with codecs.open(os.path.join(*file_paths), "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def matches(patterns: List[str], string: str) -> bool:
    string = string.replace("\\", "/")
    for pattern in patterns:
        if re.match(pattern, string):
            return True
    return False


def find_(
    root: str,
    rbase: str,
    include_files: List[str],
    include_dirs: List[str],
    excludes: List[str],
    scan_exclude: List[str],
) -> List[str]:
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
                    ret = find_(
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
    if scan_exclude is None:
        scan_exclude = []
    return find_(
        root=root,
        rbase="",
        include_files=include_files,
        include_dirs=include_dirs,
        excludes=excludes,
        scan_exclude=scan_exclude,
    )


class CleanCommand(Command):  # type: ignore
    """
    Our custom command to clean out junk files.
    """

    description = "Cleans out generated and junk files we don't want in the repo"
    dry_run: bool
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
                "^dist$",
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
    try:
        cmd.announce("Generating parsers with antlr4", level=distutils.log.INFO)
        cmd.run_command("antlr")
    except OSError as e:
        if e.errno == errno.ENOENT:
            msg = f"| Unable to generate parsers: {e} |"
            msg = "=" * len(msg) + "\n" + msg + "\n" + "=" * len(msg)
            cmd.announce(f"{msg}", level=distutils.log.FATAL)
            exit(1)
        else:
            raise


class BuildPyCommand(build_py.build_py):  # type: ignore
    def run(self) -> None:
        if not self.dry_run:
            self.run_command("clean")
            run_antlr(self)
        build_py.build_py.run(self)


class Develop(develop.develop):  # type: ignore
    def run(self) -> None:
        if not self.dry_run:
            run_antlr(self)
        develop.develop.run(self)


class SDistCommand(sdist.sdist):  # type: ignore
    def run(self) -> None:
        if not self.dry_run:
            self.run_command("clean")
            run_antlr(self)
        sdist.sdist.run(self)


class ANTLRCommand(Command):  # type: ignore
    """Generate parsers using ANTLR."""

    description = "Run ANTLR"
    user_options: List[str] = []

    def run(self) -> None:
        """Run command."""
        root_dir = abspath(dirname(__file__))
        project_root = abspath(dirname(basename(__file__)))
        for grammar in [
            "hydra/grammar/OverrideLexer.g4",
            "hydra/grammar/OverrideParser.g4",
        ]:
            command = [
                "java",
                "-jar",
                join(root_dir, "bin/antlr-4.8-complete.jar"),
                "-Dlanguage=Python3",
                "-o",
                join(project_root, "hydra/grammar/gen/"),
                "-Xexact-output-dir",
                "-visitor",
                join(project_root, grammar),
            ]

            self.announce(
                f"Generating parser for Python3: {command}", level=distutils.log.INFO
            )

            subprocess.check_call(command)

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass
