--- 
categories: ["QuickStart"]
tags: ["aio", "sample", "docs"]
title: "Deploying AIO"
linkTitle: "Deploying AIO"
weight: 1
date: 2022-08-16
description: >
  Deploying the AIO environment
---

For users who are new to KubeClipper and want to get started quickly, it is recommended to use the All-in-One installation mode, which can help you quickly deploy KubeClipper with zero configuration.


## Deploy KubeClipper

### Download kcctl

KubeClipper provides a command line tool 🔧 kcctl to simplify operation and maintenance. You can download the latest version of kcctl directly with the following command:

```Bash
# The latest distribution is installed by default
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | bash -
# Install the specified version
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=v1.3.1 bash -
#If you are in China, you can use cn environment variables during installation, in this case we will use registry.aliyuncs.com/google_containers instead of k8s.gcr.io
Curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_REGION=cn bash -
```

> You can also download the specified version from the [GitHub Release Page] ( https://github.com/kubeclipper/kubeclipper/releases ) .

Check if the installation was successful with the following command:

```Bash
Kcctl version
```

### Start installation

You can use 'kcctl deploy' to quickly install and deploy KubeClipper. kcctl uses SSH to access the target node where KubeClipper is finally deployed, so you need to provide SSH access credentials, and the following way to pass the credentials:

```bash
Kcctl deploy [--user <username>] [--passwd <password> | --pk-file <private key path>]
```

Example：
```bash
# Use the private key
kcctl deploy --user root --pk-file /root/.ssh/id_rsa
# Use a password
kcctl deploy --user root --passwd password
```

Execute the 'kcctl deploy' command kcctl will check your installation environment and will automatically enter the installation process if the conditions are met. If you see the following KubeClipper banner, the installation is successful.

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

> You can also deploy the master version of KubeClipper to experience the latest features (the master version is not rigorously validated and may contain unknown bugs that affect the experience)
>
> 1. Install the master version kcctl
>
> ```bash
> curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=master bash -
> ```
>
> 2. Set environment variables on the installation server
>
> ```bash
> export KC_VERSION=master
> ```
>
> 3. Deploy KubeClipper AIO environment
>
> ```bash
> kcctl deploy
> ```

### Login to console

After the installation is complete, open a browser and visit 'http:<kc-server ip address>' to enter the KubeClipper console. (Usually kc-server IP is the IP of the node where you deploy kubeClipper)

![console](/images/docs-quickstart/console-login.png)

You can use the default account password " admin/Thinkbig1 " to log in.

> You may need to configure port forwarding rules and open ports in security groups for external users to access the console.

## Create kubernetes cluster

After successful deployment you can create a kubernetes cluster using the ** kcctl tool ** or via the ** console ** . Use the kcctl tool to create it in this quickstart tutorial.

First, use the default account password to log in and obtain the token, which is convenient for subsequent interaction between kcctl and kc-server.

```Bash
kcctl login -H https://<kc-server ip address>:8080 -u admin -p Thinkbig1
```

Then create a Kubernetes cluster with the following command:

```Bash
NODE = $ (kcctl get node -o yaml | grep ipv4DefaultIP: | sed's/ipv4DefaultIP : //')

Kcctl create cluster --master $NODE --name demo --untaint-master
```

It takes about 3 minutes to complete the cluster creation, or you can use the following command to view the cluster status

```Bash
Kcctl get cluster -o yaml | grep status -A5
```

> You can also go to the console to view the real-time log.

The cluster installation is complete when the cluster is in the Running state, and you can use the 'kubectl get cs' command to view the cluster health.
