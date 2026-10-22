---
title: "Image registries"
linkTitle: "Image registries"
weight: 2
---

Registry resources describe Kubernetes image sources or containerd pull settings. Registering a registry does not copy images into it. Offline component packages are prepared separately.

```bash
kcctl create registry --name internal --host registry.example.com:5000 --scheme http
kcctl get registry
kcctl create registry -h
kcctl registry -h
```

This example uses an HTTP registry on a management network. Configure HTTPS, CA trust, and authentication for production. 1.6 also persists node and SSH configuration for `kcctl registry`; check existing configuration before subsequent operations.

During cluster creation, `--image-registry internal` selects the Kubernetes image source, and `--cri-registry internal` configures containerd pulls. Populate images first and verify node connectivity, certificates, and authentication. Source: [v1.6.0 Registry CLI](https://github.com/kubeclipper/kubeclipper/blob/v1.6.0/pkg/cli/create/create_registry.go).
