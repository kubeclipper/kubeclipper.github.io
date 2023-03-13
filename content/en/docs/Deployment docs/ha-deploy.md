---
title: "Deploy Highly Available KubeClipper"
date: 2022-08-16
weight: 2
description: >
  Rapidly deploy highly available, production-ready KubeClipper clusters
---


> For the first contact with KubeClipper, it is recommended to deploy AIO environment and quickly get started to experience the features provided by KubeClipper.
> If you want to apply KubeClipper to a build environment, then this document may be helpful.

## Overview

According to the KubeClipper architecture design, KubeClipper has the following 4 core components:
- Kc-server: mainly includes APISERVER, controller, static resource services and built-in message queue, etc., kc-server communicates with kc-agent through message queue (supports external); kc-server has no master-slave relationship and is independent of each other; usually deployed in independent nodes to provide stable and reliable services to the outside world.
- Kc-agent: mainly includes the task processor, which is responsible for receiving the tasks delivered by the kc-server and feeding back the task processing results; usually deployed in nodes that need to install kubernetes, it is an ultra-lightweight service process.
- Kc-etcd: The backend database of kc-server, deployed on the same node as kc-server.
- Kc-dashboard: graphical management interface, deployed on the same node with kc-server.
  To sum up, we call the node that deploys kc-server as server, and the node that deploys kc-agent as agent.

Then the key point of deploying a highly available KubeClipper cluster is how to plan and deploy server nodes while ensuring the high availability of kc-etcd.  
Generally speaking, for deploying highly available distributed application clusters, it is basically recommended to have at least 3 nodes; also for KubeClipper, 3 nodes can ensure that kc-server can still provide services after 2 nodes Downtime, and can ensure that kc-etcd will not appear Split-Brain exception.

> The above brief introduction to the KubeClipper architecture and core components is to better understand how to deploy a highly available KubeClipper cluster, so as to lead to thinking about server node planning and Hardware configuration requirements.

## Recommended configuration

> KubeClipper as an extremely lightweight Kubernetes multi-cluster full lifecycle management tool, itself will not take up too many resources.

server node
- Quantity: 3 and more
- Hardware requirements: CPU > = 2 cores, RAM > = 2GB, hard disk > = 20GB
- System: CentOS 7.x/Ubuntu 18.04/Ubuntu 20.04

Agent node
- Quantity: any
- Hardware requirements: according to actual needs
- System: CentOS 7.x/Ubuntu 18.04/Ubuntu 20.04

## Start by installing kcctl

> Kcctl is a command line tool provided by KubeClipper that enables rapid deployment of KubeClipper clusters and most Kuberneters cluster management features to simplify operations.

Install kcctl:
```bash
# The latest release is installed by default
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | bash -

# Install the specified version
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=v1.3.1 bash -

# If you are in China, you can specify the KC_REGION environment variable during installation, at this time we will use registry.aliyuncs.com/google_containers instead of k8s.gcr.io
# This is very useful for online installation of k8s cluster
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_REGION=cn bash -
```

After the installation is successful, the installation version and installation Path will be output.
> You can also download the [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases) download the specified kcctl version

Verify installation:
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

# View help documentation
kcctl -h
```

## Learn about the kcctl deploy command

> The kcctl deploy -h command is specially used to deploy KubeClipper cluster, for more examples and parameter explanation, please execute `kcctl deploy -h`

Introduction to common parameters
- --Server: IP server node, such as 192.168.10.10, 192.168.10.11, IP separated by commas.
- --Agent: Agent node IP, such as 192.168.10.10, 192.168.10.11, IP separated by commas.
- --Pk-file: ssh password-free login private key, it is recommended to use password-free login on the command line.
- --User: ssh login username, default is root.
- --Passwd: ssh login password, it is not recommended to use the password to log in at the command line.
- --Pkg: Installation package Path, support local Path and online link; get online installation package link rules: https://oss.kubeclipper.io/release/ {KC_VERSION}/kc- {GOARCH} .tar.gz . KC_VERSION for Release Version default setting current kcctl corresponding version, GOARCH is amd64 or arm64, default setting current kcctl Compilation architecture.
- --Ip-detect: Node IP discovery rules, support a variety of rules, such as specifying the name of the network interface card, etc., very useful for multiple network interface card nodes, the default is "first-found".

After understanding the basic usage of kcctl deploy, let's start deploying the KubeClipper cluster.

## Deploy KubeClipper with kcctl

> We recommend that in the multi-node installation scenario, the server nodes involved are uniformly set up password-free login to avoid password Plain Text leakage.

Deploy 3 server nodes with private key:

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--pkg https://oss.kubeclipper.io/release/{KC_VERSION}/kc-{GOARCH}.tar.gz
```

Deploy 3 server + 3 agent nodes in private key mode, specify pkg:

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--agent AGENT_IPS \
--pkg https://oss.kubeclipper.io/release/{KC_VERSION}/kc-{GOARCH}.tar.gz
```

Deploy 3 server + 3 agent nodes with private key, pkg is not specified, and the default is the same as the installed version of kcctl (recommended):

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--agent AGENT_IPS
```

Private key deployment 3 server + 3 agent node, specify etcd port, default port is client-12379 | peer-12380 | metrics-12381 :

```bash
kcctl deploy --pk-file=~/.ssh/id_rsa \
--server SERVER_IPS \
--agent AGENT_IPS \
--etcd-port 12379 --etcd-peer-port 12380 --etcd-metric-port 12381
```

> Parameter input example:  
> SERVER_IPS: 192.168.10.20,192.168.10.21  
> AGENT_IPS: 192.168.10.30,192.168.10.31  
> KC_VERSION : KubeClipper release version, see [GitHub Release Page](https://github.com/kubeclipper/kubeclipper/releases)  
> GOARCH System Architecture, AMD64 (aka x84_64), ARM64 (aka AARCH 64)

Kcctl deploy supports a variety of parameters, which can meet your specific needs for deploying KubeClipper clusters, and more functions are waiting for you to explore.  
After executing the kcctl deploy command, the command will detect whether your environment meets the installation requirements, and will synchronize warning messages, installation progress, etc. to the Console. Finally, the following KubeClipper banner will be printed after the installation is successful:

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

System default management account: `admin/Thinkbig1`
Login to Console:
Open a browser and visit `http://SERVER_IP` (accessible through any Server node) to enter the KubeClipper Console

![console](/images/docs-quickstart/console-login.png)

Login command line:

```bash
kcctl login -H http://SERVER_IP -u admin -p Thinkbig1
```

> Most kcctl commands rely on login status, so it's best to log in early when you execute the cli command.

## Add agent node to KubeClipper using kcctl

> The current kcctl join command only supports adding agent nodes, and will gradually support adding server nodes in the future.  
> Newly added agent nodes should also be uniformly set up password-free login, and the private key is the same.

Join agent node:

```bash
kcctl join --agent=AGENT_IPS
```

## Remove agent node from KubeClipper using kcctl

> The current kcctl drain command only supports deleting agent nodes, and will gradually support deleting server nodes in the future.

Drain agent node:
```bash
kcctl drain --agent=AGENT_IPS

# Force drain node, ignore errors
kcctl drain --agent=AGENT_IPS --force
```

If you find that KubeClipper cannot be successfully deployed according to this document, please move to the [KubeClipper Github Issue](https://github.com/kubeclipper/kubeclipper/issues) to provide your comments or feedback.
