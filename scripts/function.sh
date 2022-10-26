#!/bin/bash

generate_config() {
    case "$OSTYPE" in
        linux*)
            sedi='sed -i' ;;
        darwin*)
            sedi='sed -i ""' ;;
        *) ;;
    esac

    local origin_config=$1

    local config_dir="$(dirname $origin_config)"
    local temp_config="/tmp/kubeclipper.toml"
    cat "$origin_config" > "$temp_config"

    if [ -n "$CONTENT_DIR" ]; then
        $sedi "s|contentDir = \"content/zh-cn\"|contentDir= \"$CONTENT_DIR/zh-cn\"|g" "$temp_config"
        $sedi "s|contentDir = \"content/en\"|contentDir= \"$CONTENT_DIR/en\"|g" "$temp_config"
    fi

    echo "$temp_config"
}
