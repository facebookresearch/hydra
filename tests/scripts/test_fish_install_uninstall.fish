# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

set prog $argv[1]
set comp_func $argv[2]
if test -z "$prog" -o -z "comp_func"
    echo "Param error."
    exit 1
end

complete -e -c python 2> /dev/null

# Verify install.
eval "$prog -sc install=fish | source"
if test (complete | grep "$comp_func" | wc -l) -ne 2
    echo "Install test failed"
    exit 1
end

# Verify uninstall.
eval "$prog -sc uninstall=fish | source"

# foo.py rule should be removed
if test (complete | grep "$comp_func" | wc -l) -ne 1
    echo "Uninstall test 1 failed"
    exit 1
end

# python rule function emptied
if test ($comp_func | wc -l ) -ne 0
    echo "Uninstall test 2 failed"
    exit 1
end
