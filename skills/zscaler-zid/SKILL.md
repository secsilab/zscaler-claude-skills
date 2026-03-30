---
name: zscaler-zid
version: 1.0.0
postman_revision: 2026-03-30
description: Use when working with ZIdentity — user management, group management, API clients, resource servers, directory sync.
---

# ZIdentity (ZID)

## Overview
ZIdentity manages users, groups, and API clients across the Zscaler platform. Use for user/group CRUD, API client management, and identity governance.

## MCP Tools
Available: `zidentity_list_users`, `zidentity_get_user`, `zidentity_search_users`, `zidentity_get_user_groups`, `zidentity_get_user_groups_by_name`, `zidentity_list_groups`, `zidentity_get_group`, `zidentity_search_groups`, `zidentity_get_group_users`, `zidentity_get_group_users_by_name`.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zidentity/api/v1`

## Common Patterns
- Search users by name or email
- List group membership
- Manage API clients for automation

## Known Limitations
- MCP tools are read-only — write operations (create/update/delete users/groups) require Python SDK or direct API
- User write operations need `zidentity.users.manage` scope
