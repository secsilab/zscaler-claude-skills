---
name: zscaler-migrate
description: Use when migrating from a competitor product to Zscaler — assessment, vendor-specific policy translation, phased cutover with API execution. Supports Palo Alto, Check Point, Netskope, Cisco, Symantec, Forcepoint.
---

# Zscaler Migrate — Competitive Displacement with API Execution

Combines migration planning (assessment, policy translation, cutover) with live Zscaler API execution. This skill does both: plans the migration AND executes the configuration.

## Entry Point

Ask the user:

> **What are you migrating from?**
> 1. Palo Alto (Prisma Access / GlobalProtect / PAN-OS)
> 2. Check Point (NGFW / SmartConsole / VPN blades)
> 3. Netskope (SWG / CASB / NPA / DLP)
> 4. Cisco (Umbrella / AnyConnect / ASA / Firepower)
> 5. Symantec (WSS / ProxySG / Blue Coat / Vontu DLP)
> 6. Forcepoint (WSC / NGFW / DLP / FlexEdge)
> 7. Other / Generic assessment

Then ask:
> **What Zscaler products are in scope?** (ZIA, ZPA, ZTB, ZDX, ZCC — select all that apply)

## Phase 1: Assessment

### Step 1 — Export Legacy Config

Instruct the user to export their current configuration:

| Vendor | Export Method | Format |
|--------|-------------|--------|
| Palo Alto | `show config running` or API export | XML |
| Check Point | SmartConsole export or `mgmt_cli` | JSON/CSV |
| Netskope | Admin Console > Settings > Export | JSON |
| Cisco | `show running-config` or Umbrella export | Text/JSON |
| Symantec | Management Console export | XML/CSV |
| Forcepoint | Security Manager export | XML |

### Step 2 — Parse and Map Policies

For each policy in the legacy export, build a mapping row:

| Legacy Rule | Zscaler Equivalent | Product | MCP Tool | Gap? |
|-------------|-------------------|---------|----------|------|
| (from export) | (Zscaler config) | ZIA/ZPA/ZTB | (tool name) | Yes/No |

### Step 3 — Identify Gaps

Common gaps by vendor:

**Palo Alto:**
- Custom App-IDs → no direct translation. Create Zscaler custom URL categories as workaround.
- Zone-based rules → Zscaler uses identity-based (user/group/location). Requires directory integration mapping.
- Policy evaluation: PAN first-match → Zscaler most-restrictive. **Test extensively.**
- Panorama multi-tenant → Zscaler multi-tenancy requires account structure redesign.

**Check Point:**
- SmartConsole objects → Zscaler groups/categories. Manual rebuild required.
- VPN blade communities → ZPA app segments. 1:many mapping.
- Gateway-specific rules → Zscaler cloud-native (no gateway concept). Flatten rules.

**Netskope:**
- DLP rules (3,000+) → consolidation needed, not 1:1. Group by data type.
- NPA → ZPA. Private app definitions map well but connector placement differs.
- Steering config → ZCC forwarding profiles.

**Cisco:**
- Umbrella DNS policies → ZIA DNS control rules. Category mapping ~95% match.
- AnyConnect → ZCC. Profile migration requires rebuild.
- ASA ACLs → ZIA firewall rules. Flatten nested object-groups.

**Symantec:**
- ProxySG CPL rules → ZIA URL filtering. CPL syntax requires manual translation.
- Vontu DLP fingerprints → Zscaler EDM. Hash algorithm may differ — re-index required.
- Content Analysis → ZIA sandbox. Feature parity varies.

**Forcepoint:**
- WSC policies → ZIA URL filtering + SSL inspection. Direct mapping available.
- FlexEdge SD-WAN → ZTB. Topology redesign required.
- DLP → Zscaler DLP. Incident workflow rebuild needed.

### Step 4 — Risk Assessment

Score each gap:

| Risk | Impact | Mitigation |
|------|--------|------------|
| CRITICAL | Feature parity impossible | Accept risk or defer migration |
| HIGH | Workaround available but complex | Document workaround, test in pilot |
| MEDIUM | Minor behavioral difference | Monitor post-cutover |
| LOW | Cosmetic or non-functional | Ignore |

## Phase 2: Design & Configure (API Execution)

### Step 1 — Discover Current Zscaler State

Before making ANY changes, run discovery:

```
Use @zscaler-discover to scan the target tenant.
This populates memory/zscaler-tenant.md with current state.
```

### Step 2 — Take Pre-Migration Snapshot

```
Use @zscaler-snapshot to capture baseline.
All changes will be diffed against this snapshot.
```

### Step 3 — Execute Configuration by Product

**For ZIA policies (firewall, URL filtering, DLP, SSL):**
1. Create IP source/destination groups from legacy network objects → `zia_create_ip_source_group` / `zia_create_ip_destination_group`
2. Create URL categories from legacy categories → `zia_create_url_category`
3. Create firewall rules from mapped policies → `zia_create_cloud_firewall_rule`
4. Create URL filtering rules → `zia_create_url_filtering_rule`
5. Create SSL inspection rules with bypass list → `zia_create_ssl_inspection_rule`
6. Create DLP rules → `zia_create_web_dlp_rule`
7. **Activate:** `zia_activate_configuration`

