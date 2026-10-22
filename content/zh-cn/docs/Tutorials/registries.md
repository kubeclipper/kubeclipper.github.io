---
title: "镜像仓库"
linkTitle: "镜像仓库"
weight: 9
description: >
  在 1.7 中创建 Registry 资源并选择镜像来源。
---

Registry 资源用于描述 Kubernetes 镜像仓库或给 containerd 添加镜像拉取配置。它与平台离线资源包不是同一种对象，创建 Registry 也不会自动把镜像同步到仓库。

## 创建 Registry 资源

以下是管理网络中 HTTP 镜像仓库的例子。生产仓库应按实际情况配置 HTTPS、CA 和认证；完整参数见命令帮助。

```bash
kcctl create registry --name internal --host registry.example.com:5000 --scheme http
kcctl get registry
kcctl create registry -h
```

需要认证时可通过 `--auth-username` 和 `--auth-password` 配置，注意命令历史和终端日志中的凭据暴露。使用 HTTPS 时核对 `--ca` 与 `--skip-tls-verify`，不要直接沿用 HTTP 示例配置。

## 为集群选择仓库

```bash
kcctl create cluster --name demo --master 192.168.10.21 \
  --k8s-version v1.37.0 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5 \
  --image-registry internal --cri-registry internal
```

- `--image-registry` 选择用于 Kubernetes 镜像的 Registry 资源。
- `--cri-registry` 将 Registry 资源的配置加入 containerd；可按需要指定多个资源。
- 未指定镜像仓库时，各组件采用各自的默认值和适用的 Agent 镜像源配置。不要假定 Kubernetes、Calico 等组件都从同一个默认仓库拉取。

创建前把所需镜像放入仓库，并检查集群节点实际可访问的镜像路径、认证和证书。离线安装还要满足[资源包要求](/docs/getting-started/carete-k8s-cluster-offline/)。
