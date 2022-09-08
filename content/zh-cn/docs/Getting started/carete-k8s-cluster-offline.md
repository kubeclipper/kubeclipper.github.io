---
title: "使用 Kubeclipper 离线创建 k8s 集群"
linkTitle: "离线创建集群"
weight: 3
description: >
  如何使用 KC 平台离线创建 k8s 集群
---

## 1. 进入创建界面

登录 Kubeclipper 平台后点击如图所示按钮，进入集群创建界面

![](/images/docs-quickstart/cluster-begin.png)

## 2. 配置集群节点

按照文字提示完成输入集群名称、选择节点等步骤

注意: master 节点数量不能为偶数

![](/images/docs-quickstart/cluster-node-config.png)

## 3. 配置集群

此步骤用于配置集群网络以及数据库、容器运行时等组件

选择离线安装并填写首先搭建好的镜像仓库地址

![](/images/docs-quickstart/cluster-config.png)

## 4. 配置存储

选择 nfs 存储，按照文字提示填写相应内容

![](/images/docs-quickstart/cluster-storage-config.png)

## 5. 安装完成

完成所有配置确认安装

![](/images/docs-quickstart/cluster-finish.png)

安装成功，集群正常运行

![](/images/docs-quickstart/cluster-successful.png)

