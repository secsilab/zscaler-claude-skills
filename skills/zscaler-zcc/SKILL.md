---
name: zscaler-zcc
description: Use when working with ZCC (Client Connector) — device management, forwarding profiles, trusted networks, enrollment, web policies, entitlements.
---

# Zscaler Client Connector (ZCC)

## Overview
ZCC manages the Zscaler Client Connector agent on endpoints. Use for device inventory, forwarding profiles, trusted networks, and enrollment.

## MCP Tools
Available MCP tools: `zcc_list_devices`, `zcc_devices_csv_exporter`, `zcc_list_forwarding_profiles`, `zcc_list_trusted_networks`.

## API Reference

### Entitlements (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/getZpaGroupEntitlements` | getZpaGroupEntitlements |
| GET | `/v1/getZdxGroupEntitlements` | getZdxGroupEntitlements |
| PUT | `/v1/updateZdxGroupEntitlement` | updateZdxGroupEntitlement |
| PUT | `/v1/updateZdxGroupEntitlement` | updateZpaGroupEntitlement |

### Trusted Networks (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `` | getMultipleTrustedNetworks |
| POST | `/v1/webTrustedNetwork/create` | createTrustedNetwork |
| DELETE | `/v1/webTrustedNetwork/{{networkId}}/delete` | deleteTrustedNetwork |

### Web Forwarding Profile (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| DELETE | `/v1/webForwardingProfile/{{profileId}}/delete` | deleteForwardingProfile |
| GET | `/v1/webForwardingProfile/listByCompany` | forwardingProfilesByCompanyId |
| POST | `/v1/webForwardingProfile/edit` | editForwardingProfile |

### Web App Service (1 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/webAppService/listByCompany` | getAppServiceInfoByCompanyId |

### Web Fail Open (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/v1/webFailOpenPolicy/edit` | updateFailOpenPolicy |
| GET | `/v1/webFailOpenPolicy/listByCompany` | getFailOpenPolicy |

### Web Privacy (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/v1/setWebPrivacyInfo` | updatePrivacyInfo |
| GET | `/v1/getWebPrivacyInfo` | getPrivacyInfo |

### Admin Users (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/syncZiaZdxAdminUsers` | syncZiaZdxAdminUsers |
| POST | `/syncZiaZdxAdminUsers` | syncZiaZdxAdminUsers - POST |
| GET | `/v1/getAdminUsersSyncInfo` | getAdminUsersSyncInfo - Get |
| POST | `/v1/syncZpaAdminUsers` | adminUsersZpaSyncInfo |
| PUT | `/v1/editAdminUser` | editAdminUser - Update |
| GET | `/v1/getAdminRoles` | getAdminRoles - Get All |

### Devices (11 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/getDevices` | Get all enrolled devices |
| GET | `/v1/downloadDisableReasons` | Download Report as CSV with Disable Reasons |
| GET | `/v1/getDeviceDetails` | Get details of enrolled devices |
| GET | `/v1/getOtp` | Get the OTP for the specified device |
| GET | `/v1/downloadDevices` | Download device details as a CSV file |
| GET | `/v1/downloadServiceStatus` | Download service status of all devices as a CSV file |
| POST | `/v1/forceRemoveDevices` | Force remove enrolled devices |
| POST | `/v1/removeDevices` | Soft remove enrolled devices |
| PUT | `/v1/setDeviceCleanupInfo` | setDeviceCleanupInfo |
| GET | `/v1/getDeviceCleanupInfo` | getDeviceCleanupInfo |
| POST | `/v1/removeMachineTunnel` | removeMachineTunnel |

### Credentials (1 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/getPasswords` | Get the app profile password for the specified device |

## Authentication
OneAPI OAuth2. Base URL: `https://api.zsapi.net/zcc/api/v1`

## Common Patterns
- List devices by OS type or user
- Export device inventory to CSV
- Check forwarding profile assignments

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
