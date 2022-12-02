---
title: "访问控制"
date: 2022-11-29
weight: 6
description: >
  KubeClipper 访问控制功能使用指南。
---

## 用户管理

安装 KubeClipper 之后，您需要创建所需角色的用户。一开始，系统默认只有一个用户 admin，具有平台管理员角色。

点击“访问控制”>“用户”，进入用户管理页面，点击左上角“创建用户”按钮，在弹窗中填写用户名、密码、手机号码、邮箱等信息，并指定用户角色，点击“确认”按钮。系统内置四个角色如下：

- 平台管理员：拥有集群管理、用户管理、审计管理等全部平台查看和操作权限。

- 集群管理员：拥有所有集群管理权限。

- 用户管理员：拥有所有用户管理权限。

- 平台只读用户：拥有全部平台查看权限。

用户创建完成后，您可以在用户详情页面查看用户详情信息，并执行以下操作：

- 编辑：编辑用户别名、角色、手机号、邮箱信息。

- 编辑密码：编辑用户登录密码。

- 删除：删除用户。

在用户详情页面，您还可以查看当前用户的登录日志列表。

您可以编辑平台 /etc/kubeclipper-server/kubeclipper-server.yaml 文件，根据需要设置用户登录日志的最大保留条数和保留期限，每个用户的登录日志超过最大条数后，超过最大条数和期限的日志会被自动删除，仅超过保留期限但未超过最大条数的日志数据将不会被删除。

## 自定义角色

除了系统内置角色，您也可以创建自定义角色，以满足业务需要。

点击“访问控制”>“角色”，进入角色管理页面，您可以点击左上角“创建角色”按钮，创建自定义角色。

在创建角色页面，您需要填写角色名称和描述，并勾选自定义角色所需权限，一些权限依赖于其他权限，在选择这些权限时，将自动选中依赖的权限。

创建自定义角色完成后，您可以在角色详情页面查看角色基本信息、角色权限列表、授权用户列表，并对自定义角色执行以下操作：

- 编辑：编辑自定义角色别名。

- 编辑权限：编辑自定义角色下的权限。

- 删除：删除自定义角色，需确保没有用户使用待删除角色。

## 接入外部用户

KubeClipper 可以通过 OIDC 协议使用外部用户登录。

首先，平台管理员需要登录平台 server 节点，在 kubeclipepr-server.yaml 文件中的 authentication 下插入以下信息：

```undefined
oauthOptions:
    identityProviders:
    - name: keycloak
      type: OIDC
      mappingMethod: auto
      provider:
        clientID: kc
        clientSecret: EErn729BB1bKawdRtnZgrqj9Bx0]mzUs
        issuer: http://172.20.163.233:7777/auth/realms/kubeclipper
        scopes:
        - openid
        - email
        redirectURL: http://{kc-console-address}/oatuh2/redirect/{IDP-Name}
```

其中，“provider” 下需要您填写自己的 OAuth2 服务的`clientID`、`clientSecret`、`issuer`信息，以 keycloack 为例，如下图所示。

![](/images/docs-tutorials/keycloak-clients.png)

![](/images/docs-tutorials/keycloak-secret.png)

 `redirectURL`示例：http://172.0.0.90/oauth2/redirect/keycloack

OAuth2 用户可以通过以下步骤访问和使用 KubeClipper 平台：

1. 点击登录页的 “OAuth2 登录”按钮，进入 OAuth2 登录页面，输入用户名密码登录，进入 KubeClipper 平台，首次登录，您会因未被授予权限而无法访问平台。
2. 平台管理员或其他拥有用户管理权限的用户登录 KubeClipper，在用户管理页面，找到目标 OAuth2 用户，通过编辑用户指定用户角色。
3. OAuth2 用户重复第一步，登录 KubeClipper，就可以正常访问平台并执行角色权限内操作。
