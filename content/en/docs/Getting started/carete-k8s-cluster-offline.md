---
title: "Create kubernetes clusters offline using the kubeclipper platform"
linkTitle: "create kubernetes cluster offline"
weight: 2
description: >
  How to create a kubernetes cluster offline using the KC platform
---

## 1. Go to the creation screen

Log in to the `Kubeclipper` platform and click the button as shown in the figure to enter the cluster creation interface

![](/images/docs-quickstart/cluster-begin.png)

## 2. Configure cluster nodes

Follow the text prompts to complete the steps of entering the cluster name and selecting nodes

Note: The number of master nodes cannot be an even number.

![](/images/docs-quickstart/cluster-node-config.png)

## 3. Configure cluster

This step is used to configure the cluster network and components such as the database and container runtime

Select offline installation and fill in the address of the image repository you have built first

![](/images/docs-quickstart/cluster-config.png)

## 4. Configure cluster storage

Select nfs storage and follow the text prompts to fill in the appropriate fields

![](/images/docs-quickstart/cluster-storage-config.png)

## 5. Installation completed

Complete all configurations to confirm installation

![](/images/docs-quickstart/cluster-finish.png)

Installation is successful and the cluster is up and running

![](/images/docs-quickstart/cluster-successful.png)

