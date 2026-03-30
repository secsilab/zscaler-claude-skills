---
name: zscaler-easm
description: Use when working with ZEASM (External Attack Surface Management) — findings, lookalike domains, organization discovery.
---

# External Attack Surface Management (EASM)

## Overview
EASM discovers external attack surface: exposed assets, findings, lookalike domains. Use for security posture assessment and shadow IT detection.

## MCP Tools
Available: `zeasm_list_findings`, `zeasm_get_finding_details`, `zeasm_get_finding_evidence`, `zeasm_get_finding_scan_output`, `zeasm_list_lookalike_domains`, `zeasm_get_lookalike_domain`, `zeasm_list_organizations`.

## API Reference

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

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/easm/api/v1`

## Common Patterns
- List all findings sorted by severity
- Get evidence for a specific finding
- Monitor lookalike domains for brand protection

## Known Limitations
- All MCP tools are read-only
- No remediation actions via API (manual follow-up required)
