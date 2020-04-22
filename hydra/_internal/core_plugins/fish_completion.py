# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
import sys
from typing import List, Optional, Tuple

from hydra.plugins.completion_plugin import CompletionPlugin

log = logging.getLogger(__name__)


class FishCompletion(CompletionPlugin):
    """Issue 1: python script.py style rule cannot be uninstalled
    Issue 2: fish adds a space to "hydra. " automatically"""

    def install(self) -> None:
        output = self._get_exec()
        script = []
        for name, cond, exe in output:
            args = f"'({exe} -sc query=fish --_completion (commandline -cp))'"
            script.append(f"""complete -c {name} {cond}-x -a {args}\n""")
        print("".join(script))

    def uninstall(self) -> None:
        name = self._get_uninstall_exec()
        print(f"complete -e -c {name}")

    def provides(self) -> str:
        return "fish"

    def query(self, config_name: Optional[str], line: Optional[str] = None) -> None:
        if not line:
            return
        line = self.strip_python_or_app_name(line)
        print("\n".join(self._query(config_name=config_name, line=line)))

    @staticmethod
    def _get_exec() -> List[Tuple[str, str, str]]:
        # Running as an installed app (setuptools entry point)
        exe = sys.executable + " " + os.path.abspath(sys.argv[0])

        output = []
        # User scenario 1: python script.py
        name = os.path.basename(sys.executable)
        cond = f"-n '__fish_seen_subcommand_from {sys.argv[0]}' "
        output.append((name, cond, exe))

        # User scenario 2: ./script.py or src/script.py or script.py
        name = os.path.basename(sys.argv[0])
        cond = ""
        output.append((name, cond, exe))

        return output

    @staticmethod
    def _get_uninstall_exec() -> str:
        name = os.path.basename(sys.argv[0])

        return name
