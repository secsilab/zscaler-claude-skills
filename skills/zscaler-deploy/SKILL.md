---
name: zscaler-deploy
description: Use when deploying new applications, servers, locations, sites, DLP policies, or partner access in Zscaler. Pre-built deployment templates with interactive prompts.
---

# Zscaler Deploy — Deployment Recipes

Pre-built templates for common Zscaler deployments. Each template is interactive — collect all required inputs before making changes.

## Entry Point

Ask the user:

> **What do you want to deploy?**
> 1. Web application (ZPA segment + access rule + DNS + BA bookmark)
> 2. SSH/RDP server (ZPA segment + PRA console)
> 3. ZIA location (IPsec tunnel + location + firewall rules)
> 4. ZTB site (site + gateway + VLANs + PBR) — optional, requires AirGap API
> 5. DLP policy (dictionary + engine + rule + incident receiver)
> 6. Extranet partner (ZIA extranet location + ZPA partner segment)

## Pre-Flight (All Templates)

Before making ANY changes:

1. **Verify connectivity:** `zscaler_check_connectivity`
2. **Take snapshot:** Export current state of affected components to timestamped JSON files in `zscaler/snapshots/` and git commit. This enables rollback.
3. **Discover IDs:** Fetch segment groups, server groups, SCIM groups, IdP ID, policy set IDs — these are needed for most templates.

```python
# Snapshot pattern — adapt to the components being modified
import json, datetime
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# Save each component list to zscaler/snapshots/pre-deploy-<template>-<ts>.json
```

---

## Template 1: Web Application

### Collect Inputs

Ask these questions (one at a time):

1. **App name** — Display name for the segment (e.g., "CRM Portal")
2. **Domain (FQDN)** — The internal domain users will access (e.g., `crm.example.com`)
3. **Ports** — TCP ports to expose (default: `443`)
4. **Segment group** — List existing groups via `zpa_list_segment_groups` and ask which one, or create a new one
5. **Server group** — List existing via `zpa_list_server_groups` and ask which one, or create a new one
6. **Who needs access** — List SCIM groups via `get_zpa_scim_group` and ask which groups should have access
7. **BA bookmark** — "Create a Browser Access bookmark? (yes/no)" — default: yes if port 443
8. **DNS record** — "Create a DNS record? If yes, which zone?" — list available zones or let user specify

### Execute

**Step 1: Check for domain overlap**
```
Use zpa_list_application_segments and check if the domain already exists in another segment.
If overlap → use zpa_update_application_segment on the existing segment instead of creating new.
```

**Step 2: Create or update application segment**
```
zpa_create_application_segment:
  name: <app_name>
  domainNames: [<fqdn>]
  tcpPortRanges: [{"from": <port>, "to": <port>}]
  segmentGroupId: <selected>
  serverGroups: [{"id": <selected>}]
  enabled: true
  bypassType: "NEVER"
  isCnameEnabled: true
  ipAnchored: false
```

If BA bookmark requested, include in creation:
```
  commonAppsDto:
    appsConfig:
      - appTypes: ["BROWSER_ACCESS"]
        name: <app_name>
        domain: <fqdn>
        applicationPort: <port>
        applicationProtocol: "HTTPS" (or "HTTP")
        certificateId: <ba_cert_id>  # get via zpa_list_ba_certificates
        enabled: true
```

**Step 3: Create access policy rule**
```
zpa_create_access_policy_rule:
  name: "Allow <app_name>"
  action: "ALLOW"
  policySetId: <from discovery>
  conditions:
    - operands:
        - objectType: "APP"
          lhs: "id"
          rhs: <segment_id>
    - operands:
        - objectType: "SCIM_GROUP"
          lhs: <idp_id>
          rhs: <scim_group_id>
```

**Step 4: Reorder rule (before catch-all)**

MCP does NOT support rule reordering. Use direct API:
```python
# Reorder rule to position N-1 (before catch-all/default deny)
# PUT /zpa/api/v1/policySet/{policySetId}/rule/{ruleId}/reorder/{newOrder}
# Returns HTTP 204 on success
import urllib.request, json

rules = # list current rules to find total count
new_order = len(rules) - 1  # before last rule (catch-all)

req = urllib.request.Request(
    f"https://api.zsapi.net/zpa/api/v1/policySet/{policy_set_id}/rule/{rule_id}/reorder/{new_order}",
    method="PUT"
)
req.add_header("Authorization", f"Bearer {token}")
urllib.request.urlopen(req, context=ctx)
```

