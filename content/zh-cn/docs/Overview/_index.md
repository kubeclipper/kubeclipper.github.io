---
title: "概述"
linkTitle: "概述"
weight: 1
description: >
  Manage kubernetes in the most light and convenient way ☸️
---

## KubeClipper 是什么？
KubeClipper 旨在提供易使用、易运维、极轻量、生产级的 Kubernetes 多集群全生命周期管理服务，让运维工程师从繁复的配置和晦涩的命令行中解放出来，实现一站式管理跨区域、跨基础设施的多 K8S 集群。

## 为什么需要 KubeClipper？

云原生时代，Kubernetes 已毋庸置疑地成为容器编排的事实标准。虽然有诸多辅助 K8S 集群安装和管理的工具，但搭建和运维一套生产级别的 K8S 集群仍然十分复杂。九州云在大量的服务和实践过程中，沉淀出一个极轻量、易使用的图形化界面 Kubernetes 多集群管理工具——KubeClipper。

KubeClipper 在完全兼容原生 Kubernetes 的前提下，基于社区广泛使用的 kubeadm 工具进行二次封装，提供在企业自有基础设施中快速部署 K8S 集群和持续化全生命周期管理（安装、卸载、升级、扩缩容、远程访问等）能力，支持在线、代理、离线等多种部署方式，还提供了丰富可扩展的 CRI、CNI、CSI、以及各类 CRD 组件的管理服务。

与现有的 Sealos、KubeKey、Kubeasz、KubeOperator、K0S 等 K8S 生命周期管理工具相比，KubeClipper 更贴近开放原生、轻量便捷、稳定易用。

* [快速开始](/docs/getting-started/): Learn how to get started with Kubeclipper
* [用户手册](/docs/tutorials): Check out some example code!

