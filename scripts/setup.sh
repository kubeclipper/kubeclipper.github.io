#!/bin/bash

if [[ "$DEBUG" == "true" ]]; then
    set -ex
    export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
fi

CUR_DIR="$(dirname "${BASH_SOURCE[0]}")"

pushd $(dirname "$0")/.. > /dev/null

git submodule update --init --recursive
