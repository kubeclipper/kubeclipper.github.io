---
title: "Upgrade checklist"
linkTitle: "Upgrade checklist"
weight: 2
description: >
  Checks before and after upgrading the KubeClipper platform.
---

Platform upgrades and managed Kubernetes upgrades are separate procedures. This page covers platform checks; it does not promise a direct upgrade from every older release to 1.7.

## Before upgrading

1. Record Server, Agent, kcctl, and Console versions and node topology. Confirm package architecture.
2. Review release notes, security advisories, and configuration changes. 1.7 introduces Operation v2; inspect old operation records and task state in a test environment.
3. Choose a window with no running installation, upgrade, or backup operations. Resolve unfinished work first.
4. Back up platform etcd, Server and Agent configuration, certificates, and persistent authentication keys. Verify recovery. Back up managed-cluster data separately.
5. Rehearse the target upgrade path in a recoverable test environment and record interruption and recovery steps.

```bash
kcctl version
kcctl status
kcctl doctor
kcctl operation list
kcctl upgrade -h
```

## Upgrade

`kcctl upgrade` supports platform and component upgrades. Use a package with the structure described in command help that you have validated in a test environment. Client archives are not platform upgrade packages.

```bash
UPGRADE_PACKAGE=/path/to/validated-upgrade-package.tar.gz
kcctl upgrade all --pkg "$UPGRADE_PACKAGE"
```

Use online upgrades or individual component replacement only when the release or your validated deployment procedure supports them. Replacing one binary does not establish that the whole platform upgrade succeeded.

## After upgrading

Repeat `kcctl status` and `kcctl doctor` and verify versions running on every node. Check login, node data, operation details and logs, managed-cluster access, and basic Console flows. Exercise a controlled lifecycle operation and compare the Operation result with actual cluster state.

Preserve errors and logs on failure and follow the recovery procedure tested beforehand. Check data and configuration compatibility before restoring old binaries; do not repeatedly overwrite services in an unknown state.
