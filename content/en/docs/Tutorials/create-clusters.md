---
title: "Create clusters"
date: 2022-11-29
weight: 2
description: >
  KubeClipper supports the creation of kubernetes clusters via a wizard-style page.
---

### **Prepare to create a cluster**

1. You need to have enough available nodes. To add nodes, refer to \"[Add Nodes](/en/docs/tutorials/node-management/#add-node)\".

2. Prepare the image or binary files of kubernetes, CRI, calico, CSI and other plug-ins that need to be installed. You can choose online/offline according to the network environment of the platform, and choose the recommended kubernetes version on page. You can also upload the image required for deployment to your own image repository in advance, and specify the image repository during deployment. For more installation configuration, refer to \"[Cluster Configuration Guide](#cluster-configuration)\".


### **Create an AIO experimental cluster**

1. Click \"Cluster Management\" \> \"Cluster\" to enter the cluster list page, and click the \"Create Cluster\" button in the upper left corner.

2. Enter the \"Node Config\" page of the Create Cluster Wizard page. Fill in the \"Cluster Name\", such as \"test\", without selecting \"Cluster Template\". Select an available node, add it as a master node, and remove the taint from the master node in the taints list. Click the \"Next\" button.

![](/images/docs-tutorials/aioen.png)

3. Enter the \"Cluster Config\" page. Select \"Offline\" for "Image Type", retain the default values for other configurations, click the \"Create Quickly\" button, jump to the "Confirm Config" page, and click the \"Confirm\" button.

4. The experimental cluster of a single node is created. You can view the cluster details on the cluster details page, or click the \"ViewLog\" button to view the real-time log during the cluster creation process.


### **Create a cluster using a private registry**

If you create a cluster that contains large images, it is recommended that you upload the requred images to a private registry to speed up the installing process.

1. Add a private registry. Click \"Cluster Management\" \> \"Registry" to enter the registry list page, and click the \"Add\" button in the upper left corner. In the pop-up window, enter the name and address of the registry where the images are stored, and click the \"OK\" button.

2. Create a cluster. Click \"Cluster Management\" \> \"Cluster\" to enter the cluster list page, and click the \"Create Cluster\" button in the upper left corner. Configure the cluster nodes as needed. In the \"Private Registry\" of the \"Cluster Config\" page, select the registry added in the first step, and create the cluster after completing other configurations of the cluster as needed.


### **Create a cluster using the cluster template**

You can use cluster templates to simplify the cluster creation process.

1. Add a template. There are two ways to save a template. You can add a cluster template on the \"Cluster Management\" \> \"Template Management\" page, and select the template when creating a new cluster. You can also save the existing cluster configuration as a template by clicking \"More\" \>\"Cluster setings\"> \"Save as Template\" in the cluster operation, so as to create a kubernetes cluster with the same configuration as the former cluster.

2. Create a cluster. Click \"Cluster Management\" \> \"Cluster\" to enter the cluster list page, click the \"Create Cluster\" button in the upper left corner, enter the cluster creation page, fill in the \"cluster name\", such as \"demo\", select the cluster template saved in the first step. Add the required nodes, click the \"Create Quickly\" button in the lower right corner, jump to the \"Confirm Config\" page, after checking the template information, click the \"Confirm\" button to create a cluster.


### **Cluster Configuration Guide**

#### **Node configuration**

On the node config page, you can configure the node as follows:

- Region: The region to which the cluster belongs. When adding a node, a physical or logical region can be specified for the node. The kubernetes cluster created by the node under this region also belongs to this region. Creating a cluster with nodes from multiple regionals is not supported.

- Master Nodes: Specify an odd number of master nodes for the cluster. The production environments generally use 3 master nodes to achieve high availability.

- Worker nodes: Add worker nodes to the new cluster according to the business size.

- Taint management: You can configure taint for added nodes, kubeclipper will automatically add noschedule taint to the master nodes, and you can also make changes as needed.

- Node Labels: You can configure labels for added cluster nodes as needed.


You can configure the required nodes according to your business needs. If you need to create a non-highly available experimental cluster, you can also add only one master node, and remove the taint automatically added for the master node. For details, refer to \"[Creating an AIO Experimental Cluster](#create-an-aio-experimental-cluster)\".

#### **Cluster configuration**

On the cluster configuration page, you can configure the cluster as follows:

- Installation method and registry:
  - Online: public network environment
  - Offline: intranet environment

|             | no private registry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Specified private registry                                   |
| ----------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------ |
| **Online**  | Configuration package: Download from kubeclipper.io. <br />Images: The image is pulled from the official registry by default, for example, kubernetes image pulled from k8s.gcr.io, calico pulled from docker.io.                                                                                                                                                                                                                                                                                                                                   | Configuration package source: Download from kubeclipper.io.<br />Images: Pulled from the filled private registry. The components will inherit the registry by default. Please ensure that the required images are stored in the registry. You can also set an independent registry for a specific component, and the component image will be pulled from this registry. |
| **Offline** | Configuration package: Download from the local kubeclipper server nodes, you can use the "kcctl resource list" command to check the available configuration packages, or use the "kcctl resource push" command to upload the required configuration packages.<br />Images: Download from the local kubeclipper server nodes, and CRI will import the images after downloading. You can use the "kcctl resource list" command to check the available image packages, or use the "kcctl resource push" command to upload the required image packages. | Configuration package: Download from the local kubeclipper server nodes, you can use the "kcctl resource list" command to check the available configuration packages, or use the "kcctl resource push" command to upload the required configuration packages.<br />Images: Pulled from the filled private registry. The components will inherit the registry by default. Please ensure that  the required images are stored in the registry. You can also set an independent registry for a specific component, and the component image will be pulled from this address. kubeclipper provides the Docker Registry and uses the "kcctl registry" command for management. You can also use your own private registry. |

- kubernetes version: Specify the cluster kubernetes version. When you choose to install offline, you can choose from the kubernetes version of the configuration packages in the current environment; when you choose to install online, you can choose from the officially recommended versions by kubeclipper.

- ETCD Data Dir: You can specify the ETCD data directory, which defaults to /var/lib/etcd.

- kubelet Data Dir: You can specify the ETCD data directory, which defaults to /var/lib/kubelet.

- CertSANs: The IP address or domain name of the kubernetes cluster ca certificate signature, more than one can be filled in.

- Container Runtime: According to the specified kubernetes version, the default container runtime is Docker for kubernetes version before v1.20.0, the default container runtime is Contianerd after v1.20.0; Docker is not supported after v1.24.0.

- Container Runtime version: Specify the containerd/docker version. As with kubernetes, when you choose to install offline, you can choose from the version of the configuration package in the current environment; when you choose to install online, you can choose from the officially recommended version by kubeclipper.

- Containerd data Path: The \"root dir\" in the config.toml configuration can be filled in. which defaults to /var/lib/containerd.

- Docker data Path: The \"root dir\" in the daemon.json configuration can be filled in . which defaults to /var/lib/docker.

- Containerd registry: The registry address where the images are stored, the \"registry.mirrors\" in the config.toml configuration, more than one can be filled in.

- Docker registry: The registry address where the images are stored, the insecure registry in the daemon.json configuration, more than one can be filled in.

- DNS domain name: The domain name of the kubernetes cluster, which defaults to cluster.local.

- Worker load IP: Used for load balancing from worker nodes to multiple masters, no need to be set for a single master node cluster.

- External access IP: You can fill in a floating IP for user access, which can be empty.

- Backup space: Storage location of cluster backup files.


#### **CNI configuration**

The current version kubeclipper supports Calico as cluster CNI.

Calico divides the pod CIDR set by users into several blocks (network segments), dynamically allocates them to the required nodes according to business requirements, and maintains the routing table of the cluster nodes through the bgp peer in the nodes.

For example: container address pool: 172.25.0.0/16, dynamically allocated network segment pool: 172.25.0.0 - 172.25.255.192 (172.25.0.0/26 i.e. 10 bits), the number of dynamically allocated network segments: 1023, the number of pods per network segment: 61 (193-254), the total number of pods is 1023 \* 61 = 62403, the relative maximum number of nodes (according to the 200 service pod as the reference value): 312.

Clusters larger than 50 nodes are currently not recommended. Clusters larger than 50 nodes are recommended to manually configure route reflection to optimize the stability of routing table maintenance for nodes in the cluster.

To use Calico as the cluster CNI, you need the following configuration:

- Calico mode: 5 network modes are supported:
  - Overlay-IPIP-All: Use IP-in-IP technology to open up the network of pods of different nodes. Usually, this method is used in the environment where the underlying platform is IaaS. Of course, if your underlying network environment is directly a physical device, it is also completely can be used, but the efficiency and flexibility will be greatly reduced. It should be noted that you need to confirm that the underlying network environment (underlay) supports the IPIP protocol. (The network method using overlay will have a certain impact on network performance).
  - Overlay-Vxlan-All: Use IP-in-IP technology to open up the network of pods of different nodes. Usually, this method is used in the environment where the underlying platform is IaaS. Of course, if your underlying network environment is directly a physical device, it is also completely can be used, but the efficiency and flexibility will be greatly reduced. In theory, it can run on any network environment. Usually, we will use it when the underlying environment does not support the IPIP protocol. (The network method using overlay has a certain impact on network performance).
  - BGP : Use IP-in-IP technology to open up the network of pods of different nodes. Usually this method is used in a bare metal environment. Of course, if the Iaas platform supports BGP, it can also be used. In this mode, the IP communication of pods is accomplished by exchanging routing tables among nodes in the cluster. If you need to manually open up the pod network between multiple clusters, you need to pay attention that the addresses you assign should not conflict.
  - Overly-IPIP-Cross-Subnet: Use IP-in-IP technology to open up the network of pods of different nodes. Usually this method is used in the environment where the underlying platform is IaaS . It should be noted that you need to confirm the underlying network environment (underlay) supports the IPIP protocol. The difference with Overlay-IPIP-All is that if two upper Pods of different nodes in the same network segment communicate with each other through the routing table, the efficiency of upper Pods of different nodes in the same network segment can be improved.
  - Overly-Vxlan-Cross-Subnet: The logic is similar to that of Overly-IPIP-Cross-Subnet.
- IP version: The IP version can be specified as IPV4 or IPV4 IPV6 dual stack.
- Service subnet: Fill in the service subnet CIDR, v4 defaults to: 10.96.0.0/16, v6 defaults to fd03::/112, note that the Service network must not overlap with any host network.
- Pod CIDR: Fill in the pod subnet CIDR, v4 default: 172.25.0.0/24, v6 default is fd05::/120, note that the Pod network must not overlap with any host network.
- The bottom layer of the pod network:
  - First-found (default): The program will traverse all valid IP addresses (local, loop back, docker bridge, etc. will be automatically excluded) according to ipfamily (v4 or v6). Usually, if it is a multi-network interface card, it will exclude the default gateway. The network interface card ip other than the gateway will be used as the routing address between nodes.
  - Can-reach: Set the routing address between nodes by checking the reachability of the domain names or IP addresses.
  - Interface: Get all network interface card device names that satisfy the regular expression and return the address of the first network interface card as the routing address between nodes.
- MTU: Configure the maximum transmission unit (MTU) for the Calico environment. It is recommended to be no larger than 1440. The default is 1440. See <https://docs.projectcalico.org/networking/mtu> for details.


#### **Storage configuration**

The current version of Kubeclipper supports NFS as external storage types.

- **Connect to NFS storage**

For NFS type external storage, you need to set the following:

| Field            | Function description                                         | description/optional                                         |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ServerAddr       | ServerAddr, the service address of NFS                       | Required                                                     |
| SharedPath       | SharedPath, the service mount path for NFS                   | Required                                                     |
| StorageClassName | StorageClassName, the name of the storage class              | The default is nfs-sc, the name can be customized, and it cannot be repeated with other storage classes in the cluster |
| ReclaimPolicy    | ReclaimPolicy, VPC recovery strategy                         | Delete/Retain                                                |
| ArchiveOnDelete  | ArchiveOnDelete, whether to archive PVC after deletion       | Yes/No                                                       |
| MountOptions     | MountOptions, the options parameter of NFS, such as nfsvers = 4.1 | Optional, you can fill in several                            |
| Replicas         | Replicas, number of NFS provisioners                         | Default is 1                                                 |

After setting up the external storage, the card below will show the storages you have enabled. You can choose a storage class as the default storage. For PVCs that do not specify a specific StorageClass, the default storage class will be used.

#### Configuration Confirm

You can check the cluster configuration information on the Confirm Config page. After confirming the information, click Confirm. You can also click the "Edit" button of each card to skip back to the corresponding step to modify the cluster information.

The cluster installation may take several minutes. You can check the operation logs on the cluster detail page to track the cluster installation status.
