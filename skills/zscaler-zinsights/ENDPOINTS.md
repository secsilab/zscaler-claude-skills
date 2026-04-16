<!-- Manually maintained — ZInsights has no Postman collection. -->
<!-- MCP tool reference extracted from SKILL.md | Updated: 2026-03-30 -->
# Zscaler Insights (ZInsights) API Reference

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

