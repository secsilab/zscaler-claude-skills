---
name: zscaler-audit
version: 1.0.0
description: Use when auditing Zscaler tenant security posture, checking for misconfigurations, or reviewing hygiene. Use after initial setup or periodically.
---

# Zscaler Tenant Security Audit

Run automated security and hygiene checks against the Zscaler tenant. Produces a findings report with severity levels and optional auto-fix.

## Prerequisites

1. Verify `.mcp.json` exists at project root
2. Run `zscaler_check_connectivity` — abort if it fails
3. Check if `memory/zscaler-tenant.md` exists (from `/zscaler-discover`):
   - If present and less than 24h old: use it as data source to reduce API calls
   - If missing or stale: run discovery inline (call the MCP tools directly)
4. Run `zscaler_get_available_services` — note which services are available

## Audit Checks

Use **subagents** to run ZIA, ZPA, and ZTB/ZIdentity checks in parallel.

### ZIA Checks

Fetch data using MCP tools. **Note:** `zia_list_cloud_firewall_rules` fails if you pass a `search` parameter — always call it without search.

| # | Check | Severity | Tool(s) | Logic |
|---|-------|----------|---------|-------|
| Z1 | Default firewall rule is ALLOW | HIGH | `zia_list_cloud_firewall_rules` | Find rule named `Default Firewall Filtering Rule`. If `action == ALLOW`, flag it — should be `BLOCK_DROP` |
| Z2 | Default DNS rule is ALLOW | HIGH | `zia_list_cloud_firewall_rules` | Find rule named `Default Firewall DNS Rule`. If `action == ALLOW`, flag it — no DNS protection |
| Z3 | Location with SERVER profile | MEDIUM | `zia_list_locations` | Any location where `profile == SERVER` skips DNS/URL inspection |
| Z4 | DNS tunnel categories not blocked | HIGH | `zia_list_url_filtering_rules` | Check if any BLOCK rule references DNS tunnel URL categories. If none, DNS tunneling is unprotected |
| Z5 | SSL inspection disabled globally | MEDIUM | `zia_list_ssl_inspection_rules` | If list is empty or all rules are disabled, no HTTPS visibility |
| Z6 | DLP rules without incident receiver | LOW | `zia_list_web_dlp_rules` | DLP rule exists but `receiver` field is null/missing — incidents are not forwarded |
| Z7 | No custom URL categories | INFO | `zia_list_url_categories` | Only built-in categories present — no custom threat intel or policy customization |
| Z8 | ATP malicious URLs list empty | MEDIUM | `zia_list_atp_malicious_urls` | No custom threat intelligence URLs configured |

### ZPA Checks

| # | Check | Severity | Tool(s) | Logic |
|---|-------|----------|---------|-------|
| P1 | Access rule without user restriction | HIGH | `zpa_list_access_policy_rules` | Rule has empty `conditions` for users, groups, and SCIM attributes — anyone with ZPA access matches |
| P2 | Segment group empty | LOW | `zpa_list_segment_groups` | Segment group with 0 application segments (`applicationCount == 0` or empty `applications` array) |
| P3 | App segment unreachable | MEDIUM | `zpa_list_application_segments`, `zpa_list_server_groups` | App segment references a server group with no connectors, or server group's connector group has 0 connectors |
| P4 | Overlapping domains | MEDIUM | `zpa_list_application_segments` | Same domain appears in multiple app segments — causes routing ambiguity |
| P5 | Rule order anomaly | MEDIUM | `zpa_list_access_policy_rules` | A DENY rule appears after a broader ALLOW rule that matches the same resources — the DENY is shadowed |
| P6 | Catch-all ALLOW not at bottom | HIGH | `zpa_list_access_policy_rules` | A rule with no app-segment conditions and action ALLOW is not in the last 2 positions — overly permissive |
| P7 | Connector group with no connectors | HIGH | `zpa_list_app_connector_groups` | App connector group where `connectors` array is empty or all connectors are disabled |

### ZTB Checks (Optional)

**Skip if** `ZSCALER_AIRGAP_SITE` is not set in `.env`.

Use Python urllib to call the AirGap API (same pattern as `/zscaler-discover`):

```python
import urllib.request, urllib.parse, json, ssl, os

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

# OAuth2 token
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

# Collect ZTB data for audit
gateways = api_get("/api/v3/Gateway/")
ipsec = api_get("/api/v2/cluster/ipsec-status")
# Per-cluster VRRP status and per-gateway PBR policies
```

