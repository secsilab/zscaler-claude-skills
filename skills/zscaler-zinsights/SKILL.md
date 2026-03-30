---
name: zscaler-zinsights
version: 1.0.0
description: Use when querying Zscaler analytics — web traffic, firewall stats, cyber incidents, shadow IT, IoT devices, CASB reports, threat intelligence.
---

# Zscaler Insights (ZInsights)

## Overview

ZInsights provides analytics and reporting across the Zscaler platform. Use for web traffic analysis, firewall statistics, cyber incident tracking, shadow IT discovery, IoT device inventory, and CASB application reports.

## MCP Tools

All ZInsights operations are read-only via MCP tools:

| Tool | Description |
|------|-------------|
| `zinsights_get_web_traffic_no_grouping` | Web traffic summary without grouping |
| `zinsights_get_web_traffic_by_location` | Web traffic grouped by location |
| `zinsights_get_web_protocols` | Web traffic by protocol (HTTP/HTTPS/etc.) |
| `zinsights_get_firewall_by_action` | Firewall events by action (allow/block) |
| `zinsights_get_firewall_by_location` | Firewall events by location |
| `zinsights_get_firewall_network_services` | Firewall events by network service |
| `zinsights_get_cyber_incidents` | Cyber incident summary |
| `zinsights_get_cyber_incidents_daily` | Daily cyber incident trend |
| `zinsights_get_cyber_incidents_by_location` | Cyber incidents by location |
| `zinsights_get_cyber_incidents_by_threat_and_app` | Cyber incidents by threat type and application |
| `zinsights_get_threat_class` | Threat classification breakdown |
| `zinsights_get_threat_super_categories` | Threat super-category breakdown |
| `zinsights_get_shadow_it_apps` | Shadow IT application list |
| `zinsights_get_shadow_it_summary` | Shadow IT summary statistics |
| `zinsights_get_iot_device_stats` | IoT device inventory and statistics |
| `zinsights_get_casb_app_report` | CASB application security report |


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication

Uses OneAPI OAuth2 (same as ZIA/ZPA). No separate auth flow.

## Common Patterns

- Daily security briefing: cyber incidents + threat classes + shadow IT summary
- Location risk assessment: web traffic + firewall blocks + incidents per location
- Shadow IT review: list unsanctioned apps, check CASB reports
- IoT inventory: device stats for network segmentation planning

## Known Limitations

- All tools are read-only (analytics/reporting only)
- No Postman collection available — endpoints only accessible via MCP tools
- Time range parameters vary by tool — check MCP tool schema
- Data freshness depends on Zscaler cloud processing (typically 15-30 min delay)
