<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# Zscaler Workflow Automation (ZWA) API Reference

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

