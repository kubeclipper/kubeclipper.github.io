---
title: "1.7 发布说明"
linkTitle: "1.7 发布说明"
weight: 2
description: >
  1.7.0 适用范围、组件版本及使用入口。
---

本套文档对应 **KubeClipper v1.7.0**，发布于 2026 年 9 月 8 日。官方发布记录：[v1.7.0](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.7.0)。

## 主要变化

- Operation v2 通过 API 管理操作、任务和执行状态，Agent 与 Server 使用 mTLS 通信。
- `kcctl operation` 提供操作列表、详情、日志、重试和取消。
- `kcctl status` 与 `kcctl doctor` 提供平台状态检查和诊断。
- Registry 资源可用于选择 Kubernetes 镜像仓库和配置 containerd 镜像拉取。
- 部署预检查给出节点、角色和错误原因；Server 安装前等待平台 etcd 健康。

## 组件版本

| Kubernetes | containerd | Calico |
|---|---|---|
| v1.37.0 | 2.2.4 | v3.31.5 |
| v1.36.4 | 2.2.4 | v3.31.5 |
| v1.35.8 | 2.2.4 | v3.31.5 |

默认 Kubernetes 版本为 v1.37.0。实际可选项以平台组件资源为准；离线环境还需准备对应 CPU 架构的包。版本来源：[v1.7.0 支持矩阵](https://github.com/kubeclipper/kubeclipper/blob/v1.7.0/README_zh.md#支持的版本)。

## 版本边界

本文描述 v1.7.0 已发布能力。生产使用前查看 Release、安全公告和所用二进制版本。升级前参考[升级检查](/docs/deployment-docs/upgrade/)。

版本菜单保留 1.6～1.1 历史文档。[1.6 文档](https://kubeclipper.io/v1.6/docs/)按 v1.6.0 发布标签整理。
