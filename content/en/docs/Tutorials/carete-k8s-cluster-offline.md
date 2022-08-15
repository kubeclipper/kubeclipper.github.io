---
title: "Create k8s clusters offline using the kubeclipper platform"
linkTitle: "create k8s cluster offline"
weight: 6
description: >
  How to create a k8s cluster offline using the KC platform
---

## 1. Go to the creation screen

Log in to the `Kubeclipper` platform and click the button as shown in the figure to enter the cluster creation interface

![](/images/docs/cluster-begin.png)

## 2. Configure cluster nodes

Follow the text prompts to complete the steps of entering the cluster name and selecting nodes

Note: The number of master nodes cannot be an even number.

![](/images/docs/cluster-node-config.png)

## 3. Configure cluster

This step is used to configure the cluster network and components such as the database and container runtime

Select offline installation and fill in the address of the image repository you have built first

![](/images/docs/cluster-config.png)

## 4. Configure cluster storage

Select nfs storage and follow the text prompts to fill in the appropriate fields

![](/images/docs/cluster-storage-config.png)

## 5. Configure cluster plugins

This step is used to install Kubesphere

Enter any string as a jwt key

![](/images/docs/cluster-plugin-config-jwt.png)

You can change the default memory parameters to avoid installation failure when the runtime environment has insufficient memory

![](/images/docs/cluster-plugin-config-memory.png)

Choose to install the plug-in according to your needs

![](/images/docs/cluster-plugin-install.png)

## 6. Installation completed

Complete all configurations to confirm installation

![](/images/docs/cluster-finish.png)

Installation is successful and the cluster is up and running

![](/images/docs/cluster-success.png)

