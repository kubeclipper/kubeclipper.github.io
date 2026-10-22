---
title: "Features"
linkTitle: "Features"
weight: 2
description: >
  KubeClipper 1.7 capabilities.
---

## Cluster lifecycle

Create, delete, upgrade, back up, and restore Kubernetes clusters. Manage cluster nodes and import existing clusters. Online and offline installation support amd64 and arm64 resources; use the [1.7 component matrix](/en/docs/overview/release-1.7/) when selecting versions.

## Operations and troubleshooting

Operation v2 records asynchronous cluster changes. Inspect execution state and logs, then retry or cancel when appropriate. [Operation commands](/en/docs/tutorials/operations/) and [platform diagnostics](/en/docs/tutorials/diagnostics/) help locate failures.

## Image and resource management

[Registry resources](/en/docs/tutorials/registries/) configure image sources and containerd pull settings. [Offline packages](/en/docs/getting-started/make-offline-package/) provide component resources separately.

## Platform and access

Deploy a single-node lab or a [high-availability platform](/en/docs/deployment-docs/ha-deploy/). Agents use mTLS to access the Server API. RBAC provides user permissions; see [access control](/en/docs/tutorials/access-control/).