**For ZPA policies (app segments, access rules):**
1. Create segment groups → `zpa_create_segment_group`
2. Create server groups → `zpa_create_server_group`
3. Create app segments from legacy VPN splits / private apps → `zpa_create_application_segment`
4. Create access policy rules → `zpa_create_access_policy_rule`
5. Reorder rules → `PUT /policySet/{id}/rule/{ruleId}/reorder/{order}` (API, no MCP)
6. No activation needed — ZPA changes are instant.

**For ZTB (branch sites, gateways):**
Load `@zscaler-ztb` and use AirGap API for site/gateway/VLAN/PBR configuration.

### Step 4 — Validate Configuration

After each product block:
1. Run `@zscaler-audit` to check for misconfigurations
2. Compare against pre-migration snapshot with `@zscaler-snapshot`
3. List all created resources and verify counts match the mapping table

## Phase 3: Cutover

Follow the cutover framework from `@zscaler-deploy` (Cutover Best Practices section).

Key reminders:
1. **Stagger rollout** — 20% per batch, never big-bang
2. **Uninstall legacy client BEFORE deploying ZCC** (especially GlobalProtect — routing conflicts)
3. **War room required** for production cutover
4. **Rollback procedure tested** before starting

## Phase 4: Post-Migration Validation

1. Run `@zscaler-audit` — full 22-check security posture scan
2. Take post-migration snapshot → `@zscaler-snapshot`
3. Compare pre vs post snapshots for drift
4. Monitor ZDX scores for 7 days (if ZDX deployed)
5. Tune DLP rules based on first-week false positive data

## Vendor-Specific Gotchas (Critical)

### Palo Alto → Zscaler
- **GlobalProtect + ZCC routing conflict:** Both are VPN clients. Uninstall GlobalProtect FIRST.
- **Certificate pinning:** Clients pin Prisma Access cert. Switching to Zscaler cert causes TLS failures. Distribute new cert or update client trust store.
- **URL category variance:** 5-10% mismatch between PAN and Zscaler URL categorization. Create custom categories for gaps.
- **Decryption expectation mismatch:** PAN controls which apps to decrypt; Zscaler decrypts by default. Users may perceive privacy concern — communicate early.
- **Incident correlation gap:** Panorama is a central console; Zscaler has distributed logs. Requires SIEM integration for equivalent visibility.

### Check Point → Zscaler
- **Gateway-specific rules don't map** — Zscaler is cloud-native with no gateway concept. Flatten rules.
- **VPN blade communities** — Map to ZPA segment groups. May require splitting large communities into multiple segments.
- **SmartConsole automation** — Check Point CLI/API scripts won't transfer. Rebuild automation using Zscaler MCP tools.

### Netskope → Zscaler
- **DLP rule count explosion** — Netskope allows very granular DLP. Consolidate to Zscaler patterns (fewer, broader rules).
- **Steering config** — Netskope client steering → ZCC forwarding profiles. Different configuration model.
- **CASB inline vs API** — Feature mapping is close but policy syntax differs. Rebuild policies.

### Cisco → Zscaler
- **AnyConnect posture** → ZCC posture profiles. Configuration concepts differ significantly.
- **Umbrella DNS-only mode** — Some orgs use DNS-only (no proxy). Moving to ZIA full proxy is a bigger change than expected.
- **ASA nested object-groups** → Flatten before mapping to Zscaler IP groups.

### Symantec → Zscaler
- **CPL (Content Policy Language)** is proprietary syntax. No automated translation. Manual policy rebuild required.
- **Vontu DLP fingerprints** use different hashing. Must re-index data with Zscaler EDM.
- **BlueCoat SG appliance** rules are order-dependent with complex layer evaluation. Simplify during migration.

### Forcepoint → Zscaler
- **WSC hybrid mode** (on-prem + cloud) has no Zscaler equivalent. Fully cloud-native migration required.
- **FlexEdge SD-WAN** → ZTB is a complete topology redesign, not a config migration.
- **DLP incident workflow** differences — Forcepoint has built-in case management; Zscaler uses ZWA or SIEM integration.

## Known Limitations

1. **No automated policy import** — Legacy config must be manually parsed and mapped. This skill provides the framework but a human must validate each mapping.
2. **URL category mismatch is expected** — 5-10% variance between any two vendors' URL categorization. Accept or create custom categories.
3. **Legacy automation won't transfer** — Scripts, API integrations, and SOAR playbooks targeting the old vendor must be rebuilt for Zscaler.
4. **Cutover requires maintenance window** — Plan 4-6 hours for production with 2-4 hours stabilization.
5. **Client conflicts** — Multiple security clients create routing and SSL conflicts. Strict uninstall-before-install order required.
