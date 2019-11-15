# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.plugins.completion_plugin import CompletionPlugin
import logging
import sys
import os
import re

log = logging.getLogger(__name__)

# TODO:
# Test with /miniconda3/envs/hydra36/bin/python , seems to be running python for some reason.
# Test handling of errors loading config from command line during completion


class BashCompletion(CompletionPlugin):
    # TODO: detect python with path like /foo/bar/python
    def install(self):
        script = """hydra_bash_completion()
{
    words=($COMP_LINE)
    if [ "${words[0]}" == "python" ]; then
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

    if ! [ -x "$(command -v $helper)" ]; then
        false
    fi

    if [ $? == 0 ]; then
        options=$( COMP_POINT=$COMP_POINT COMP_LINE=$COMP_LINE $helper -sc query=bash)
        word=${words[$COMP_CWORD]}

        if [ "$HYDRA_COMP_DEBUG" == "1" ]; then
            printf "\\n"
            printf "COMP_LINE='$COMP_LINE'\\n"
            printf "COMP_POINT='$COMP_POINT'\\n"
            printf "Word='$word'\\n"
            printf "Output suggestions:\\n"
            printf "\\t%s\\n" ${options[@]}
        fi
        COMPREPLY=($( compgen -o nospace -o default -W '$options' -- "$word" ));
    fi
}

COMP_WORDBREAKS=${COMP_WORDBREAKS//=}
COMP_WORDBREAKS=$COMP_WORDBREAKS complete -o nospace -o default -F hydra_bash_completion """
        print(script + self._get_exec())

    def uninstall(self):
        print("unset hydra_bash_completion\ncomplete -r " + self._get_exec())

    def provides(self):
        return "bash"

    @staticmethod
    def strip_python_or_app_name(line):
        """
        Take the command line (COMP_LINE) received from bash completion, and strip the app name from it
        which could be at the form of python script.py or some_app.
        it also corrects the index (COMP_INDEX) to reflect the same location in the striped command line.
        :param line: input line, may contain python file.py followed=by_args..
        :param index: index of cursor in input line
        :return: tuple(args line, index of cursor in args line)
        """
        python_args = r"^\s*[\w\/]*python\s*[\w/\.]*\s*(.*)"
        app_args = r"^\s*[\w_\-=\./]+\s*(.*)"
        match = re.match(python_args, line)
        if match:
            return match.group(1)
        else:
            match = re.match(app_args, line)
            if match:
                return match.group(1)
            else:
                raise RuntimeError("Error parsing line '{}'".format(line))

    def query(self, config_file):
        line = os.environ["COMP_LINE"]
        index = os.environ["COMP_POINT "] if "COMP_POINT " in os.environ else len(line)

        if index == "":
            index = 0
        if isinstance(index, str):
            index = int(index)

        # currently index is ignored.
        line = self.strip_python_or_app_name(line)
        print(" ".join(self._query(config_file=config_file, line=line)))

    @staticmethod
    def _get_exec():
        if sys.argv[0].endswith(".py"):
            return "python"
        else:
            # Running as an installed app (setuptools entry point)
            executable = os.path.basename(sys.argv[0])
            return executable
