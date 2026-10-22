---
title: "Access control"
date: 2022-11-29
weight: 6
description: >
  KubeClipper access control usage guide.
---

## **Create user**

After installing KubeClipper, you need to create a user of a desired role. Initially, there is only one user, admin, by default, with the platform administrator role.

Click "Access Control" \> "Users" to enter the user management page, click the "Create User" button in the upper left corner, fill in the user name, password, alias name and other information in the pop-up window, specify the user role, and click the "OK" button. The four initial roles in the system are as follows:

- platform-admin: Platform administrator, with the authority to set platform, cluster management, user management, audit, etc.

- cluster-manager: Cluster administrator, with all cluster management permissions.

- iam-manager: User administrator, with all user management permissions.

- platform-view: Platform read-only user, with all platform viewing permissions.


After the user is created, you can view the user details and login logs on the user detail page and perform the following operations:

- Edit: Edit user alias, role, mobile phone number, email information.

- Edit Password: Edit the user login password.

- Delete: Delete the user.


## **Create a custom role**

In addition to system initial roles, you can also create customized roles to meet business needs.

Click "Access Control" \> "Roles" to enter the role management page. You can click the "Create Role" button in the upper left corner to create a custom role.

On the Create Role page, you need to fill in the role name and description, and check the permissions required. Some permissions depend on other permissions. When these permissions are selected, the dependent permissions will be automatically selected.

After creating a customized role, you can view the basic role information, role permission list, authorized user list on the role detail page, and perform the following operations:

- Edit: Edit the custom role description.

- Edit permissions: Edit permissions of the customized role.

- Delete: To delete a customized role, make sure that no user is using the role to be deleted.


## **Access to external users**

External users can log in to KubeClipper via the OIDC protocol .

First, the platform administrator needs to log in to the platform server node and insert the following information under "authentication" in the kubeclipper-server.yaml file:

```yaml
oauthOptions:
    identityProviders:
    - name: keycloak
      type: OIDC
      mappingMethod: auto
      provider:
        clientID: kc
        clientSecret: REPLACE_WITH_CLIENT_SECRET
        issuer: https://idp.example.com/realms/kubeclipper
        scopes:
        - openid
        - email
        redirectURL: https://console.example.com/oauth2/redirect/keycloak
```

Merge this fragment under `authentication` in the existing configuration. Replace the example domains and `REPLACE_WITH_CLIENT_SECRET`. Register exactly the same `redirectURL` with the IdP; its final path component must match the provider `name`. Update each Server and restart `kc-server` one node at a time.

Under "provider", you need to fill in the clientID , clientSecret , and issuer information of your OAuth2 service, taking keycloak as an example, as shown in the figure below.

![](/images/docs-tutorials/keycloak-clients.png)

![](/images/docs-tutorials/keycloak-secret.png)

RedirectURL example: https://console.example.com/oauth2/redirect/keycloak

OAuth2 users can log in to the KubeClipper platform by following these steps:

1. Click the "OAuth2 Login" button on the login page, enter the OAuth2 login page, fill in the username and password to enter the KubeClipper platform. When logging in for the first time, you will not be able to access the platform because you have not been granted any permission.

2. The platform administrator or other user with user management rights log in to KubeClipper, find the target OAuth2 user on the user management page, and set the user role by editing the user information.

3. The OAuth2 user repeats the first step, logs in to KubeClipper, and accesses the platform normally.