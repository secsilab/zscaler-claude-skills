---
name: zscaler-zid
description: Use when working with ZIdentity — user management, group management, API clients, resource servers, directory sync.
---

# ZIdentity (ZID)

## Overview
ZIdentity manages users, groups, and API clients across the Zscaler platform. Use for user/group CRUD, API client management, and identity governance.

## MCP Tools
Available: `zidentity_list_users`, `zidentity_get_user`, `zidentity_search_users`, `zidentity_get_user_groups`, `zidentity_get_user_groups_by_name`, `zidentity_list_groups`, `zidentity_get_group`, `zidentity_search_groups`, `zidentity_get_group_users`, `zidentity_get_group_users_by_name`.

## API Reference

### api-clients (8 endpoints)

#### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api-clients` | Apiclient Ops list |
| POST | `/api-clients` | Apiclient Ops add |

#### {id}

| Method | Endpoint | Description |
|--------|----------|-------------|
| DELETE | `/api-clients/{{id}}/secrets/{{secretsId}}` | Apiclient Ops delete Secret |
| GET | `/api-clients/{{id}}/secrets` | Apiclient Ops get Secrets |
| POST | `/api-clients/{{id}}/secrets` | Apiclient Ops add Secret |
| PUT | `/api-clients/{{id}}` | Apiclient Ops update |
| DELETE | `/api-clients/{{id}}` | Apiclient Ops remove |
| GET | `/api-clients/{{id}}` | Apiclient Ops get |

### resource-servers (2 endpoints)

#### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resource-servers` | Resource Servers Ops list |

#### {id}

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resource-servers/{{id}}` | Resource Servers Ops get |

### users (11 endpoints)

#### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Users Ops list |
| POST | `/users` | Users Ops add |

#### {id}

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{{id}}/admin-entitlements` | Users Ops get User Admin Entitlements |
| GET | `/users/{{id}}/groups` | Users Ops get User Groups |
| GET | `/users/{{id}}/service-entitlements` | Users Ops get User Service Entitlements |
| PUT | `/users/{{id}}` | Users Ops update |
| DELETE | `/users/{{id}}` | Users Ops remove |
| GET | `/users/{{id}}` | Users Ops get |

#### {id}:resetpassword

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/{{id}}:resetpassword` | Users Ops reset Password |

#### {id}:setskipmfa

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/{{id}}:setskipmfa` | Users Ops mfa |

#### {id}:updatepassword

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/users/{{id}}:updatepassword` | Users Ops update Password |

### groups (10 endpoints)

#### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/groups` | Groups Ops list |
| POST | `/groups` | Groups Ops add |

#### {id}

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/groups/{{id}}/users/{{userId}}` | Groups Ops add User |
| DELETE | `/groups/{{id}}/users/{{userId}}` | Groups Ops remove User |
| POST | `/groups/{{id}}/users` | Groups Ops add Users |
| PUT | `/groups/{{id}}/users` | Groups Ops put Users |
| GET | `/groups/{{id}}/users` | Groups Ops get Group Members |
| PUT | `/groups/{{id}}` | Groups Ops update |
| DELETE | `/groups/{{id}}` | Groups Ops remove |
| GET | `/groups/{{id}}` | Groups Ops get |

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zidentity/api/v1`

## Common Patterns
- Search users by name or email
- List group membership
- Manage API clients for automation

## Known Limitations
- MCP tools are read-only — write operations (create/update/delete users/groups) require Python SDK or direct API
- User write operations need `zidentity.users.manage` scope
