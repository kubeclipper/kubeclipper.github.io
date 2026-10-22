---
title: "Create clusters"
linkTitle: "Create clusters"
weight: 1
description: >
  Create Kubernetes clusters with 1.7.
---

Before creating a cluster, confirm the platform is healthy, nodes are registered and ready, and resource versions match node architecture. Complete [Getting started](/en/docs/getting-started/) to validate the deployment path.

## Create in the Console

Create a cluster from the cluster page. Set a name, control-plane and worker nodes, component versions, and Pod / Service CIDRs that fit your network. Plan control-plane availability, API access, and storage for production deployments; a single-node lab configuration is insufficient.

Use the [1.7 component matrix](/en/docs/overview/release-1.7/). [Upload missing resources](/en/docs/getting-started/make-offline-package/) first. See [Registry](/en/docs/tutorials/registries/) for private image settings; image registries and component packages serve different purposes.

## CLI and verification

[Offline cluster creation](/en/docs/getting-started/carete-k8s-cluster-offline/) includes a CLI example with explicit versions. After submitting the request, inspect the [Operation](/en/docs/tutorials/operations/) and confirm cluster state, Ready nodes, system Pods, and Kubernetes API health. Preserve logs when troubleshooting; resetting state does not resolve failed installation steps.
