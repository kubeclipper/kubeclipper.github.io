---
title: "Offline clusters"
linkTitle: "Offline clusters"
weight: 3
description: >
  Offline clusters
---

Offline installation needs a platform deployment package and component resources for Kubernetes, the CRI, and the CNI. Registry resources describe image repositories; they do not replace offline packages.

## Check resources

After [deploying the platform](/en/docs/getting-started/), log in and inspect resources and nodes:

```bash
kcctl resource list
kcctl get node
```

Match package architecture to the target nodes. The 1.7 matrix uses Kubernetes v1.37.0 / v1.36.4 / v1.35.8, containerd 2.2.4, and Calico v3.31.5. See [offline component packages](/en/docs/getting-started/make-offline-package/) when more resources are needed.

## Create the cluster

`kcctl create cluster` defaults to offline installation. This example uses one test node:

```bash
kcctl create cluster --name offline-demo --master 192.168.10.21 --untaint-master \
  --k8s-version v1.37.0 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5
kcctl operation list -c offline-demo
kcctl get cluster offline-demo -o yaml
```

In the Console wizard, select prepared component versions, target nodes, and offline installation. Populate any image repository and configure its [Registry resource](/en/docs/tutorials/registries/) first. Select storage plugins according to actual requirements; a particular NFS plugin is not a mandatory cluster-creation step.

## Confirm installation

Use Operations and node logs to locate failures. After obtaining kubeconfig, check Ready nodes, system Pods, and API readiness. Resolve missing resources, architecture mismatches, and unreachable image paths before retrying. See [operations and logs](/en/docs/tutorials/operations/).
