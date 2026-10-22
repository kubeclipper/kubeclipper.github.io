---
title: "快速开始"
linkTitle: "快速开始"
weight: 2
---

以下命令在 **Linux amd64** 部署机的 Bash 中执行，使用 v1.6.0 客户端和完整部署包。准备使用 systemd、SSH 可达且部署用户有 sudo 权限的 Linux 节点；配置时间同步，核对 Kubernetes 的内核、cgroup 和磁盘要求。

## 安装客户端

1.6 发布标签中的旧安装脚本使用 `oss.kubeclipper.io`，该域名当前证书已过期。下面直接从 GitHub Release 下载客户端，不关闭证书校验。

```bash
curl -fL -o kc-linux-amd64-v1.6.0.tar.gz \
  https://github.com/kubeclipper/kubeclipper/releases/download/v1.6.0/kc-linux-amd64.tar.gz
mkdir -p kc-client-v1.6.0
tar -xzf kc-linux-amd64-v1.6.0.tar.gz -C kc-client-v1.6.0
sudo install -m 0755 kc-client-v1.6.0/kcctl /usr/local/bin/kcctl
kcctl version
```

其他客户端架构从 [1.6 Release](https://github.com/kubeclipper/kubeclipper/releases/tag/v1.6.0)选择对应包。arm64 归档中的二进制位于架构子目录，先用 `tar -tzf` 查看路径。

## 下载完整部署包并安装平台

客户端归档不能替代完整部署包。下面使用项目的 OSS 原生域名，amd64 和 arm64 均有对应完整部署包。

```bash
curl -fL -o kc-amd64-v1.6.0.tar.gz \
  https://kubeclipper.oss-ap-southeast-1.aliyuncs.com/release/v1.6.0/kc-amd64.tar.gz
read -r -s -p '设置 admin 密码: ' KC_ADMIN_PASSWORD
printf '\n'
kcctl deploy --user root --pk-file "$HOME/.ssh/id_rsa" \
  --pkg "$PWD/kc-amd64-v1.6.0.tar.gz" \
  --initial-password "$KC_ADMIN_PASSWORD"
unset KC_ADMIN_PASSWORD
```

使用可登录目标节点的 SSH 私钥，密码设为 8–16 位并包含大写、小写字母和数字。多节点部署参数通过 `kcctl deploy -h` 核对。保持 API 与 NATS 的 TLS 配置开启。

## 登录与创建集群

将 Server 地址和节点 IP 替换为自己的值，命令会提示输入 admin 密码。控制台入口为 `http://SERVER_IP`，CLI 使用 HTTPS API。

```bash
SERVER_IP=192.168.10.10
kcctl login --host "https://${SERVER_IP}:8080" --username admin
kcctl get node
kcctl resource list
```

先确认平台资源列表包含所需版本及节点架构，再创建单节点实验集群：

```bash
NODE=192.168.10.10
kcctl create cluster --name demo --master "$NODE" --untaint-master \
  --k8s-version v1.36.1 --cri containerd --cri-version 2.2.4 \
  --cni calico --cni-version v3.31.5
kcctl operation list -c demo
kcctl get cluster demo -o yaml
```

安装完成后，从集群详情获取 kubeconfig，检查 `kubectl get nodes -o wide`、`kubectl get pods -A` 和 `kubectl get --raw='/readyz?verbose'`。操作排查见[操作与日志](/docs/tutorials/operations/)。
