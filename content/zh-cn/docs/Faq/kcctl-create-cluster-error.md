---
categories: ["FAQ"]
tags: ["kcctl", "create", "cluster"]
title: "通过 kcctl 命令创建集群错误"
linkTitle: "通过 kcctl 命令创建集群错误"
weight: 4
date: 2022-11-03
description: >
  在 v1.2.1 版本（包括 v1.2.1）之前，使用 `kcctl create cluster` 命令创建集群功能，会发生创建失败错误，以下提供一种临时的解决方法。
  在 v1.2.1 版本之后，我们修复了该问题。
---

## 问题复现

安装 v1.2.1 版本的 kcctl

```bash
curl -sfL https://oss.kubeclipper.io/get-kubeclipper.sh | KC_VERSION=v1.2.1 bash -
```

通过 kcctl deploy 命令部署 KubeClipper 集群

```bash
# 安装 AIO 环境
kcctl deploy
```

通过 kcctl create cluster 命令创建 kubernetes 集群

```bash
# 需要先登录
kcctl login --host http://127.0.0.1 --username admin --password Thinkbig1
# 创建集群
kcctl create cluster --name test --master 192.168.10.98 --untaint-master
```

登录 KubeClipper 管理界面，查看创建集群操作日志，日志显示在安装 cni 过程中发现下载 calico v3.21.2  404 无法找到

![](/images/docs-faq/create-cluster-error.png)

## 问题修复 PR

提交已经合并到了 master，PR：https://github.com/kubeclipper/kubeclipper/commit/7e6eb0ed199ff1cb00fde0c2624c62cdc5ca0b9c 

但 v1.2.1 已经发布了，按照发版规范无法在该版本打补丁，需要等到后续 v1.2.2 发布解决，因此我们提供一种临时方案来解决这个问题。

## 解决方法

制作离线资源包
下载 calico v3.21.2 的安装包，打包为指定格式的离线资源包

```bash
# 创建资源目录
mkdir -pv calico/v3.21.2/amd64

# 下载 v3.21.2 版本的 calico
wget -P calico/v3.21.2/amd64 https://oss.kubeclipper.io/packages/calico/v3.21.2/amd64/images.tar.gz
wget -P calico/v3.21.2/amd64 https://oss.kubeclipper.io/packages/calico/v3.21.2/amd64/manifest.json

# 压缩文件为指定命令
tar -zcvf calico-v3.21.2-amd64.tar.gz calico
```

推送离线资源包

```bash
# 推送
kcctl resource push --pkg calico-v3.21.2-amd64.tar.gz --type cni

# 验证
kcctl resource list|grep v3.21.2
```

> 如果在执行 `kcctl resource push` 报了如下错误：
> ![](/images/docs-faq/need-login.png)
> 解决方法如下：
> 1. 编辑 /root/.kc/deploy-config.yaml 文件。  
> 2. 找到 ssh 配置项，添加 pkFile 字段配置，值为当前服务器的 ssh 公钥文件的绝对路径。  
> ![](/images/docs-faq/add-key.png)

通过命令行安装 kubernetes 集群，在 KubeClipper 管理后台查看操作日志

```bash
kcctl create cluster --name test --master 192.168.10.98 --untaint-master
```

查看 kubernetes 集群 pods 运行状态

```bash
kubectl get pods -A
```
