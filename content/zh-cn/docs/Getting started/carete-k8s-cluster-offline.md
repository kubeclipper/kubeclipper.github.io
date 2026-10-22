---
title: "离线创建集群"
linkTitle: "离线创建集群"
weight: 3
description: >
  离线创建集群
---

离线安装需要先准备平台部署包，以及 Kubernetes、CRI、CNI 等组件资源。Registry 资源只描述镜像仓库，不能替代离线包。

## 检查资源

完成[平台部署](/docs/getting-started/)后登录并检查：

```bash
kcctl resource list
kcctl get node
```

确认目标节点架构与资源包一致。1.7 推荐矩阵为 Kubernetes v1.37.0 / v1.36.4 / v1.35.8、containerd 2.2.4、Calico v3.31.5。需要补充组件包时参考[准备离线组件包](/docs/getting-started/make-offline-package/)。

## 创建集群

`kcctl create cluster` 默认离线安装。示例使用一个实验节点：

```bash
kcctl create cluster --name offline-demo --master 192.168.10.21 --untaint-master \
  --k8s-version v1.37.0 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5
kcctl operation list -c offline-demo
kcctl get cluster offline-demo -o yaml
```

在 Console 创建时同样选择已准备好的组件版本、目标节点和离线方式。需要镜像仓库时先准备镜像并配置[Registry 资源](/docs/tutorials/registries/)。存储插件按实际需求单独选择，不把某一种 NFS 插件当作创建集群的必选步骤。

## 确认安装结果

结合 Operation 和节点日志定位失败原因。取得 kubeconfig 后检查节点 Ready、系统 Pod 和 API readiness。离线资源缺失、架构不一致或镜像地址不可达时，先修正资源再重试，参见[操作与日志](/docs/tutorials/operations/)。
