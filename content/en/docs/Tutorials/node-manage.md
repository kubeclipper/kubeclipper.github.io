---
title: "Node & Zone Management"
date: 2022-08-16
weight: 2
description: >
  A short lead description about this content page. It can be **bold** or _italic_ and can be split over multiple paragraphs.
---

On the \"Node Information\" page, you can view the list of all nodes managed in the platform, node specifications, status and other information. Click the node name to enter the node details page, you can view detailed node basic information and system information.

![](/images/docs-tutorials/node-info.png)

The node status in KubeClipper represents the management status of the node by kc-gent. Under normal circumstances, the node status is displayed as \"Ready\". When the node is out of contact for 4 minutes (within 10s of the error time), the status will be updated to \"Unknown\". Nodes with unknown status cannot perform any operations, nor can they create clusters or add/remove nodes for clusters.

## **Add node**

When deploying KubeClipper, you can add the initial server nodes which are used to deploy KubeClipper\'s own services, and agent nodes which are used to deploy K8S clusters. In a KubeClipper environment for experimentation or development, you can add a server node as an agent node at the same time. However, if it is used in a production environment, it is recommended not to reuse the server node as an agent node.

You can also use the kcctl join command to add agent nodes to KubeClipper, and mark a region for each agent node. The region can be a physical or logical location. You can use nodes in the same region to create a K8S cluster, but you cannot use nodes across regions to create a cluster. Nodes in unmarked regions belong to the default region. For details, see \"Kcctl Operation Guide\".

Command line example:

```Plaintext
kcctl join --agent beijing:1.2.3.4 --agent shanghai:2.3.4.5
```

## **Remove node**

When you no longer need some nodes, you can use the kcctl drain command to remove nodes from the platform. See \"Kcctl Operation Guide\" for details.

Command line example:

```Plaintext
kcctl drain --agent 192.168.10.19
```

## **Connect Terminal**

On the node list page, you can click the \"Connect Terminal\" button on the right side of the target node, enter the node port and username password information in the pop-up window, access the node SSH console and execute the command.

![](/images/docs-tutorials/node-terminal.png)
