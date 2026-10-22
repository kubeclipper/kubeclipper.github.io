---
title: "快速开始"
linkTitle: "快速开始"
weight: 2
description: >
  使用 KubeClipper 1.7.0 部署平台并创建第一个 Kubernetes 集群。
---

本文使用 KubeClipper **v1.7.0**。准备一台通过 SSH 可访问、使用 systemd 的 Linux 主机，部署 KubeClipper，再在该主机创建单节点实验集群。生产环境请参考[高可用部署](/docs/deployment-docs/ha-deploy/)。

## 准备主机

- 安装 `curl`、`tar`、`sudo`，确保 SSH 服务可用，部署用户有 sudo 权限。
- 启用 chrony、ntp 或 systemd-timesyncd 中的一种时间同步服务。
- 准备可登录目标节点的 SSH 私钥，并确认节点之间的地址可达。
- 核对目标 Kubernetes 版本对内核、cgroup 和容器运行时的要求。历史文档中的操作系统列表不代表新版本 Kubernetes 的兼容性范围。
- 为部署包下载、解压和容器镜像预留磁盘空间。1.7.0 的完整部署包约 1.2 GiB，GitHub Release 中约 60 MB 的二进制包不能替代完整部署包。

## 安装 kcctl

下载与 1.7.0 发布标签一致的安装脚本，再执行安装。脚本通过项目的阿里云 OSS 原生域名下载二进制，不依赖旧的 `oss.kubeclipper.io` 域名。

```bash
curl -fL -o get-kubeclipper.sh \
  https://raw.githubusercontent.com/kubeclipper/kubeclipper/v1.7.0/scripts/get-kubeclipper.sh
KC_VERSION=v1.7.0 bash get-kubeclipper.sh
kcctl version
```

脚本支持 Linux、macOS 的 amd64 和 arm64 客户端。平台服务部署在 Linux 上；以下命令在 Linux 部署机运行。也可以从 [v1.7.0 Release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.7.0) 下载对应客户端。

## 下载完整部署包

按目标平台架构设置 `ARCH`。下例为 amd64；arm64 主机将其改为 `arm64`。

```bash
ARCH=amd64
curl -fL -o "kc-${ARCH}.tar.gz" \
  "https://kubeclipper.oss-ap-southeast-1.aliyuncs.com/release/v1.7.0/kc-${ARCH}.tar.gz"
tar -tzf "kc-${ARCH}.tar.gz" | head
```

完整部署包包含平台服务、控制台及离线资源。离线环境需要提前在联网机器下载，再传入部署机。创建 Kubernetes 集群时还应核对平台中已有的组件包和架构，见[离线创建集群](/docs/getting-started/carete-k8s-cluster-offline/)。

## 部署 All-in-One 平台

以下示例使用 SSH 私钥。替换为自己的私钥路径；部署机必须能够通过 SSH 登录目标节点，即使目标节点就是本机。

```bash
read -r -s -p '设置 admin 密码: ' KC_ADMIN_PASSWORD
printf '\n'
kcctl deploy --user root --pk-file "$HOME/.ssh/id_rsa" \
  --pkg "$PWD/kc-${ARCH}.tar.gz" \
  --initial-password "$KC_ADMIN_PASSWORD"
unset KC_ADMIN_PASSWORD
```

初始密码需满足平台校验要求：8–16 位，包含大写字母、小写字母和数字。部署前检查失败时，先处理输出中对应的节点和检查项，不要反复重装。

1.7 的 Agent 通过 mTLS 访问 Server API，部署时保持 TLS 开启。默认控制台为 `http://SERVER_IP:80`，Server API 为 `https://SERVER_IP:8080`，这两个入口用途不同。

## 登录并检查平台

将 `SERVER_IP` 替换为实际 Server 地址。命令会提示输入刚才设置的 admin 密码。

```bash
SERVER_IP=192.168.10.10
kcctl login --host "https://${SERVER_IP}:8080" --username admin
kcctl status
kcctl doctor
kcctl get node
kcctl resource list
```

通过浏览器访问 `http://SERVER_IP` 可打开控制台。生产环境应在控制台入口配置 HTTPS。`status` 检查平台状态，`doctor` 给出诊断证据；它们不会自动修复环境。

## 创建第一个集群

从 `kcctl get node` 的结果选择就绪节点，将节点 ID 或 IP 填入 `NODE`。离线方式是默认值；先确认已有对应架构和版本的资源包。

```bash
NODE=192.168.10.10
kcctl create cluster --name demo --master "$NODE" --untaint-master \
  --k8s-version v1.37.0 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5
kcctl operation list -c demo
kcctl get cluster demo -o yaml
```

`--untaint-master` 允许实验集群在控制节点调度普通工作负载。安装耗时取决于机器、网络和镜像准备情况。命令提交成功后，继续查看 Operation 和集群状态，不能把提交成功当作安装完成。

从集群详情页获取 kubeconfig，设置 `KUBECONFIG` 后检查 Kubernetes：

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get --raw='/readyz?verbose'
```

确认集群处于 Running、节点 Ready，并检查系统 Pod 和 API 健康状况。任务失败时参考[操作与日志](/docs/tutorials/operations/)和[平台诊断](/docs/tutorials/diagnostics/)。

## 清理实验集群

以下操作会删除 demo 集群，先确认其中没有需要保留的工作负载和数据：

```bash
kcctl delete cluster demo
kcctl operation list -c demo
kcctl get cluster
```

等待删除操作结束并确认集群已移除。不要使用重置状态或强制删除来代替失败原因排查。
