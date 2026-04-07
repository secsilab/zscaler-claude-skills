---
name: zscaler-ztb
version: 1.2.0
postman_revision: 2026-03-30
description: Use when working with ZTB (Zero Trust Branch) — AirGap API for sites, gateways, VLANs, PBR, VRRP, IPsec, GRE, WireGuard, IPAM, SNMP, device posture, remote isolation, BGP, OSPF, templates, integrations.
---

# Zero Trust Branch (ZTB)

## Overview

ZTB manages branch office connectivity via Zscaler Branch Connectors. Uses the AirGap API (NOT OneAPI). No MCP tools available -- all operations require direct HTTP calls via Python urllib or curl.

## MCP Tools

No MCP tools. All ZTB operations use the AirGap API directly.

## Authentication

Same Zscaler OneAPI OAuth2 token (client_credentials grant):

```python
import urllib.request, urllib.parse, json, ssl

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

token_data = urllib.parse.urlencode({
    "client_id": env["ZSCALER_CLIENT_ID"],
    "client_secret": env["ZSCALER_CLIENT_SECRET"],
    "grant_type": "client_credentials"
}).encode()
req = urllib.request.Request("https://<vanity>.zslogin.net/oauth2/v1/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
token = json.loads(urllib.request.urlopen(req, context=ctx).read())["access_token"]

# AirGap API call
req = urllib.request.Request("https://<site-name>-api.goairgap.com/api/v2/<endpoint>")
req.add_header("Authorization", f"Bearer {token}")
result = json.loads(urllib.request.urlopen(req, context=ctx).read())
```

| Property | Value |
|----------|-------|
| **Base URL** | `https://<site-name>-api.goairgap.com` |
| **Web UI** | `https://<site-name>.goairgap.com` |
| **Auth** | Same Zscaler OneAPI OAuth2 token (client_credentials) |
| **API versions** | v2 and v3 (NOT v1) |

---


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Common Patterns

### Create site + network + gateway
```
1. POST /api/v2/Site/           → create site
2. POST /api/v2/Network/        → create network (VLAN) on site
3. POST /api/v2/Gateway/        → create gateway in site
4. POST /api/v2/Gateway/sendactivationlink → send activation to gateway
```

### Configure IPsec tunnel to ZIA
```
1. GET  /api/v2/cluster/ipsec-config    → check existing config
2. POST /api/v2/cluster/ipsec-config    → configure IPsec with ZIA DC IP
3. GET  /api/v2/cluster/ipsec-status    → verify tunnel UP
```

### Add PBR rule for traffic steering
```
1. GET  /api/v3/pbr/interfaces?gateway_id=<id>  → discover interfaces
2. GET  /api/v3/pbr/policies?gateway_id=<id>    → list existing policies
3. POST /api/v3/pbr/policies                     → create new PBR policy
4. POST /api/v3/pbr/policies-reorder             → reorder as needed
```

### Configure VRRP for HA
```
1. GET  /api/v3/vrrp/config/{cluster_id}    → current VRRP config
2. POST /api/v3/vrrp/config/{cluster_id}    → update VRRP config
3. GET  /api/v3/vrrp/vrrpstatus/{cluster_id} → verify HA status
```

### Deploy from template
```
1. GET  /api/v3/templates                          → list templates
2. POST /api/v3/templates/{id}/deploy_site         → deploy site from template
```

### Configure dynamic routing
```
1. POST /api/v3/Bgp/config      → add BGP peer
2. GET  /api/v3/Bgp/bgpstatus/{cluster_id} → verify BGP session
# Or for OSPF:
1. POST /api/v3/Ospf/config     → add OSPF config
```

---

## Known Limitations

1. **No MCP tools** -- all operations require direct HTTP calls to the AirGap API
2. **AirGap API is separate from OneAPI** -- different base URL (`*.goairgap.com`), same OAuth2 token
3. **`dns_servers` field is read-only via API** -- PUT returns 200 OK but does not change the value
4. **Transparent DNS proxy** intercepts ALL port 53 at L7 before PBR rules apply; to bypass, move traffic outside ZTB VLANs or use DoH
5. **PBR endpoints require `?gateway_id=`** query parameter -- calls without it will fail
6. **v2 vs v3 migration** -- some endpoints moved from v2 to v3 (PBR, VRRP, devices, BGP, OSPF); if one version returns 404, try the other
7. **Cloud Connector API** is a separate API at `connector.<cloud>.net/api/v1` -- not covered here

## Field Gotchas (Deployment Experience)

### Hardware Cutover

**ZTP Enrollment:**
- If ZTP enrollment fails, device falls back to default config (not previous config). **Verify DNS resolution to bootstrap server before starting.**
- Cable swap without failover setup = full site outage. **Always have HA secondary ready first.**
- Cutover window: 2-3 hours for large branch (100+ VLANs). Schedule during maintenance window.

**Network Gotchas:**
- **MTU mismatch** — ZTB defaults 1500, upstream may be 1480 = tunnel fragmentation = throughput degradation. Validate end-to-end MTU.
- **SVI IP reuse** — Old firewall still active during cutover = duplicate IP = ARP storms. Use temporary IPs or strict failover sequence.
- **BGP convergence delay** — New routes not immediately used after cutover. May need BGP flap or route cache clear.
- **VLAN trunking misconfiguration** — Some VLANs missing on ZTB after cutover. Always verify with `show vlan` output.
- **Licensing** — ZTP assigns default throughput tier. Manual license upgrade needed for higher speeds. Check post-enrollment.

### Rollback

**Mid-cutover failure = routing asymmetry = packet loss.** Plan hard rollback to old firewall, not soft revert:
1. Revert BGP metrics to old firewall priority
2. Restore old firewall config
3. Verify all VLANs restored
4. Document root cause before re-attempting

### Device Segmentation

**IoT/OT Gotchas:**
- VLAN-based segmentation is static — dynamic devices (printers, cameras) need profiling rules
- PBR requires `?gateway_id=` on ALL endpoints — this applies to segmentation rules too
- Transparent DNS proxy intercepts port 53 before PBR — IoT devices using custom DNS resolvers will be intercepted

## MCP Server

Live operations for ZTB are available via the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server). ZTB uses the AirGap API (`*.goairgap.com`) rather than OneAPI — no dedicated MCP tools exist. Use direct HTTP calls with the same OAuth2 token. See the MCP server repository for any newly added ZTB tools.
