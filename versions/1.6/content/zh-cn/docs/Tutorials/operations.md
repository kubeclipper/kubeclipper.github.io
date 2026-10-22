---
title: "操作与日志"
linkTitle: "操作与日志"
weight: 1
---

1.6 的 Operation 通过旧版任务模型和 NATS 执行。查询当前操作，复制实际 ID 查看详情和日志：

```bash
kcctl operation list
kcctl operation list -c demo
OPERATION_ID='<实际操作 ID>'
kcctl operation describe "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID" --follow
kcctl operation logs "$OPERATION_ID" --summary
```

在交互式终端中，按集群进入 TUI：

```bash
kcctl operation logs --cluster demo
```

保留失败节点和步骤的日志，处理原因后再重试。1.6 的 retry 只接受 failed 状态：

```bash
kcctl operation retry "$OPERATION_ID"
```

终止 running 状态的操作使用 `terminate`，不是 1.7 的 `cancel`：

```bash
kcctl operation terminate "$OPERATION_ID"
kcctl operation describe "$OPERATION_ID"
```

终止请求不代表节点变更已回滚。检查任务、集群和实际节点状态后再清理。命令来源：[v1.6.0 Operation CLI](https://github.com/kubeclipper/kubeclipper/tree/v1.6.0/pkg/cli/operation)。
