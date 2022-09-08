---
title: "Cluster management"
date: 2022-08-16
weight: 1
description: >
  A short lead description about this content page. It can be **bold** or _italic_ and can be split over multiple paragraphs.
---

## **Create a kubernetes cluster**

You can create a kubernetes cluster through the wizard-style page, and install the required plugins such as CNI and CSI. You can also save the cluster template in advance, and create a cluster quickly after selecting the template.

## **Prepare to create a cluster**

1. You need to have enough available nodes. To add nodes, refer to \"Add Nodes\".

2. Prepare the image or binary files of K8S, CRI, calico, CSI and other plug-ins that need to be installed. You can choose online/offline according to the network environment of the platform, and then choose the recommended K8S version on page. You can also upload the image required for deployment to your own image repository in advance, and specify the image repository during deployment. For more installation configuration, refer to \"Cluster Configuration Guide\".


## **Create a single-node experimental cluster**

1. Click \"Cluster Management\" \> \"Cluster\" to enter the cluster list page, and click the \"Create Cluster\" button in the upper left corner.

2. Enter the \"Node Configuration\" page of the Create Cluster Wizard page. Fill in the \"Cluster Name\", such as \"test\", without selecting \"Cluster Template\". Select an available node, add it as a control node, and remove the taint from the master node in the taint management list. Click the \"Next\" button.

![](/images/docs-tutorials/select-node.png)

3. Enter the \"Cluster Configuration\" page of the Create Cluster Wizard page. Select \"Offline Installation\", no need to specify \"Mirror Repository\", retain the default values for other configurations, click the \"Quick Create\" button, jump to the configuration confirmation page, and click the \"OK\" button.

4. The experimental cluster of a single node is created. You can view the cluster details on the cluster details page, or click the \"ViewLog\" button to view the real-time log during the cluster creation process.


## **Create a cluster using a mirror repository**

If you create a cluster that contains large images, it is recommended that you upload all images to a specific image repository, the creating process will be faster and smoother.

1. Add a mirror repository. Click \"Cluster Management\" \> \"Mirror Repository\" to enter the mirror repository list page, and click the \"Add\" button in the upper left corner. Enter the IP address of the repository where the mirror is stored in the pop-up window of adding a mirror repository, and click the \"OK\" button.

2. Create a cluster. Click \"Cluster Management\" \> \"Cluster\" to enter the cluster list page, and click the \"Create Cluster\" button in the upper left corner. Configure the cluster nodes as needed. In the \"Mirror Repository\" of the \"Cluster Configuration\" page, select the mirror repository added in the first step, and create the cluster after completing other configurations of the cluster as needed.


## **Create a cluster using the cluster template**

You can use cluster templates to simplify the cluster creation process.

1. Add a template. There are two ways to save a template. You can add a cluster template on the \"Cluster Management\" \> \"Template Management\" page, and select the template when creating a new cluster. You can also save the existing cluster configuration as a template by clicking \"More\" \> \"Save as Template\" in the cluster operation, so as to create a K8S cluster with the same configuration as the former cluster.

2. Create a cluster. Click \"Cluster Management\" \> \"Cluster\" to enter the cluster list page, click the \"Create Cluster\" button in the upper left corner, enter the cluster creation page, fill in the \"cluster name\", such as \"demo\", select the cluster template saved in the first step, Add the required nodes, click the \"Quick Create\" button in the lower right corner, jump to the \"Configuration Confirmation\" page, after checking the template information, click the \"OK\" button to create a cluster.


## **Cluster Configuration Guide**

### **Node configuration steps**

On the node configuration page, you can configure the node as follows:

- Region: The region to which the cluster belongs. When adding a node, a physical or logical region can be specified for the node. The K8S cluster created by the node under this area also belongs to this region. Creating a cluster using multiple regional nodes is not supported.

- Control Nodes: Specify an odd number of control nodes for the cluster. The production environments generally use 3 control nodes to achieve high availability.

- Worker nodes: Add worker nodes to the new cluster according to the business size.

- Taint management: You can configure taint for added nodes, kubeclipper will automatically add no schedule taint to the control nodes, and you can also make changes as needed.

- Node Labels: You can configure labels for added cluster nodes as needed.


You can configure the required nodes according to your business needs. If you need to create a non-highly available experimental cluster, you can also add only one control node, and remove the taint automatically added for the control node. For details, see \"Creating a Single-Node Experimental Cluster\".

### **Cluster configuration steps**

On the cluster configuration page, you can configure the cluster as follows:

Installation method and mirror repository:

| Page configuration                                           | Configure Package/Image Sources                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Online** (public network environment)**Mirror repository** is empty | Configuration package source: Download from kubeclipper.io.Image pull method: The image is pulled from the official image repository by default, such as k8s image pulled from k8s.gcr.io, calico pulled from docker.io. |
| **Online** (public network environment)**Mirror repository** specification | Configuration package source: Download from kubeclipper.io.Image pull method: Pull from the filled mirror repository. The components will inherit the repository address by default. Please ensure that the repository has the related component images. You can also set an independent mirror repository for a specific component, and the component image will be pulled from this address. |
| **Offline** (intranet environment)**Mirror repository** is empty | Configuration package source: Download from the local kubeclipper cluster server node, you can use the "kcctl resource list" command to check the available configuration packages, or use the "kcctl resource push" command to upload the required configuration packages.Image pull method: Download from the local kubeclipper cluster server node. CRI will import the image after downloading. You can use the "kcctl resource list" command to check the available image packages, or use the "kcctl resource push" command to upload the required image packages. |
| **Offline** (intranet environment)**Mirror repository** specification | Configuration package source: Download from the local kubeclipper cluster server node, you can use the "kcctl resource list" command to check the available configuration packages, or use the "kcctl resource push" command to upload the required configuration packages.Image pull method: Pull from the filled mirror repository. The components will inherit the repository address by default. Please ensure that the repository has the related component images. You can also set an independent mirror repository for a specific component, and the component image will be pulled from this address. kubeclipper provides the Docker Registry and uses the kcctl registry command for management. You can also use your own image repositories. |

- K8S version: Specify the cluster K8S version. When you choose to install offline, you can choose from the K8S version of the configuration package in the current environment; when you choose to install online, you can choose from the officially recommended version of kubeclipper.

- ETCD Data Dir: You can specify the ETCD data directory, the default is /var/lib/etcd.

- CertSANs: The IP address or domain name of the k8s cluster ca certificate signature, more than one can be filled in.

- Container Runtime: According to the specified K8S version, the default container runtime is Docker for K8S version before v1.20.0, the default container runtime is Contianerd after v1.20.0; Docker is not supported after v1.24.0.

- Container Runtime version: Specify the containerd/docker version. As with K8S, when you choose to install offline, you can choose from the version of the configuration package in the current environment; when you choose to install online, you can choose from the officially recommended version of kubeclipper.

- Containerd data Path: The \"root dir\" in the config.toml configuration can be filled in. The default is /var/lib/containerd.

- Docker data Path: The \"root dir\" in the daemon.json configuration can be filled in . The default is /var/lib/docker.

- Containerd image repository: The repository address where the containerd image is stored, the \"registry.mirrors\" in the config.toml configuration, more than one can be filled in.

- Docker image repository: The repository address where the Docker image is stored, the insecure registry in the daemon.json configuration, more than one can be filled in.

- DNS domain name: The domain name of the k8s cluster, the default is cluster.local.

- Worker load IP: Used for load balancing from worker nodes to multiple masters, a single master does not need to be set.

- External access IP: You can fill in a floating IP for user access, which can be empty.


### **CNI configuration**

The current version kubeclipper only supports Calico as cluster CNI.

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


### **Storage configuration**

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

By default, multiple NFS storage types can be connected. Click the \"Continue to add\" button below to add another NFS storage. Note that the storage class name cannot be repeated.

After setting up the external storage, the card below will show the storages you have enabled. You can choose a storage class as the default storage. For PVCs that do not specify a specific StorageClass, the default storage class will be used.

## **Cluster operation log view**

On the cluster details page, click the \"operation log\" tab to view the cluster operation log list. Click the \"View Log\" button on the right side of an operation log to view the detailed logs of all steps and nodes in the pop-up window. Click the step name on the left to view the detailed log output of the execution steps.

During the execution of cluster operations, click View Log, you can view real-time log updates to trace the operation execution. For tasks that fail to execute, you can also view the log to find the execution steps and nodes marked with red dots, quickly locate errors, and troubleshoot the cause of operation failure.

