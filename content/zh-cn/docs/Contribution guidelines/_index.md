---
title: "贡献指南"
linkTitle: "贡献指南"
weight: 6
description: >
  如何为 kubeclipper 做贡献
---

文档存放在 [kubeclipper.github.io](https://github.com/kubeclipper/kubeclipper.github.io)，中文和英文分别位于 `content/zh-cn` 与 `content/en`。提交修改时请尽量同步两种语言；暂时无法翻译时，在 PR 中说明。

1. Fork 文档仓库，修改对应页面。功能和版本信息请以已发布的软件版本为准，不把规划中的能力写成现状。
2. 按仓库 [README](https://github.com/kubeclipper/kubeclipper.github.io#readme) 安装依赖，在本地预览，并运行 `make check` 检查多版本构建和站内链接。
3. 提交 Pull Request，说明改了哪些页面、依据是什么，以及本地检查结果。若是一组面向用户的重要变化，可同时在[项目动态](/blog/)新增一篇简短更新。
4. 合并并发布后，核对线上页面与入口。构建成功不等于线上内容已经更新。

发现错误但暂时无法修改时，可[提交文档问题](https://github.com/kubeclipper/kubeclipper.github.io/issues/new)。软件问题请提交到[项目仓库](https://github.com/kubeclipper/kubeclipper/issues/new)。

