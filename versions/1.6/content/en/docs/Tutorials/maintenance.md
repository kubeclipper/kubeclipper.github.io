---
title: "Diagnostics and upgrade checks"
linkTitle: "Diagnostics and upgrade checks"
weight: 3
---

1.6 does not include the 1.7 `kcctl status` and `kcctl doctor` commands. Start with versions, API access, node services, and operation logs.

```bash
kcctl version
kcctl get node
kcctl get cluster
kcctl operation list
kcctl resource list
```

Inspect services according to each Linux node's role. Diagnose NATS, platform etcd, and Server failures separately.

```bash
sudo systemctl status kc-server kc-agent kc-etcd kc-nats --no-pager
sudo journalctl -u kc-server -n 100 --no-pager
sudo journalctl -u kc-agent -n 100 --no-pager
sudo journalctl -u kc-nats -n 100 --no-pager
```

Agent nodes may not run Server, etcd, or NATS. External NATS deployments have no local kc-nats service. Check actual roles and deployment configuration.

## Before upgrading to 1.7

Back up platform etcd, configuration, certificates, authentication keys, and managed-cluster data. Rehearse the upgrade in a recoverable test environment, checking the NATS to Operation v2 transition, active tasks, and old operation records. Consult the [1.7 upgrade checklist](https://kubeclipper.io/v1.7/en/docs/deployment-docs/upgrade/) and verify versions running across all components.

This page does not guarantee an in-place upgrade for every 1.6 deployment. Preserve errors and follow the recovery steps you rehearsed.
