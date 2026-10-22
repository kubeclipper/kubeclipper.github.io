---
title: "Getting started"
linkTitle: "Getting started"
weight: 2
description: >
  Deploy KubeClipper 1.7.0 and create your first Kubernetes cluster.
---

This guide uses **KubeClipper v1.7.0**. Deploy the platform on an SSH-accessible Linux host with systemd, then create a single-node test cluster. See [high availability](/en/docs/deployment-docs/ha-deploy/) for production topology.

## Prepare the host

- Install `curl`, `tar`, and `sudo`. Enable SSH and give the deployment user sudo privileges.
- Run chrony, ntp, or systemd-timesyncd to keep clocks synchronized.
- Prepare an SSH private key that can log in to the target host and check network connectivity.
- Check the kernel, cgroup, and runtime requirements of the Kubernetes version you select. Operating system lists from older guides do not establish compatibility with newer Kubernetes versions.
- Allow disk space for downloading and extracting packages and loading container images. The complete 1.7.0 deployment package is about 1.2 GiB. The roughly 60 MB binary archives on GitHub Release do not replace it.

## Install kcctl

Download the installer from the 1.7.0 release tag before running it. It downloads binaries from the project's native Alibaba Cloud OSS endpoint rather than the old `oss.kubeclipper.io` domain.

```bash
curl -fL -o get-kubeclipper.sh \
  https://raw.githubusercontent.com/kubeclipper/kubeclipper/v1.7.0/scripts/get-kubeclipper.sh
KC_VERSION=v1.7.0 bash get-kubeclipper.sh
kcctl version
```

The client supports Linux and macOS on amd64 and arm64. Platform services run on Linux; run the following deployment commands on a Linux deployment host. Clients are also available from the [v1.7.0 Release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.7.0).

## Download the complete deployment package

Set `ARCH` to the target architecture. Use `arm64` instead of `amd64` for ARM hosts.

```bash
ARCH=amd64
curl -fL -o "kc-${ARCH}.tar.gz" \
  "https://kubeclipper.oss-ap-southeast-1.aliyuncs.com/release/v1.7.0/kc-${ARCH}.tar.gz"
tar -tzf "kc-${ARCH}.tar.gz" | head
```

The complete package includes platform services, the console, and offline resources. Download it on a connected host and transfer it to the deployment host for an air-gapped installation. Before creating a cluster, check that resource versions and architectures are present; see [offline clusters](/en/docs/getting-started/carete-k8s-cluster-offline/).

## Deploy All-in-One

Replace the private key path below. SSH access to the target is required even when the target is the deployment host itself.

```bash
read -r -s -p 'Set the admin password: ' KC_ADMIN_PASSWORD
printf '\n'
kcctl deploy --user root --pk-file "$HOME/.ssh/id_rsa" \
  --pkg "$PWD/kc-${ARCH}.tar.gz" \
  --initial-password "$KC_ADMIN_PASSWORD"
unset KC_ADMIN_PASSWORD
```

The initial password must be 8–16 characters and include uppercase letters, lowercase letters, and digits. If prechecks fail, resolve the reported node and check before retrying.

Agents in 1.7 access the Server API over mTLS. Keep TLS enabled during deployment. The default console endpoint is `http://SERVER_IP:80`; the Server API is `https://SERVER_IP:8080`. They serve different purposes.

## Log in and check the platform

Replace `SERVER_IP` with your Server address. Login prompts for the admin password you set above.

```bash
SERVER_IP=192.168.10.10
kcctl login --host "https://${SERVER_IP}:8080" --username admin
kcctl status
kcctl doctor
kcctl get node
kcctl resource list
```

Open `http://SERVER_IP` for the console. Configure HTTPS at the console entry point in production. `status` reports platform health and `doctor` provides diagnostic evidence; neither repairs the environment.

## Create a cluster

Choose a Ready node from `kcctl get node` and set `NODE` to its ID or IP. Offline installation is the default; first confirm that matching resource packages are available.

```bash
NODE=192.168.10.10
kcctl create cluster --name demo --master "$NODE" --untaint-master \
  --k8s-version v1.37.0 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5
kcctl operation list -c demo
kcctl get cluster demo -o yaml
```

`--untaint-master` lets this test cluster schedule regular workloads on the control-plane node. Installation time depends on hardware, connectivity, and image availability. Successful submission is followed by an asynchronous Operation; inspect its result and the cluster state.

Obtain the cluster kubeconfig from the console, set `KUBECONFIG`, then check Kubernetes:

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get --raw='/readyz?verbose'
```

Confirm Running cluster state, Ready nodes, system Pod health, and API readiness. See [operations and logs](/en/docs/tutorials/operations/) and [platform diagnostics](/en/docs/tutorials/diagnostics/) when a task fails.

## Remove the test cluster

This deletes the demo cluster. Confirm that no workloads or data must be retained before running it:

```bash
kcctl delete cluster demo
kcctl operation list -c demo
kcctl get cluster
```

Wait for deletion to finish and confirm the cluster is gone. Investigate failures before considering state resets or forced deletion.
