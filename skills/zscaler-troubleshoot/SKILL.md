---
name: zscaler-troubleshoot
description: Use when diagnosing Zscaler connectivity issues, access problems, blocked websites, DNS failures, performance degradation, or ZTB gateway issues. Interactive diagnostic wizard.
---

# Zscaler Troubleshoot

Interactive diagnostic wizard for Zscaler issues. Guides the user through structured troubleshooting flows using MCP tools and AirGap API.

## Entry Point

Ask the user ONE question:

> What issue are you experiencing?
> 1. User can't access an application (ZPA)
> 2. Website blocked or not loading (ZIA)
> 3. DNS not resolving (ZIA/ZTB)
> 4. Slow performance (ZDX)
> 5. ZTB gateway issue
> 6. Other (describe)

Route to the matching flow below.

---

## Flow 1: ZPA Access Issue

**Goal**: determine why a user cannot reach a ZPA-published application.

### Step 1 — Identify the application
Ask: "Which application or domain is failing?"

### Step 2 — Find the app segment
Call `zpa_list_application_segments`. Filter results by the domain or name provided.
- If no match: **Diagnosis** — domain is not published in ZPA. Suggest creating an app segment.
- If found: note the segment ID, segment group ID, server group IDs, and enabled status.

### Step 3 — Check server group and connectors
For each server group ID on the app segment, call `zpa_get_server_group`.
- Check `enabled` is true
- Note the app connector group IDs

For each connector group, call `zpa_get_app_connector_group`.
- Check connectors exist and their `enabled` status
- If all connectors are down: **Diagnosis** — no active connectors.

### Step 4 — Identify the user
Ask: "Which user is affected? (email or display name)"

### Step 5 — Evaluate access policy
Call `zpa_list_access_policy_rules`. For each rule (processed in order):
1. Check if rule conditions match the user (SCIM groups, SAML attributes, IdP)
2. Check if rule conditions match the app segment or segment group
3. If a **DENY** rule matches before any ALLOW: **Diagnosis** — blocked by deny rule (give rule name and position).
4. If an **ALLOW** rule matches: user should have access, problem is elsewhere.
5. If no rule matches: **Diagnosis** — no matching access policy rule. Suggest adding one.

### Step 6 — Check ZTB routing (optional)
If tenant has ZTB (check if `ZSCALER_AIRGAP_SITE` is in `.env`):
- Verify PBR policy routes ZPA traffic (TCP/443 to ZPA broker IPs) correctly
- Check gateway is healthy (see Flow 5 steps)

### Step 7 — Print diagnosis
Summarize:
- Application: name, segment, enabled status
- Connectors: status
- Policy: matching rule (or lack thereof)
- Root cause and recommended fix

---

## Flow 2: ZIA Website Blocked

**Goal**: determine why a website is blocked or not loading through ZIA.

### Step 1 — Identify the URL
Ask: "Which URL or domain is blocked?"

### Step 2 — Check URL category
Call `zia_list_url_categories` and search for the domain in custom categories.
- Note if the URL is in a custom BLOCK category
- Note the URL's categorization

### Step 3 — Check URL filtering rules
Call `zia_list_url_filtering_rules`. Walk rules in order:
- Find which rule matches the URL's category, user/group, and location
- If a BLOCK or CAUTION rule matches: **Diagnosis** — blocked by URL filtering rule (give rule name, order, action).

### Step 4 — Check SSL inspection
Call `zia_list_ssl_inspection_rules`. Check if:
- The domain is being SSL-inspected (could cause certificate errors, not a block)
- The domain is in a DO_NOT_INSPECT rule (could cause bypass issues)
- If the user sees a certificate error: **Diagnosis** — SSL inspection without root CA installed on client.

### Step 5 — Check cloud firewall rules
Call `zia_list_cloud_firewall_rules` (no search parameter — list all, then filter locally).
- Check if any BLOCK rule matches the destination IP/port
- Check if any rule drops non-HTTP traffic to the destination

### Step 6 — Check ZTB routing (optional)
If ZTB is configured, verify PBR routes web traffic through ZIA (not direct).

### Step 7 — Print diagnosis
Summarize:
- URL category (predefined + custom)
- Matching URL filter rule (name, order, action)
- SSL inspection status
- Firewall rule match
- Root cause and recommended fix

---

## Flow 3: DNS Issue

**Goal**: determine why DNS resolution fails for a domain.

### Step 1 — Identify the domain and location
Ask: "Which domain is not resolving? From which location or network?"

### Step 2 — Check ZIA location
Call `zia_list_locations`, find the user's location.
- Check if `profile` is set (CORPORATE, etc.)
- Check if DNS resolution is enabled for the location

### Step 3 — Check DNS control rules
**Note**: There is no MCP tool for DNS control rules. Use the ZIA API directly:

```python
import urllib.request, urllib.parse, json, ssl, os

env = {}
with open(".env") as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k] = v

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Get OAuth2 token
vanity = env.get("ZSCALER_VANITY_DOMAIN", env.get("ZSCALER_CLIENT_ID", "").split("@")[0])
token_data = urllib.parse.urlencode({
    "client_id": env["ZSCALER_CLIENT_ID"],
    "client_secret": env["ZSCALER_CLIENT_SECRET"],
    "grant_type": "client_credentials"
}).encode()
req = urllib.request.Request(f"https://{vanity}.zslogin.net/oauth2/v1/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
token = json.loads(urllib.request.urlopen(req, context=ctx).read())["access_token"]

# List DNS control rules
api_req = urllib.request.Request("https://api.zsapi.net/zia/api/v1/dnsPolicy/rules")
api_req.add_header("Authorization", f"Bearer {token}")
rules = json.loads(urllib.request.urlopen(api_req, context=ctx).read())
print(json.dumps(rules, indent=2))
```

