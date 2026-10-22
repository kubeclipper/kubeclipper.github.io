---
title: "Image registries"
linkTitle: "Image registries"
weight: 9
description: >
  Create Registry resources and select image sources in 1.7.
---

A Registry resource describes a Kubernetes image source or adds image-pull configuration to containerd. It is separate from platform offline resource packages. Creating a Registry does not copy images into it.

## Create a Registry

The following example describes an HTTP registry on a management network. Configure HTTPS, CA trust, and authentication for your actual registry; consult command help for all flags.

```bash
kcctl create registry --name internal --host registry.example.com:5000 --scheme http
kcctl get registry
kcctl create registry -h
```

Authentication uses `--auth-username` and `--auth-password`; protect credentials from shell history and terminal logs. For HTTPS, review `--ca` and `--skip-tls-verify` instead of reusing the HTTP example unchanged.

## Select a registry for a cluster

```bash
kcctl create cluster --name demo --master 192.168.10.21 \
  --k8s-version v1.37.0 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5 \
  --image-registry internal --cri-registry internal
```

- `--image-registry` selects a Registry resource for Kubernetes images.
- `--cri-registry` adds Registry configuration to containerd; select multiple resources as needed.
- Without an explicit image registry, components use their own defaults and applicable Agent image-mirror settings. Kubernetes and Calico do not necessarily use the same default repository.

Populate the registry with the required images first. Check actual image paths, authentication, certificates, and connectivity from cluster nodes. Offline installation also needs the [resource packages](/en/docs/getting-started/carete-k8s-cluster-offline/).
