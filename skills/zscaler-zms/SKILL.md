---
name: zscaler-zms
version: 1.0.0
description: Use when working with Zscaler Microsegmentation (ZMS) — agents, agent groups, provisioning keys (nonces), resources, resource groups, policy rules, app zones, app catalog, and tags.
---

# Zscaler Microsegmentation (ZMS)

## Overview

ZMS provides identity-based microsegmentation for workloads. It enforces zero trust policy at the workload level by tagging resources, grouping them, and applying policy rules that control east-west traffic. Use this skill for managing the full ZMS lifecycle: deploying agents, provisioning resources, building policy rules, and managing app zones.

ZMS uses a GraphQL-based API. Operations are executed via the `zms_` MCP tool prefix.

## MCP Tools

ZMS operations use the `zms_` tool prefix. The primary modules and their operations:

### Agents
| Operation | MCP Tool |
|-----------|----------|
| List agents | `zms_list_agents` |
| Get agent | `zms_get_agent` |
| Update agent | `zms_update_agent` |
| Delete agent | `zms_delete_agent` |

### Agent Groups
| Operation | MCP Tool |
|-----------|----------|
| List agent groups | `zms_list_agent_groups` |
| Get agent group | `zms_get_agent_group` |
| Create agent group | `zms_create_agent_group` |
| Update agent group | `zms_update_agent_group` |
| Delete agent group | `zms_delete_agent_group` |

### Provisioning Keys (Nonces)
| Operation | MCP Tool |
|-----------|----------|
| List nonces | `zms_list_nonces` |
| Get nonce | `zms_get_nonce` |
| Create nonce | `zms_create_nonce` |
| Delete nonce | `zms_delete_nonce` |

### Resources
| Operation | MCP Tool |
|-----------|----------|
| List resources | `zms_list_resources` |
| Get resource | `zms_get_resource` |
| Create resource | `zms_create_resource` |
| Update resource | `zms_update_resource` |
| Delete resource | `zms_delete_resource` |

### Resource Groups
| Operation | MCP Tool |
|-----------|----------|
| List resource groups | `zms_list_resource_groups` |
| Get resource group | `zms_get_resource_group` |
| Create resource group | `zms_create_resource_group` |
| Update resource group | `zms_update_resource_group` |
| Delete resource group | `zms_delete_resource_group` |

### Policy Rules
| Operation | MCP Tool |
|-----------|----------|
| List policy rules | `zms_list_policy_rules` |
| Get policy rule | `zms_get_policy_rule` |
| Create policy rule | `zms_create_policy_rule` |
| Update policy rule | `zms_update_policy_rule` |
| Delete policy rule | `zms_delete_policy_rule` |

### App Zones
| Operation | MCP Tool |
|-----------|----------|
| List app zones | `zms_list_app_zones` |
| Get app zone | `zms_get_app_zone` |
| Create app zone | `zms_create_app_zone` |
| Update app zone | `zms_update_app_zone` |
| Delete app zone | `zms_delete_app_zone` |

### App Catalog
| Operation | MCP Tool |
|-----------|----------|
| List catalog entries | `zms_list_app_catalog` |
| Get catalog entry | `zms_get_app_catalog` |
| Create catalog entry | `zms_create_app_catalog` |
| Update catalog entry | `zms_update_app_catalog` |
| Delete catalog entry | `zms_delete_app_catalog` |

### Tags
| Operation | MCP Tool |
|-----------|----------|
| List tags | `zms_list_tags` |
| Get tag | `zms_get_tag` |
| Create tag | `zms_create_tag` |
| Update tag | `zms_update_tag` |
| Delete tag | `zms_delete_tag` |

## Authentication

OneAPI OAuth2 with `client_credentials` grant.

- **Token endpoint:** `https://<vanity>.zslogin.net/oauth2/v1/token`
- **API type:** GraphQL

MCP tools handle authentication automatically via `.mcp.json` credentials.

## Common Patterns

### Deploy a New Agent

1. Create a provisioning key (nonce): `zms_create_nonce`
   - Nonces are one-time-use tokens for agent bootstrap
   - Set an expiry appropriate for the deployment window
2. Deploy the ZMS agent on the workload using the nonce
3. Verify agent registration: `zms_list_agents` — agent appears after bootstrap
4. Assign agent to group: `zms_update_agent` with `agent_group_id`

### Create Resource Groups and Apply Policy

1. Create resource group: `zms_create_resource_group`
   - Group resources by workload type (e.g., web-tier, db-tier, api-tier)
2. Add resources to group: `zms_create_resource` with `resource_group_id`
3. Create policy rule: `zms_create_policy_rule`
   - Specify source resource group, destination resource group, allowed protocols/ports
   - Default posture: deny-all. Only explicitly permitted traffic flows.
4. Validate rule: `zms_get_policy_rule` to confirm configuration

### Configure App Zones

App zones define logical security perimeters for application tiers.

1. Create app zone: `zms_create_app_zone`
   - Name zone by function (e.g., `production-web`, `staging-db`)
2. Register app in catalog: `zms_create_app_catalog`
   - Catalog ties the business application identity to the zone
3. Associate resource groups with app zone via policy rules
4. Tag resources for observability: `zms_create_tag` + assign to resources

### Manage Agent Groups

Agent groups control which workloads share policy scope.

1. List existing groups: `zms_list_agent_groups`
2. Create group by environment or function: `zms_create_agent_group`
3. Move agents between groups: `zms_update_agent` with updated `agent_group_id`
4. Delete empty groups only — active agents must be reassigned first

## Known Limitations

- **Nonces are single-use** — create one per agent deployment; do not reuse
- **Policy is deny-all by default** — every required traffic flow must have an explicit policy rule
- **Agent removal** — deleting an agent does not automatically remove its resource mappings; clean up resources first
- **GraphQL schema** — use Context7 to look up exact field names and mutation shapes before calling mutations
- **MCP tool availability** — not all ZMS operations may have MCP tools; use the Python SDK (`ZMSService`) for any gaps

## MCP Server

Live CRUD operations for ZMS are available via the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server). This skill provides workflow guidance and context; the MCP server executes the API calls.
