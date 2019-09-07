# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.plugins.completion_plugin import CompletionPlugin
import logging
import sys
import os

log = logging.getLogger(__name__)

# TODO:
# Add testing and integration testing


class BashCompletion(CompletionPlugin):
    def install(self):
        script = """hydra_bash_completion()
{
    words=($COMP_LINE)
    if [ ${words[0]} == "python" ]; then
        if (( ${#words[@]} < 2 )); then
            return
        fi
        file_path=$(pwd)/${words[1]}
        if [ ! -f "$file_path" ]; then
            return
        fi
        grep "@hydra.main" $file_path -q
        helper="${words[0]} ${words[1]}"
    else
        helper="${words[0]}"
        true
    fi
    if [ $? == 0 ]; then
        options=$( COMP_INDEX=$COMP_INDEX COMP_LINE=$COMP_LINE $helper --shell_completion query=bash)
    fi
    word=${words[$COMP_CWORD]}
    COMPREPLY=($( compgen -W '$options' -- "$word" ));
}

complete -F hydra_bash_completion """
        print(script + self._get_exec())

    def uninstall(self):
        print(
            """
unset hydra_bash_completion
complete -r """
            + self._get_exec()
        )

    def provides(self):
        return "bash"

    def query(self, config_loader, cfg):
        # line = os.environ["COMP_LINE"]
        # index = os.environ["COMP_INDEX"]
        print("10 20 30")

    @staticmethod
    def _get_exec():
        if sys.argv[0].endswith(".py"):
            return "python"
        else:
            # Running as an installed app (setuptools entry point)
            executable = os.path.basename(sys.argv[0])
            return executable
