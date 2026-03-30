---
name: zscaler-zcbc
version: 1.0.0
postman_revision: 2026-03-30
description: Use when working with ZCBC (Cloud & Branch Connector) via OneAPI — partner integrations, policy resources, admin roles, location management, connector groups.
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
