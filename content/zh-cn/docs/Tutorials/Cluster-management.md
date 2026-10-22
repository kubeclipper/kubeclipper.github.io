---
title: "集群管理"
linkTitle: "集群管理"
weight: 4
description: >
  集群管理
---

KubeClipper 1.7 的集群生命周期操作由 Operation v2 执行。先查看集群对象，再用操作详情和节点实际状态确认结果。

```bash
kcctl get cluster
kcctl get cluster demo -o yaml
kcctl operation list -c demo
```

## 日志、重试和取消

完整命令见[操作与日志](/docs/tutorials/operations/)。失败后先处理根因再重试；重置集群状态不会修复失败的节点或撤销已执行操作。

## 访问集群

在 Console 的集群详情页获取 kubeconfig，设置 `KUBECONFIG` 后执行：

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get --raw='/readyz?verbose'
```

平台状态正常不代表所有受管集群都正常。升级、扩缩容、备份和恢复后，都要检查对应集群中的节点、系统 Pod 和业务数据。

## 扩缩容与镜像仓库

先用 `kcctl join` 将新增机器纳入平台，确认节点就绪、区域与目标集群一致，再在集群详情中添加节点。移除节点前迁移工作负载并检查容量；平台的 `kcctl drain` 用于移除平台 Agent，不等同于集群缩容。节点接入步骤见[节点管理](/docs/tutorials/node-management/)。

Kubernetes 镜像仓库与 containerd 拉取仓库分别配置，具体步骤见[镜像仓库](/docs/tutorials/registries/)。变更后检查实际镜像拉取结果。

## 备份与恢复

1. 配置备份空间，并在编辑集群时关联该备份空间。使用目录备份空间时，先在相关节点创建并挂载约定路径，确认可写。
2. 在集群中发起备份，或通过定时备份设置执行时间和保留数量；确认备份记录成功且文件可读取。
3. 恢复时选择该集群的备份记录，跟踪恢复 Operation，完成后检查 API、节点、系统 Pod 和业务状态。

这里的集群备份以 Kubernetes etcd 快照为核心，不包含业务持久卷中的文件；应用数据需要另行备份。恢复会改变集群状态，先在隔离环境演练，不能仅凭备份记录存在判断可恢复。

## Kubernetes 版本升级

这与 KubeClipper 平台升级是两项操作。先备份并验证恢复方案，检查目标版本的组件资源、镜像和工作负载兼容性，再从集群的升级入口选择目标版本。托管的 kubeadm 集群不提供此升级入口。

CLI 参数可用下列命令查看：

```bash
kcctl cluster upgrade --help
```

升级命令使用 `--cluster-name` 和 `--version` 指定集群与目标版本，默认采用离线方式；`--online` 改为在线方式，`--image-registry` 选择已配置的 Registry 资源。目标版本必须在平台可用资源中，不能将支持矩阵当作任意版本间升级成功的保证。提交后跟踪 Operation，并执行上面的集群健康检查。

## 删除集群

先确认工作负载和数据已备份，再发起删除并跟踪 Operation：

```bash
kcctl delete cluster demo
kcctl operation list -c demo
kcctl get cluster
```

确认删除结束后再复用节点。失败时保留日志和节点状态，参考[平台诊断](/docs/tutorials/diagnostics/)，不要用强制删除掩盖未完成的清理。
