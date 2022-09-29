---
categories: ["QuickStart"]
tags: ["docs"] 
title: "快速开始"
linkTitle: "快速开始"
weight: 1
description: >
  快速搭建平台使用功能
---


对于初次接触 KubeClipper 并想快速上手的用户，建议使用 All-in-One 安装模式，它能够帮助您零配置快速部署 KubeClipper。

### 准备工作

KubeClipper 本身并不会占用太多资源，但是为了后续更好的运行 Kubernetes 建议硬件配置不低于最低要求。

您仅需参考以下对机器硬件和操作系统的要求准备一台主机。

#### 硬件推荐配置

- 确保您的机器满足最低硬件要求：CPU >= 2 核，内存 >= 2GB。
- 操作系统：CentOS 7.x / Ubuntu 18.04 / Ubuntu 20.04。

#### 节点要求

- 节点必须能够通过 `SSH` 连接。
- 节点上可以使用 `sudo` / `curl` / `wget` / `tar` 命令。

> 建议您的操作系统处于干净状态（不安装任何其他软件），否则可能会发生冲突。

### 部署 KubeClipper

#### 下载 kcctl

KubeClipper 提供了命令行工具🔧 kcctl 以简化运维工作，您可以直接使用以下命令下载最新版 kcctl：

```bash
# curl -sfL https://oss.kubeclipper.io/kcctl.sh | sh -
# 如果你在中国， 你可以在安装时使用 cn  环境变量, 此时我们会使用 registry.aliyuncs.com/google_containers 代替 k8s.gcr.io
curl -sfL https://oss.kubeclipper.io/kcctl.sh | KC_REGION=cn sh -
```

> 您也可以在 [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases) 下载指定版本。

通过以下命令检测是否安装成功:

```bash
kcctl version
```

#### 开始安装

在本快速入门教程中，您只需执行一个命令即可安装 KubeClipper，其模板如下所示：

```bash
kcctl deploy  [--user root] (--passwd SSH_PASSWD | --pk-file SSH_PRIVATE_KEY)
```

若使用 ssh passwd 方式则命令如下所示:

```bash
kcctl deploy --user root --passwd $SSH_PASSWD
```

私钥方式如下：

```bash
kcctl deploy --user root --pk-file $SSH_PRIVATE_KEY
```

> 您只需要提供 ssh user 以及 ssh passwd 或者 ssh 私钥即可在本机部署 KubeClipper。

执行该命令后，Kcctl 将检查您的安装环境，若满足条件将会进入安装流程。在打印出如下的 KubeClipper banner 后即表示安装完成。

```console
 _   __      _          _____ _ _
| | / /     | |        /  __ \ (_)
| |/ / _   _| |__   ___| /  \/ |_ _ __  _ __   ___ _ __
|    \| | | | '_ \ / _ \ |   | | | '_ \| '_ \ / _ \ '__|
| |\  \ |_| | |_) |  __/ \__/\ | | |_) | |_) |  __/ |
\_| \_/\__,_|_.__/ \___|\____/_|_| .__/| .__/ \___|_|
                                 | |   | |
                                 |_|   |_|
```

### 登录控制台

安装完成后，打开浏览器，访问 `http://$IP` 即可进入 KubeClipper 控制台。

![console](docs/img/console-login.png)

您可以使用默认帐号密码 `admin / Thinkbig1` 进行登录。

> 您可能需要配置端口转发规则并在安全组中开放端口，以便外部用户访问控制台。

### 创建 k8s 集群

部署成功后您可以使用 **kcctl 工具**或者通过**控制台**创建 k8s 集群。在本快速入门教程中使用 kcctl 工具进行创建。

首先使用默认帐号密码进行登录获取 token，便于后续 kcctl 和 kc-server 进行交互。

```bash
kcctl login -H http://localhost -u admin -p Thinkbig1
```

然后使用以下命令创建 k8s 集群:

```bash
NODE=$(kcctl get node -o yaml|grep ipv4DefaultIP:|sed 's/ipv4DefaultIP: //')

kcctl create cluster --master $NODE --name demo --untaint-master
```

大概 3 分钟左右即可完成集群创建,也可以使用以下命令查看集群状态

```bash
kcctl get cluster -o yaml|grep status -A5
```

> 您也可以进入控制台查看实时日志。

进入 Running 状态即表示集群安装完成,您可以使用 `kubectl get cs` 命令来查看集群健康状况。
