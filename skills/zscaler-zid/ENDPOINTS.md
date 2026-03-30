<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# ZIdentity (ZID) API Reference

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

