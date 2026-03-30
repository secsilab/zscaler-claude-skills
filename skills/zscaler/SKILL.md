---
name: zscaler
description: Use when managing ANY Zscaler component and you need to determine which product API to use, or when working across multiple products. Routes to the appropriate product skill.
---

# Zscaler Platform — Orchestrator

This skill routes requests to the correct product skill. It does NOT contain detailed MCP tool lists or API endpoint tables — those live in each product skill.

## Product Map

| Product | Skill | Endpoints | MCP Tools | Use For |
|---------|-------|-----------|-----------|---------|
| ZIA | @zscaler-zia | 428 | 77 | Firewall, URL filtering, DLP, SSL, locations, sandbox, ATP |
| ZPA | @zscaler-zpa | 328 | 70 | App segments, access policies, PRA, BA, connectors |
| ZTB | @zscaler-ztb | 674 | 0 (AirGap API) | Branch sites, gateways, PBR, IPsec, VRRP, IPAM, SNMP |
| ZCBC | @zscaler-zcbc | 97 | 0 | Cloud/Branch Connector via OneAPI |
| ZCC | @zscaler-zcc | 33 | 4 | Client Connector devices, forwarding |
| ZDX | @zscaler-zdx | 42 | 17 | Digital experience monitoring, alerts |
| ZID | @zscaler-zid | 31 | 10 | Users, groups, API clients |
| EASM | @zscaler-easm | 7 | 7 | External attack surface, findings |
| ZWA | @zscaler-zwa | 19 | 0 | DLP incident lifecycle |
| AI Guard | @zscaler-aiguard | 2 | 0 | Content detection, policy execution |
| ZInsights | @zscaler-zinsights | 16 | 16 | Analytics, shadow IT, threat intel |

## Operational Skills

| Skill | Use For |
|-------|---------|
| @zscaler-setup | Initial MCP server setup and credential wizard |
| @zscaler-onboard | Full tenant onboarding (setup > discover > audit > snapshot) |
| @zscaler-discover | Tenant inventory and auto-discovery |
| @zscaler-audit | Security posture audit (22 checks) |
| @zscaler-snapshot | Config backup, compare, and restore |
| @zscaler-deploy | Deployment templates (web app, SSH/RDP, location, site, DLP, extranet) |
| @zscaler-troubleshoot | Interactive diagnostic flows (6 scenarios) |
| @zscaler-migrate | Competitive migration (assessment, 6 vendor playbooks, API execution) |
| @zscaler-bridge | Translate design documents into executable API call sequences |

## Resolution Strategy

**Always follow this priority order:**

```
1. MCP tool (mcp__zscaler__*)         → preferred, fastest
2. OneAPI v2 (api.zsapi.net)          → when MCP has no tool for it
3. AirGap API (*.goairgap.com)        → ZTB management (no MCP tools exist)
4. Legacy API (zsapi.<cloud>.net)     → specific fields only exposed here
5. Python SDK (zscaler package)       → ZIdentity write ops (MCP is read-only)
```

**Routing logic:**
- If the task targets a single product, invoke that product skill directly.
- If the task spans multiple products (e.g., create ZIA location + ZPA segment + ZTB site), orchestrate by calling each product skill in sequence.
- If unsure which product owns a feature, check the Product Map above.

## OneAPI Authentication

All Zscaler APIs (except AirGap) share the same OAuth2 token.

| Method | Endpoint | Usage |
|--------|----------|-------|
| MCP | Auto (configured in `.mcp.json`) | All MCP tool calls |
| OneAPI OAuth2 | `https://<vanity>.zslogin.net/oauth2/v1/token` | `client_credentials` grant |
| AirGap (ZTB) | `https://<site>-api.goairgap.com` | Same OAuth2 token |
| Legacy | `https://zsapi.<cloud>.net/api/v1` | Only for fields missing from OneAPI |

