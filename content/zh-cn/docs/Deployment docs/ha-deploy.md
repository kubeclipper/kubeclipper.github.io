---
title: "部署高可用 KubeClipper"
date: 2022-08-16
weight: 2
description: >
  快速部署高可用、生产就绪的 KubeClipper 集群
---

> 对于初次接触 KubeClipper，建议部署 AIO 环境，快速上手体验 KubeClipper 提供的功能特性。
> 对于想将 KubeClipper 应用到生成环境，那么本文档或许对您有所帮助。 

## 概述
根据 KubeClipper 架构设计可知，KubeClipper 有以下 4 个核心组件：
- kc-server：主要包括 APISERVER 、控制器、静态资源服务以及内置消息队列等，kc-server 通过消息队列（支持外置）与 kc-agent 通信；kc-server 之间无主从关系，且相互独立；通常部署在独立的节点，从而对外提供稳定可靠的服务。
- kc-agent：主要包括任务处理器，负责接收 kc-server 投递的任务，并反馈任务处理结果；通常部署在需要安装 kubernetes 的节点，是一个超轻量级的服务进程。
- kc-etcd：kc-server 的后端数据库，跟随 kc-server 部署在同一节点上。
- kc-dashboard：图形化管理界面，跟随 kc-server 部署在同一节点。
  综上，我们将部署 kc-server 的节点称为 server，部署 kc-agent 的节点称为 agent。

那么部署高可用 KubeClipper 集群的关键点，就在于如何规划部署 server 节点同时保证 kc-etcd 的高可用。
通常来看，对于部署高可用的分布式应用集群，基本建议节点至少 3 个；同样对于 KubeClipper，3 个节点能保证 kc-server 在其中 2 个节点宕机后依旧可以提供服务，同时能保证 kc-etcd 不会出现脑裂异常。

> 以上简单介绍了 KubeClipper 架构以及核心组件，是为了更好的理解该如何部署高可用 KubeClipper 集群，从而引出关于对服务器节点规划以及硬件配置要求的思考。


## 推荐配置

> KubeClipper 作为一个极轻量的 Kubernetes 多集群全生命周期管理工具，本身不会占用太多资源

server 节点
- 数量：3 个及以上
- 硬件要求：CPU >= 2 核，内存 >= 2GB，硬盘 >= 20GB
- 系统：CentOS 7.x / Ubuntu 18.04 / Ubuntu 20.04

agent 节点
- 数量：任意
- 硬件要求：依据实际需求而定
- 系统：CentOS 7.x / Ubuntu 18.04 / Ubuntu 20.04

## 从安装 kcctl 开始

> kcctl 是 KubeClipper 提供的命令行工具，它支持快速部署 KubeClipper 集群以及大部分 Kuberneters 集群管理功能，用以简化运维工作。

安装 kcctl：

```bash
# 默认安装最新发行版
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | bash -

# 安装指定版本
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=v1.3.1 bash -

# 如果您在中国，您可以在安装时指定 KC_REGION 环境变量，此时我们会使用 registry.aliyuncs.com/google_containers 代替 k8s.gcr.io
# 这对于在线安装 k8s 集群非常有用
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_REGION=cn bash -
```

安装成功后，会输出安装版本以及安装路径等信息。
> 您也可以在 [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases) 下载指定的 kcctl 版本

验证安装：

```bash
kcctl version -o json

kcctl version:
{
"major": "1",
"minor": "3",
"gitVersion": "v1.3.1",
"gitCommit": "5f19dcf78d3a9dc2d1035a779152fa993e0553df",
"gitTreeState": "clean",
"buildDate": "2022-12-02T10:12:36Z",
"goVersion": "go1.19.2",
"compiler": "gc",
"platform": "linux/amd64"
}

# 查看帮助文档
kcctl -h
```

## 了解 kcctl deploy 命令

> kcctl deploy 命令是专门用于部署 KubeClipper 集群，更多示例以及参数解释请执行 kcctl deploy -h

