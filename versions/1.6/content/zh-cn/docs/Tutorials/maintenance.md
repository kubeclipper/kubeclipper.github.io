---
title: "诊断与升级检查"
linkTitle: "诊断与升级检查"
weight: 3
---

1.6 不包含 1.7 的 `kcctl status` 和 `kcctl doctor`。从版本、API、节点服务和任务日志开始排查。

```bash
kcctl version
kcctl get node
kcctl get cluster
kcctl operation list
kcctl resource list
```

在 Linux 节点按实际角色检查 systemd 服务，保留错误日志。NATS、平台 etcd 和 Server 的故障需要分别定位。

```bash
sudo systemctl status kc-server kc-agent kc-etcd kc-nats --no-pager
sudo journalctl -u kc-server -n 100 --no-pager
sudo journalctl -u kc-agent -n 100 --no-pager
sudo journalctl -u kc-nats -n 100 --no-pager
```

Agent 节点不一定部署 Server、etcd 或 NATS，使用外部 NATS 时也不会有本地 kc-nats 服务。核对实际角色及部署配置。

## 升级到 1.7 前

备份平台 etcd、配置、证书、认证密钥及受管集群数据。在可恢复的测试环境验证升级路径，重点核对 NATS 到 Operation v2 的差异、运行中任务及旧操作记录。查看[1.7 升级检查](https://kubeclipper.io/v1.7/docs/deployment-docs/upgrade/)，并确认实际运行的全部组件版本。

本页不承诺所有 1.6 部署都可直接原地升级。失败时先保留日志并按演练过的恢复步骤处理。
