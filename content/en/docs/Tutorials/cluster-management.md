---
title: "Cluster management"
linkTitle: "Cluster management"
weight: 4
description: >
  Cluster management
---

KubeClipper 1.7 executes cluster lifecycle work through Operation v2. Inspect the cluster object, then confirm outcomes using operation details and actual nodes.

```bash
kcctl get cluster
kcctl get cluster demo -o yaml
kcctl operation list -c demo
```

## Logs, retries, and cancellation

See [operations and logs](/en/docs/tutorials/operations/) for commands. Resolve the cause of a failure before retrying. Resetting cluster state does not repair nodes or undo completed work.

## Access a cluster

Obtain kubeconfig from the Console cluster details page, set `KUBECONFIG`, and run:

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get --raw='/readyz?verbose'
```

Healthy platform status does not establish the health of every managed cluster. After upgrades, scaling, backup, or recovery, inspect the relevant nodes, system Pods, and application data.

## Scaling and registries

Use `kcctl join` to register new machines with the platform. Confirm that nodes are Ready and in the cluster's region before adding them from the cluster details page. Evacuate workloads and check remaining capacity before removing cluster nodes. Platform `kcctl drain` removes an Agent; it is a separate operation from shrinking a cluster. See [node management](/en/docs/tutorials/node-management/).

Configure Kubernetes image repositories and containerd pull registries separately. See [registries](/en/docs/tutorials/registries/) and verify actual image pulls after changes.

## Backup and restore

1. Configure a backup space and associate it with the cluster through the edit action. For directory backup spaces, create and mount the agreed path on the relevant nodes and confirm write access.
2. Start a backup, or configure a scheduled backup with its execution time and retention count. Confirm successful backup status and readable files.
3. Select a backup belonging to the cluster for restoration. Follow its Operation, then check the API, nodes, system Pods, and application state.

Cluster backups center on Kubernetes etcd snapshots. They do not include application files in persistent volumes; back up those separately. Restoration changes cluster state. Rehearse in an isolated environment: the existence of a backup record alone does not establish recoverability.

## Upgrade Kubernetes

Kubernetes upgrades are separate from KubeClipper platform upgrades. Back up the cluster, validate restoration, and check target component resources, images, and workload compatibility before selecting a target in the cluster upgrade action. This action is unavailable for hosted kubeadm clusters.

Inspect the CLI parameters with:

```bash
kcctl cluster upgrade --help
```

Use `--cluster-name` and `--version` to select the cluster and target. Offline mode is the default; `--online` selects online mode and `--image-registry` selects a configured Registry resource. The target must exist in platform resources. The support matrix does not guarantee successful upgrades between every listed version. Follow the resulting Operation and repeat the cluster health checks above.

## Delete a cluster

Back up workloads and data before deletion, then follow the Operation:

```bash
kcctl delete cluster demo
kcctl operation list -c demo
kcctl get cluster
```

Confirm deletion has finished before reusing nodes. Preserve errors and node state for [diagnostics](/en/docs/tutorials/diagnostics/); forced deletion does not establish that cleanup completed.
