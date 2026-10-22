---
title: "集群创建排障"
linkTitle: "集群创建排障"
weight: 1
description: >
  排查 1.7 集群创建中的资源、网络和任务错误。
---

本页适用于 1.7。旧版 v1.2.1 的 Calico 下载问题及临时处理方法保留在[1.2 历史文档](https://kubeclipper.io/v1.2/docs/faq/kcctl-create-cluster-error/)，不应直接应用于 1.7。

## 提交后集群没有就绪

```bash
kcctl operation list -c demo
kcctl get cluster demo -o yaml
kcctl get node
```

继续查看 Operation 详情和日志。请求已接受、Operation 已结束和 Kubernetes 节点就绪需要分别确认。

## 离线包或镜像错误

用 `kcctl resource list` 核对版本和架构；通过失败步骤日志确认镜像路径、认证和网络。参考[离线创建集群](/docs/getting-started/carete-k8s-cluster-offline/)。

## 平台或 Agent 异常

运行 `kcctl status`、`kcctl doctor`，检查 API 入口、服务和 SSH 访问。平台使用的 SSH 凭据应为私钥；不要把公钥路径填入私钥字段。

排查顺序和日志命令见[平台诊断](/docs/tutorials/diagnostics/)；重试和取消见[操作与日志](/docs/tutorials/operations/)。
