---
name: zscaler-snapshot
description: Use when backing up Zscaler tenant config, comparing changes between points in time, detecting drift, or rolling back to a previous state.
---

# Zscaler Tenant Snapshot

Capture, compare, and restore Zscaler tenant configuration snapshots.

## Prerequisites

1. Verify `.mcp.json` exists at project root
2. Run `zscaler_check_connectivity` — abort if it fails
3. Run `zscaler_get_available_services` — note which services are available

## Mode 1: `take` — Capture Current State

### 1. Collect Data

Use **subagents** to export ZIA, ZPA, and ZTB/ZIdentity in parallel.

#### ZIA Resources

| File | Tool |
|------|------|
| `zia-locations.json` | `zia_list_locations` |
| `zia-firewall-rules.json` | `zia_list_cloud_firewall_rules` (no search param) |
| `zia-url-filtering-rules.json` | `zia_list_url_filtering_rules` |
| `zia-ssl-rules.json` | `zia_list_ssl_inspection_rules` |
| `zia-dlp-rules.json` | `zia_list_web_dlp_rules` |

#### ZPA Resources

| File | Tool |
|------|------|
| `zpa-app-segments.json` | `zpa_list_application_segments` |
| `zpa-access-rules.json` | `zpa_list_access_policy_rules` |
| `zpa-segment-groups.json` | `zpa_list_segment_groups` |
| `zpa-server-groups.json` | `zpa_list_server_groups` |

#### ZIdentity Resources

| File | Tool |
|------|------|
| `zidentity-groups.json` | `zidentity_list_groups` |

#### ZTB Resources (Optional)

**Skip if** `ZSCALER_AIRGAP_SITE` is not set in `.env`.

Use Python urllib to call the AirGap API:

```python
import urllib.request, urllib.parse, json, ssl

env = {}
with open(".env") as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k] = v

site = env.get("ZSCALER_AIRGAP_SITE")
if not site:
    print("SKIP: No ZSCALER_AIRGAP_SITE in .env")
    exit(0)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

vanity = env.get("ZSCALER_VANITY_DOMAIN", env.get("ZSCALER_CLIENT_ID", "").split("@")[0])
token_data = urllib.parse.urlencode({
    "client_id": env["ZSCALER_CLIENT_ID"],
    "client_secret": env["ZSCALER_CLIENT_SECRET"],
    "grant_type": "client_credentials"
}).encode()
req = urllib.request.Request(f"https://{vanity}.zslogin.net/oauth2/v1/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
token = json.loads(urllib.request.urlopen(req, context=ctx).read())["access_token"]

BASE = f"https://{site}-api.goairgap.com"
def api_get(path):
    r = urllib.request.Request(f"{BASE}{path}")
    r.add_header("Authorization", f"Bearer {token}")
    return json.loads(urllib.request.urlopen(r, context=ctx).read())

sites_data = api_get("/api/v2/Site/")
networks_data = api_get("/api/v2/Network/")
# PBR policies per gateway
gateways = api_get("/api/v3/Gateway/")
pbr_policies = {}
for gw in gateways.get("list", gateways if isinstance(gateways, list) else []):
    gw_id = gw.get("id")
    if gw_id:
        pbr_policies[gw_id] = api_get(f"/api/v2/gateway/{gw_id}/pbr-policy")
```

| File | Source |
|------|--------|
| `ztb-sites.json` | `/api/v2/Site/` |
| `ztb-networks.json` | `/api/v2/Network/` |
| `ztb-pbr-policies.json` | `/api/v2/gateway/<id>/pbr-policy` (per gateway, combined) |

### 2. Save Snapshot

Generate timestamp: `YYYY-MM-DD-HHMMSS` (UTC).

Create directory: `zscaler/snapshots/<timestamp>/`

Write each resource as pretty-printed JSON (indent=2). Each file contains the raw API response.

### 3. Git Commit

Stage and commit all files in the snapshot directory:

```
zscaler: snapshot <timestamp>
```

### 4. Print Summary

- Snapshot path
- Count per resource type (e.g., "ZIA: 3 locations, 12 firewall rules, ...")
- Total file count and combined size
- ZTB status (captured or skipped)

## Mode 2: `diff` — Compare Two Snapshots

### 1. List Available Snapshots

Scan `zscaler/snapshots/` for directories. Display them sorted by date with resource counts.

### 2. Select Snapshots

Ask the user to pick two snapshots. Support shortcuts:
- `latest` — most recent snapshot
- `previous` — second most recent
- Direct timestamp

### 3. Compare

For each resource type file present in both snapshots:

1. Load both JSON files
2. Match resources by `id` field (or `name` if no id)
3. Categorize changes:
   - **Added**: resource exists in new snapshot only
   - **Removed**: resource exists in old snapshot only
   - **Modified**: resource exists in both but fields differ

For modified resources, identify changed fields. Ignore metadata fields: `modifiedTime`, `modifiedBy`, `creationTime`.

### 4. Print Diff Report

```
=== Zscaler Config Diff ===
Comparing: 2026-03-10-143000 → 2026-03-16-090000

--- ZIA Firewall Rules ---
  ADDED:   "Block DNS Tunneling" (id: 12345)
  REMOVED: "Temp Allow Rule" (id: 67890)
  MODIFIED: "Default Firewall Filtering Rule" (id: 11111)
    - action: ALLOW → BLOCK_DROP
    - description: "" → "Block all unmatched traffic"

--- ZPA Access Rules ---
  No changes

--- ZPA App Segments ---
  MODIFIED: "Infra - Core" (id: 22222)
    - domainNames: ["a.example.com"] → ["a.example.com", "b.example.com"]

(... repeat for each resource type ...)

Summary: 2 added, 1 removed, 3 modified across 10 resource types
```

