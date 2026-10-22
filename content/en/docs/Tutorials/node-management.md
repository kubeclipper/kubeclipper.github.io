---
title: "Node management"
date: 2022-11-29
weight: 5
description: >
  KubeClipper supports node and cluster management across multiple regions.
---

## Region management

KubeClipper supports multi-region management. That is, all nodes and clusters managed by the platform are divided into physical or logical regions. On the Region Management page, you can view all regions in the platform. Click a region name to enter the region detail page, and you can view the clusters and nodes in the region.

![](/images/docs-tutorials/region-en.png)

## Node management

The platform supports multi-region management, that is, the owning region of all nodes managed by the platform. On the Region Management page, you can view all regions managed by the platform. Click a region name to go to the region details page, where you can view the list of all clusters and nodes in the region.

On the "Node Info" page, you can view the list of all nodes managed in the platform, node specifications, status and other information. Click the node name to enter the node detail page, you can view detailed node basic information and system information.

The node status in KubeClipper represents the management status of the node by kc-agent. Under normal circumstances, the node status is displayed as "Ready". The default monitoring grace period is 4 minutes, checked every 10 seconds. After the grace period, the status changes to "Unknown"; scheduling or communication delays can affect when the change becomes visible. Investigate the Agent, network, and Server connectivity before scheduling new cluster installation or expansion on an unknown node.

### **Add node**

When deploying KubeClipper, you can add the initial server nodes which are used to deploy KubeClipper\'s own services, and agent nodes which are used to deploy kubernetes clusters. In a KubeClipper environment for experimentation or development, you can add a server node as an agent node at the same time. However, if it is used for a production environment, it is recommended not to reuse the server node as an agent node.

You can also use the kcctl join command to add agent nodes to KubeClipper, and mark a region for each agent node. The region can be a physical or logical location. You can use nodes in the same region to create a kubernetes cluster, but cannot use nodes across regions to create a cluster. Nodes in unmarked regions belong to the default region.

Command line example:

```Plaintext
kcctl join --agent beijing:1.2.3.4 --agent shanghai:2.3.4.5
```

### **Remove node**

When you no longer need some nodes, you can use the kcctl drain command to remove nodes from the platform.

Command line example:

```Plaintext
kcctl drain --agent 192.168.10.19
```

### **Connect Terminal**

On the node list page, you can click the "Connect Terminal" button on the right side of the target node, enter the node port and username password information in the pop-up window, access the node SSH console and execute command tasks.

### Enable/disable a node

You can click the Disable button on the right side of the node to temporarily disable the node. The node in the disabled state cannot be created or added to the cluster.