**Step 5: Create DNS record (if requested)**

Use the technitium-dns skill if available, or create the record directly:
```bash
# Use the technitium-dns skill or your DNS provider's API
# Example: curl "http://<dns-server>:<port>/api/zones/records/add?token=<token>&domain=<fqdn>&type=A&ipAddress=<ip>"
```

**Step 6: Validate deployment**

1. Verify app segment exists and is enabled: `zpa_get_application_segment` with the new segment ID
2. Verify access rule exists and is in correct position: `zpa_list_access_policy_rules`, find the new rule
3. Verify connector group has active connectors: check server group -> connector group -> connector status
4. If DNS was created: verify DNS resolves (run `dig <fqdn> @<dns_server>` or use Python `socket.getaddrinfo`)
5. If BA bookmark: verify the segment has `clientlessApps` in its response

Print validation results as checklist:
```
Validation:
  [✓] App segment created and enabled
  [✓] Access rule at position N (before catch-all)
  [✓] Connectors healthy (2/2 active)
  [✓] DNS resolves: crm.example.com → 10.0.1.5
  [✓] BA bookmark configured
```
If any check fails, print `[✗]` with the reason and suggest fix.

**Step 7: Print summary**
```
=== Web Application Deployed ===
App:          <app_name>
Domain:       <fqdn>
Ports:        <ports>
Segment:      <segment_name> (ID: <id>)
Access Rule:  Allow <app_name> (position: <N>)
BA Bookmark:  <yes/no>
DNS Record:   <fqdn> → <ip> (zone: <zone>)
Access URL:   https://<fqdn>
Access Groups: <group_names>
```

---

## Template 2: SSH/RDP Server

### Collect Inputs

1. **Server name** — Display name (e.g., "DB Server 01")
2. **Domain (FQDN)** — Internal hostname (e.g., `db01.example.com`)
3. **Protocol** — SSH (port 22) or RDP (port 3389)
4. **PRA portal** — List existing portals via `zpa_list_pra_portals`, ask which one or create new
5. **PRA credential** — List existing via `zpa_list_pra_credentials`, ask which one or create new
6. **Who needs access** — SCIM groups for access policy

### Execute

**Step 1: Create application segment with PRA**
```
zpa_create_application_segment:
  name: <server_name>
  domainNames: [<fqdn>]
  tcpPortRanges: [{"from": <port>, "to": <port>}]
  segmentGroupId: <selected>
  serverGroups: [{"id": <selected>}]
  commonAppsDto:
    appsConfig:
      - appTypes: ["SECURE_REMOTE_ACCESS"]
        name: <server_name>
        domain: <fqdn>
        applicationPort: <port>
        applicationProtocol: <"SSH" or "RDP">
        enabled: true
```

**Step 2: Get PRA app ID from response**
```
# After creating segment, the response includes praApps[].id
# This is NOT the segment ID — it's the PRA-specific app ID
pra_app_id = response["praApps"][0]["id"]
```

**Step 3: Create PRA console (no MCP tool — use API directly)**
```python
# POST /zpa/api/v1/praConsole
console_data = json.dumps({
    "name": f"PRA - {server_name}",
    "praApplication": {"id": pra_app_id},
    "praPortals": [{"id": portal_id}],
    "description": f"PRA console for {fqdn}",
    "enabled": True,
    "praCredentials": [{"id": credential_id}] if credential_id else []
}).encode()

req = urllib.request.Request(
    "https://api.zsapi.net/zpa/api/v1/praConsole",
    data=console_data,
    method="POST"
)
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Content-Type", "application/json")
result = json.loads(urllib.request.urlopen(req, context=ctx).read())
```

**Note:** Check tenant console limit — API returns `entity.limit.exceeded` when exceeded.

**Step 4: Create access policy rule**

Same pattern as Template 1, with the APP condition pointing to the PRA segment.

**Step 5: Create DNS record (if needed)**

Same as Template 1.

**Step 6: Validate deployment**

1. Verify app segment exists with PRA app type: `zpa_get_application_segment` with the new segment ID, confirm `praApps` is populated
2. Verify PRA console created: `GET /zpa/api/v1/praConsole` and search for the new console by name
3. Verify access rule exists: `zpa_list_access_policy_rules`, find the new rule
4. Verify connector group has active connectors: check server group -> connector group -> connector status

