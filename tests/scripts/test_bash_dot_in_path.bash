#!/bin/bash

# Navigate to app with minimal configuration
cd tests/test_apps/app_with_cfg/

# Locate python
PYTHON=$(command -v python)

# Setup hydra bash completion
eval "$(python my_app.py -sc install=bash)"

# Setup debugging
export HYDRA_COMP_DEBUG=1
export PATH=$PATH:.

# Do actual test
test=$(COMP_LINE='python my_app.py' hydra_bash_completion |\
    grep EXECUTABLE_FIRST |\
    awk '{split($0,a,"=");b=substr(a[2],2,length(a[2])-2);print b}')

if [ $test == $PYTHON ]; then
    echo TRUE
else
    echo FALSE
fi
