---
title: "1.7 release notes"
linkTitle: "1.7 release notes"
weight: 2
description: >
  Release scope, components, and entry points for 1.7.0.
---

This documentation targets **KubeClipper v1.7.0**, released on September 8, 2026. See the official [v1.7.0 release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.7.0).

## Main changes

- API-driven Operation v2 manages operations, tasks, and execution state. Agents communicate with Servers over mTLS.
- `kcctl operation` provides lists, details, logs, retries, and cancellation.
- `kcctl status` and `kcctl doctor` report platform health and diagnostic evidence.
- Registry resources select Kubernetes image repositories and configure containerd image pulls.
- Deployment prechecks identify the node, role, and underlying error. Server installation waits for platform etcd health.

## Component versions

| Kubernetes | containerd | Calico |
|---|---|---|
| v1.37.0 | 2.2.4 | v3.31.5 |
| v1.36.4 | 2.2.4 | v3.31.5 |
| v1.35.8 | 2.2.4 | v3.31.5 |

Kubernetes v1.37.0 is the default. Available selections depend on platform resources; offline installations also need packages for the target CPU architecture. Source: [v1.7.0 support matrix](https://github.com/kubeclipper/kubeclipper/blob/v1.7.0/README.md).

## Release scope

This documentation describes v1.7.0. Review release notes, security advisories, and binary versions before production use. See the [upgrade checklist](/en/docs/deployment-docs/upgrade/).

The version menu preserves documentation for 1.6 through 1.1. The [1.6 documentation](https://kubeclipper.io/v1.6/en/docs/) follows the v1.6.0 release tag.
