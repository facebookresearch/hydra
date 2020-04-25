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
        script = """function hydra_fish_completion
    # Hydra will access COMP_LINE to generate completion candidates
    set -lx COMP_LINE (commandline -cp)

    # Find out how to call the underlying script
    set -l parts (string split -n ' ' $COMP_LINE)
    if test "$parts[1]" = "python" -o "$parts[1]" = "python3"
        set cmd "$parts[1] $parts[2]"
    else
        set cmd "$parts[1]"
    end

    # Generate candidates
    eval "$cmd -sc query=fish"
end
        """
        output = self._get_exec()
        reg_cmd = []
        for name, cond in output:
            reg_cmd.append(
                f"complete -c {name} {cond}-x -a '(hydra_fish_completion)'\n"
            )
        print(script)
        print("".join(reg_cmd))

    def uninstall(self) -> None:
        name = self._get_uninstall_exec()
        print(f"complete -e -c {name}")

    def provides(self) -> str:
        return "fish"

    def query(self, config_name: Optional[str]) -> None:
        line = os.environ["COMP_LINE"]
        line = self.strip_python_or_app_name(line)
        print("\n".join(self._query(config_name=config_name, line=line)))

    @staticmethod
    def _get_exec() -> List[Tuple[str, str]]:
        # Running as an installed app (setuptools entry point)
        output = []
        # User scenario 1: python script.py
        name = os.path.basename(sys.executable)
        cond = f"-n '__fish_seen_subcommand_from {sys.argv[0]}' "
        output.append((name, cond))

        # User scenario 2: ./script.py or src/script.py or script.py
        name = os.path.basename(sys.argv[0])
        cond = ""
        output.append((name, cond))

        return output

    @staticmethod
    def _get_uninstall_exec() -> str:
        name = os.path.basename(sys.argv[0])

        return name
