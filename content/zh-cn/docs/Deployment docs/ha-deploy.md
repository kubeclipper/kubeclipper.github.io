---
title: "高可用部署"
linkTitle: "高可用部署"
weight: 1
description: >
  使用三个 Server 节点部署 KubeClipper 1.7 平台。
---

本文部署 KubeClipper 平台的高可用控制面。平台 Server 的高可用与受管 Kubernetes 集群的高可用是两件事，需分别规划。

## 准备节点与网络

准备三个 Linux Server 节点，以及需要纳管的 Agent 节点。部署用户通过同一 SSH 私钥访问所有节点，并具备 sudo 权限。时间同步和端口要求见[架构与网络](/docs/overview/)。

Server 节点部署平台 etcd，节点数量和故障容忍按 etcd 仲裁要求规划。生产环境建议将平台 Server 与运行 Kubernetes 工作负载的节点分开。

## 安装和下载

按照[快速开始](/docs/getting-started/)安装 v1.7.0 kcctl，下载与目标架构匹配的完整 `kc-amd64.tar.gz` 或 `kc-arm64.tar.gz` 部署包。不要将 GitHub Release 的客户端二进制包传给 `--pkg`。

## 部署三个 Server 和 Agent

将示例 IP、私钥和部署包路径替换为实际值。`--server` 使用逗号分隔地址，`--agent` 可按区域填写。

```bash
read -r -s -p '设置 admin 密码: ' KC_ADMIN_PASSWORD
printf '\n'
kcctl deploy \
  --server 192.168.10.11,192.168.10.12,192.168.10.13 \
  --agent default:192.168.10.21,192.168.10.22 \
  --user root --pk-file "$HOME/.ssh/id_rsa" \
  --pkg "$PWD/kc-amd64.tar.gz" \
  --initial-password "$KC_ADMIN_PASSWORD"
unset KC_ADMIN_PASSWORD
```

保持 TLS 开启。多网卡环境通过 `--ip-detect` 与 `--node-ip-detect` 显式选择可达地址；可使用 `kcctl deploy -h` 核对参数。默认平台 etcd 端口为 12379、12380、12381。

## 验证结果

```bash
kcctl login --host https://192.168.10.11:8080 --username admin
kcctl status
kcctl doctor
kcctl get node
```

检查三个 Server 的服务状态、平台 etcd 成员和 Agent 是否正常。在其他 Server 地址重复检查 API 可达性。需要统一域名或 VIP 时，另行配置入口负载均衡和证书；部署三个 Server 不会自动创建入口 VIP。

浏览器默认访问各 Server 的 HTTP 80 控制台入口；CLI 使用 HTTPS 8080 API。生产入口应配置 HTTPS，并按实际网络限制管理端口访问。

## 添加和移除 Agent

```bash
kcctl join --agent default:192.168.10.23
kcctl get node
```

确认节点没有需要保留的集群和工作负载后，再执行移除：

```bash
kcctl drain --agent 192.168.10.23
```

先查看正常 drain 的错误原因，再决定后续处理；不要默认使用强制参数。升级前参见[升级检查](/docs/deployment-docs/upgrade/)。
