---
name: zscaler-zcc
version: 1.2.0
postman_revision: 2026-03-30
description: Use when working with ZCC (Client Connector) — device management, forwarding profiles, trusted networks, enrollment, web policy, web privacy, failopen policy, custom/predefined IP apps, process-based apps, application profiles, web app service, admin roles, entitlements.
---

# Zscaler Client Connector (ZCC)

## Overview
ZCC manages the Zscaler Client Connector agent on endpoints. Use for device inventory, forwarding profiles, trusted networks, and enrollment.

## MCP Tools
Available MCP tools: `zcc_list_devices`, `zcc_devices_csv_exporter`, `zcc_list_forwarding_profiles`, `zcc_list_trusted_networks`.


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zcc/papi/public/v1`

**Note:** ZCC uses the path prefix `/zcc/papi/public/v1` (not `/zcc/api/v1`). Both Go and Python SDKs confirm this.

## Common Patterns
- List devices by OS type or user
- Export device inventory to CSV
- Check forwarding profile assignments

## Full API Module Coverage

The ZCC API exposes ~20 service modules. The 4 MCP tools cover read-only device operations. All other modules require direct OneAPI calls.

**Important:** ZCC uses RPC-style action endpoints (`/listByCompany`, `/edit`, `/getXyz`, `/setXyz`), not REST resource verbs. Several modules are read-only at the API level — write operations may require the admin portal.

### Web Policy

Controls which web categories and applications ZCC intercepts and forwards.

| Operation | Endpoint |
|-----------|----------|
| List web policies | `GET /web/policy/listByCompany` |
| Edit web policy | `PUT /web/policy/edit` |
| Activate web policy | `PUT /web/policy/activate` |
| Delete web policy | `DELETE /web/policy/{id}/delete` |

### Web Privacy

Configures privacy-exempt domains and IPs — traffic to these destinations bypasses ZCC inspection.

| Operation | Endpoint |
|-----------|----------|
| Get web privacy config | `GET /getWebPrivacyInfo` |
| Set web privacy config | `PUT /setWebPrivacyInfo` |

### Failopen Policy

Defines ZCC behavior when the Zscaler cloud is unreachable: allow traffic (failopen) or block traffic (failclosed).

| Operation | Endpoint |
|-----------|----------|
| List failopen policies | `GET /webFailOpenPolicy/listByCompany` |
| Edit failopen policy | `PUT /webFailOpenPolicy/edit` |

**Recommendation:** Set to failopen for external users (internet dependency), failclosed for privileged/PCI workloads.

### Forwarding Profiles

Forwarding profiles define tunnel mode (full/split), exclusions, and ZIA/ZPA targeting. Note: there is no GET-by-id; both create and update go through `POST /edit` (the request body carries the id for updates).

| Operation | Endpoint |
|-----------|----------|
| List profiles | `GET /webForwardingProfile/listByCompany` |
| Create or update profile | `POST /webForwardingProfile/edit` |
| Delete profile | `DELETE /webForwardingProfile/{profileId}/delete` |

### Custom IP Apps (Read-Only)

Custom IP applications define specific IP ranges or subnets. **Read-only at the API level** — create/update/delete are not exposed.

| Operation | Endpoint |
|-----------|----------|
| List custom IP apps | `GET /custom-ip-based-apps` |
| Get custom IP app | `GET /custom-ip-based-apps/{appId}` |

### Predefined IP Apps (Read-Only)

Predefined IP applications are Zscaler-managed app definitions (e.g., Microsoft 365 IP ranges, video conferencing endpoints). **Read-only.**

| Operation | Endpoint |
|-----------|----------|
| List predefined IP apps | `GET /predefined-ip-based-apps` |
| Get predefined IP app | `GET /predefined-ip-based-apps/{appId}` |

### Process-Based Apps (Read-Only)

Process-based applications map specific OS process names to ZCC forwarding behavior. **Read-only.**

| Operation | Endpoint |
|-----------|----------|
| List process-based apps | `GET /process-based-apps` |
| Get process-based app | `GET /process-based-apps/{appId}` |

### Application Profiles

Application profiles bundle forwarding configuration, tunnel settings, trusted networks, and policy exclusions into a reusable template assigned to device groups. Update uses `PATCH`, not `PUT`. No create/delete via API.

| Operation | Endpoint |
|-----------|----------|
| List app profiles | `GET /application-profiles` |
| Get app profile | `GET /application-profiles/{profileId}` |
| Update app profile | `PATCH /application-profiles/{profileId}` |

### Web App Service

Web app service configuration controls ZCC's local HTTP/HTTPS proxy behavior for specific applications.

| Operation | Endpoint |
|-----------|----------|
| List web app service config | `GET /webAppService/listByCompany` |

### Admin Roles (Read-Only)

Admin roles scope what ZCC portal administrators can view and modify. **Read-only at the API level.**

| Operation | Endpoint |
|-----------|----------|
| Get admin roles | `GET /getAdminRoles` |

### Entitlements

Entitlements control which ZCC features are licensed and available to users. There is no unified `/entitlements` endpoint — entitlements are split per service (ZDX vs ZPA).

| Operation | Endpoint |
|-----------|----------|
| Get ZDX group entitlements | `GET /getZdxGroupEntitlements` |
| Update ZDX group entitlement | `PUT /updateZdxGroupEntitlement` |
| Get ZPA group entitlements | `GET /getZpaGroupEntitlements` |
| Update ZPA group entitlement | `PUT /updateZpaGroupEntitlement` |

### Other Modules

| Module | Notes |
|--------|-------|
| Admin Users | ZCC-specific admin accounts |
| Company | Tenant company profile |
| Trusted Networks | Read via MCP (`zcc_list_trusted_networks`), write via API |
| Manage Password | Uninstall password management |
| Secrets | Registration secrets for enrollment |
| Remove Devices | Bulk device removal |
| Download Devices | Device inventory download |

## Known Limitations
- MCP tools are read-only (4 tools)
- Write operations (create/update forwarding profiles) require direct API calls

## MCP Server

Live read operations for ZCC are available via the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server) (`zcc_*` tools). Write operations and the extended module coverage documented above require direct OneAPI calls. See the MCP server repository for available tools and parameters.

## Field Gotchas (Deployment Experience)

### Z-Tunnel Version

**Z-Tunnel 1.0 is DEPRECATED (EOL 2026). Do NOT deploy new installations with 1.0.**

| Feature | Z-Tunnel 1.0 | Z-Tunnel 2.0 |
|---------|-------------|-------------|
| Architecture | User-space agent | Kernel VPN driver |
| Latency overhead | 5-10ms | <1ms |
| CPU idle | 5-15% | 1-3% |
| Status | **Deprecated** | **Current, recommended** |

Migrate all existing 1.0 to 2.0 within 12 months. Z-Tunnel 2.0 is kernel-based, performs like native OS VPN.

### App Profile Best Practices

| Profile | Tunnel Mode | Exclusions | Use Case |
|---------|------------|------------|----------|
| Corporate Desktop | Full tunnel | Exclude video conferencing, VPN | Standard employee |
| Contractor | Split tunnel (limited apps) | Corporate apps only | Third-party access |
| BYOD | Split tunnel (minimal) | Email + Slack + portal only | Personal devices |
| VIP/Executive | Full tunnel | No exclusions | High-security users |

### Deployment Waves (Don't Big-Bang)

1. **Wave 1 — Pilot (50 IT staff + 50 power users):** Validate install, tunnel stability, app access. 1-2 weeks.
2. **Wave 2 — Early Adopter (500 mixed users):** Expand to one department. Tune policies based on Wave 1 feedback. 1 week.
3. **Wave 3 — General Population (remaining users):** Stagger 20% per day. Monitor for 24h between batches.
- **Success criteria per wave:** >95% install success, <2% support tickets, no critical app failures
- **Rollback trigger:** >20% install failure OR critical app broken → pause and investigate

### Common Issues

- **GlobalProtect + ZCC conflict:** Both are VPN clients. If GlobalProtect not fully removed, routing is ambiguous. **Uninstall GlobalProtect completely before deploying ZCC.**
- **MDM profile assignment lag:** Profile changes via Intune/JAMF may take 15-60 min to propagate. Don't escalate prematurely.
- **Certificate trust:** ZCC auto-downloads Zscaler root CA during enrollment. If IT pre-loaded a different cert, conflicts arise. Verify cert chain post-install.
