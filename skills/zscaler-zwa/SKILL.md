---
name: zscaler-zwa
version: 1.1.0
postman_revision: 2026-03-30
description: Use when working with Zscaler Workflow Automation — DLP incident search, evidence retrieval, incident closure, labels, audit logs.
---

# Zscaler Workflow Automation (ZWA)

## Overview
ZWA manages DLP incident lifecycle. Use for searching, reviewing, annotating, and closing DLP incidents programmatically. Essential for SOC automation and compliance workflows.

## MCP Tools
No MCP tools. All operations require direct API calls.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication
Separate from OneAPI. Uses its own token endpoint:
`POST {{baseUrl}}/v1/auth/api-key/token` with API key.

Base URL: `https://{{baseUrl}}/dlp/v1`

## Common Patterns
- Search DLP incidents by time range for SOC review
- Get incident evidence and details for investigation
- Close incidents with notes after remediation
- Attach labels for categorization and tracking
- Query audit logs for compliance reporting

## Known Limitations
- No MCP tools — completely manual API integration required
- Separate authentication from OneAPI (own token endpoint)
- DLP incident evidence may contain sensitive data — handle with care

## MCP Server

Live operations for ZWA are available via the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server). No dedicated `zwa_*` MCP tools exist yet — use direct API calls with the ZWA-specific token (see Authentication above). Check the MCP server repository for any newly added ZWA tools.
