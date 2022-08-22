---
title: "Deploy HA"
date: 2022-08-16
weight: 2
description: >
  deploy a high available kubeclipper by some simple cmd.
---

The purpose of this document is to deploy an HA  KubeClipper with a simple operation.
> If you just want a simple experience, please refer to [QuickStart](https://github.com/kubeclipper-labs/kubeclipper#quick-start) to deploy AIO environment.



## Preparations

You only need to prepare a host with reference to the following requirements for machine hardware and operating system: Preparations

HA Deploy Recommend:

- Kubeclipper uses etcd as backend storage. In order to ensure high availability, it is recommended to use 3 nodes and above for deployment.
- At the same time, the production environment recommends that the server node and the agent node be separated to avoid acting as both the server node and the agent node at the same time.
  Node planning:

## Deploying KubeClipper

### Download kcctl

KubeClipper provides command line tools 🔧 kcctl to simplify operation and maintenance work. You can directly download the latest version of kcctl with the following command:

```bash
curl -sfL https://oss.kubeclipper.io/kcctl.sh | sh -

# 如果你在中国， 你可以在安装时使用 cn  环境变量, 此时我们会使用 registry.aliyuncs.com/google_containers 代替 k8s.gcr.io
# curl -sfL https://oss.kubeclipper.io/kcctl.sh | KC_REGION=cn sh -
```

> You can also download the specified version on the [GitHub Release Page](https://github.com/kubeclipper-labs/kubeclipper/releases).

Check if the installation is successful with the following command:

```bash
kcctl version
```



### Get Started with Installation

All you need to do is execute a command to install KubeClipper, whose template looks like this:

```bash
kcctl deploy  [--user root] (--passwd SSH_PASSWD | --pk-file SSH_PRIVATE_KEY) (--server SERVER_NODES) (--agent AGENT_NODES)
```

If you use the ssh passwd method, the command is as follows:

```bash
kcctl deploy --user root --passwd $SSH_PASSWD --server SERVER_NODES --agent AGENT_NODES
```

The private key method is as follows:

```bash
kcctl deploy --user root --pk-file $SSH_PRIVATE_KEY --server SERVER_NODES --agent AGENT_NODES
```

> You only need to provide ssh user and ssh passwd or ssh private key to deploy KubeClipper on the corresponding node.

This tutorial uses the private key to deploy, the specific commands are as follows:

```bash
kcctl deploy --server 192.168.10.110,192.168.10.111,192.168.10.112 --agent 192.168.10.113,192.168.10.114,192.168.10.115 --pk-file ~/.ssh/id_rsa --pkg https://oss.kubeclipper.io/release/v1.1.0/kc-amd64.tar.gz
```

> This  command shows kubeclipper platform will has 3 server node and 3 agent node.

> You can visit the [GitHub Release Page](https://github.com/kubeclipper-labs/kubeclipper/releases) to view the current KubeClipper release version and modify the version number in the pkg parameter.
>
> For example, after the v1.2.0 release you can specify --pkg as the https://oss.kubeclipper.io/release/v1.2.0/kc-amd64.tar.gz to install the v1.2.0 version.

After you runn this command, kcctl will check your installation environment and enter the installation process, if the conditions are met.
After printing the KubeClipper banner, the installation is complete.

```bash
| | / /     | |        /  __ \ (_)
| |/ / _   _| |__   ___| /  \/ |_ _ __  _ __   ___ _ __
|    \| | | | '_ \ / _ \ |   | | | '_ \| '_ \ / _ \ '__|
| |\  \ |_| | |_) |  __/ \__/\ | | |_) | |_) |  __/ |
\_| \_/\__,_|_.__/ \___|\____/_|_| .__/| .__/ \___|_|
| |   | |
|_|   |_|
```



### Login console

When deployed successfully, you can open a browser and visit http://$IP to enter the KubeClipper console.

![console](/images/docs-quickstart/console-login.png)

You can log in with the default account password `admin/Thinkbig1`.

> You may need to configure port forwarding rules and open ports in security groups for external users to access the console.