Check if any DNS rule blocks the domain or its category.

### Step 4 — Check ZTB DNS config (optional)
If ZTB is configured:
- Check `dns_servers` on the gateway — is ZIA set as upstream?
- Check if transparent DNS proxy is enabled
- Check if the domain falls within a split-DNS zone that bypasses ZIA

### Step 5 — Check block categories
Call `zia_list_url_categories` — check if the domain's category is in a blocked category that also affects DNS.

### Step 6 — Print diagnosis
Summarize:
- Location profile and DNS settings
- DNS control rule match (if any)
- ZTB DNS configuration (if applicable)
- Root cause and recommended fix

---

## Flow 4: Performance (ZDX)

**Goal**: diagnose slow application performance using ZDX telemetry.

### Step 1 — Identify the application
Ask: "Which application is slow?"
Call `zdx_list_applications` to find the matching app ID.

### Step 2 — Get application score
Call `zdx_get_application_score_trend` with the app ID.
- If score is consistently high (>80): performance is normal from ZDX perspective.
- If score is degraded (<60): continue investigation.

### Step 3 — Get detailed metrics
Call `zdx_get_application_metric` with the app ID.
- Identify which metric is degraded: DNS time, TCP connect, TLS handshake, TTFB, total response time.
- This pinpoints the slow hop.

### Step 4 — Check affected users
Call `zdx_list_application_users` with the app ID.
- If all users are affected: likely a server-side or network-wide issue.
- If specific users/locations: likely a local network or ISP issue.

### Step 5 — Hop analysis (deep trace)
If a specific user/device is identified, call `zdx_list_device_deep_traces` then `zdx_get_device_deep_trace` to get network path data.
- Identify which hop introduces latency (client → ZCC → ZIA → Internet → server)
- Check if the bottleneck is local network, Zscaler cloud, or server-side

### Step 6 — Check ZDX alerts
Call `zdx_list_alerts`.
- Look for active alerts related to the application.
- Check alert severity and affected device count.

### Step 7 — Print diagnosis
Summarize:
- Application score trend (good/degraded/critical)
- Degraded metric (DNS / TCP / TLS / TTFB / total)
- Affected scope (all users vs. specific locations)
- Active alerts
- Root cause hypothesis and recommended next steps

---

## Flow 5: ZTB Gateway Issue

**Goal**: diagnose ZTB (Branch Connector) gateway health issues.

**Prerequisite**: Check if `ZSCALER_AIRGAP_SITE` is set in `.env`. If not, tell the user ZTB diagnostics require AirGap API credentials and stop.

Use the AirGap API helper pattern from the DNS flow (same OAuth2 + urllib approach). Set `BASE = f"https://{site}-api.goairgap.com"`.

### Step 1 — Check gateway status
`GET /api/v3/Gateway/`
- List all gateways, check `status` field
- Flag any gateway that is not in expected state

### Step 2 — Check VRRP status
For each cluster, call `GET /api/v3/vrrp/vrrpstatus/{cluster_id}`
- Verify one gateway is MASTER, others are BACKUP
- Flag split-brain (multiple MASTER) or all-BACKUP conditions

### Step 3 — Check IPsec tunnels
`GET /api/v2/cluster/ipsec-status`
- Check tunnel states (UP/DOWN)
- Flag any DOWN tunnels — this breaks ZIA/ZPA forwarding

### Step 4 — Check alarms
`GET /api/v2/alarm`
- List active alarms
- Highlight critical alarms (tunnel down, gateway unreachable, etc.)

### Step 5 — Print diagnosis
Summarize:
- Gateway health (per gateway)
- VRRP state (per cluster)
- IPsec tunnel status (per tunnel)
- Active alarms
- Root cause and recommended fix

---

## Flow 6: Other

Ask the user to describe the issue in detail.

Based on keywords, route to the closest flow:
- "access", "connect", "app", "ZPA" -> Flow 1
- "block", "website", "URL", "filter" -> Flow 2
- "DNS", "resolve", "lookup" -> Flow 3
- "slow", "latency", "performance", "ZDX" -> Flow 4
- "gateway", "ZTB", "tunnel", "VRRP", "IPsec" -> Flow 5

If no flow matches, investigate manually using available MCP tools and the information provided.

---

## General Guidelines

- **Interactive**: Use `AskUserQuestion` at each decision point where user input is needed.
- **Concise output**: Print structured diagnosis — not raw API output. Use tables for multi-item results.
- **ZTB is optional**: Skip ZTB-related steps if `ZSCALER_AIRGAP_SITE` is not in `.env`.
- **Firewall rule search**: `zia_list_cloud_firewall_rules` does NOT support a search parameter — always list all and filter locally.
- **DNS rules**: No MCP tool exists — use the Python urllib pattern to call `/zia/api/v1/dnsPolicy/rules` directly.
- **No tenant-specific IDs**: This skill is generic. Read all IDs from API responses, never hardcode them.
- **Error handling**: If an MCP tool or API call fails, report the error and continue with remaining checks.

## Related API Reference

For detailed endpoint documentation used by diagnostic flows:
- ZPA access issues → See @zscaler-zpa skill (access policies, connectors)
- ZIA blocked websites → See @zscaler-zia skill (URL filtering, firewall, SSL)
- DNS issues → See @zscaler-zia skill (DNS control)
- ZDX performance → See @zscaler-zdx skill (metrics, deep traces)
- ZTB gateway issues → See @zscaler-ztb skill (AirGap API)
- Analytics context → See @zscaler-zinsights skill
