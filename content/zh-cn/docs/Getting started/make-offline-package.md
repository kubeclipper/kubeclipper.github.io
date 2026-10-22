---
title: "准备离线组件包"
linkTitle: "准备离线组件包"
weight: 4
description: >
  为 1.7 准备并上传 Kubernetes、containerd 和 Calico 资源。
---

1.7.0 的完整部署包和额外的 Kubernetes / CRI / CNI 组件包用途不同。先使用[快速开始](/docs/getting-started/)中的完整部署包部署平台，再按实际需求补充组件资源。

## 选择版本和架构

以 [1.7 版本说明](/docs/overview/release-1.7/)中的矩阵为准。以下示例下载 Kubernetes v1.37.0 的 amd64 组件；arm64 节点需准备 arm64 包，不要混用架构。

## 在联网机器下载并打包

以下命令在 Bash 中执行，使用项目 OSS 原生域名。`curl -fL` 会在下载失败时退出；不要忽略证书或 HTTP 错误后继续打包。

```bash
set -e
ARCH=amd64
VERSION=v1.37.0
PKG_DIR="$(mktemp -d)"
COMPONENT_DIR="k8s/${VERSION}/${ARCH}"
mkdir -p "${PKG_DIR}/${COMPONENT_DIR}"
for FILE in manifest.json configs.tar.gz images.tar.gz; do
  curl -fL -o "${PKG_DIR}/${COMPONENT_DIR}/${FILE}" \
    "https://kubeclipper.oss-ap-southeast-1.aliyuncs.com/packages/${COMPONENT_DIR}/${FILE}"
done
tar -czf "k8s-${VERSION}-${ARCH}.tar.gz" -C "$PKG_DIR" k8s
tar -tzf "k8s-${VERSION}-${ARCH}.tar.gz"
```

归档中需保留 `k8s/版本/架构/` 层级，不能只压缩文件本身。下载目录保留在 `$PKG_DIR`，核对后可自行清理。

其他组件使用相同层级，按下表准备文件，再压缩对应组件目录：

| 组件目录 | 版本 | 必需文件 | 上传类型 |
| --- | --- | --- | --- |
| k8s | v1.37.0 | manifest.json、configs.tar.gz、images.tar.gz | k8s |
| containerd | 2.2.4 | manifest.json、configs.tar.gz | cri |
| calico | v3.31.5 | manifest.json、images.tar.gz、charts.tgz | cni |

例如 Calico 路径为 `packages/calico/v3.31.5/amd64/manifest.json`。这些是已有组件资源的打包方式，不代表任意自定义版本都已被平台支持。

## 传入离线环境并上传

把归档传到能访问平台的部署机。该机器需保留部署配置和可登录 Server 的 SSH 凭据。

```bash
kcctl resource push --pkg k8s-v1.37.0-amd64.tar.gz --type k8s
kcctl resource list
```

上传 containerd 和 Calico 时分别使用 `--type cri`、`--type cni`。确认平台能列出匹配的版本和架构，再按[离线创建集群](/docs/getting-started/carete-k8s-cluster-offline/)验证。镜像仓库的配置参见 [Registry](/docs/tutorials/registries/)。
