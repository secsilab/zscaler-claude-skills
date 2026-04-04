---
name: zscaler-zpa
version: 1.2.0
postman_revision: 2026-03-30
description: Use when working with ZPA — application segments, access/forwarding/timeout/isolation policies, PRA, BA, connectors, service edges, segment groups, server groups, SCIM, LSS, isolation, certificates, microtenants, tags, microsegmentation.
---

# Zscaler Private Access (ZPA)

## Overview

ZPA provides zero trust application access. Use this skill for application segments, access/forwarding/timeout policies, PRA (Privileged Remote Access), BA (Browser Access), app connectors, service edges, segment/server groups, SCIM integration, log streaming (LSS), browser isolation (CBI), inspection profiles, certificate management, microtenants, and tagging.

ZPA changes are instant — no activation step needed (unlike ZIA).

## MCP Tools (70 tools)

### Application Segments
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_application_segments` |
| Get | `zpa_get_application_segment` |
| Create | `zpa_create_application_segment` |
| Update | `zpa_update_application_segment` |
| Delete | `zpa_delete_application_segment` |
| Get by type (BA/PRA/Inspect) | `get_zpa_app_segments_by_type` |

### Access Policy Rules
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_access_policy_rules` |
| Get | `zpa_get_access_policy_rule` |
| Create | `zpa_create_access_policy_rule` |
| Update | `zpa_update_access_policy_rule` |
| Delete | `zpa_delete_access_policy_rule` |

### Forwarding Policy Rules
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_forwarding_policy_rules` |
| Get | `zpa_get_forwarding_policy_rule` |
| Create | `zpa_create_forwarding_policy_rule` |
| Update | `zpa_update_forwarding_policy_rule` |
| Delete | `zpa_delete_forwarding_policy_rule` |

### Timeout Policy Rules
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_timeout_policy_rules` |
| Get | `zpa_get_timeout_policy_rule` |
| Create | `zpa_create_timeout_policy_rule` |
| Update | `zpa_update_timeout_policy_rule` |
| Delete | `zpa_delete_timeout_policy_rule` |

### Isolation Policy Rules
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_isolation_policy_rules` |
| Get | `zpa_get_isolation_policy_rule` |
| Create | `zpa_create_isolation_policy_rule` |
| Update | `zpa_update_isolation_policy_rule` |
| Delete | `zpa_delete_isolation_policy_rule` |

### App Protection Rules
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_app_protection_rules` |
| Get | `zpa_get_app_protection_rule` |
| Create | `zpa_create_app_protection_rule` |
| Update | `zpa_update_app_protection_rule` |
| Delete | `zpa_delete_app_protection_rule` |

### Segment Groups
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_segment_groups` |
| Get | `zpa_get_segment_group` |
| Create | `zpa_create_segment_group` |
| Update | `zpa_update_segment_group` |
| Delete | `zpa_delete_segment_group` |

### Server Groups
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_server_groups` |
| Get | `zpa_get_server_group` |
| Create | `zpa_create_server_group` |
| Update | `zpa_update_server_group` |
| Delete | `zpa_delete_server_group` |

### App Connector Groups
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_app_connector_groups` |
| Get | `zpa_get_app_connector_group` |
| Create | `zpa_create_app_connector_group` |
| Update | `zpa_update_app_connector_group` |
| Delete | `zpa_delete_app_connector_group` |

### Service Edge Groups
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_service_edge_groups` |
| Get | `zpa_get_service_edge_group` |
| Create | `zpa_create_service_edge_group` |
| Update | `zpa_update_service_edge_group` |
| Delete | `zpa_delete_service_edge_group` |

### Application Servers
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_application_servers` |
| Get | `zpa_get_application_server` |
| Create | `zpa_create_application_server` |
| Update | `zpa_update_application_server` |
| Delete | `zpa_delete_application_server` |

### BA Certificates
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_ba_certificates` |
| Get | `zpa_get_ba_certificate` |
| Create | `zpa_create_ba_certificate` |
| Delete | `zpa_delete_ba_certificate` |

### PRA Portals
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_pra_portals` |
| Get | `zpa_get_pra_portal` |
| Create | `zpa_create_pra_portal` |
| Update | `zpa_update_pra_portal` |
| Delete | `zpa_delete_pra_portal` |

### PRA Credentials
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_pra_credentials` |
| Get | `zpa_get_pra_credential` |
| Create | `zpa_create_pra_credential` |
| Update | `zpa_update_pra_credential` |
| Delete | `zpa_delete_pra_credential` |

### Provisioning Keys
| Operation | MCP Tool |
|-----------|----------|
| List | `zpa_list_provisioning_keys` |
| Get | `zpa_get_provisioning_key` |
| Create | `zpa_create_provisioning_key` |
| Update | `zpa_update_provisioning_key` |
| Delete | `zpa_delete_provisioning_key` |

