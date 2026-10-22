---
title: "操作与日志"
linkTitle: "操作与日志"
weight: 7
description: >
  查看 Operation v2 进度、定位失败任务并重试或取消。
---

KubeClipper 1.7 将安装、升级、备份、删除等工作建模为 Operation，并按步骤和节点执行 Task。提交命令成功只表示请求已被接受，最终结果需要继续查询。

## 查找操作

```bash
kcctl operation list
kcctl operation list -c demo
```

从列表复制实际操作 ID 后查看详情和日志：

```bash
OPERATION_ID='<实际操作 ID>'
kcctl operation describe "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID" --follow
```

通过日志定位失败步骤和节点。在交互式终端中，可按集群打开 TUI 日志视图：

```bash
kcctl operation logs --cluster demo
```

脚本和非交互终端使用带操作 ID 的纯文本日志命令。

## 处理失败

先保留操作详情、失败节点日志和集群状态，处理包缺失、镜像下载、节点网络或服务异常等原因，再重试：

```bash
kcctl operation retry "$OPERATION_ID"
kcctl operation describe "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID" --follow
```

重试后再次检查实际集群和节点，不能只看 retry 命令返回值。若参数本身错误，先核对任务配置，不要用反复重试代替修正。

## 取消操作

```bash
kcctl operation cancel "$OPERATION_ID"
kcctl operation describe "$OPERATION_ID"
```

取消不等于回滚已经执行的安装或数据操作。继续确认任务是否停止，以及节点上已经产生的变更；清理前先确定资源归属。

## 确认成功

结合 Operation 结果、`kcctl get cluster demo -o yaml`、Kubernetes 节点与 Pod 状态确认结果。集群删除后还要检查平台列表和节点残留。平台问题参考[诊断指南](/docs/tutorials/diagnostics/)。