If a resource file exists in one snapshot but not the other, note it as "resource type not captured".

## Mode 3: `restore` — Rollback to a Snapshot

**WARNING: This mode makes destructive changes to the live tenant.**

### 1. List and Select

List available snapshots (same as diff mode). Ask user which snapshot to restore.

### 2. Take Pre-Restore Snapshot

Automatically run Mode 1 (`take`) to capture current state before any changes. This ensures rollback-of-rollback is possible.

### 3. Show Impact

Run Mode 2 (`diff`) comparing current state (just captured) vs target snapshot. Display the full diff report.

### 4. Confirm

Print a clear warning:

```
WARNING: This will apply the following changes to the LIVE tenant:
  - ZIA: X resources to update, Y to delete, Z to create
  - ZPA: X resources to update, Y to delete, Z to create
  - ZIdentity: not restored (read-only)
  - ZTB: not restored (use AirGap portal)

Type "RESTORE" to confirm, anything else to abort.
```

**Do NOT proceed without explicit "RESTORE" confirmation from the user.**

### 5. Apply Changes

Process each resource type. Order matters:

1. **ZPA segment groups** (create first — app segments reference them)
2. **ZPA server groups** (create first — app segments reference them)
3. **ZPA app segments** (create/update/delete)
4. **ZPA access rules** (update last — reference app segments)
5. **ZIA firewall rules** (create/update/delete)
6. **ZIA URL filtering rules**
7. **ZIA SSL inspection rules**
8. **ZIA DLP rules**

For each resource type:

| Action | Logic | Tool Pattern |
|--------|-------|--------------|
| Create | Resource in snapshot but not in current | `zpa_create_*` / `zia_create_*` |
| Update | Resource in both, fields differ | `zpa_update_*` / `zia_update_*` |
| Delete | Resource in current but not in snapshot | `zpa_delete_*` / `zia_delete_*` |

**Skip:** default/system rules (they cannot be deleted, only updated). Identify them by `name` containing "Default" or by `defaultRule == true`.

### 6. Activate ZIA

If any ZIA changes were made, call `zia_activate_configuration` to push changes live.

### 7. Post-Restore Snapshot

Run Mode 1 (`take`) again to capture the restored state. This confirms the restore was applied correctly.

### 8. Print Results

- Number of changes applied per resource type
- Any failures (with error details)
- Path to pre-restore and post-restore snapshots

## Resource Type Mapping

| Resource | List Tool | Create Tool | Update Tool | Delete Tool |
|----------|-----------|-------------|-------------|-------------|
| ZIA Firewall Rules | `zia_list_cloud_firewall_rules` | `zia_create_cloud_firewall_rule` | `zia_update_cloud_firewall_rule` | `zia_delete_cloud_firewall_rule` |
| ZIA URL Filtering | `zia_list_url_filtering_rules` | `zia_create_url_filtering_rule` | `zia_update_url_filtering_rule` | `zia_delete_url_filtering_rule` |
| ZIA SSL Rules | `zia_list_ssl_inspection_rules` | `zia_create_ssl_inspection_rule` | `zia_update_ssl_inspection_rule` | `zia_delete_ssl_inspection_rule` |
| ZIA DLP Rules | `zia_list_web_dlp_rules` | `zia_create_web_dlp_rule` | `zia_update_web_dlp_rule` | `zia_delete_web_dlp_rule` |
| ZPA App Segments | `zpa_list_application_segments` | `zpa_create_application_segment` | `zpa_update_application_segment` | `zpa_delete_application_segment` |
| ZPA Access Rules | `zpa_list_access_policy_rules` | `zpa_create_access_policy_rule` | `zpa_update_access_policy_rule` | `zpa_delete_access_policy_rule` |
| ZPA Segment Groups | `zpa_list_segment_groups` | `zpa_create_segment_group` | `zpa_update_segment_group` | `zpa_delete_segment_group` |
| ZPA Server Groups | `zpa_list_server_groups` | `zpa_create_server_group` | `zpa_update_server_group` | `zpa_delete_server_group` |

**Not restored** (read-only or external):
- ZIA Locations (infrastructure-dependent)
- ZIdentity Groups (identity source of truth)
- ZTB (managed via AirGap portal)

## Error Handling

- If a service is unavailable (from `get_available_services`), skip its resources and note in output
- If an MCP tool call fails during `take`, log the error and continue with remaining resources
- If ZTB API fails, skip ZTB files and note the error
- During `restore`, if a single resource fails: log it, continue with others, report failures at end
- Never fail the entire operation because one resource fails — report partial results
- If `restore` encounters more than 5 consecutive failures, pause and ask the user before continuing

## Related API Reference

For detailed endpoint documentation used by snapshots:
- ZIA config export (locations, firewall, URL, SSL, DLP) → See @zscaler-zia skill
- ZPA config export (segments, policies, groups) → See @zscaler-zpa skill
- ZTB config export (sites, networks, PBR) → See @zscaler-ztb skill
- ZIdentity groups → See @zscaler-zid skill
