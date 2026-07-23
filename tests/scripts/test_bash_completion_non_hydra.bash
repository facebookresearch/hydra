#!/bin/bash
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

prog=("$@")

eval "$("${prog[@]}" -sc install=bash)"

COMP_LINE=${COMP_LINE:-"python non_hydra.py "}
COMP_POINT=${#COMP_LINE}
COMP_CWORD=2
hydra_bash_completion
