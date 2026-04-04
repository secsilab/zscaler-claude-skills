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
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zcc/api/v1`

## Common Patterns
- List devices by OS type or user
- Export device inventory to CSV
- Check forwarding profile assignments

## Full API Module Coverage

The ZCC API (and Go SDK) has 20 service modules. The 4 MCP tools cover read-only device operations. All other modules require direct OneAPI calls (`https://api.zsapi.net/zcc/api/v1`).

### Web Policy (`/webPolicy`)

Controls which web categories and applications ZCC intercepts and forwards.

| Operation | Endpoint |
|-----------|----------|
| Get web policy | `GET /webPolicy` |
| Update web policy | `PUT /webPolicy` |

### Web Privacy (`/webPrivacy`)

Configures privacy-exempt domains and IPs — traffic to these destinations bypasses ZCC inspection.

| Operation | Endpoint |
|-----------|----------|
| Get web privacy config | `GET /webPrivacy` |
| Update web privacy config | `PUT /webPrivacy` |

### Failopen Policy (`/failOpenPolicy`)

Defines ZCC behavior when the Zscaler cloud is unreachable: allow traffic (failopen) or block traffic (failclosed).

| Operation | Endpoint |
|-----------|----------|
| Get failopen policy | `GET /failOpenPolicy` |
| Update failopen policy | `PUT /failOpenPolicy` |

**Recommendation:** Set to failopen for external users (internet dependency), failclosed for privileged/PCI workloads.

### Forwarding Profiles (`/forwardingProfiles`)

Forwarding profiles define tunnel mode (full/split), exclusions, and ZIA/ZPA targeting.

| Operation | Endpoint |
|-----------|----------|
| List profiles | `GET /forwardingProfiles` |
| Get profile | `GET /forwardingProfiles/{id}` |
| Create profile | `POST /forwardingProfiles` |
| Update profile | `PUT /forwardingProfiles/{id}` |
| Delete profile | `DELETE /forwardingProfiles/{id}` |

### Custom IP Apps (`/customIpApps`)

Custom IP applications define specific IP ranges or subnets that ZCC should handle with custom routing logic.

| Operation | Endpoint |
|-----------|----------|
| List custom IP apps | `GET /customIpApps` |
| Get custom IP app | `GET /customIpApps/{id}` |
| Create custom IP app | `POST /customIpApps` |
| Update custom IP app | `PUT /customIpApps/{id}` |
| Delete custom IP app | `DELETE /customIpApps/{id}` |

### Predefined IP Apps (`/predefinedIpApps`)

Predefined IP applications are Zscaler-managed app definitions (e.g., Microsoft 365 IP ranges, video conferencing endpoints).

| Operation | Endpoint |
|-----------|----------|
| List predefined IP apps | `GET /predefinedIpApps` |
| Get predefined IP app | `GET /predefinedIpApps/{id}` |
| Update predefined IP app | `PUT /predefinedIpApps/{id}` |

### Process-Based Apps (`/processBasedApps`)

Process-based applications map specific OS process names to ZCC forwarding behavior — route or bypass by executable.

| Operation | Endpoint |
|-----------|----------|
| List process-based apps | `GET /processBasedApps` |
| Get process-based app | `GET /processBasedApps/{id}` |
| Create process-based app | `POST /processBasedApps` |
| Update process-based app | `PUT /processBasedApps/{id}` |
| Delete process-based app | `DELETE /processBasedApps/{id}` |

### Application Profiles (`/applicationProfiles`)

Application profiles bundle forwarding configuration, tunnel settings, trusted networks, and policy exclusions into a reusable template assigned to device groups.

| Operation | Endpoint |
|-----------|----------|
| List app profiles | `GET /applicationProfiles` |
| Get app profile | `GET /applicationProfiles/{id}` |
| Create app profile | `POST /applicationProfiles` |
| Update app profile | `PUT /applicationProfiles/{id}` |
| Delete app profile | `DELETE /applicationProfiles/{id}` |

### Web App Service (`/webAppService`)

Web app service configuration controls ZCC's local HTTP/HTTPS proxy behavior for specific applications.

| Operation | Endpoint |
|-----------|----------|
| Get web app service config | `GET /webAppService` |
| Update web app service config | `PUT /webAppService` |

### Admin Roles (`/adminRoles`)

Admin roles scope what ZCC portal administrators can view and modify.

| Operation | Endpoint |
|-----------|----------|
| List admin roles | `GET /adminRoles` |
| Get admin role | `GET /adminRoles/{id}` |
| Create admin role | `POST /adminRoles` |
| Update admin role | `PUT /adminRoles/{id}` |
| Delete admin role | `DELETE /adminRoles/{id}` |

### Entitlements (`/entitlements`)

Entitlements control which ZCC features are licensed and available to users.

| Operation | Endpoint |
|-----------|----------|
| Get entitlements | `GET /entitlements` |

### Other Modules

| Module | Endpoint | Notes |
|--------|----------|-------|
| Admin Users | `/adminUsers` | ZCC-specific admin accounts |
| Company | `/company` | Tenant company profile |
| Trusted Networks | `/trustedNetworks` | Read via MCP (`zcc_list_trusted_networks`), write via API |
| Manage Password | `/managePass` | Uninstall password management |
| Secrets | `/secrets` | Registration secrets for enrollment |
| Remove Devices | `/removeDevices` | Bulk device removal |
| Download Devices | `/downloadDevices` | Device inventory download |

## Known Limitations
- MCP tools are read-only (4 tools)
- Write operations (create/update forwarding profiles) require direct API calls

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
