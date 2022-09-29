---
title: "Access control"
date: 2022-08-16
weight: 3
description: >
  A short lead description about this content page. It can be **bold** or _italic_ and can be split over multiple paragraphs.
---

## **Create user**

After installing KubeClipper, you need to create a user for the desired role. Initially, the system has only one user, admin, by default, with the platform administrator role.

Click \"Access Control\" \> \"Users\" to enter the user management page, click the \"Create User\" button in the upper left corner, fill in the user name, password, mobile phone number, email and other information in the pop-up window, specify the user role, and click the \"OK\" button. The four built-in roles in the system are as follows:

- Platform administrator: have platform configuration, cluster management, user management and other platform viewing and operation rights.

- Cluster Administrator: Have all cluster management rights.

- User Administrator: Have all user management rights.

- Platform read-only users: have platform viewing rights.


After the user is created, you can view the user details and login logs on the user details page and do the following:

- Edit: Edit user alias, role, mobile phone number, email information.

- Edit Password: Edit the user login password.

- Delete: Delete the user.


## **Create a custom role**

In addition to system built-in roles, you can also create custom roles to meet business needs.

Click \"Access Control\" \> \"Roles\" to enter the role management page. You can click the \"Create Role\" button in the upper left corner to create a custom role.

On the Create Role page, you need to fill in the role name and description, and check the permissions required to customize the role. Some permissions depend on other permissions. When these permissions are selected, the dependent permissions will be automatically selected.

After creating a custom role, you can view the basic role information, role permission list, authorized user list on the role details page, and perform the following operations for the custom role:

- Edit: Edit the custom role alias.

- Edit permissions: Edit permissions under the custom role.

- Delete: To delete a custom role, make sure that no user is using the role to be deleted.


## **Access to external users**

KubeClipper can log in using external users via the OIDC protocol .

First, the platform administrator needs to log in to the platform server node and insert the following information under authentication in the kubeclipepr-server.yaml file:

```Plain
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

Under \"provider\", you need to fill in the clientID , clientSecret , and issuer information of your OAuth2 service, taking keycloack as an example, as shown in the figure below.

RedirectURL example: http://172.0.0.90/oauth2/redirect/keycloack

![](/images/docs-tutorials/keycloak-client.png)

![](/images/docs-tutorials/keycloak-client2.png)

OAuth2 users can access and use the KubeClipper platform by following these steps:

1. Click the \"OAuth2 Login\" button on the login page, enter the OAuth2 login page, enter the username and password to log in, enter the KubeClipper platform. When logging in for the first time, you will not be able to access the platform because you have not been granted any permission.

2. The platform administrator or other user with user management rights log in to KubeClipper, find the target OAuth2 user on the user management page, and set the user role by editing the user information.

3. The OAuth2 user repeats the first step, logs in to KubeClipper, and can access the platform normally and perform operations within the role permissions.
