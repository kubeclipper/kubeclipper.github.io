---
categories: ["QuickStart"]
tags: ["aio", "sample", "docs"]
title: "部署 AIO"
linkTitle: "部署 AIO"
weight: 2
date: 2022-08-16
description: >
  部署 AIO 环境
---

对于初次接触 KubeClipper 并想快速上手的用户，建议使用 AIO（即 All-in-One，使用单个节点安装 KubeClipper）模式，它能够帮助您零配置快速部署 KubeClipper。


## 部署 KubeClipper

### 下载并安装 kcctl

KubeClipper 提供了命令行工具🔧 kcctl 以简化运维工作，您可以直接使用以下命令下载最新版 kcctl：

```bash
# 默认安装最新的发行版
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | bash -
# 安装指定版本
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=v1.3.1 bash -
# 如果您在中国， 您可以在安装时使用 cn  环境变量, 此时 KubeClipper 会使用 registry.aliyuncs.com/google_containers 代替 k8s.gcr.io
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_REGION=cn bash -
```

> 您也可以在 [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases) 下载指定版本。

可以通过以下命令验证 kcctl 是否安装成功:

```bash
# 如果一切顺利，您将看到 kcctl 版本信息
kcctl version
```

### 开始安装

您可以使用 `kcctl deploy` 快速安装部署 KubeClipper。kcctl 使用 SSH 访问最终部署 KubeClipper 的目标节点，因此需要您提供 SSH 访问凭证，传递凭证的方法如下：

```bash
Kcctl deploy [--user <username>] [--passwd <password> | --pk-file <private key path>]
```

示例：
```bash
# 使用私钥
kcctl deploy --user root --pk-file /root/.ssh/id_rsa
# 使用密码
kcctl deploy --user root --passwd password
```

执行 `kcctl deploy` 命令 kcctl 将会检查您的安装环境，若满足条件将自动进入安装流程。若您看到如下 KubeClipper banner 后即表示安装成功。

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

> 您也可以部署 master 版本的 KubeClipper，来体验最新的功能特性（master 版本没有经过严格验证，可能包含影响体验的未知错误）
> 
> 1. 安装 master 版本 kcctl
> 
> ```bash
> curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=master bash -
> ```
> 
> 2. 在安装服务器上设置环境变量
> 
> ```bash
> export KC_VERSION=master
> ```
> 
> 3. 以 AIO 方式部署 KubeClipper
> 
> ```bash
> kcctl deploy
> ```

### 登录控制台

安装完成后，打开浏览器，访问 `http://<kc-server ip address>` 即可进入 KubeClipper 控制台。(通常 kc-server ip 是您部署 kubeClipper 节点的 ip)

![console](/images/docs-quickstart/console-login.png)

您可以使用默认帐号密码 `admin / Thinkbig1` 进行登录。

> 您可能需要配置端口转发规则并在安全组中开放端口，以便外部用户访问控制台。

## 创建 Kubernetes 集群

部署成功后您可以使用 **kcctl 工具**或者通过**控制台**创建 Kubernetes 集群。在本快速入门教程中使用 kcctl 工具进行创建。

首先使用默认帐号密码进行登录获取 token，便于后续 kcctl 和 kc-server 进行交互。

```bash
kcctl login -H https://<kc-server ip address>:8080 -u admin -p Thinkbig1
```

通过以下命令创建 Kubernetes 集群:

```bash
NODE=$(kcctl get node -o yaml|grep ipv4DefaultIP:|sed 's/ipv4DefaultIP: //')

kcctl create cluster --master $NODE --name demo --untaint-master
```

大概 3 分钟左右即可完成集群创建,您可以使用以下命令查看集群状态

```bash
kcctl get cluster -o yaml|grep status -A5
```

> 您也可以进入控制台查看实时日志。

集群处于 Running 状态即表示集群安装完成,您可以使用 `kubectl get cs` 命令来查看集群健康状况。