Print validation results as checklist:
```
Validation:
  [✓] App segment created and enabled (PRA type)
  [✓] PRA console created: PRA - <server_name>
  [✓] Access rule at position N (before catch-all)
  [✓] Connectors healthy (2/2 active)
```
If any check fails, print `[✗]` with the reason and suggest fix.

**Step 7: Print summary**
```
=== PRA Server Deployed ===
Server:       <server_name>
Domain:       <fqdn>
Protocol:     <SSH/RDP> (port <port>)
PRA Portal:   <portal_name>
PRA Console:  <console_name>
Credential:   <credential_name>
Access Rule:  Allow <server_name>
Access URL:   https://<portal_domain>/console/<console_name>
Access Groups: <group_names>
```

---

## Template 3: ZIA Location

### Collect Inputs

1. **Location name** — Descriptive name (e.g., "Branch Paris 01")
2. **Profile** — CORPORATE / SERVER / WORKLOAD / EXTRANET
   - CORPORATE: full DNS + web inspection (user traffic, branches)
   - SERVER: minimal DNS, limited web (server workloads)
   - WORKLOAD: via Branch Connector (cloud workloads)
   - EXTRANET: extranet-specific filtering (partner traffic)
3. **Tunnel type** — IPsec or GRE
4. **Source IP or UFQDN** — Public IP or UFQDN for the tunnel source
5. **Enable IPS?** — yes/no (Intrusion Prevention)
6. **Enable SSL inspection?** — yes/no

### Execute

**Step 1: Create static IP (if using fixed public IP)**
```
zia_create_static_ip:
  ipAddress: <source_ip>
  comment: "Static IP for <location_name>"
```

**Step 2: Create VPN credential**
```
zia_create_vpn_credential:
  type: "UFQDN" or "IP"
  fqdn: <ufqdn> (if UFQDN type)
  ipAddress: <ip> (if IP type)
  preSharedKey: <generate or ask>
  comments: "VPN credential for <location_name>"
```

**Step 3: Create location**
```
zia_create_location:
  name: <location_name>
  ipAddresses: [<source_ip>]
  vpnCredentials: [{"id": <credential_id>}]
  profile: <selected_profile>
  ipsControl: <true/false>
  sslScanEnabled: <true/false>
  dnsBandwidthControl: true
  ofwEnabled: true
```

**Step 4: Activate**
```
zia_activate_configuration
```

**Step 5: Validate deployment**

1. Verify location created: `zia_get_location` with the new location ID
2. Verify VPN credential: `zia_get_vpn_credential` with the new credential ID
3. Check activation status: `zia_get_activation_status` — should be "ACTIVE"
4. Use `zia_geo_search` to confirm nearest ZIA DC for tunnel destination

Print validation results as checklist:
```
Validation:
  [✓] Location created: <location_name> (ID: <id>)
  [✓] VPN credential configured (type: <UFQDN/IP>)
  [✓] Configuration activated (status: ACTIVE)
  [✓] Nearest ZIA DC: <dc_name> (<dc_ip>)
  [—] Tunnel status: waiting for remote side
```
If any check fails, print `[✗]` with the reason and suggest fix. Note: tunnel UP verification requires the remote side to be configured.

**Step 6: Print tunnel config for remote side**
```
=== ZIA Location Deployed ===
Location:     <location_name>
Profile:      <profile>
Location ID:  <id>

Tunnel Configuration (for remote device):
  Type:           <IPsec/GRE>
  Destination:    <ZIA DC IP — use zia_geo_search to find nearest>
  Source IP:      <source_ip>
  Pre-Shared Key: <psk>
  IKE Version:    2
  Phase 1:        AES-256, SHA-256, DH Group 19
  Phase 2:        AES-256, SHA-256, PFS Group 19
  DPD Interval:   10s

Features Enabled:
  IPS:            <yes/no>
  SSL Inspection: <yes/no>

Next Steps:
  1. Configure the tunnel on your remote device using the parameters above
  2. Verify tunnel status in ZIA > Administration > VPN Tunnels
  3. Traffic should appear in ZIA logs within 2-3 minutes
```

---

## Template 4: ZTB Site (Optional — AirGap API)

**Requires AirGap API access. No MCP tools available — all operations use direct API calls.**

### Collect Inputs

1. **Site name** — Name for the ZTB site
2. **Gateway count** — Number of gateways (1 for standalone, 2 for HA)
3. **VLANs** — List of VLANs to configure (ID, subnet, name)
4. **PBR rules** — Traffic routing: which VLANs go to ZIA, ZPA, or direct
5. **IPsec config** — ZIA tunnel destination, PSK

