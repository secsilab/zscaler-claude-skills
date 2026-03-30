<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# External Attack Surface Management (EASM) API Reference

### Organizations (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/organizations` | Organizations |

### Findings (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/organizations/{{orgId}}/findings` | Get List of Findings |
| GET | `/organizations/{{orgId}}/findings/{{findingId}}/details` | Get Details of Findings |
| GET | `/organizations/{{orgId}}/findings/{{findingId}}/evidence` | Retrieve Scan Evidence |
| GET | `/organizations/{{orgId}}/findings/{{findingId}}/scan-output` | Retrieve Scan Output |

### LookALike Domains (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/organizations/{{orgId}}/lookalike-domains` | Retrieve List of LookALike Domains |
| GET | `/organizations/{{orgId}}/lookalike-domains/{{lookalikeRaw}}/details` | Retrieve Details of LookALike Domains By ID |

