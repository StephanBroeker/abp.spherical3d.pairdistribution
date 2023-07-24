#!/bin/bash

set -e

if [ -d ./pdoc_env ]; then
    . ./pdoc_env/bin/activate  
else
    python3 -m venv ./pdoc_env
    . ./pdoc_env/bin/activate
    pip install numpy scipy pdoc
fi

rm -rf ./doc
PYTHONPATH=$(pwd) pdoc --math -d google -o doc abp.spherical3d.pairdistribution
