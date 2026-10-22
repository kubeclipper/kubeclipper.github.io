---
title: "平台诊断"
linkTitle: "平台诊断"
weight: 8
description: >
  使用 status、doctor 和节点日志排查平台异常。
---

先确定故障发生在平台、Agent、资源下载还是 Kubernetes 集群，再针对对应层排查。

## 平台状态

```bash
kcctl version
kcctl status
kcctl status -o json
kcctl doctor
```

`status` 汇总 kc-server、kc-etcd 和 kc-agent 的健康状态。`doctor` 检查本地访问、服务、平台 etcd 和 Agent，并输出失败证据。非健康结果会返回非零退出码，适合用于检查脚本；两个命令都不会自动修复环境。

若平台 API 无法访问，检查 `kcctl login` 使用的地址是否为 HTTPS API 入口，默认端口 8080。检查本地登录和部署配置，以及部署机到各节点的 SSH 连通性。

## 节点服务

在对应的 Linux 节点执行：

```bash
sudo systemctl status kc-server kc-etcd kc-agent --no-pager
sudo journalctl -u kc-server -n 100 --no-pager
sudo journalctl -u kc-agent -n 100 --no-pager
```

只部署 Agent 的节点不应要求存在 Server 或平台 etcd 服务。结合实际节点角色解读结果，并检查磁盘、时间同步、管理地址和防火墙。

## 部署失败

预检查错误会指出检查项和节点。若服务已存在，先确认该节点是否属于正在使用的平台；不要删除服务来绕过检查。下载错误应核对地址、证书、文件大小和包内容，不能用关闭证书校验掩盖错误。

## 集群任务失败

```bash
kcctl operation list -c demo
kcctl get cluster demo -o yaml
kcctl get node
kcctl resource list
```

通过[操作与日志](/docs/tutorials/operations/)定位具体步骤和节点。离线安装核对版本、架构和资源包；镜像拉取失败核对镜像仓库地址、认证和网络。提交 Issue 时提供版本、拓扑、脱敏后的错误和操作 ID，移除密码、token、私钥与 kubeconfig 凭据。
