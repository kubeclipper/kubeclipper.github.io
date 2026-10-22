---
title: "镜像仓库"
linkTitle: "镜像仓库"
weight: 2
---

Registry 资源描述 Kubernetes 镜像源或 containerd 拉取配置。注册仓库不会自动复制镜像，离线组件包也需独立准备。

```bash
kcctl create registry --name internal --host registry.example.com:5000 --scheme http
kcctl get registry
kcctl create registry -h
kcctl registry -h
```

上例是管理网络中的 HTTP 仓库；生产环境按实际仓库配置 HTTPS、CA 和认证。1.6 还支持持久化 `kcctl registry` 的节点和 SSH 配置，后续操作前核对已有配置。

创建集群时，`--image-registry internal` 选择 Kubernetes 镜像源，`--cri-registry internal` 配置 containerd 镜像拉取。先准备镜像，再检查节点到仓库的连通性、证书和认证。参数来源：[v1.6.0 Registry CLI](https://github.com/kubeclipper/kubeclipper/blob/v1.6.0/pkg/cli/create/create_registry.go)。