| # | Check | Severity | API Endpoint | Logic |
|---|-------|----------|-------------|-------|
| T1 | VRRP not enabled | HIGH | `/api/v2/cluster/<id>/vrrp-status` | Cluster has VRRP disabled — single gateway, no HA |
| T2 | IPsec tunnel down | CRITICAL | `/api/v2/cluster/ipsec-status` | Any tunnel where `status != connected` |
| T3 | Gateway version outdated | MEDIUM | `/api/v3/Gateway/` | Compare `version` field across gateways; flag if not matching the highest version seen |
| T4 | PBR rule sends to direct | MEDIUM | `/api/v2/gateway/<id>/pbr-policy` | PBR rule with `forwardTo == direct` — traffic bypasses ZIA/ZPA |
| T5 | Network enforcement disabled | HIGH | `/api/v2/Network/` | VLAN/network exists but enforcement policies are not active |

### ZIdentity Checks

| # | Check | Severity | Tool(s) | Logic |
|---|-------|----------|---------|-------|
| I1 | User not in any group | LOW | `zidentity_list_users`, `zidentity_get_user_groups` | User exists but belongs to zero groups — no group-based policies apply |
| I2 | Group with no members | LOW | `zidentity_list_groups`, `zidentity_get_group_users` | Group exists but has zero members — potentially stale |

## Check Execution Strategy

1. Fetch all required data first (or read from `memory/zscaler-tenant.md`)
2. Run all checks against the collected data
3. Collect findings into a structured list
4. Sort findings by severity: CRITICAL > HIGH > MEDIUM > LOW > INFO

## Report Format

Write the report to `zscaler/audits/YYYY-MM-DD-audit.md` (create directory if needed).

```markdown
# Zscaler Audit Report

Date: <YYYY-MM-DD HH:MM UTC>
Tenant: <vanity domain>

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | X |
| HIGH     | X |
| MEDIUM   | X |
| LOW      | X |
| INFO     | X |

## Findings

### [CRITICAL] IPsec tunnel down
**Resource:** ZTB Cluster <cluster_name>, tunnel to <peer_ip>
**Detail:** IPsec tunnel status is `disconnected` since <timestamp>
**Recommendation:** Check ZTB gateway connectivity and IPsec configuration
**Fix:** Reconnect via AirGap portal or restart IPsec service on the gateway

### [HIGH] Default firewall rule allows all traffic
**Resource:** ZIA Cloud Firewall — Default Firewall Filtering Rule (ID: <id>)
**Detail:** The default (last) firewall rule action is ALLOW instead of BLOCK_DROP. All traffic not matching explicit rules is permitted.
**Recommendation:** Change default rule action to BLOCK_DROP after verifying explicit ALLOW rules cover legitimate traffic
**Fix:** `zia_update_cloud_firewall_rule` with `action: BLOCK_DROP`

(... repeat for each finding ...)

## Checks Passed

- Z3: No locations with SERVER profile
- Z5: SSL inspection rules active (N rules)
- (... list passed checks for completeness ...)
```

## Auto-fix Option

After displaying the report summary, ask:

> "Found X CRITICAL and Y HIGH findings. Do you want me to auto-fix them?"

If the user agrees, apply fixes using MCP tools:

| Finding | Fix Tool | Parameters |
|---------|----------|------------|
| Z1 (default FW ALLOW) | `zia_update_cloud_firewall_rule` | Set `action` to `BLOCK_DROP` |
| Z2 (default DNS ALLOW) | `zia_update_cloud_firewall_rule` | Set `action` to `BLOCK_DROP` |
| P2 (empty segment group) | `zpa_delete_segment_group` | Delete if confirmed |
| P7 (empty connector group) | Flag only | Requires manual connector deployment |

**After any ZIA fix**, call `zia_activate_configuration` to push changes live.

**IMPORTANT:** Before applying any fix:
1. Show the exact change that will be made
2. Get explicit user confirmation
3. Note the current value for rollback

## Output

1. Save report to `zscaler/audits/YYYY-MM-DD-audit.md`
2. Print summary to conversation:
   - Total findings by severity
   - Top 3 most critical findings with one-line descriptions
   - List of passed checks count
3. If `memory/zscaler-tenant.md` was used, note its age

## Error Handling

- If a service is unavailable (from `get_available_services`), skip its checks and note in report
- If an MCP tool call fails, log the error and continue with remaining checks
- If ZTB API fails, skip ZTB section and note the error
- Never fail the entire audit because one check fails — report partial results

## Related API Reference

For detailed endpoint documentation used by audit checks:
- ZIA checks (firewall, DLP, SSL, URL filtering) → See @zscaler-zia skill
- ZPA checks (access policies, connectors, segments) → See @zscaler-zpa skill
- ZTB checks (VRRP, IPsec, PBR, gateways) → See @zscaler-ztb skill
- ZIdentity checks (users, groups) → See @zscaler-zid skill
