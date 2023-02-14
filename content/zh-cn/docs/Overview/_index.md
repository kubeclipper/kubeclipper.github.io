---
title: "概述"
linkTitle: "概述"
weight: 1
description: >
  Manage kubernetes in the most light and convenient way ☸️
---

## KubeClipper 是什么？
KubeClipper 旨在提供易使用、易运维、极轻量、生产级的 Kubernetes 多集群全生命周期管理服务，让运维工程师从繁复的配置和晦涩的命令行中解放出来，实现一站式管理跨区域、跨基础设施的多 kubernetes 集群。

## 为什么需要 KubeClipper？

云原生时代，Kubernetes 已毋庸置疑地成为容器编排的事实标准。虽然有诸多辅助 kubernetes 集群安装和管理的工具，但搭建和运维一套生产级别的 kubernetes 集群仍然十分复杂。九州云在大量的服务和实践过程中，沉淀出一个极轻量、易使用的图形化界面 Kubernetes 多集群管理工具—— KubeClipper。

KubeClipper 在完全兼容原生 Kubernetes 的前提下，基于社区广泛使用的 kubeadm 工具进行二次封装，提供在企业自有基础设施中快速部署 kubernetes 集群和持续化全生命周期管理（安装、卸载、升级、扩缩容、远程访问等）能力，支持在线、代理、离线等多种部署方式，还提供了丰富可扩展的 CRI、CNI、CSI、以及各类 CRD 组件的管理服务。

与现有的 Sealos、KubeKey、Kubeasz、KubeOperator、K0S 等 kubernetes 生命周期管理工具相比，KubeClipper 更贴近开放原生、轻量便捷、稳定易用。

* [快速开始](/docs/getting-started/): Learn how to get started with Kubeclipper
* [用户手册](/docs/tutorials): Check out some example code!

## KubeClipper 架构设计

### 核心架构

![](/images/docs-overview/kc-arch2.png)

KubeClipper 分为三个部分：
* kc-server：原则上部署在独立节点，负责收集节点上报信息，分发前端操作任务至指定 kc-agent 并汇总执行结果等，是 KubeClipper 控制核心。
* kc-agent: 部署在纳管节点，通过消息队列（内置 nats）与 kc-server 通信，负责上报节点信息以及处理下发任务并执行，是 KubeClipper 节点代理工具。
* kcctl: KubeClipper 的终端命令行工具，可快捷高效的部署、管理 KubeClipper 集群，能够替代大多数页面操作。

### 节点纳管

![](/images/docs-overview/kc-arch.png)

### 部署网络模型

![](/images/docs-overview/kc-network.png)

KubeClipper 支持可以通过参数配置来部署分层网络模型，以下是不同网络的概要：  

运维管理网络(Management Network):   
在 `kcctl deploy` 部署 KubeClipper 集群时，可通过 `--ip-detect` 参数指定网卡接口，默认为 `first-found`。
该网卡接口对应的 IP 地址即是 `kc-server` 与 `kc-agent` 的路由地址。

K8S 主机网络(K8S Host Network):   
在 `kcctl deploy` 部署 KubeClipper 集群时，可通过 `--node-ip-detct` 参数指定网卡接口，默认继承 `--ip-detect` 参数值，亦可独立设置。
该网卡接口对应的 IP 地址即是 K8S 的节点路由地址。

K8S Pod 网络(SDN Pod Network):   
在安装 K8S 集群时，可通过填入 CNI 的 `POD 网路底层` 指定网卡接口，默认为 `first-found`。
该网卡接口对应的 IP 地址即是 K8S POD 网路底层的路由地址。