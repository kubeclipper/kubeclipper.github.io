---
title: "1.6 release guide"
linkTitle: "1.6 release guide"
weight: 1
---

KubeClipper **v1.6.0** was released on **June 2, 2026** as a stable release. [Release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.6.0) · [Full changelog](https://github.com/kubeclipper/kubeclipper/compare/v1.5.0...v1.6.0).

## Included changes

- containerd 2 and Calico v3.31.5 support, with an updated Kubernetes matrix.
- Improved Operation commands and logs, including a cluster-wide TUI.
- `kcctl set cluster` for external cluster access configuration.
- Persistent registry configuration and fixes that preserve existing containerd configuration when updating registry authentication.

## Component matrix

| Kubernetes | containerd | Calico |
| --- | --- | --- |
| v1.36.1 (default) | 2.2.4 | v3.31.5 |
| v1.35.0 | 1.7.29 | v3.29.6 |
| v1.34.2 | 1.7.29 | v3.29.6 |

Source: [v1.6.0 README](https://github.com/kubeclipper/kubeclipper/blob/v1.6.0/README.md#supported-versions). Available resources also depend on the uploaded versions and architecture.

## Architecture and default ports

1.6 consists of kc-server, kc-agent, kcctl, Console, and platform etcd. It distributes tasks using built-in or external **NATS**. This differs from the API-driven Operation v2 architecture in 1.7.

| Purpose | Default port |
| --- | --- |
| Console | HTTP 80 |
| Server API | HTTPS 8080 |
| Resource service | 8081 |
| NATS client / cluster | 9889 / 9890, TLS enabled by default |
| Platform etcd client / peer / metrics | 12379 / 12380 / 12381 |
| SSH deployment | 22 |

Restrict management access and check your actual deployment configuration. Sources: [v1.6.0 deployment options](https://github.com/kubeclipper/kubeclipper/blob/v1.6.0/cmd/kcctl/app/options/options.go).

## Command differences from 1.7

- 1.6 uses `kcctl operation terminate`; 1.7 uses `cancel`.
- 1.6 does not provide `kcctl status` or `kcctl doctor`; inspect node services and logs instead.
- Use the 1.6 matrix, NATS configuration, and task model with 1.6 binaries.
