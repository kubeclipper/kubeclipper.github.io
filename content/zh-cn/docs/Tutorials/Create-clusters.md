---
title: "创建集群"
linkTitle: "创建集群"
weight: 1
description: >
  使用 1.7 创建 Kubernetes 集群。
---

创建集群前，确认 KubeClipper 平台可用、节点已注册并就绪、组件资源的版本和架构匹配。建议先完成[快速开始](/docs/getting-started/)，验证一条完整的部署路径。

## 控制台创建

登录控制台，在集群页面创建集群。填写名称，选择控制节点、工作节点及组件版本，再按实际网络规划设置 Pod / Service CIDR。生产集群需提前规划控制平面高可用、API 访问地址和存储；单节点实验配置不能直接用于生产。

1.7 的推荐组件组合参见[版本说明](/docs/overview/release-1.7/)。资源不在平台中时先[上传组件包](/docs/getting-started/make-offline-package/)。私有仓库相关字段参见 [Registry](/docs/tutorials/registries/)；镜像仓库和组件包是两种独立资源。

## CLI 创建与验证

[离线创建集群](/docs/getting-started/carete-k8s-cluster-offline/)提供带明确版本的 CLI 示例。创建请求提交后，在[Operation](/docs/tutorials/operations/)中查看执行结果，并检查集群状态、节点 Ready、系统 Pod 和 Kubernetes API 健康状态。失败时先保留日志并排查，不要通过重置状态跳过失败步骤。