### Execute

**Step 1: Create site**
```python
# POST /api/v2/Site/
site_data = json.dumps({
    "name": site_name,
    "description": f"ZTB site {site_name}"
}).encode()
# Use AirGap API: https://<site>-api.goairgap.com/api/v2/Site/
```

**Step 2: Create networks/VLANs**
```python
# POST /api/v2/Network/
for vlan in vlans:
    network_data = json.dumps({
        "name": vlan["name"],
        "vlanId": vlan["id"],
        "subnet": vlan["subnet"],
        "gateway": vlan["gateway"]
    }).encode()
    # POST to /api/v2/Network/
```

**Step 3: Configure PBR policies**
```python
# POST /api/v3/pbr/policies
# Requires ?gateway_id= parameter on all PBR endpoints
for rule in pbr_rules:
    pbr_data = json.dumps({
        "name": rule["name"],
        "action": rule["action"],  # "ZIA", "ZPA", "DIRECT"
        "sourceNetworks": rule["source_vlans"],
        "enabled": True
    }).encode()
    # POST to /api/v3/pbr/policies?gateway_id=<gw_id>
```

**Step 4: Configure IPsec**
```python
# POST /api/v2/cluster/ipsec-config
ipsec_data = json.dumps({
    "remoteGateway": ipsec_destination,
    "preSharedKey": psk,
    "ikeVersion": 2
}).encode()
```

**Step 5: Validate deployment**

1. Verify site created: `GET /api/v2/Site/` and confirm the new site appears
2. Verify networks created: `GET /api/v2/Network/` and confirm all VLANs are present

Print validation results as checklist:
```
Validation:
  [✓] Site created: <site_name> (ID: <id>)
  [✓] Networks created: <count> VLANs configured
  [✓] PBR policies: <count> rules configured
  [—] Gateway provisioning: async — check AirGap portal
```
If any check fails, print `[✗]` with the reason and suggest fix. Note: gateway provisioning is asynchronous and requires the gateway to boot and register.

**Step 6: Print summary**
```
=== ZTB Site Deployed ===
Site:         <site_name>
Gateways:     <count> (<standalone/HA>)
VLANs:        <list>
PBR Rules:    <count> rules configured
IPsec:        <destination> (IKEv2)

Management:
  AirGap Portal: https://<site>.goairgap.com
  AirGap API:    https://<site>-api.goairgap.com

Next Steps:
  1. Provision gateway hardware/VM with ZscalerOS
  2. Gateway will auto-register with the site
  3. Verify tunnel status in AirGap portal
  4. Enable enforcement on each network when ready:
     PATCH /api/v2/Network/enforcement
```

---

## Template 5: DLP Policy

### Collect Inputs

1. **Policy name** — Descriptive name (e.g., "Block Credit Card Uploads")
2. **Content to detect** — Describe what to detect:
   - Predefined patterns: credit cards, SSNs, IBANs, passports, etc.
   - Custom keywords or regex
   - File types
3. **Action** — BLOCK / ALLOW with logging / ALERT only
4. **Incident receiver** — Send incidents to ZIR? If yes, which receiver?

### Execute

**Step 1: Create or select DLP dictionary**

MCP only has read-only access to dictionaries. Use API directly for CRUD:
```python
# List existing dictionaries
# GET /zia/api/v1/dlpDictionaries
# Check if a suitable dictionary already exists

# Create new dictionary if needed
# POST /zia/api/v1/dlpDictionaries
dict_data = json.dumps({
    "name": f"Dict - {policy_name}",
    "description": f"Dictionary for {policy_name}",
    "dictionaryType": "PATTERNS_AND_PHRASES",
    "phrases": [{"phrase": kw, "action": "PHRASE_COUNT_TYPE_ALL"} for kw in keywords],
    "patterns": [{"pattern": p, "action": "PATTERN_COUNT_TYPE_ALL"} for p in patterns]
}).encode()
```

**Step 2: Create or select DLP engine**
```python
# GET /zia/api/v1/dlpEngines — list existing
# POST /zia/api/v1/dlpEngines — create new
engine_data = json.dumps({
    "name": f"Engine - {policy_name}",
    "description": f"Engine for {policy_name}",
    "engineExpression": f"D.{dictionary_id}.S > 0",
    "customDlpEngine": True
}).encode()
```

