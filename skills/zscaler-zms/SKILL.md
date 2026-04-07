---
name: zscaler-zms
version: 1.0.0
description: Use when working with Zscaler Microsegmentation (ZMS) — read-only inventory of agents, agent groups, provisioning keys (nonces), resources, resource groups, policy rules, app zones, app catalog, and tags via the MCP server. Write operations require the admin portal or SDK.
---

# Zscaler Microsegmentation (ZMS)

## Overview

ZMS provides identity-based microsegmentation for workloads. It enforces zero trust policy at the workload level by tagging resources, grouping them, and applying policy rules that control east-west traffic. Use this skill for inventorying ZMS state: agents, resources, policy rules, and app zones.

ZMS uses a GraphQL-based API. The `zscaler-mcp-server` exposes **20 read-only tools** under the `zms_` prefix. **No write operations** (create/update/delete) are available through MCP — those must be done via the ZMS admin portal or the Python SDK (`ZMSService`).

## MCP Tools

ZMS MCP tools are read-only. The full list:

### Agents
| Tool | Purpose |
|------|---------|
| `zms_list_agents` | List all agents |
| `zms_get_agent_connection_status_statistics` | Aggregate connection-status stats |
| `zms_get_agent_version_statistics` | Aggregate version stats |

### Agent Groups
| Tool | Purpose |
|------|---------|
| `zms_list_agent_groups` | List all agent groups |
| `zms_get_agent_group_totp_secrets` | Retrieve TOTP secrets for an agent group |

### Nonces (Provisioning Keys)
| Tool | Purpose |
|------|---------|
| `zms_list_nonces` | List provisioning nonces |
| `zms_get_nonce` | Get a single nonce |

### Resources
| Tool | Purpose |
|------|---------|
| `zms_list_resources` | List all resources |
| `zms_get_resource_protection_status` | Get protection status for a resource |
| `zms_get_metadata` | Get resource metadata |

### Resource Groups
| Tool | Purpose |
|------|---------|
| `zms_list_resource_groups` | List all resource groups |
| `zms_get_resource_group_members` | List members of a resource group |
| `zms_get_resource_group_protection_status` | Protection status of a resource group |

### Policy Rules
| Tool | Purpose |
|------|---------|
| `zms_list_policy_rules` | List configured policy rules |
| `zms_list_default_policy_rules` | List built-in default policy rules |

### App Zones
| Tool | Purpose |
|------|---------|
| `zms_list_app_zones` | List all app zones |

### App Catalog
| Tool | Purpose |
|------|---------|
| `zms_list_app_catalog` | List app catalog entries |

### Tags
| Tool | Purpose |
|------|---------|
| `zms_list_tag_namespaces` | List tag namespaces |
| `zms_list_tag_keys` | List tag keys |
| `zms_list_tag_values` | List tag values |

## Authentication

OneAPI OAuth2 with `client_credentials` grant.

- **Token endpoint:** `https://<vanity>.zslogin.net/oauth2/v1/token`
- **API type:** GraphQL

MCP tools handle authentication automatically via `.mcp.json` credentials.

## Common Patterns

### Inventory Active Agents

1. List all agents: `zms_list_agents`
2. Check connection health: `zms_get_agent_connection_status_statistics`
3. Check version distribution: `zms_get_agent_version_statistics`
4. Identify which agent group each belongs to via `zms_list_agent_groups`

### Audit Resource Protection Coverage

1. List resources: `zms_list_resources`
2. For each critical resource, check protection: `zms_get_resource_protection_status`
3. List resource groups: `zms_list_resource_groups`
4. Walk group members: `zms_get_resource_group_members`
5. Confirm group-level protection: `zms_get_resource_group_protection_status`

### Review Policy Rules

1. List configured rules: `zms_list_policy_rules`
2. List default (built-in) rules: `zms_list_default_policy_rules`
3. Cross-reference with resource groups to validate intended traffic flows

### Explore Tag Hierarchy

ZMS tags are namespaced (namespace → key → value).

1. List namespaces: `zms_list_tag_namespaces`
2. List keys in a namespace: `zms_list_tag_keys`
3. List values for a key: `zms_list_tag_values`

### Provision a New Agent (Write — Admin Portal or SDK)

Provisioning agents requires write operations not exposed via MCP. Workflow:

1. **Admin portal:** Settings → Provisioning → Generate Nonce
2. Deploy ZMS agent on the workload using the nonce
3. Verify registration via MCP: `zms_list_agents`
4. Assign agent to group via the admin portal or `ZMSService` Python SDK

## Known Limitations

- **Read-only via MCP** — no `create_*`, `update_*`, or `delete_*` tools exist
- **Write operations** require the admin portal or the Python SDK (`from zscaler import ZscalerClient; client.zms.policy_rules.create(...)`)
- **Nonces are single-use** — generate a new one for each agent deployment
- **Default-deny policy** — all traffic flows must be explicitly permitted by a policy rule
- **GraphQL schema** — for SDK or direct API work, use Context7 to look up exact field names and mutation shapes

## MCP Server

The 20 read-only ZMS tools are provided by the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server). For write operations, use the Python SDK or the ZMS admin portal — the MCP server does not currently expose ZMS mutations.
