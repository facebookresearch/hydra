#!/usr/bin/env bash

prog=$1

eval "$($prog -sc install=bash)"

COMP_LINE="python non_hydra.py "
COMP_POINT=${#COMP_LINE}
COMP_CWORD=2
hydra_bash_completion
