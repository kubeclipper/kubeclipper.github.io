---
title: "Operations and logs"
linkTitle: "Operations and logs"
weight: 1
---

1.6 Operations use the older task model and NATS. List operations, then copy the actual ID to inspect details and logs:

```bash
kcctl operation list
kcctl operation list -c demo
OPERATION_ID='<actual operation ID>'
kcctl operation describe "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID" --follow
kcctl operation logs "$OPERATION_ID" --summary
```

Open the cluster-wide TUI in an interactive terminal:

```bash
kcctl operation logs --cluster demo
```

Preserve failed-step and node logs and resolve the cause before retrying. 1.6 only retries operations in failed status:

```bash
kcctl operation retry "$OPERATION_ID"
```

Use `terminate` for running operations, rather than the 1.7 `cancel` command:

```bash
kcctl operation terminate "$OPERATION_ID"
kcctl operation describe "$OPERATION_ID"
```

A termination request does not roll back node changes. Inspect task, cluster, and node state before cleanup. Source: [v1.6.0 Operation CLI](https://github.com/kubeclipper/kubeclipper/tree/v1.6.0/pkg/cli/operation).