**Step 3: Create Web DLP rule**
```
zia_create_web_dlp_rule:
  name: <policy_name>
  action: <BLOCK / ALLOW>
  dlpEngines: [{"id": <engine_id>}]
  state: "ENABLED"
  protocols: ["FTP_RULE", "HTTPS_RULE", "HTTP_PROXY", "HTTP_RULE", "SSL_RULE"]
  zscalerIncidentReceiver: true (if incident receiver requested)
```

**Note:** The `receiver` field on webDlpRules is only exposed by the **legacy API** (`zsapi.<cloud>.net`), not OneAPI. If a specific incident receiver must be set, use the legacy endpoint:
```python
# PUT https://zsapi.<cloud>.net/api/v1/webDlpRules/{ruleId}
# Include "receiver": {"id": <receiver_id>} in the payload
```

**Step 4: Activate**
```
zia_activate_configuration
```

**Step 5: Validate deployment**

1. Verify DLP rule exists and is enabled: `zia_get_web_dlp_rule` with the new rule ID
2. Verify activation status: `zia_get_activation_status` — should be "ACTIVE"

Print validation results as checklist:
```
Validation:
  [✓] DLP rule created and enabled: <rule_name> (ID: <id>)
  [✓] Configuration activated (status: ACTIVE)
```
If any check fails, print `[✗]` with the reason and suggest fix.

**Step 6: Print summary**
```
=== DLP Policy Deployed ===
Policy:       <policy_name>
Dictionary:   <dict_name> (ID: <id>)
Engine:       <engine_name> (ID: <id>)
Rule:         <rule_name> (ID: <id>)
Action:       <BLOCK/ALLOW+LOG/ALERT>
Protocols:    FTP, HTTPS, HTTP, SSL
Receiver:     <receiver_name or N/A>

Detection:
  <description of what is detected>

Next Steps:
  1. Test with a sample upload matching the detection pattern
  2. Check ZIA logs > DLP Incidents for matches
  3. If using ZIR, verify incidents arrive in S3 buckets
```

---

## Template 6: Extranet Partner

### Collect Inputs

1. **Partner name** — Name of the partner organization (e.g., "Acme Corp")
2. **Source IPs/ranges** — Partner's public IPs or CIDR ranges
3. **Domains to access** — Internal domains the partner needs to reach
4. **Access level** — What the partner can do (web only, SSH, RDP, etc.)

### Execute

**Step 1: Create ZIA IP source group for partner**
```
zia_create_ip_source_group:
  name: "Partner - <partner_name>"
  ipAddresses: [<source_ips>]
  description: "Source IPs for partner <partner_name>"
```

**Step 2: Create ZIA extranet location**
```
zia_create_location:
  name: "Extranet - <partner_name>"
  ipAddresses: [<source_ips>]
  profile: "EXTRANET"
  description: "Extranet location for partner <partner_name>"
```

**Step 3: Create ZPA segment for partner domains**
```
zpa_create_application_segment:
  name: "Partner - <partner_name>"
  domainNames: [<partner_domains>]
  tcpPortRanges: <based on access level>
  segmentGroupId: <partner segment group>
  serverGroups: [{"id": <appropriate server group>}]
```

**Step 4: Create ZPA access policy with partner conditions**
```
zpa_create_access_policy_rule:
  name: "Allow Partner - <partner_name>"
  action: "ALLOW"
  conditions:
    - operands:
        - objectType: "APP"
          lhs: "id"
          rhs: <segment_id>
    - operands:
        - objectType: "SCIM_GROUP"
          lhs: <idp_id>
          rhs: <partner_scim_group_id>
```

**Step 5: Activate ZIA**
```
zia_activate_configuration
```

**Step 6: Validate deployment**

1. Verify ZIA location created with EXTRANET profile: `zia_get_location` with the new location ID
2. Verify ZPA segment created: `zpa_get_application_segment` with the new segment ID
3. Verify access rule exists: `zpa_list_access_policy_rules`, find the new rule

Print validation results as checklist:
```
Validation:
  [✓] ZIA location created: Extranet - <partner_name> (profile: EXTRANET)
  [✓] ZPA segment created: Partner - <partner_name>
  [✓] Access rule: Allow Partner - <partner_name>
```
If any check fails, print `[✗]` with the reason and suggest fix.

