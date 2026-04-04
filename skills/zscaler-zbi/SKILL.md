---
name: zscaler-zbi
version: 1.0.0
description: Use when working with Zscaler Business Insights (ZBI) — custom application definitions, report configurations, and report generation/retrieval.
---

# Zscaler Business Insights (ZBI)

## Overview

ZBI provides business-level visibility into application usage and security posture. Use this skill for defining custom application classifications, configuring report templates, and generating or retrieving business insight reports. ZBI complements ZInsights (raw analytics) by adding business context to traffic and security data.

ZBI uses a REST-based API. No dedicated MCP tools exist — all operations require direct OneAPI calls.

## MCP Tools

No dedicated MCP tools. Use OneAPI directly.

## Authentication

OneAPI OAuth2 with `client_credentials` grant.

- **Token endpoint:** `https://<vanity>.zslogin.net/oauth2/v1/token`
- **Base URL:** `https://api.zsapi.net/zbi/api/v1`

MCP tools handle authentication automatically; for ZBI direct calls, use the OneAPI token pattern from the @zscaler orchestrator skill.

## Modules

### Custom Apps (`/customApps`)

Define named business application groupings. Custom apps map traffic (by domain, IP, or cloud app) to meaningful business labels for reporting.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List custom apps | `GET` | `/customApps` |
| Get custom app | `GET` | `/customApps/{id}` |
| Create custom app | `POST` | `/customApps` |
| Update custom app | `PUT` | `/customApps/{id}` |
| Delete custom app | `DELETE` | `/customApps/{id}` |

### Report Configs (`/reportConfigs`)

Report configurations define what data to collect, the time range, filters, and output format for a report.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List report configs | `GET` | `/reportConfigs` |
| Get report config | `GET` | `/reportConfigs/{id}` |
| Create report config | `POST` | `/reportConfigs` |
| Update report config | `PUT` | `/reportConfigs/{id}` |
| Delete report config | `DELETE` | `/reportConfigs/{id}` |

### Reports (`/reports`)

Reports are generated instances of report configurations. Generation is asynchronous — poll for status.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List reports | `GET` | `/reports` |
| Get report | `GET` | `/reports/{id}` |
| Generate report | `POST` | `/reports` |
| Delete report | `DELETE` | `/reports/{id}` |

## Common Patterns

### Define a Custom App

1. Identify traffic identifiers: domain names, IP ranges, or cloud app IDs to associate with this business app
2. Create the custom app:
   ```
   POST /customApps
   {
     "name": "Salesforce CRM",
     "description": "All Salesforce traffic",
     "domains": ["salesforce.com", "*.salesforce.com", "*.force.com"]
   }
   ```
3. The custom app becomes available as a dimension in reports

### Configure and Generate a Report

1. Create a report config with the desired dimensions and filters:
   ```
   POST /reportConfigs
   {
     "name": "Monthly App Usage",
     "dimensions": ["customApp", "department", "user"],
     "metrics": ["bytesIn", "bytesOut", "sessions"],
     "timeRange": "LAST_30_DAYS"
   }
   ```
2. Trigger report generation:
   ```
   POST /reports
   { "reportConfigId": "<id>" }
   ```
3. Poll for completion:
   ```
   GET /reports/{id}
   ```
   Check `status` field — values: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`
4. Download results when `status == COMPLETED` — the response includes a download URL or embedded data

### Retrieve Existing Reports

- List all generated reports: `GET /reports`
- Filter by config: `GET /reports?reportConfigId=<id>`
- Reports are retained for a limited period (typically 30 days); export promptly

## Known Limitations

- **No MCP tools** — all operations require direct OneAPI calls using the Python pattern from @zscaler
- **Async report generation** — reports do not return data immediately; poll until `COMPLETED`
- **Custom apps are report-only** — they do not create ZIA/ZPA policy; they are metadata labels for analytics
- **ENDPOINTS.md not yet available** — this skill predates Postman collection integration; consult the ZBI API documentation directly
