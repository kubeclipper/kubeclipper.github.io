---
title: "High availability"
linkTitle: "High availability"
weight: 1
description: >
  Deploy a KubeClipper 1.7 platform with three Server nodes.
---

This guide deploys a highly available KubeClipper control plane. Platform availability and the availability of managed Kubernetes clusters require separate planning.

## Prepare nodes and networking

Prepare three Linux Server nodes and the Agent nodes you want to manage. The deployment user needs SSH access to every node with the same private key and sudo privileges. See [architecture and networking](/en/docs/overview/) for clock synchronization and ports.

Platform etcd runs on Server nodes. Plan membership and failure tolerance around etcd quorum requirements. Keep platform Servers separate from Kubernetes workload nodes in production.

## Install and download

Follow [Getting started](/en/docs/getting-started/) to install v1.7.0 kcctl and download the complete `kc-amd64.tar.gz` or `kc-arm64.tar.gz` package for your targets. GitHub Release client archives are not deployment packages for `--pkg`.

## Deploy Servers and Agents

Replace the IP addresses, private key, and package path. `--server` accepts comma-separated addresses; `--agent` can include a region.

```bash
read -r -s -p 'Set the admin password: ' KC_ADMIN_PASSWORD
printf '\n'
kcctl deploy \
  --server 192.168.10.11,192.168.10.12,192.168.10.13 \
  --agent default:192.168.10.21,192.168.10.22 \
  --user root --pk-file "$HOME/.ssh/id_rsa" \
  --pkg "$PWD/kc-amd64.tar.gz" \
  --initial-password "$KC_ADMIN_PASSWORD"
unset KC_ADMIN_PASSWORD
```

Keep TLS enabled. On hosts with multiple interfaces, select reachable addresses using `--ip-detect` and `--node-ip-detect`; consult `kcctl deploy -h`. Platform etcd ports default to 12379, 12380, and 12381.

## Verify the platform

```bash
kcctl login --host https://192.168.10.11:8080 --username admin
kcctl status
kcctl doctor
kcctl get node
```

Check services on all three Servers, platform etcd membership, and Agent health. Repeat API connectivity checks against the other Servers. Configure a load balancer and certificates separately if you need a common hostname or VIP; deploying three Servers does not provision an entry-point VIP.

Browsers use each Server's default HTTP port 80 console entry point; the CLI uses the HTTPS port 8080 API. Configure HTTPS at the production console entry point and restrict management ports to the intended networks.

## Add and remove Agents

```bash
kcctl join --agent default:192.168.10.23
kcctl get node
```

After confirming the node has no clusters or workloads to retain, remove it:

```bash
kcctl drain --agent 192.168.10.23
```

Investigate a normal drain failure before choosing further actions. Do not use force options by default. See the [upgrade checklist](/en/docs/deployment-docs/upgrade/) before changing versions.
