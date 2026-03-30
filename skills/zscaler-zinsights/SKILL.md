---
name: zscaler-zinsights
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

## API Reference

ZInsights endpoints are accessed via MCP tools (no direct REST API documentation in Postman). The MCP tools map to internal Zscaler reporting APIs.

### Web Traffic Analytics

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_web_traffic_no_grouping` | time range | Total requests, bytes, users |
| `get_web_traffic_by_location` | time range | Traffic per location |
| `get_web_protocols` | time range | HTTP vs HTTPS vs other |

### Firewall Analytics

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_firewall_by_action` | time range | Allow/block/drop counts |
| `get_firewall_by_location` | time range | Events per location |
| `get_firewall_network_services` | time range | Events per service (DNS, HTTP, etc.) |

### Cyber Incidents

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_cyber_incidents` | time range | Incident summary |
| `get_cyber_incidents_daily` | time range | Daily trend |
| `get_cyber_incidents_by_location` | time range | Per location |
| `get_cyber_incidents_by_threat_and_app` | time range | By threat × app matrix |

### Threat Intelligence

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_threat_class` | time range | Threat class breakdown |
| `get_threat_super_categories` | time range | Super-category breakdown |

### Shadow IT & IoT

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_shadow_it_apps` | time range | Unsanctioned app list with risk |
| `get_shadow_it_summary` | time range | Summary stats |
| `get_iot_device_stats` | time range | Device types, counts |

### CASB

| Tool | Parameters | Returns |
|------|-----------|---------|
| `get_casb_app_report` | app name | Security posture report |

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
