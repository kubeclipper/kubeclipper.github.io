---
title: "概述"
linkTitle: "概述"
weight: 1
description: >
  KubeClipper 1.7 的组成、通信方式和网络。
---

KubeClipper 为 Kubernetes 集群提供创建、扩缩容、升级、备份、恢复和删除等生命周期管理能力，提供 Web 控制台、API 和 kcctl 命令行。

## 1.7 架构

![KubeClipper Operation v2 架构](/images/docs-overview/operation-v2.svg)

- **kc-server** 提供 API，保存集群和 Operation、Task 等资源，由控制器推进任务状态。
- **kc-agent** 安装在受管节点，通过 mTLS 访问 Server API，观察分配给本节点的任务，执行安装等操作并回报结果。
- **kcctl / Console** 提交管理请求，查看平台状态、操作进度和日志。
- **etcd** 保存平台资源和状态。平台 etcd 与所管理 Kubernetes 集群的 etcd 分别规划。

1.7 使用 API 驱动的 Operation v2，不再通过内置 NATS 分发任务。操作提交后异步执行，需结合 Operation、集群状态和节点实际状态确认结果。参见[操作与日志](/docs/tutorials/operations/)。

## 网络与端口

| 用途 | 默认端口 | 使用方 |
|---|---|---|
| 控制台 | TCP 80 | 浏览器；生产入口配置 HTTPS |
| Server API | TCP 8080，HTTPS | kcctl、Console、Agent |
| 资源文件服务 | TCP 8081 | 下载平台资源的节点 |
| Agent 任务日志 | TCP 10260 | Server 访问 Agent；按实际配置限制访问 |
| 平台 etcd | TCP 12379 / 12380 / 12381 | client / peer / metrics，限制在管理网络 |
| SSH | TCP 22 | 部署、节点维护 |

端口可通过部署配置修改。Agent 任务日志监听配置也应与防火墙策略一起核对；不要直接套用旧版 NATS 端口表。

`--ip-detect` 选择平台管理地址；`--node-ip-detect` 选择 Kubernetes 节点地址。多网卡环境需要确认所选地址与管理网络可达。Pod 网络的地址发现规则由所选 CNI 配置决定。

## 版本与入门

- [1.7 发布说明与组件矩阵](/docs/overview/release-1.7/)
- [快速开始](/docs/getting-started/)
- [高可用部署](/docs/deployment-docs/ha-deploy/)
- [平台诊断](/docs/tutorials/diagnostics/)
