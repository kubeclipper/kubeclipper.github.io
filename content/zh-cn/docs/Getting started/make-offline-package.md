# 制作 K8S 组件离线安装包

本文档介绍如何制作 K8S 组件离线安装包，对于没有外网的环境，可以通过离线安装包进行安装。

当前 kubeclipper v1.4 版本离线部署包中仅包含以下 K8S 组件：

* k8s: v1.27.4
* containerd: v1.6.4
* calico: v3.26.1

对于有特殊需求的用户，可以通过本文档介绍的方法自行制作离线组件包，然后在 kubeclipper 中使用。

##    

## 1. 准备工作

按照 [文档](https://github.com/kubeclipper/kubeclipper) 部署好 kubeclipper，确保 `kcctl` 命令可以正常使用。

```bash
kcctl version
```

以下操作均在 kubeclipper 部署节点上执行，使用 `kcctl resource` 命令进行组件包上传。

## 2. 确认组件版本

根据以下两个表格信息，确认需要制作的组件包版本，使用推送脚本或者手动上传组件包到 kubeclipper。

`k8s 组件包表` 记录当前对象存储里已制作好的各类组件包，后续我们将逐步开源更多组件包以及打包脚本。  
`k8s 版本与组件推荐版本对应关系表` 记录了各个 k8s 版本对应的组件版本，可以根据自己的需求选择对应的组件版本。

#### k8s 版本与组件推荐版本对应关系表

| k8s 版本    | containerd 版本 | docker 版本 | calico 版本 |
|:----------|:--------------|:----------|:----------|
| v1.28.0   | v1.6.4        | -         | v3.26.1   |
| v1.27.4   | v1.6.4        | -         | v3.26.1   |
| v1.26.7   | v1.6.4        | -         | v3.26.1   |
| v1.25.4   | v1.6.4        | -         | v3.22.4   |
| v1.24.8   | v1.6.4        | -         | v3.22.4   |
| v1.23.9   | v1.6.4        | 20.10.20  | v3.22.4   |
| v1.23.6   | v1.6.4        | 20.10.20  | v3.22.4   |
| v1.22.12  | v1.6.4        | 20.10.20  | v3.22.4   |
| v1.21.14  | v1.6.4        | 20.10.20  | v3.22.4   |
| v1.20.15  | v1.6.4        | 20.10.20  | v3.16.10  |
| v1.19.16  | v1.6.4        | 20.10.20  | v3.16.10  |
| v1.18.20  | v1.6.4        | 20.10.20  | v3.16.10  |

#### k8s 组件包表

| 组件名称       | 版本       |
|:-----------|:---------|
| k8s        | v1.28.0  |
| k8s        | v1.27.4  |
| k8s        | v1.26.7  |
| k8s        | v1.25.4  |
| k8s        | v1.24.8  |
| k8s        | v1.23.9  |
| k8s        | v1.23.6  |
| k8s        | v1.22.12 |
| k8s        | v1.21.14 |
| k8s        | v1.20.15 |
| k8s        | v1.19.16 |
| k8s        | v1.18.20 |
| containerd | 1.6.4    |
| docker     | 20.10.20 |
| calico     | v3.26.1  |
| calico     | v3.22.4  |
| calico     | v3.21.2  |
| calico     | v3.16.10 |
| calico     | v3.11.2  |

## 3. 推送离线组件包到 kubeclipper

`push_component.sh` 脚本：

```bash
#!/usr/bin/env bash

set -e

if type kcctl &>/dev/null; then
  kcctl version
else
  echo "kcctl command not found, please install it first!"
fi

PKG_URL_PREFIX="https://oss.kubeclipper.io/packages"
fileList=()

name=$1
if [[ "${name}" != "k8s" ]] && [[ "${name}" != "calico" ]] && [[ "${name}" != "containerd" ]] && [[ "${name}" != "docker" ]]; then
  echo "only 'k8s', 'calico' packages are supported. default: $name"
  exit 1
fi
version=$2
if [[ -z "${version}" ]]; then
  echo "Please specify the package version!"
  exit 1
fi
arch=$3
if [[ "${arch}" != "amd64" ]] && [[ "${arch}" != "arm64" ]]; then
  echo "only 'amd64', 'arm64' architectures are supported. default: $arch"
  exit 1
fi

build_dir=${name}/${version}/${arch}
pkg_name=${name}-${version}-${arch}.tar.gz
pkg_type="k8s"

packaging() {
  case $name in
  k8s)
    fileList=(
      images.tar.gz
      configs.tar.gz
      manifest.json
    )
    pkg_type="k8s"
    ;;
  calico)
    fileList=(
      images.tar.gz
      manifest.json
    )
    if [[ "$(echo -e "3.26\n${version}" | sort -V | tail -n 1)" == "${version}" ]]; then
      fileList=(
        images.tar.gz
        charts.tgz
        manifest.json
      )
    fi
    pkg_type="cni"
    ;;
  containerd,docker)
    fileList=(
      configs.tar.gz
      manifest.json
    )
    pkg_type="cri"
    ;;
  esac

  for file in "${fileList[@]}"; do
    echo "download ${file}..."
    wget ${PKG_URL_PREFIX}/${build_dir}/${file} -P ${build_dir}
  done

  echo "packaging ${pkg_name}..."
  tar -zcvf ${pkg_name} ${build_dir}
  echo "packaging ${pkg_name} done"
  echo "push ${pkg_name} to kc..."
  kcctl resource push --pkg ${pkg_name} --type ${pkg_type}
  echo "push ${pkg_name} to kc done"
}

packaging
echo "clean up..."
rm -rf ${build_dir}
rm -rf ${pkg_name}
echo "clean up done"
```

使用 `push_component.sh` 脚本推送组件包到 kubeclipper：

```bash
chmod +x push_component.sh

# 推送 k8s 组件包
./push_component.sh k8s v1.23.9 amd64

# 推送 calico 组件包
./push_component.sh calico v3.22.4 amd64

# 推送 containerd 组件包
./push_component.sh containerd v1.6.4 amd64

# 推送 docker 组件包
./push_component.sh docker 20.10.20 amd64
```

## 4. 查看离线组件包

使用 `kcctl resource list` 命令查看已上传的离线组件包：

```bash
kcctl resource list
```

## 5. 使用离线组件包

登录 kubeclipper 控制台，点击`创建集群`，进入`集群配置`页，`镜像类型`选择`离线`，即可选择已上传的离线组件包。

![集群配置01](/images/docs-quickstart/cluster-config01.png)
![集群配置02](/images/docs-quickstart/cluster-config02.png)





