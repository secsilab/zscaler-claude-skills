---
name: zscaler-zwa
description: Use when working with Zscaler Workflow Automation — DLP incident search, evidence retrieval, incident closure, labels, audit logs.
---

# Zscaler Workflow Automation (ZWA)

## Overview
ZWA manages DLP incident lifecycle. Use for searching, reviewing, annotating, and closing DLP incidents programmatically. Essential for SOC automation and compliance workflows.

## MCP Tools
No MCP tools. All operations require direct API calls.

## API Reference

### Authentication (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/auth/api-key/token` | get-token-by-api-key |

### Incident Retrieval (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dlp/v1/incidents/transactions/{{transactionId}}` | get-dlp-incidents-by-transaction-id |
| GET | `/dlp/v1/incidents/{{incidentId}}` | get-dlp-incident-details |
| GET | `/dlp/v1/incidents/{{incidentId}}/evidence` | get-dlp-incident-evidence |
| GET | `/dlp/v1/incidents/{{incidentId}}/tickets` | get-dlp-incident-tickets |
| GET | `/dlp/v1/incidents/{{incidentId}}/change-history` | get-dlp-incident-change-history |

### Incident Details (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dlp/v1/incidents/{{incidentId}}/triggers` | get-dlp-incident-triggers |

### Incident Actions (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/dlp/v1/incidents/{{incidentId}}/close` | close-dlp-incident |
| POST | `/dlp/v1/incidents/{{incidentId}}/notes` | attach-note-to-incident |
| POST | `/dlp/v1/incidents/{{incidentId}}/labels` | attach-label-to-incident |
| DELETE | `/dlp/v1/incidents/{{incidentId}}` | delete-dlp-incident |

### Incident Search (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/dlp/v1/incidents/search` | search-dlp-incidents-by-priority |
| POST | `/dlp/v1/incidents/search` | search-dlp-incidents-by-transaction-id |
| POST | `/dlp/v1/incidents/search` | search-dlp-incidents-by-time-range |
| POST | `/dlp/v1/incidents/search` | search-dlp-incidents-by-labels |
| POST | `/dlp/v1/incidents/search` | search-dlp-incidents-by-incident-group-ids |
| POST | `/dlp/v1/incidents/search` | search-dlp-incidents-by-engine |

### Incident Groups (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/dlp/v1/incidents/{{incidentId}}/incident-groups/search` | search-dlp-incident-groups |

### Audit (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/dlp/v1/customer/audit/` | search-audit-log-by-time-range |

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
