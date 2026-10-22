---
title: "Cluster creation troubleshooting"
linkTitle: "Cluster creation troubleshooting"
weight: 1
description: >
  Investigate resource, network, and task failures in 1.7.
---

This page applies to 1.7. Older v1.2.1 Calico download workarounds do not apply directly to this release.

## Cluster not Ready after submission

```bash
kcctl operation list -c demo
kcctl get cluster demo -o yaml
kcctl get node
```

Inspect operation details and logs next. Request acceptance, operation completion, and Kubernetes node readiness are separate checks.

## Offline package or image errors

Use `kcctl resource list` to confirm version and architecture. Inspect image paths, authentication, and connectivity using the failed step's logs. See [offline clusters](/en/docs/getting-started/carete-k8s-cluster-offline/).

## Platform or Agent errors

Run `kcctl status` and `kcctl doctor` to check API access, services, and SSH connectivity. Supply an SSH private key as deployment credentials, not a public key path.

See [platform diagnostics](/en/docs/tutorials/diagnostics/) for the investigation sequence and [operations and logs](/en/docs/tutorials/operations/) for retries and cancellation.