**Step 7: Print summary**
```
=== Extranet Partner Deployed ===
Partner:       <partner_name>
Source IPs:    <ip_list>
ZIA Location:  Extranet - <partner_name> (ID: <id>, profile: EXTRANET)
IP Group:      Partner - <partner_name> (ID: <id>)
ZPA Segment:   Partner - <partner_name> (ID: <id>)
Access Rule:   Allow Partner - <partner_name>
Domains:       <domain_list>
Access Level:  <description>

Next Steps:
  1. Share the tunnel/connectivity parameters with the partner
  2. Verify partner traffic appears in ZIA logs (location: Extranet - <partner_name>)
  3. Test ZPA access from partner network
  4. Configure URL filtering rules specific to the extranet location if needed
```

---

## Rollback

If anything goes wrong during deployment, rollback in reverse order:

1. **ZPA rules** — `zpa_delete_access_policy_rule` (requires `kwargs={"confirmed": true}` on second call)
2. **ZPA segments** — Check for BA/PRA refs first, then `zpa_delete_application_segment`
3. **ZIA rules** — Delete DLP rules, firewall rules, etc.
4. **ZIA locations** — `zia_delete_location`
5. **ZIA activate** — `zia_activate_configuration` to apply deletions
6. **DNS records** — Remove any DNS records created

Always compare current state against the pre-deployment snapshot to ensure clean rollback.

## Cutover Best Practices

When any deployment involves production traffic migration (location cutover, ZCC rollout, ZTB site activation), follow this framework.

### Pre-Cutover Timeline

| When | Action |
|------|--------|
| T-5 days | Confirm pilot phase complete (5-10% users, 1-2 weeks, no issues) |
| T-3 days | Send user communication (cutover date, expected downtime, support contacts) |
| T-2 days | Final validation — sample traffic through new config vs legacy |
| T-1 day | Stage config changes (NOT activated), verify monitoring dashboards live |
| T-0 | Go/no-go decision at war room |

### Staggered Rollout

**Never big-bang production.** Stagger all changes:
- Network/BGP: Activate, monitor convergence (30-60s), decision checkpoint at 2 min
- Policy rules: Activate, monitor hit rate, spot-check blocking. Checkpoint if >5% unexpected blocks.
- Client rollout (ZCC/MDM): Push 20% of devices per 5 min. Pause if install failure >20%.
- Legacy removal: Push removal 20% per 10 min. Pause if uninstall failure >10%.

### Rollback Triggers (Immediate Rollback)

- Critical app down (O365, Salesforce, VoIP)
- >20% of users unable to connect
- Policy enforcement broken (all allowed OR all blocked)
- Zscaler cloud unreachable
- Performance <50% of baseline

### War Room Roles

| Role | Responsibility |
|------|----------------|
| **Cutover Lead** | Timeline ownership, go/no-go decisions, escalation authority |
| **Infrastructure Lead** | Network config, MDM rollout, legacy removal |
| **Security Lead** | Policy enforcement monitoring, anomaly detection, false positive triage |
| **Application Lead** | App connectivity testing, user report monitoring |
| **Scribe** | Log all decisions, timestamps, outcomes for post-mortem |

### Success Criteria (4 Phases)

1. **T+0 to T+30 min:** Routes converge <2 min, >95% traffic routed, policies enforcing
2. **T+30 min to T+2h:** Client rollout >95%, legacy uninstall >95%, zero conflicts
3. **T+2h to T+4h:** Apps accessible, latency within 20% of baseline, DLP functional
4. **T+4h to T+24h:** >90% user satisfaction, 99%+ device migration, no critical incidents

## Common Mistakes

1. **Forgetting ZIA activation** — ZIA writes are staged until activated
2. **ZPA domain overlap** — Always check existing segments before creating new ones
3. **Rule ordering** — New ZPA rules go to bottom; always reorder before catch-all
4. **PRA console limit** — Tenant has a max console count; check before creating
5. **DLP receiver field** — Only available via legacy API, not OneAPI
6. **EXTRANET profile** — Use this for partner locations, not CORPORATE
7. **Missing snapshot** — Always snapshot before changes for rollback capability

## Related API Reference

For detailed endpoint documentation used by deployment templates:
- Web App / SSH-RDP / DLP deployments → See @zscaler-zia and @zscaler-zpa skills
- ZTB Site deployments → See @zscaler-ztb skill (AirGap API)
- Extranet deployments → See @zscaler-zpa skill (segment groups, access rules)
- DLP incident management after deployment → See @zscaler-zwa skill
