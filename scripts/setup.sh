#!/bin/bash

if [[ "$DEBUG" == "true" ]]; then
    set -ex
    export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
fi

CUR_DIR="$(dirname "${BASH_SOURCE[0]}")"

pushd $(dirname "$0")/.. > /dev/null

git submodule update --init --recursive

pushd themes > /dev/null
if [ ! -d "docsy" ]; then
    git clone --recurse-submodules --depth 1 https://github.com/google/docsy.git
else
    pushd docsy > /dev/null
    if [ ! -d "assets/vendor/bootstrap/dist" ]; then
        git pull --recurse-submodules --depth 1
    fi
    popd > /dev/null
fi
popd > /dev/null
