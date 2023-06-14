---
title: "Overview"
linkTitle: "Overview"
weight: 1
description: >
  Manage kubernetes in the most light and convenient way ☸️
---

## What is KubeClipper?

KubeClipper is a lightweight web service that provides a friendly web console GUI, APIs, and a CLI tool for Kubernetes cluster lifecycle management.

KubeClipper provides flexible Kubernetes as a Service (KaaS), which allows users to rapidly deploy K8S clusters anywhere(cloud, hypervisor, bare metal) and provides continuous lifecycle management capabilities (installation, deleting, upgrading, backup and restoration, cluster scaling, remote access, plug-in management, application store).

## Project Goal

Manage Kubernetes in the most light and convenient way.

## Why do I want KubeClipper?

In the cloud-native era, Kubernetes has undoubtedly become the de facto standard for container orchestration. Although there are many tools to assist in the installation and management of kubernetes clusters, it is still very complicated to build and operate a production-level kubernetes cluster. In the process of a large number of services and practices, 99cloud has precipitated an extremely lightweight and easy-to-use graphical interface Kubernetes multi-cluster management tool - KubeClipper.

Under the premise of being fully compatible with native Kubernetes, KubeClipper is repackaged based on the kubeadm tool widely used by the community, providing rapid deployment of kubernetes clusters and continuous full life cycle management (installation, uninstallation, upgrade, scaling) in the enterprise's own infrastructure. It supports multiple deployment methods such as online, proxy, and offline, and also provides rich and scalable management services for CRI, CNI, CSI, and various CRD components.

Compared with the existing kubernetes lifecycle management tools such as KubeKey, Kubeasz, KubeOperator, and K0S, KubeClipper is more open and native, lightweight, convenient, stable and easy to use.

## Architecture

![](/images/docs-overview/kc-arch2.png)

KubeClipper 分为三个部分：
* kc-server：collecting information reported by kc-agent, distributing front-end operations to the designated kc-agent and summarizing execution results, etc., which is the core of each control of KubeClipper.
* kc-agent: Deployed on the management node, it communicates with kc-server through the message queue (built-in nats), and is responsible for reporting node information and processing and executing tasks. It is a KubeClipper node proxy tool.
* kcctl: KubeClipper's terminal command line tool can quickly and efficiently deploy and manage KubeClipper clusters, and can replace most page operations.

## Topology

![](/images/docs-overview/kc-arch.png)

## Network

![](/images/docs-overview/kc-network.png)

## Quick Start

* [Getting Started](/en/docs/getting-started/): Get started with $project