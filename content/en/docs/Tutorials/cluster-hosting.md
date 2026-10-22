---
title: "Cluster hosting"
date: 2022-11-29
weight: 3
description: >
  For kubernetes clusters running outside the kubeclipper platform, you can host them within the kubeclipper platform for management. The current version supports host kubeadm clusters.
---

## Kubeadm cluster hosting

For a host cluster created and managed by kubeadm, kubeclipper gets the cluster and node information from the kubeconfig file and imports it into the kubeclipper platform.

Click "Cluster Management" > "Cluster Hosting" button to enter the cluster hosting page. Click "Add" button at the upper left corner. In the pop-up window of Add Provider, fill in the provider name (such as kubeadm-demo) and description, and then fill in the following information:

- Region: The region of the cluster and node in the kubeclipper platform.
- Provider type: Select kubeadm.
- SSH: Specifies the connection method of cluster nodes. Private Key or Password can be selected. Ensure that all cluster nodes can be connected through the selected method.
  - Private Key: enter the node user name and private key information.
  - Password: enter the node user name and password.

- Cluster name: Specifies the display name on the platform and cannot be the same as any other clusters.
- KubeConfig: The KubeConfig file of the host cluster.

Click the "OK" button to import the cluster and node into the platform. Click the provider name (kubeadm-demo) to enter the Provider detail page, where you can view the cluster under the provider and perform the following operations on the provider:

- Synchronization: Kubeclipper synchronizes cluster information every four hours. You can also click "Synchronize" to manually perform the operation.
- Edit: Edit the provider's name, description, access information, and node connection method.
- Remove: Detach platform management while preserving Kubernetes itself. Cleanup also removes imported kc-agent installations and platform-created ServiceAccount, ClusterRoleBinding, and kubectl terminal resources. Previously managed nodes follow separate preservation rules. Check node ownership and retain kubeconfig before removal.

## Managed cluster management

You can choose "Cluster Management" > "Cluster" to go to the cluster list page and view the list of all clusters, including hosted clusters and local clusters. The following table lists the operations supported by different clusters:

Image sources for plug-ins and external storage depend on the selected component package and configuration. Prepare images before offline installation and confirm that every node can pull them. Configure the [CRI registry](/en/docs/tutorials/registries/) first when authentication or a private CA is required.

| Function                    | Clusters created by Kubeclipper | Hosted kubeadm cluster |
| --------------------------- | ------------------------------- | ---------------------- |
| View log                    | ✔                               | ✔                      |
| Retry after failed task     | ✔                               | ✔                      |
| Access Kubectl              | ✔                               | ✔                      |
| Edit                        | ✔                               | ✔                      |
| Save as template            | ✔                               | ✘                      |
| CRI Registry                | ✔                               | ✔                      |
| Add/remove cluster nodes    | ✔                               | ✔                      |
| Cluster Backup and Recovery | ✔                               | ✔                      |
| Version Upgrade             | ✔                               | ✘                      |
| Delete cluster              | ✔                               | ✘                      |
| Remove cluster (provider)   | /                               | ✔                      |
| Reset status                | ✔                               | ✔                      |
| Cluster plugin management   | ✔                               | ✔                      |
| Update cluster certificate  | ✔                               | ✔                      |
| View kubeconfig file        | ✔                               | ✔                      |