**Cloud domains:** `zscaler.net`, `zscalerone.net`, `zscalertwo.net`, `zscalerthree.net`, `zscloud.net`, `zscalerbeta.net`, `zscalergov.net`

### Python API Call Pattern (when MCP has no tool)

```python
import urllib.request, urllib.parse, json, ssl

# Load credentials from .env
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
token_data = urllib.parse.urlencode({
    "client_id": env["ZSCALER_CLIENT_ID"],
    "client_secret": env["ZSCALER_CLIENT_SECRET"],
    "grant_type": "client_credentials"
}).encode()
req = urllib.request.Request("https://<vanity>.zslogin.net/oauth2/v1/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
token = json.loads(urllib.request.urlopen(req, context=ctx).read())["access_token"]

# OneAPI call
req = urllib.request.Request("https://api.zsapi.net/zia/api/v1/<endpoint>")
req.add_header("Authorization", f"Bearer {token}")
result = json.loads(urllib.request.urlopen(req, context=ctx).read())

# Legacy API call (same token)
req = urllib.request.Request("https://zsapi.<cloud>.net/api/v1/<endpoint>")
req.add_header("Authorization", f"Bearer {token}")
result = json.loads(urllib.request.urlopen(req, context=ctx).read())

# AirGap API call (same token)
req = urllib.request.Request("https://<site>-api.goairgap.com/api/v2/<endpoint>")
req.add_header("Authorization", f"Bearer {token}")
result = json.loads(urllib.request.urlopen(req, context=ctx).read())
```

### ZIA Activation Reminder

**Every ZIA write operation requires activation to take effect.**
After any ZIA create/update/delete, call `zia_activate_configuration` (MCP) or `POST /status/activate` (API).
ZPA changes are instant — no activation needed.

## Common Mistakes

1. **Forgetting ZIA activation** — write ops are staged until `zia_activate_configuration`
2. **Using search param on firewall rules** — `zia_list_cloud_firewall_rules(search=...)` returns 400. List all and filter client-side.
3. **ZIA DNS Control not in MCP** — must use OneAPI directly for DNS policy rules
4. **DLP `receiver` field** — only exposed by legacy API, not OneAPI
5. **ZPA rule reordering** — MCP creates rules at bottom, must reorder via direct API
6. **ZPA domain overlap** — update existing segments, don't create new overlapping ones
7. **ZIdentity write** — MCP is read-only, use Python SDK for group/user management
8. **Location profile mismatch** — SERVER profiles don't log DNS; use CORPORATE for full inspection
9. **ZTB dns_servers silent failure** — PUT returns 200 but doesn't change the value; field is effectively read-only via API
10. **ZTB transparent DNS proxy** — intercepts ALL port 53 at L7 before PBR; to bypass, move traffic outside ZTB VLANs or use DoH
11. **ZTB PBR requires gateway_id** — all PBR endpoints need `?gateway_id=` query param
12. **ZTB API versioning** — some endpoints moved from v2 to v3; if you get 404, try the other version

## General Utilities

| Tool | Description |
|------|-------------|
| `zscaler_check_connectivity` | Test API connectivity to all services |
| `zscaler_get_available_services` | List accessible services for current credentials |

## Context7 Documentation Lookup

**Before calling any MCP tool you haven't used before**, fetch the exact parameters and examples:

1. Resolve library: `resolve-library-id` with query "zscaler" — pick the matching library
2. Query docs: `query-docs` with the library ID and your question

| Library | Context7 ID | Use for |
|---------|-------------|---------|
| MCP Server | `/zscaler/zscaler-mcp-server` | MCP tool parameters, required fields, examples |
| Python SDK | `/zscaler/zscaler-sdk-python` | Direct API calls, SDK methods, field formats |

**Example:** before calling `zpa_create_application_segment`, query:
> "How to create a ZPA application segment with all required parameters"

This avoids trial-and-error on parameter names, port range formats, required vs optional fields, etc.
