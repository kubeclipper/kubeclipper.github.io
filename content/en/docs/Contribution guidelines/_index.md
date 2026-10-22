---
title: "Contribution Guidelines"
linkTitle: "Contribution Guidelines"
weight: 6
description: >
  How to contribute to the docs
---

The documentation lives in [kubeclipper.github.io](https://github.com/kubeclipper/kubeclipper.github.io), with Chinese and English content in `content/zh-cn` and `content/en`. Update both languages when practical; otherwise, note the translation gap in your pull request.

1. Fork the documentation repository and edit the relevant page. Base version and feature claims on released software.
2. Follow the repository [README](https://github.com/kubeclipper/kubeclipper.github.io#readme) to install dependencies and preview locally. Run `make check` to build all versions and check local links.
3. Open a pull request describing the pages changed, evidence for technical claims, and local check results. For a substantial user-facing change, add a short [project update](/en/blog/).
4. After merge and publication, check the live pages and navigation. A passing build alone does not establish that the site has updated.

If you cannot make a correction yet, [open a documentation issue](https://github.com/kubeclipper/kubeclipper.github.io/issues/new). Report software issues in the [project repository](https://github.com/kubeclipper/kubeclipper/issues/new).
