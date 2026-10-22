---
title: "1.6 发布说明"
linkTitle: "1.6 发布说明"
weight: 1
---

KubeClipper **v1.6.0** 于 **2026 年 6 月 2 日**正式发布。[Release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.6.0) · [完整变更](https://github.com/kubeclipper/kubeclipper/compare/v1.5.0...v1.6.0)。

## 发布内容

- containerd 2 和 Calico v3.31.5 支持，更新 Kubernetes 组件矩阵。
- Operation 命令和日志查看改进，包括按集群打开 TUI。
- `kcctl set cluster` 可配置集群外部访问。
- 镜像仓库配置持久化，以及更新 registry 认证时保留现有 containerd 配置等修复。

## 组件矩阵

| Kubernetes | containerd | Calico |
| --- | --- | --- |
| v1.36.1（默认） | 2.2.4 | v3.31.5 |
| v1.35.0 | 1.7.29 | v3.29.6 |
| v1.34.2 | 1.7.29 | v3.29.6 |

来源：[v1.6.0 README](https://github.com/kubeclipper/kubeclipper/blob/v1.6.0/README.md#supported-versions)。可用资源还取决于平台中已上传的版本和架构。

## 架构与默认端口

1.6 由 kc-server、kc-agent、kcctl、Console 及平台 etcd 组成，使用内置或外部 **NATS** 分发任务。它与 1.7 的 API 驱动 Operation v2 架构不同。

| 用途 | 默认端口 |
| --- | --- |
| Console | HTTP 80 |
| Server API | HTTPS 8080 |
| 资源服务 | 8081 |
| NATS 客户端 / 集群 | 9889 / 9890，默认启用 TLS |
| 平台 etcd client / peer / metrics | 12379 / 12380 / 12381 |
| SSH 部署 | 22 |

限制管理端口访问，并按部署配置核对实际端口。默认值来源：[v1.6.0 部署选项](https://github.com/kubeclipper/kubeclipper/blob/v1.6.0/cmd/kcctl/app/options/options.go)。

## 与 1.7 的命令差异

- 1.6 终止操作使用 `kcctl operation terminate`；1.7 使用 `cancel`。
- 1.6 不提供 1.7 的 `kcctl status`、`kcctl doctor`，使用节点服务和日志排查。
- 1.6 文档中的组件矩阵、NATS 配置和任务模型应与 1.6 二进制配套使用。
