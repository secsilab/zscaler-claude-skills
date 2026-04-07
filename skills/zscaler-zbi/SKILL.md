---
name: zscaler-zbi
version: 1.0.0
description: Use when working with Zscaler Business Insights (ZBI) — custom application definitions, report configurations, and report generation/retrieval.
---

# Zscaler Business Insights (ZBI)

## Overview

ZBI provides business-level visibility into application usage and security posture. Use this skill for defining custom application classifications, configuring report templates, and downloading business insight reports. ZBI complements ZInsights (raw analytics) by adding business context to traffic and security data.

ZBI uses a REST-based API. No dedicated MCP tools exist — all operations require direct OneAPI calls.

## MCP Tools

No dedicated MCP tools. Use OneAPI directly via the Python pattern from @zscaler.

## Authentication

OneAPI OAuth2 with `client_credentials` grant.

- **Token endpoint:** `https://<vanity>.zslogin.net/oauth2/v1/token`
- **Base URL:** `https://api.zsapi.net/bi/api/v1`

**Note:** The base path is `/bi/api/v1` (not `/zbi/api/v1`). Path segments use **lowercase** (`customapps`, `report`), not camelCase.

## Modules

### Custom Apps

Define named business application groupings. Custom apps map traffic to meaningful business labels for reporting via match signatures (URL, domain, IP, etc.).

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List custom apps | `GET` | `/customapps` |
| Get custom app by id | `GET` | `/customapps?id={id}` |
| Create custom app | `POST` | `/customapps` |
| Update custom app | `PUT` | `/customapps/{id}` |
| Delete custom app | `DELETE` | `/customapps/{id}` |

**Note:** "Get by id" uses a query parameter (`?id=`), not a path parameter.

### Report Configs

Report configurations define what data to collect and the delivery schedule. ZBI report configs are tied to a specific report type — `customapps` is currently the only supported type.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List report configs | `GET` | `/reports/customapps` |
| Get report config by id | `GET` | `/reports/customapps?id={id}` |
| Create report config | `POST` | `/reports/customapps` |
| Update report config | `PUT` | `/reports/customapps/{id}` |
| Delete report config | `DELETE` | `/reports/customapps/{id}` |

### Reports

Generated report instances. Listing returns all reports across configs; downloading retrieves the actual report file.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List all reports | `GET` | `/report/all` |
| Download a report | `POST` | `/report/download` |

**Note:** Singular `/report` (not `/reports`) for these operations.

## Common Patterns

### Define a Custom App

1. Identify match signatures for the application (URLs, hostnames, IPs)
2. Create the custom app:
   ```
   POST /customapps
   {
     "name": "Salesforce CRM",
     "description": "All Salesforce traffic",
     "signatures": [
       {"type": "URL", "matchLevel": "EXACT", "value": "salesforce.com"},
       {"type": "URL", "matchLevel": "PREFIX", "value": "*.force.com"}
     ]
   }
   ```
3. The custom app becomes available as a classification dimension in reports.

**Signature fields** (per `CustomApp` SDK model):
- `type` — match type (e.g., `URL`, `DOMAIN`)
- `matchLevel` — match strictness
- `value` — the literal string to match

### Create a Report Config

```
POST /reports/customapps
{
  "name": "Monthly Custom App Usage",
  "sub_type": "OVERVIEW",
  "enabled": true,
  "custom_ids": ["<custom-app-id-1>", "<custom-app-id-2>"],
  "delivery_information": { ... },
  "schedule_params": { ... }
}
```

**Report config fields** (per SDK `ReportConfig` model):
- `name` — display name
- `sub_type` — `OVERVIEW` or `USERS`
- `enabled` — boolean
- `custom_ids` — list of custom app IDs to include
- `delivery_information` — delivery target (email, etc.)
- `schedule_params` — recurring schedule
- `backfill_params` — historical backfill

### Download a Report

```
POST /report/download
{
  "fileName": "<report-file-name>",
  "reportType": "customapps",
  "subType": "OVERVIEW"
}
```

The response contains the report payload (CSV or JSON depending on configuration).

### List All Reports

```
GET /report/all
```

Returns metadata for every generated report. Use `fileName` from this response to drive `POST /report/download`.

## Known Limitations

- **No MCP tools** — all operations require direct OneAPI calls
- **Only `customapps` report type** — the SDK currently supports only this single report type
- **No path-param GET for single items** — use query param `?id=` instead
- **Custom apps are report-only** — they do not create ZIA/ZPA policy; they are classification labels for analytics
- **ENDPOINTS.md not yet available** — this skill is not Postman-derived; consult the Python SDK (`zscaler/bi/`) for the source of truth
