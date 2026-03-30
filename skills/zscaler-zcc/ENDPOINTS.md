<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->
# Zscaler Client Connector (ZCC) API Reference

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

