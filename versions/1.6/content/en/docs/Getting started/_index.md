---
title: "Getting started"
linkTitle: "Getting started"
weight: 2
---

Run this example in Bash on a **Linux amd64** deployment machine, using v1.6.0 binaries and the full deployment package. Prepare Linux nodes with systemd, SSH access, sudo permissions, and synchronized clocks. Check Kubernetes kernel, cgroup, and disk requirements.

## Install the client

The old installer at the 1.6 tag uses `oss.kubeclipper.io`, whose certificate has expired. Download directly from GitHub Release while keeping certificate verification enabled.

```bash
curl -fL -o kc-linux-amd64-v1.6.0.tar.gz \
  https://github.com/kubeclipper/kubeclipper/releases/download/v1.6.0/kc-linux-amd64.tar.gz
mkdir -p kc-client-v1.6.0
tar -xzf kc-linux-amd64-v1.6.0.tar.gz -C kc-client-v1.6.0
sudo install -m 0755 kc-client-v1.6.0/kcctl /usr/local/bin/kcctl
kcctl version
```

Select other client architectures from the [1.6 Release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.6.0). arm64 archives contain an architecture subdirectory; inspect paths with `tar -tzf` before installing.

## Download the full package and deploy

The client archive is not the deployment package. Use the native OSS endpoint below. Full packages are available for amd64 and arm64.

```bash
curl -fL -o kc-amd64-v1.6.0.tar.gz \
  https://kubeclipper.oss-ap-southeast-1.aliyuncs.com/release/v1.6.0/kc-amd64.tar.gz
read -r -s -p 'Set admin password: ' KC_ADMIN_PASSWORD
printf '\n'
kcctl deploy --user root --pk-file "$HOME/.ssh/id_rsa" \
  --pkg "$PWD/kc-amd64-v1.6.0.tar.gz" \
  --initial-password "$KC_ADMIN_PASSWORD"
unset KC_ADMIN_PASSWORD
```

Use an SSH private key that can access the nodes. The password must contain 8–16 characters, including uppercase and lowercase letters and digits. Consult `kcctl deploy -h` for multi-node options. Keep API and NATS TLS enabled.

## Log in and create a cluster

Replace Server and node addresses. Login prompts for the admin password. The Console uses `http://SERVER_IP`; the CLI uses the HTTPS API.

```bash
SERVER_IP=192.168.10.10
kcctl login --host "https://${SERVER_IP}:8080" --username admin
kcctl get node
kcctl resource list
```

Confirm resource versions and architecture before creating a single-node lab cluster:

```bash
NODE=192.168.10.10
kcctl create cluster --name demo --master "$NODE" --untaint-master \
  --k8s-version v1.36.1 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5
kcctl operation list -c demo
kcctl get cluster demo -o yaml
```

Obtain kubeconfig from cluster details. Verify `kubectl get nodes -o wide`, `kubectl get pods -A`, and `kubectl get --raw='/readyz?verbose'`. See [operations and logs](/en/docs/tutorials/operations/) for troubleshooting.
