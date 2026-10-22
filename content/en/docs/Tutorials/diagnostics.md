---
title: "Platform diagnostics"
linkTitle: "Platform diagnostics"
weight: 8
description: >
  Use status, doctor, and node logs to investigate platform problems.
---

Locate the failing layer first: the platform, Agent, resource downloads, or the Kubernetes cluster.

## Platform health

```bash
kcctl version
kcctl status
kcctl status -o json
kcctl doctor
```

`status` summarizes kc-server, kc-etcd, and kc-agent health. `doctor` checks local access, services, platform etcd, and Agents, with evidence for failed checks. Unhealthy results return a nonzero exit code for scripting. Neither command repairs the environment.

If the API cannot be reached, check that `kcctl login` points to the HTTPS API endpoint, normally port 8080. Inspect local login and deployment configuration and SSH connectivity from the deployment host.

## Node services

Run on the relevant Linux node:

```bash
sudo systemctl status kc-server kc-etcd kc-agent --no-pager
sudo journalctl -u kc-server -n 100 --no-pager
sudo journalctl -u kc-agent -n 100 --no-pager
```

An Agent-only node is not expected to run a Server or platform etcd. Interpret service results according to node roles. Check disk space, clock synchronization, management addresses, and firewall rules.

## Deployment failures

Precheck errors identify the check and node. If services already exist, establish whether they belong to an active platform before changing anything. For download failures, verify the URL, certificate, file size, and archive contents. Do not hide certificate failures by disabling verification.

## Cluster task failures

```bash
kcctl operation list -c demo
kcctl get cluster demo -o yaml
kcctl get node
kcctl resource list
```

Use [operations and logs](/en/docs/tutorials/operations/) to locate the failing step and node. Check package versions and architectures for offline installation. For image pull failures, check the registry address, credentials, and connectivity. Include versions, topology, sanitized errors, and operation IDs in an issue; remove passwords, tokens, private keys, and kubeconfig credentials.
