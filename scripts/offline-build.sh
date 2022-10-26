#!/bin/bash

if [[ "$DEBUG" == "true" ]]; then
    set -ex
    export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
fi

CUR_DIR="$(dirname "${BASH_SOURCE[0]}")"

source "$CUR_DIR/function.sh"

export CURRENT_BRANCH="master"
export CURRENT_VERSION=${VERSIONS_ARRAY[0]}
export VERSIONS=${VERSIONS_STRING}
HUGO_TITLE="KubeClipper Doc - local"

pushd $(dirname "$0")/.. > /dev/null
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

npm install

config_file=$(generate_config "$CUR_DIR/../config.toml")

if [ -n "$SCOPE" ]; then
    hugo_cmd="hugo --baseURL=/docs/$SCOPE/ --destination=public/docs/$SCOPE"
else
    hugo_cmd="hugo --baseURL=/docs/ --destination=public/docs"
fi

$hugo_cmd --config "$config_file"

# api_file="public/docs/api/index.html"
# TODO: 支持离线 swagger 文档
# 重写 api, 路径指向离线文档的 swagger
# cat >$api_file <<EOF
# <head>
# <meta http-equiv="refresh" content="0; url=/docs/swagger/" />
# </head>
# EOF

if [[ "$DEBUG" == "true" ]]; then
    set +ex
    export PS4=
fi
