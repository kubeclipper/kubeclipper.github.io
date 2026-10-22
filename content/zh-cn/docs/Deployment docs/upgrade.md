---
title: "升级检查"
linkTitle: "升级检查"
weight: 2
description: >
  升级 KubeClipper 平台前后的检查与验证。
---

平台升级与受管 Kubernetes 集群升级分别处理。本文介绍 KubeClipper 平台升级前后的检查，不承诺任意旧版本都可直接升级到 1.7。

## 升级前

1. 记录 Server、Agent、kcctl 和 Console 的版本及节点拓扑，确认目标包的 CPU 架构。
2. 查看目标版本的 Release、安全公告和配置变化。1.7 改用 Operation v2，旧操作记录和任务状态需要在测试环境核对。
3. 在没有运行中安装、升级、备份等操作的窗口执行。先处理未完成或失败的操作。
4. 备份平台 etcd、Server/Agent 配置、证书与持久化认证密钥，并验证恢复方法。受管集群的数据备份需要单独安排。
5. 在可恢复的测试环境演练目标升级路径，记录服务中断和恢复步骤。

```bash
kcctl version
kcctl status
kcctl doctor
kcctl operation list
kcctl upgrade -h
```

## 执行升级

`kcctl upgrade` 支持整个平台或组件升级。目标包应满足命令帮助中的目录结构，并已经在测试环境验证；不要把客户端包当成平台升级包。

```bash
UPGRADE_PACKAGE=/path/to/validated-upgrade-package.tar.gz
kcctl upgrade all --pkg "$UPGRADE_PACKAGE"
```

只有 Release 或已验证部署流程明确支持时，才使用在线升级或组件独立替换。不要把替换一个二进制文件视为整个升级完成。

## 升级后

再次检查 `kcctl status`、`kcctl doctor`，核对各节点实际运行版本。验证登录、节点信息、操作详情与日志、受管集群访问及 Console 基本流程。测试一个受控的生命周期操作，确认 Operation 和实际集群状态一致。

升级失败时保留错误和日志，按事先验证的恢复步骤处理。恢复旧二进制前先判断数据和配置是否仍兼容，不要在未知状态下反复覆盖服务。