### Read-Only Helpers
| MCP Tool | Description |
|----------|-------------|
| `get_zpa_scim_group` | SCIM groups by IdP |
| `get_zpa_scim_attribute` | SCIM attribute headers |
| `get_zpa_saml_attribute` | SAML attributes |
| `get_zpa_posture_profile` | Posture profiles |
| `get_zpa_trusted_network` | Trusted networks |
| `get_zpa_enrollment_certificate` | Enrollment certificates |
| `get_zpa_isolation_profile` | Isolation profiles |
| `get_zpa_app_protection_profile` | App protection profiles |

## Authentication

OneAPI OAuth2 with `client_credentials` grant.

- **Token endpoint:** `https://<vanity>.zslogin.net/oauth2/v1/token`
- **Base URL:** `https://api.zsapi.net/zpa/mgmtconfig/v1/admin/customers/{{customerId}}`
- **CBI base:** `https://api.zsapi.net/zpa/cbiconfig/cbi/api/customers/{{customerId}}`
- **User config base:** `https://api.zsapi.net/zpa/userconfig/v1/customers/{{customerId}}`

MCP tools handle authentication automatically via `.mcp.json` credentials.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Common Patterns

### Adding an Application

1. Create segment group (if needed): `zpa_create_segment_group`
2. Create server group with connectors: `zpa_create_server_group`
3. Create application segment: `zpa_create_application_segment`
4. Create access policy rule: `zpa_create_access_policy_rule`
5. Reorder rule (MCP cannot reorder):
   `PUT /policySet/{policySetId}/rule/{ruleId}/reorder/{newOrder}` returns HTTP 204

**Domain overlap check:** ZPA blocks duplicate domains across segments. If overlap, update the existing segment instead.

### Adding BA Bookmarks

Update existing segment with `commonAppsDto.appsConfig[].appTypes: ["BROWSER_ACCESS"]`. Requires a BA certificate ID (`zpa_list_ba_certificates`). No domain overlap issue for BA.

### Adding PRA (Privileged Remote Access)

1. Add PRA app to segment: `commonAppsDto.appsConfig[].appTypes: ["SECURE_REMOTE_ACCESS"]`
2. Get praApp ID from response: `praApps[].id` (NOT the segment ID)
3. Create PRA portal: `zpa_create_pra_portal`
4. Create PRA credential: `zpa_create_pra_credential`
5. Create PRA console: `POST /praConsole` (not available via MCP)
6. Check tenant console limit — returns "entity.limit.exceeded" when exceeded

### Access Policy Rule Conditions

```json
{
  "conditions": [
    {
      "operands": [
        {
          "objectType": "SCIM_GROUP",
          "lhs": "<idp_id>",
          "rhs": "<scim_group_id>"
        }
      ]
    }
  ]
}
```

Always prefer `SCIM_GROUP` over individual SCIM attributes — groups scale better.

### Discovering Tenant IDs

```
1. Customer ID         -> ZSCALER_CUSTOMER_ID env or admin portal
2. Access Policy Set   -> zpa_list_access_policy_rules -> policySetId from any rule
3. IdP ID              -> get_zpa_scim_group -> idpId from response
4. Segment Groups      -> zpa_list_segment_groups
5. Server Groups       -> zpa_list_server_groups
6. SCIM Groups         -> get_zpa_scim_group (query by IdP name)
```

### Configuring LSS (Log Streaming)

1. List available log formats: `GET /lssConfig/logType/formats`
2. List client types: `GET /lssConfig/customers/{customerId}/clientTypes`
3. Create LSS config: `POST /lssConfig` with log type, format, and receiver details
4. Supported receivers: SIEM, Splunk, QRadar, Azure Sentinel, etc.

### Configuring Inspection (AppProtect)

1. List predefined controls: `GET /inspectionControls/predefined`
2. Create inspection profile: `POST /inspectionProfile`
3. Associate controls: `PUT /inspectionProfile/{id}/associateAllPredefinedControls`
4. Create app protection rule: `zpa_create_app_protection_rule`

## Known Limitations

- **PRA console creation** not available via MCP — use OneAPI directly (`POST /praConsole` or `/praConsole/bulk`)
- **Rule reordering** not available via MCP — use `PUT /policySet/{id}/rule/{ruleId}/reorder/{order}` (returns 204)
- **Bulk reorder** available: `PUT /policySet/{id}/reorder` reorders all rules in one call
- **ZPA identity** — `displayname` may differ from `loginname` (check SCIM attributes before modifying rules)
- **Domain overlap** — ZPA blocks duplicate domains across segments; update existing instead of creating new
- **Delete policy rule** via MCP requires `kwargs={"confirmed": true}` on second call
- **CBI endpoints** use a different base path: `/cbiconfig/cbi/api/` instead of `/mgmtconfig/v1/admin/`
- **PRA credential pool** endpoints use `/waap-pra-config/v1/admin/` base path
- **SCIM/user endpoints** use `/userconfig/v1/customers/` base path
- **LSS endpoints** use v2: `/mgmtconfig/v2/admin/`
- **Deprecated endpoints** — `clientlessCertificate` and some `lssConfig/clientTypes` are marked for deprecation; use newer equivalents

## Safety Rules