![](https://zhc3o5gmf9.feishu.cn/space/api/box/stream/download/asynccode/?code=YmM4ZjUzODc3MThmZWIxNTVmODUzZmI1YzMzNzAxYTVfOVJ3QURVS2RnOWJrRTJiRHBPOWpDZEdpMWJZRU4yWm5fVG9rZW46Ym94Y25Xc3VmcE52dE1LNGJRRlRvTk9GTEtnXzE2NjA2MzQzNzE6MTY2MDYzNzk3MV9WNA)

## **Access cluster kubectl**

You can access the kubectl of the running cluster, click \"More\" \> \"Connect Terminal\" in the cluster operation, and you can execute the kubectl command line operation in the cluster kuebectl pop-up window.

## **Cluster plugin management**

In addition to installing plugins when creating a cluster, you can also install plugins for a running cluster. Taking the installation of storage plugins as an example, click the \"More\" \> \"Add Storage Item\" button in the cluster operation to enter the Add Storage Item page. You can install NFS plugins for the cluster. The installation configuration is the same as the configuration in cluster creation.

For installed plugins, you can view the plugin information on the cluster details page. You can click the \"Save as Template\" button in the upper right corner of the plugin card to save the plugin information as a template. You can also uninstall the cluster plugin by clicking the \"Remove\" button in the upper right corner of the plugin card.

## **Cluster node management**

On the \"Nodes\" list page of the cluster detail page, you can view the list of nodes in the current cluster, their specifications, status and role information.

### **Add cluster node**

When the cluster load is high, you can add nodes to the cluster to expand capacity. Adding nodes does not affect the running services.

On the cluster details page, under the Node List tab, click the \"Add Node\" button on the left, select the available nodes in the pop-up window, set the node labels, and click the \"OK\" button. The current version only supports adding worker nodes.

### **Remove cluster node**

On the cluster details page, under the Node List tab, you can remove a node by clicking the \"Remove\" button on the right of the node. The current version only supports removing worker nodes.

Note: To remove cluster nodes, you need to pay attention to security issues in production to avoid application interruptions.

## **Cluster version upgrade**

If the cluster version does not meet the requirements, you can upgrade the K8S version for the cluster. Similar to creating a cluster, you need to prepare the configuration package required for the cluster version and the K8S image of the target version and upload it to the specified location. For details, see \"Preparing to Create a Cluster\".

Click the \"More\" \> \"Cluster Upgrade\" button of the cluster operation. In the cluster upgrade pop-up window, select the installation mode and mirror repository, and select the target version of the upgrade. The installation method of the upgrade and the configuration of the K8S version are the same as those of creating a cluster. For details, please refer to \"Cluster Configuration Guide\".

Cluster upgrades can be performed across minor versions, but upgrades skipped over later versions are not supported. For example, you can upgrade from v1.20.2 to v1.20.13, or from v1.20.x to v1.21.x, but not from v1.20.x to v1.22.x. For version 1.23.x, upgrading to version 1.24.x is not currently supported.

The cluster upgrade operation may take a long time. You can view the operation log on the cluster details page to track the cluster upgrade status.

## **Cluster Backup and Recovery**

The backup of K8S cluster by KubeClipper mainly backs up ETCD database data, and k8s resource object, such as namespaces, deployments, configMaps. The files and data generated by the resource itself are not backed up. For example, the data and files generated by the mysql pod will not be backed up. Similarly, the files under the PV object of the file class are not backed up, only the pv object is backed up. The backup function provided by KubeClipper is hot backup, which does not affect cluster usage during backup. While KubeClipper is not against backing up during the \"busy period\" of the cluster, it also strongly disapproves of backing up during the \"busy period\" of the cluster.

### **Create a backup point**

Before performing a backup, you need to set a backup point for the cluster, that is, set the storage location of the backup files. The storage type of the backup point can be FS storage or S3 storage . The following are node local storage , NFS storage and MINIO storage as examples:

- ### **Node local storage (only for single-node experimental clusters):**

1. Create a storage directory. Connect to the cluster master node terminal (see Connect Nodes Terminal) and use the mkdir command to create the \"/root/backup\" directory in the master node.

2. Create a backup point. Click \"Cluster Management\" \> \"Backup Point\" to enter the backup point list page, click the \"Create\" button in the upper left corner, in the Create Backup Point pop-up window, enter \"Backup Point Name\", such as \"local\", select \"Storage Type\" as \"FS\", fill in \"Backup Path\", such as \"/root/backup\".

3. Set up a cluster backup point. When creating a cluster, select \"Backup Point\" as \"local\" on the \"Cluster Configuration\" page, or edit an existing cluster and select \"local\" in the \"Backup Point\" pop-up.


Note: Using a local node to store backup files does not require the introduction of external storage. The disadvantage is that if the local node is damaged, the backup files will also be lost, so it is strongly disapproved in a production environment .

- **NFS：**

1. Prepare NFS storage. Prepare an NFS service and create a directory on the NFS server to store backup files, such as \"/data/kubeclipper/cluster-backups\".

2. Mount the storage directory. Connect the cluster master node terminal (see Connect node Terminal), use the mkdir command to create the \"/data/kubeclipper/cluster-backups\" directory in each master node, and mount it to the /data/kubeclipper/cluster-backups directory of the NFS server. Command example: mount -t nfs {NFS\_IP}:/data/kubeclipper/cluster-backups /opt/kubeclipper/cluster-backups -o proto = tcp -o nolock.

3. Create a backup point. Click \"Cluster Management\" \> \"Backup Point\" to enter the backup point list page, click the \"Create\" button in the upper left corner, in the Create Backup Point pop-up window, enter \"Backup Point Name\", such as \"nfs\", select \"Storage Type\" as \"FS\", fill in \"Backup Path\" as \"/opt/kubeclipper/cluster-backups\".

4. Set up a cluster backup point. When creating a cluster, select \"Backup Point\" as \"nfs\" on the \"Cluster Configuration\" page, or edit an existing cluster and select \"nfs\" in the \"Backup Point\" pop-up.


- **MINIO：**

1. Prepare MINIO storage. Build MINIO services, refer to the official website https://docs.min.io/docs/minio-quickstart-guide.html for the deployment process, or use existing MINIO services.

2. Create a backup point. Click \"Cluster Management\" \> \"Backup Point\" to enter the backup point list page, click the \"Create\" button in the upper left corner, in the Create Backup Point pop-up window, enter \"Backup Point Name\", such as \"minio\", select \"Storage Type\" as \"S3\", fill in \"bucket name\", such as \"kubeclipper-backups\", the bucket will be automatically created by kubeclipper, fill in the IP and port number of the MINIO storage service in the first step in \"Endpoint\", fill in the service username and password, click the \"OK\" button.

3. Set up a cluster backup point. When creating a cluster, select \"backup point\" as \"minio\" on the \"Cluster Configuration\" page, or edit an existing cluster and select \"minio\" in the \"Backup Point\" pop-up.


You can view the list and details of all backup points on the \"Backup Points\" page of \"Cluster Management\" and do the following:

- Edit: Edit the backup point description, and the username/password of the S3 type backup point.

- Delete: Delete the backup point. If there are backup files under the backup point, deletion is not allowed.


### **Cluster backup**

You can back up your cluster ETCD data by clicking the \"More\" \> \"Cluster Backup\" button in the cluster operation.

You can view all backup files for the current cluster under the Backup tab on the cluster details page, and you can also perform the following operations for backups:

- Edit: Edit the backup description.

- Restore: Performs a cluster restore operation to restore the cluster to the specified backup state.

- Delete: Deletes the backup file.


### **Scheduled backup**

You can also create a timed backup for the cluster, click the \"More\" \> \"Scheduled Backup\" button in the cluster operation, in the timed backup pop-up window, enter the timed backup name, execution type ( repeat / only once) and execution time, and set the number of valid backups for repeated timed backups, and click the \"OK\" button.

kubeClipper will perform backup tasks for the cluster at the execution time you set, and the backup file will be automatically named \"Cluster Name - Timed Backup Name - Random Code\". For repeated timed backups, when the number of backup files exceeds the number of valid backup files, kubeClipper will automatically delete the later backup files.

After the scheduled backup is added, you can view the scheduled backup information on the \"Scheduled Backup\" tab of the cluster details page, and you can also view the backup files generated by the scheduled backup on the \"Backup\" tab.

For scheduled backup tasks, you can also perform the following operations:

- Edit: Edit the execution time of the scheduled backup task and the number of valid backups for repeated scheduled backups.

- Enable/Disable: Disabled scheduled backup tasks are temporarily stopped.

- Delete: Deletes a scheduled backup task.


### **Cluster Backup Restore**

If you perform restore operation while the cluster is running, KubeClipper will perform overlay recovery on the cluster, that is, backup the ETCD data in the file, overwriting the existing data .

You can click the \"Restore\" button on the right side of the backup under the Backup tab of the cluster details page; or click the \"More\" \> \"Restore Cluster\" button in the cluster operation, and select the backup to be restored in the Restore Cluster pop-up window. The current cluster can be restored to the specified backup state.

Note: After the K8S version of the cluster is upgraded, it will no longer be possible to restore the backup to the pre-upgrade version.
