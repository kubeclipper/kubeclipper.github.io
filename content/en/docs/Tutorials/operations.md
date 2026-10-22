---
title: "Operations and logs"
linkTitle: "Operations and logs"
weight: 7
description: >
  Inspect Operation v2 progress and logs, retry failures, and cancel work.
---

KubeClipper 1.7 represents installation, upgrades, backup, and deletion as Operations, with Tasks assigned by step and node. A successful submission means the request was accepted; query its result afterward.

## Find an operation

```bash
kcctl operation list
kcctl operation list -c demo
```

Copy an actual operation ID from the list, then inspect details and logs:

```bash
OPERATION_ID='<actual operation ID>'
kcctl operation describe "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID" --follow
```

Use logs to identify the failed step and node. In an interactive terminal, open the cluster's TUI log viewer:

```bash
kcctl operation logs --cluster demo
```

Use the operation-ID commands for plain-text logs in scripts and non-interactive terminals.

## Handle a failure

Preserve operation details, failed-node logs, and cluster state. Resolve the missing package, image download, node connectivity, or service problem before retrying:

```bash
kcctl operation retry "$OPERATION_ID"
kcctl operation describe "$OPERATION_ID"
kcctl operation logs "$OPERATION_ID" --follow
```

Check actual cluster and node state after the retry. Its command return value alone does not establish recovery. If parameters are wrong, review the task configuration rather than retrying repeatedly.

## Cancel work

```bash
kcctl operation cancel "$OPERATION_ID"
kcctl operation describe "$OPERATION_ID"
```

Cancellation does not roll back installation or data changes that have already happened. Confirm tasks have stopped and inspect existing changes on the nodes before cleanup.

## Confirm the result

Check the Operation result, `kcctl get cluster demo -o yaml`, Kubernetes nodes, and system Pods together. After cluster deletion, check the platform list and node residue. See [platform diagnostics](/en/docs/tutorials/diagnostics/) for platform-level issues.
