---
name: zscaler-zcbc
version: 1.1.0
postman_revision: 2026-03-30
description: Use when working with ZCBC (Cloud & Branch Connector) via OneAPI — partner integrations, policy resources, admin roles, location management, connector groups. Also known as ZTC (Zero Trust Cloud) in newer tooling.
---

# Zscaler Cloud & Branch Connector (ZCBC)

## Overview
ZCBC manages Cloud Connectors and Branch Connectors via OneAPI (complementary to ZTB AirGap API). Use for partner integrations, policy management, admin roles, and connector lifecycle.

## MCP Tools
No dedicated MCP tools. Use OneAPI directly.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zcbc/api/v1`

## Common Patterns
- List connector groups and their status
- Manage partner integrations
- Configure admin roles for branch management

## Known Limitations
- No MCP tools — all operations via OneAPI direct calls
- For AirGap-level gateway management, use @zscaler-ztb skill instead

## Naming Note: ZCBC → ZTC (Zero Trust Cloud)

ZCBC is being rebranded as **ZTC (Zero Trust Cloud)** in newer Zscaler tooling and documentation. The skill name remains `zscaler-zcbc` for continuity, but be aware of the following aliases:

| Context | Name Used |
|---------|-----------|
| This skill | `zscaler-zcbc` |
| Zscaler SDKs (Python, Go) | `ztw` (Zero Trust Workloads) |
| New Terraform provider | `terraform-provider-ztc` |
| Zscaler Terraformer resources | `ztc_*` resource prefix |
| Newer Zscaler documentation | ZTC (Zero Trust Cloud) |

**Terraform provider:** The Terraform provider for ZCBC/ZTC is now published as `terraform-provider-ztc`. If you see references to `terraform-provider-zcbc`, they point to the same product but use the legacy name. Use `terraform-provider-ztc` for new Terraform work.

**SDK alias:** In the Zscaler Python and Go SDKs, the ZCBC module is named `ztw`. When referencing SDK documentation or source code, search for `ztw` rather than `zcbc`.

## MCP Server

Live CRUD operations for ZCBC are available via the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server). No dedicated `zcbc_*` MCP tools exist yet — use direct OneAPI calls to `https://api.zsapi.net/zcbc/api/v1`. See the MCP server repository for any newly added ZCBC tools.
