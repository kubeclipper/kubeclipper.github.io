---
title: "Overview"
linkTitle: "Overview"
weight: 1
description: >
  Components and networking in KubeClipper 1.7.
---

KubeClipper manages the Kubernetes cluster lifecycle, including creation, scaling, upgrades, backup, recovery, and deletion, through a web console, API, and the kcctl CLI.

## Architecture in 1.7

![KubeClipper Operation v2 architecture](/images/docs-overview/operation-v2.svg)

- **kc-server** serves the API and persists clusters, Operations, and Tasks. Controllers advance their state.
- **kc-agent** runs on managed nodes. It accesses the Server API over mTLS, watches assigned tasks, executes them, and reports results.
- **kcctl / Console** submit management requests and display platform health, progress, and logs.
- **etcd** stores platform resources and state. Plan platform etcd separately from the etcd clusters used by managed Kubernetes clusters.

1.7 uses API-driven Operation v2 rather than built-in NATS task delivery. Operations run asynchronously. Confirm results using Operations, cluster state, and the actual nodes. See [operations and logs](/en/docs/tutorials/operations/).

## Networking

| Purpose | Default port | Clients |
|---|---|---|
| Console | TCP 80 | Browsers; configure HTTPS at the production entry point |
| Server API | TCP 8080, HTTPS | kcctl, Console, Agents |
| Resource file service | TCP 8081 | Nodes downloading resources |
| Platform etcd | TCP 12379 / 12380 / 12381 | client / peer / metrics; restrict to the management network |
| Agent task logs | TCP 10260 | Server to Agent; restrict access for the actual configuration |
| SSH | TCP 22 | Deployment and node maintenance |

Deployment configuration can change these ports. Check Agent task-log listener configuration against firewall rules as well; older NATS port lists do not apply.

`--ip-detect` selects the platform management address. `--node-ip-detect` selects the Kubernetes node address. Check connectivity explicitly on hosts with multiple interfaces. Pod network address detection belongs to the selected CNI configuration.

## Start here

- [1.7 release notes and component matrix](/en/docs/overview/release-1.7/)
- [Getting started](/en/docs/getting-started/)
- [High availability](/en/docs/deployment-docs/ha-deploy/)
- [Platform diagnostics](/en/docs/tutorials/diagnostics/)
