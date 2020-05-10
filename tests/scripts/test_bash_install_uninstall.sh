# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

prog=$1
comp_func=$2
if [[ -z "$prog" || -z "comp_func" ]]; then
    echo "Param error"
    exit 1
fi

dummy_completion(){ :; }

complete -r python

# Install stub completion function
complete -o nospace -o default -F dummy_completion python

# Verify install
eval "$($prog -sc install=bash)"
if ! complete -p python | grep -q "$comp_func"; then
    echo "Install test failed"
    exit 1
fi

# Verify uninstall
eval "$($prog -sc uninstall=bash)"
if ! complete -p python | grep -q dummy_completion; then
    echo "Uninstall test failed"
    exit 1
fi