常用参数简介
- --server: server 节点 IP，例如 192.168.10.10,192.168.10.11，多个 IP 以逗号隔开。
- --agent: agent 节点 IP，例如 192.168.10.10,192.168.10.11，多个 IP 以逗号隔开。
- --pk-file: ssh 免密登录私钥，推荐在命令行使用免密登录。
- --user: ssh 登录用户名，默认为 root。
- --passwd: ssh 登录密码，不推荐在命令行使用密码登录。
- --pkg: 安装包路径，支持本地路径以及在线链接；获取在线安装包链接规则：https://oss.kubeclipper.io/release/{KC_VERSION}/kc-{GOARCH}.tar.gz 。KC_VERSION 为 Release Version 默认设置当前 kcctl 对应版本，GOARCH 为 amd64 或 arm64，默认设置当前 kcctl 的编译架构。
- --ip-detect: 节点 ip 发现规则，支持多种规则，例如指定网卡名称等，对于多网卡节点非常有用，默认为 "first-found"。

了解完 kcctl deploy 的基础使用，那么接下来就开始部署 KubeClipper 集群吧。

## 使用 kcctl 部署 KubeClipper

> 我们推荐在多节点安装场景中，将涉及到的服务器节点都统一设置免密登录，避免密码明文泄露。

私钥方式部署 3 server 节点：

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--pkg https://oss.kubeclipper.io/release/{KC_VERSION}/kc-{GOARCH}.tar.gz
```

私钥方式部署 3 server + 3 agent 节点，指定 pkg：

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--agent AGENT_IPS \
--pkg https://oss.kubeclipper.io/release/{KC_VERSION}/kc-{GOARCH}.tar.gz
```

私钥方式部署 3 server + 3 agent 节点，未指定 pkg，默认与 kcctl 安装版本一致（推荐）：

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--agent AGENT_IPS
```

私钥方式部署 3 server + 3 agent 节点，指定 etcd 端口，默认端口为 client-12379 | peer-12380 | metrics-12381：

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--agent AGENT_IPS \
--etcd-port 12379 --etcd-peer-port 12380 --etcd-metric-port 12381
```

> 参数输入示例：  
> SERVER_IPS: 192.168.10.20,192.168.10.21  
> AGENT_IPS: 192.168.10.30,192.168.10.31  
> KC_VERSION: KubeClipper 的 release version，查看 [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases) 获取  
> GOARCH：系统架构，amd64 （又名 x84_64），arm64（又名 aarch64）

kcctl deploy 支持多种参数，能够满足您对部署 KubeClipper 集群的特定需求，更多功能等您探索。  
在执行 kcctl deploy 命令后，命令会检测您的环境是否符合安装要求，会将警告信息、安装进度等同步输出到控制台，最后在安装成功后会打印如下 KubeClipper banner：

```bash
 _   __      _          _____ _ _
| | / /     | |        /  __ \ (_)
| |/ / _   _| |__   ___| /  \/ |_ _ __  _ __   ___ _ __
|    \| | | | '_ \ / _ \ |   | | | '_ \| '_ \ / _ \ '__|
| |\  \ |_| | |_) |  __/ \__/\ | | |_) | |_) |  __/ |
\_| \_/\__,_|_.__/ \___|\____/_|_| .__/| .__/ \___|_|
                                 | |   | |
                                 |_|   |_|
```

系统默认管理账号：`admin / Thinkbig1`

登录控制台：
打开浏览器，访问 `http://SERVER_IP` （通过任意一个 Server 节点均可访问）即可进入 KubeClipper 控制台

![console](/images/docs-quickstart/console-login.png)

登录命令行：

```bash
kcctl login -H http://SERVER_IP -u admin -p Thinkbig1
```

> 大多数 kcctl 命令都依赖登录状态，因此最好在执行 cli 命令时提前登录。

## 使用 kcctl 添加 agent 节点到 KubeClipper

> 当前 kcctl join 命令仅支持添加 agent 节点，后续会逐步支持添加 server 节点。
> 新加入的 agent 节点也应该统一设置免密登录，且私钥相同。

Join agent 节点：

```bash
kcctl join --agent=AGENT_IPS
```


## 使用 kcctl 从 KubeClipper 中删除 agent 节点

> 当前 kcctl drain 命令仅支持删除 agent 节点，后续会逐步支持删除 server 节点。

Drain agent 节点：

```bash
kcctl drain --agent=AGENT_IPS

# 强制 drain 节点，忽略错误
kcctl drain --agent=AGENT_IPS --force
```

如果您发现根据本文档无法成功部署 KubeClipper，请移步 [KubeClipper Github Issue](https://github.com/kubeclipper/kubeclipper/issues)，提出您的意见或反馈。