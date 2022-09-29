---
title: "部署 HA"
date: 2022-08-16
weight: 2
description: >
  通过简单的操作部署一个高可用的 kubeclipper
---


本文档旨在通过简单的操作部署一个 HA 版本的 kubeclipper。
> 如果只是想简单体验一下，请参考 [QuickStart](https://github.com/kubeclipper/kubeclipper/blob/master/README_zh.md#quick-start) 部署 AIO 环境。

## 准备工作

HA 部署注意事项：

- kubeclipper 使用 etcd 作为后端存储，为了保证高可用，建议使用 3 节点及以上来部署。
- 生产环境建议 server 节点和 agent 节点分离，避免某一主机同时作为 server 节点和 agent 节点。

主机要求：您仅需参考  [准备工作](https://github.com/kubeclipper/kubeclipper/blob/master/README_zh.md#%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C) 中对机器硬件和操作系统的要求准备多台主机。


## 部署 KubeClipper

### 下载 kcctl

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



### 开始安装

您只需执行一个命令即可安装 KubeClipper，其模板如下所示：

```
kcctl deploy  [--user root] (--passwd SSH_PASSWD | --pk-file SSH_PRIVATE_KEY) (--server SERVER_NODES) (--agent AGENT_NODES)
```



若使用 ssh passwd 方式则命令如下所示:

```bash
kcctl deploy --user root --passwd $SSH_PASSWD --server SERVER_NODES --agent AGENT_NODES
```

私钥方式如下：

```bash
kcctl deploy --user root --pk-file $SSH_PRIVATE_KEY --server SERVER_NODES --agent AGENT_NODES
```

> 您只需要提供 ssh user 以及 ssh passwd 或者 ssh 私钥即可在对应节点部署 KubeClipper。

本教程使用 私钥 方式进行部署，具体命令如下：

```bash
kcctl deploy --server 192.168.10.110,192.168.10.111,192.168.10.112 --agent 192.168.10.113,192.168.10.114,192.168.10.115 --pk-file ~/.ssh/id_rsa --pkg https://oss.kubeclipper.io/release/v1.1.0/kc-amd64.tar.gz
```

> 该命令指定 kubeclipper 包含 3 server 节点，3 agent 节点。

您可以访问  [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases)  查看当前 KubeClipper 的 Release 版本，来修改 pkg 参数中的版本号。

> 比如在 v1.2.0 版本 release 之后您可以指定 --pkg 为 `https://oss.kubeclipper.io/release/v1.2.0/kc-amd64.tar.gz` 来安装 v1.2.0 版本。



执行该命令后，Kcctl 将检查您的安装环境，若满足条件将会进入安装流程。在打印出如下的 KubeClipper banner 后即表示安装完成。

```text
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
![console](/images/docs-quickstart/console-login.png)

您可以使用默认帐号密码 `admin / Thinkbig1` 进行登录。


> 您可能需要配置端口转发规则并在安全组中开放端口，以便外部用户访问控制台。