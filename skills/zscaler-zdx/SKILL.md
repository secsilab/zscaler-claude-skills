---
name: zscaler-zdx
version: 1.0.0
postman_revision: 2026-03-30
description: Use when working with ZDX (Digital Experience) — application monitoring, device metrics, alerts, user experience scores, deep traces, software inventory.
---

# Zscaler Digital Experience (ZDX)

## Overview
ZDX monitors end-user digital experience. Use for application performance, device health, alerts, deep traces, and software inventory.

## MCP Tools
Available MCP tools: `zdx_list_applications`, `zdx_get_application`, `zdx_list_devices`, `zdx_get_device`, `zdx_list_alerts`, `zdx_get_alert`, `zdx_list_application_users`, `zdx_get_application_user`, `zdx_get_application_score_trend`, `zdx_get_application_metric`, `zdx_list_departments`, `zdx_list_locations`, `zdx_list_software`, `zdx_get_software_details`, `zdx_list_device_deep_traces`, `zdx_get_device_deep_trace`, `zdx_list_historical_alerts`.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zdx/api/v1`

## Common Patterns
- Check application health score trends
- List alerts for a specific timeframe
- Get device deep trace for troubleshooting
- List software inventory across fleet

## Known Limitations
- All MCP tools are read-only
- Alert acknowledgment requires direct API
