#!/bin/bash

CUR_DIR="$(dirname "${BASH_SOURCE[0]}")"

source "$CUR_DIR/function.sh"

VERSIONS_ARRAY=(
    'dev'
)

join_versions() {
    versions=$(printf ",%s" "${VERSIONS_ARRAY[@]}")
    echo ${versions:1}
}

VERSIONS_STRING=$(join_versions)

run() {
    export CURRENT_BRANCH="$(git name-rev --name-only HEAD)"
    export CURRENT_VERSION=${VERSIONS_ARRAY[0]}
    export VERSIONS=${VERSIONS_STRING}
    HUGO_TITLE="KubeClipper Doc - local"

    pushd $(dirname "$0")/.. > /dev/null

    if [ -z "$NOT_SYNC_SUBMOD" ]; then
        pushd themes > /dev/null
        if [ ! -d "docsy" ]; then
            git clone --recurse-submodules --depth 1 https://github.com/google/docsy.git
        else
            pushd docsy > /dev/null
            git pull --recurse-submodules --depth 1
            popd > /dev/null
        fi
        popd > /dev/null
    fi

    local config_file=$(generate_config "$CUR_DIR/../config.toml")
    CURRENT_VERSION=${CURRENT_VERSION} hugo server -w --config "$config_file"
    popd > /dev/null
}

run