1. **Snapshot before any change** — export state to JSON, git commit before + after
2. **Check BA/PRA refs** before deleting segments — persistent refs block deletion
3. **Domain overlap protection** — update existing segments, never create overlapping new ones
4. **Rule order matters** — top-to-bottom, first match wins. New rules go to bottom — always reorder
5. **Verify SCIM identity** before modifying rules — displayname may differ from loginname
6. **No activation needed** — ZPA changes take effect immediately (unlike ZIA)

## Field Gotchas (Deployment Experience)

### Connector Sizing & Placement

**Sizing Rules (Field-Proven):**
- 1 connector per 500 concurrent users
- Max 2,500 users per HA pair
- Baseline: 4 vCPU, 8GB RAM
- High load (2,500+ users): 8 vCPU, 16GB RAM
- Minimum 20GB free on `/var` — logs fill fast, rotate daily

**Connector Group Scope:**
- One group per logical boundary (DC / cloud region)
- **Never mix DC + cloud in same group** — latency penalties from cross-region traffic
- Each group = failover domain = same policy evaluation point

**HA Pair Gotchas:**
- Active-passive recommended (simpler); active-active requires same subnet
- Connectors must have independent power, network, disk to avoid cascading failure
- Health check: every 30s, >60s disconnection triggers failover
- **License expiration silently stops forwarding** — no error, just dropped traffic

**Network Requirements:**
- Outbound TCP/UDP 443 only — NO inbound ports
- Whitelist ZPA broker IP **ranges**, not individual IPs (they rotate weekly)
- CIDR overlap between app segment servers and connector traffic CIDR causes routing loops

### App Segment Design

**FQDN vs IP Decision Matrix:**

| Use Case | FQDN vs IP | Double-Encrypt | Server Group |
|----------|-----------|----------------|--------------|
| Kubernetes/cloud | FQDN wildcard | Yes if sensitive | 10+ with health probe |
| Legacy Windows | IP static | No | 2-4 manual failover |
| Database (PII) | IP + FQDN | **Yes (mandatory)** | 3-5 with priority |
| API gateway | FQDN exact | Yes if auth critical | 5+ active-active |

**Segment Gotchas:**
- FQDN resolution happens on **connector**, not user device. If connector can't resolve → segment fails silently.
- Exact FQDN takes precedence over wildcard — create exact for critical apps, wildcard for catch-all
- Double-encrypt adds latency — measure before enforcing for high-frequency apps
- Server group health probes disabled by default — **enable for production** (TCP/HTTP, 30s interval)
- Port mismatch: app listens 8080 internally, segment publishes 443 → must match exactly

### Identity & Access

**SCIM Sync Gotchas:**
- SCIM changes propagate in 1-4 hours. For urgent access changes, use manual override.
- **Group name casing matters:** "Engineering" ≠ "engineering" — validate exact case from IdP
- Posture checks evaluated every login. Stale posture from old session can block legitimate access.
- Some posture check modules fail-open on crash (allow access). **Verify fail-closed behavior.**

**Policy Rule Gotchas:**
- First-matching rule wins. Contradictory rules fail silently — the first one matched applies.
- Bypass rules inherit all previous rules. Narrow bypass scope to specific segments only.
- Policy grants access but servers not in connector group = connection timeout, no clear error

## Microsegmentation and Related Capabilities

### ZPA and Microsegmentation

ZPA provides identity-based access to applications (north-south: user to app). For workload-to-workload east-west traffic control, use **Zscaler Microsegmentation (ZMS)** — see @zscaler-zms for dedicated management.

ZPA has several capabilities that complement or overlap with microsegmentation:

**Policy V2 Controller**
The ZPA Policy V2 engine supports more granular rule conditions including workload tags, posture signals, and step-up authentication. When building access rules for workloads (not just users), prefer Policy V2 constructs for better expressiveness.

**Extranet Resources**
ZPA can expose resources to external partners and contractors without requiring full network connectivity. Extranet segments are standard application segments with restricted identity conditions — use SAML/SCIM attributes to scope access to partner IdPs.

**Browser Protection (Cloud Browser Isolation)**
CBI wraps ZPA-accessed applications in an isolated browser session. This is distinct from microsegmentation but serves a similar containment goal: even if a user session is compromised, the application's data plane is protected by CBI's air-gap rendering.

**Workload Tag Groups**
ZPA supports tagging application servers and connectors with workload metadata (environment, tier, data classification). Workload tags enable policy rules to dynamically scope access based on infrastructure labels rather than static IPs — bridging ZPA policy with cloud workload identity.

### Relationship to ZMS

| Dimension | ZPA | ZMS |
|-----------|-----|-----|
| Traffic direction | North-south (user → app) | East-west (workload → workload) |
| Identity anchor | User identity (SAML/SCIM) | Workload identity (agent + nonce) |
| Policy granularity | App segment + user group | Resource group + port/protocol |
| Managed via | @zscaler-zpa | @zscaler-zms |

For full microsegmentation lifecycle (agent deployment, resource groups, policy rules, app zones), use @zscaler-zms.
