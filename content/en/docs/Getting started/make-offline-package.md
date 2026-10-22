---
title: "Offline component packages"
linkTitle: "Offline component packages"
weight: 4
description: >
  Prepare and upload component resources for 1.7.
---

The full 1.7.0 deployment package installs the platform. Additional Kubernetes, CRI, and CNI packages provide cluster resources. Deploy the platform using [Getting started](/en/docs/getting-started/) first.

## Choose versions and architecture

Use the [1.7 matrix](/en/docs/overview/release-1.7/). This Bash example prepares Kubernetes v1.37.0 for amd64. Prepare arm64 packages for arm64 nodes.

```bash
set -e
ARCH=amd64
VERSION=v1.37.0
PKG_DIR="$(mktemp -d)"
COMPONENT_DIR="k8s/${VERSION}/${ARCH}"
mkdir -p "${PKG_DIR}/${COMPONENT_DIR}"
for FILE in manifest.json configs.tar.gz images.tar.gz; do
  curl -fL -o "${PKG_DIR}/${COMPONENT_DIR}/${FILE}" \
    "https://kubeclipper.oss-ap-southeast-1.aliyuncs.com/packages/${COMPONENT_DIR}/${FILE}"
done
tar -czf "k8s-${VERSION}-${ARCH}.tar.gz" -C "$PKG_DIR" k8s
tar -tzf "k8s-${VERSION}-${ARCH}.tar.gz"
```

Preserve the `k8s/version/architecture/` hierarchy. Keep certificate and HTTP verification enabled. The download directory remains at `$PKG_DIR` for inspection and subsequent cleanup.

Other components use the same hierarchy. Archive the component directory with the following files:

| Directory | Version | Required files | Upload type |
| --- | --- | --- | --- |
| k8s | v1.37.0 | manifest.json, configs.tar.gz, images.tar.gz | k8s |
| containerd | 2.2.4 | manifest.json, configs.tar.gz | cri |
| calico | v3.31.5 | manifest.json, images.tar.gz, charts.tgz | cni |

For example, Calico uses `packages/calico/v3.31.5/amd64/manifest.json`. Packaging existing resources does not imply support for arbitrary custom versions.

## Upload in the offline environment

Transfer the archive to a deployment machine that can reach the platform and has the deployment configuration and Server SSH credentials.

```bash
kcctl resource push --pkg k8s-v1.37.0-amd64.tar.gz --type k8s
kcctl resource list
```

Use `--type cri` for containerd and `--type cni` for Calico. Confirm the versions and architecture in the resource list before [creating an offline cluster](/en/docs/getting-started/carete-k8s-cluster-offline/). See [Registry configuration](/en/docs/tutorials/registries/) for image registry settings.
