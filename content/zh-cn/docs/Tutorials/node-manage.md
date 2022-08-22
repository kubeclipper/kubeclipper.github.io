---
title: "节点管理"
date: 2022-08-16
weight: 2
description: >
  KubeClipper 节点管理功能使用指南
---

在“节点信息”页面，您可以查看平台中管理的全部节点列表，节点规格、状态等信息。点击节点名称进入节点详情页面，您可以查看详细的节点基本信息和系统信息。

![](/images/docs-tutorials/node-info.png)

KubeClipper 中的节点状态表示 kc-gent 对节点的管理状态。正常情况下，节点状态显示为“就绪”，当节点失联4分钟（误差时间10s内）后，状态会更新为“未知”，未知状态的节点无法进行任何操作，也无法创建集群或为集群添加/移除节点。

## 添加节点

在部署 KubeClipper 时，您就可以添加初始的 server 节点和 agent 节点，其中，server节点用于部署 KubeClipper 自身服务，agent 节点可用于部署 K8S 集群。在用于实验或开发的 KubeClipper 环境，您可以将 server 节点同时添加为 agent 节点。但如果用于生产环境，建议不要将 server 节点复用为 agent 节点。

您也可以使用 kcctl join 命令为 KubeClipper 添加 agent 节点。同时，您可以为每个 agent 节点标记一个区域，区域可以是物理的或逻辑的位置，您可以使用同一区域的节点创建 K8S 集群，但不可以使用跨区域的节点创建集群。未标记区域的节点默认属于 default 区域。详情参见“Kcctl 操作指南“。

命令行示例：

```Plaintext
kcctl join --agent beijing:1.2.3.4 --agent shanghai:2.3.4.5
```

## 移除节点

当您不再需要某些节点，可以使用 kcctl drain 命令将节点从平台中移除。详情参见“Kcctl 操作指南“。

命令行示例：

```Plaintext
kcctl drain --agent 192.168.10.19
```

## 连接终端

在节点列表页面，您可以点击目标节点右侧的“连接终端”按钮，在连接终端的弹窗中输入节点端口和用户名密码信息后，访问节点SSH控制台并执行命令。

![](/images/docs-tutorials/node-terminal.png)

