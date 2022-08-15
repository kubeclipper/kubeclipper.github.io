---
title: "使用 Kubeclipper 离线创建 k8s 集群"
linkTitle: "离线创建集群"
weight: 6
description: >
  如何使用 KC 平台离线创建 k8s 集群
---

## 1. 进入创建界面

登录 Kubeclipper 平台后点击如图所示按钮，进入集群创建界面

![](/images/docs/cluster-begin.png)

## 2. 配置集群节点

按照文字提示完成输入集群名称、选择节点等步骤

注意: master 节点数量不能为偶数

![](/images/docs/cluster-node-config.png)

## 3. 配置集群

此步骤用于配置集群网络以及数据库、容器运行时等组件

选择离线安装并填写首先搭建好的镜像仓库地址

![](/images/docs/cluster-config.png)

## 4. 配置存储

选择 nfs 存储，按照文字提示填写相应内容

![](/images/docs/cluster-storage-config.png)

## 5. 配置插件

此步骤用于安装 Kubesphere

输入任意字符串作为 jwt 密钥

![](/images/docs/cluster-plugin-config-jwt.png)

当运行环境内存不足时可修改默认内存参数，以免安装失败

![](/images/docs/cluster-plugin-config-memory.png)

根据自己需求选择安装插件

![](/images/docs/cluster-plugin-install.png)

## 6. 安装完成

完成所有配置确认安装

![](/images/docs/cluster-finish.png)

安装成功，集群正常运行

![](/images/docs/cluster-success.png)

