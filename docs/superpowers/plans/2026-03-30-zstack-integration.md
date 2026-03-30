# ZStack Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate zstack's field expertise into zscaler-claude-skills by enriching existing product skills with gotchas, creating a migration skill with API execution, and building a bridge skill that translates zstack design outputs into executable API sequences.

**Architecture:** Three-layer approach — (1) cherry-pick field gotchas from zstack into existing product skills, (2) create `/zscaler-migrate` skill combining zstack's vendor-specific playbooks with our MCP execution, (3) create `/zscaler-bridge` skill that takes zstack design documents and maps them to API call sequences. zstack remains a separate install for PS planning; our project handles execution.

**Tech Stack:** Markdown (SKILL.md files), Bash (install.sh), existing YAML frontmatter format.

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `skills/zscaler-zia/SKILL.md` | Add field gotchas: SSL bypass lists, CA models, compliance mapping, DLP phased rollout, regex DoS |
| Modify | `skills/zscaler-zpa/SKILL.md` | Add field gotchas: connector sizing, HA sync, FQDN vs IP matrix, SCIM latency, posture fail-open |
| Modify | `skills/zscaler-ztb/SKILL.md` | Add field gotchas: ZTP timeout, MTU mismatch, ARP storms, BGP convergence, VLAN trunking |
| Modify | `skills/zscaler-zcc/SKILL.md` | Add field gotchas: Z-Tunnel EOL, app profiles, deployment waves |
| Modify | `skills/zscaler-deploy/SKILL.md` | Add cutover best practices: pre-flight timeline, staggered rollout, war room roles, rollback triggers |
| Create | `skills/zscaler-migrate/SKILL.md` | Migration skill: assessment framework, 6 vendor playbooks with API execution, cutover runbook |
| Create | `skills/zscaler-bridge/SKILL.md` | Bridge skill: parse zstack design outputs, map to MCP tool sequences, execute with safety checks |
| Modify | `skills/zscaler/SKILL.md` | Add zscaler-migrate and zscaler-bridge to router product map and operational skills |
| Modify | `install.sh` | Add zscaler-migrate and zscaler-bridge to install lists |
| Modify | `README.md` | Update skill count, add new skills to table |

---

### Task 1: Enrich ZIA skill with field gotchas

**Files:**
- Modify: `skills/zscaler-zia/SKILL.md` (append before `## Location Profiles` section, ~line 998)

- [ ] **Step 1: Add Field Gotchas section to ZIA skill**

Insert the following content before the `## Location Profiles` section (after `## Known Limitations` item 10):

```markdown

## Field Gotchas (Deployment Experience)

### SSL Inspection

**Three CA Models — Pick One Before Go-Live:**

| Model | Pros | Cons | Best For |
|-------|------|------|----------|
| Zscaler CA (default) | Zero deployment burden, auto-lifecycle | Cert pinning breaks (Slack, Teams), users see Zscaler CA | Fast deployments, low compliance |
| Custom Sub-CA | Customer controls CA, fewer pinning issues | CSR/key management, 3-year renewal burden | HIPAA, PCI environments |
| BYOK | FIPS 140-2 compliant, DoD acceptable | Complex setup (8-12 weeks), HSM cost | DoD DFARS, sovereign |

**SSL Bypass List (CRITICAL — No bypass = 10,000 false alerts/day):**
- **Always bypass:** Banks (cert pinning breaks login), Healthcare (`*.mychart.org`, `*.epic.com`), APIs (`github.com`, `stripe.com`, `webhook.slack.com`), SaaS pinners (Slack desktop, Teams desktop)
- **Bypass by category:** Financial services, healthcare portals, P2P/torrents
- **Never bypass:** Streaming (want bandwidth throttle visibility), social media (DLP inspection needed)
- **Rule of thumb:** Start with 80% traffic inspected, bypass risky 20%. Gradually expand. Overreach = user circumvention via personal VPN.

**Compliance Mapping for SSL Inspection:**
- **HIPAA:** Permitted with conditions — must use customer CA (Model 2/3), audit log all access
- **PCI-DSS:** Permitted — must NOT inspect payment card data; whitelist payment processors
- **GDPR:** Not illegal in EU, but must disclose interception to users (use customer CA for comfort)
- **DoD DFARS:** BYOK (Model 3) only acceptable

### DLP Deployment

**Phased Rollout (Don't Skip Phases):**
1. **Week 1-4:** Audit mode (no blocking) — establish false positive baseline
2. **Week 5-8:** Caution mode (warnings + user coaching) — measure user compliance
3. **Week 9+:** Selective block — start with high-confidence patterns only (exact PII, credit cards)
- **Success metrics per phase:** False positive rate <0.5%, block rate <2% of traffic, user complaints <0.1%
- **Rollback trigger:** If any metric exceeds 3x threshold, revert to previous phase

**EDM (Exact Data Match) Gotchas:**
- EDM matches are "all or nothing" — partial field matches fail if formatting differs (spaces, dashes). **Always implement field normalization.**
- Hash uploads expose sensitive data during transfer — use encrypted SFTP with certificate pinning
- Index refresh windows create detection gaps — records added between refreshes go undetected until next cycle
- High-cardinality fields (emails) with EDM + pattern matching = duplicate detections. Implement correlation logic.
- Multi-field EDM requires ALL fields to match exactly — one field sanitized differently = silent miss

**Regex Safety:**
- Complex DLP regex patterns can cause exponential matching (ReDoS). Audit pattern complexity before deploying.
- Credit card regex must reject test numbers (`4111-1111-1111-1111`)

### Policy Design

**Rule Evaluation Order (Recommended):**
1. Block Malware/C&C (non-negotiable, top of policy)
2. Block High-Risk Countries (geo-blocking)
3. Block P2P/Torrents (bandwidth protection)
4. Allow Business Critical (Salesforce, Box, O365)
5. Caution Social Media (coaching page)
6. Block News/Entertainment (or throttle)
7. Default action (Block recommended)

**Common Policy Mistakes:**
- Overly broad allow rules kill entire policy stack
- No exceptions process → endless "Can I allow YouTube?" requests
- Not logging → can't prove compliance or troubleshoot
- Dynamic categorization disabled → stale URL definitions
- Bandwidth throttling too aggressive → users circumvent via personal VPN
```

- [ ] **Step 2: Verify the edit is clean**

Run: `head -1020 skills/zscaler-zia/SKILL.md | tail -50` to verify the new section sits cleanly between Known Limitations and Location Profiles.

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-zia/SKILL.md
git commit -m "feat(zia): add field gotchas from zstack — SSL bypass, CA models, DLP phased rollout, compliance mapping"
```

---

### Task 2: Enrich ZPA skill with field gotchas

**Files:**
- Modify: `skills/zscaler-zpa/SKILL.md` (append after `## Safety Rules` section, before end of file)

- [ ] **Step 1: Add Field Gotchas section to ZPA skill**

Append the following content after the `## Safety Rules` section:

```markdown

## Field Gotchas (Deployment Experience)

### Connector Sizing & Placement

**Sizing Rules (Field-Proven):**
- 1 connector per 500 concurrent users
- Max 2,500 users per HA pair
- Baseline: 4 vCPU, 8GB RAM
- High load (2,500+ users): 8 vCPU, 16GB RAM
- Minimum 20GB free on `/var` — logs fill fast, rotate daily

**Connector Group Scope:**
- One group per logical boundary (DC / cloud region)
- **Never mix DC + cloud in same group** — latency penalties from cross-region traffic
- Each group = failover domain = same policy evaluation point

**HA Pair Gotchas:**
- Active-passive recommended (simpler); active-active requires same subnet
- Connectors must have independent power, network, disk to avoid cascading failure
- Health check: every 30s, >60s disconnection triggers failover
- **License expiration silently stops forwarding** — no error, just dropped traffic

**Network Requirements:**
- Outbound TCP/UDP 443 only — NO inbound ports
- Whitelist ZPA broker IP **ranges**, not individual IPs (they rotate weekly)
- CIDR overlap between app segment servers and connector traffic CIDR causes routing loops

### App Segment Design

**FQDN vs IP Decision Matrix:**

| Use Case | FQDN vs IP | Double-Encrypt | Server Group |
|----------|-----------|----------------|--------------|
| Kubernetes/cloud | FQDN wildcard | Yes if sensitive | 10+ with health probe |
| Legacy Windows | IP static | No | 2-4 manual failover |
| Database (PII) | IP + FQDN | **Yes (mandatory)** | 3-5 with priority |
| API gateway | FQDN exact | Yes if auth critical | 5+ active-active |

**Segment Gotchas:**
- FQDN resolution happens on **connector**, not user device. If connector can't resolve → segment fails silently.
- Exact FQDN takes precedence over wildcard — create exact for critical apps, wildcard for catch-all
- Double-encrypt adds latency — measure before enforcing for high-frequency apps
- Server group health probes disabled by default — **enable for production** (TCP/HTTP, 30s interval)
- Port mismatch: app listens 8080 internally, segment publishes 443 → must match exactly

### Identity & Access

**SCIM Sync Gotchas:**
- SCIM changes propagate in 1-4 hours. For urgent access changes, use manual override.
- **Group name casing matters:** "Engineering" ≠ "engineering" — validate exact case from IdP
- Posture checks evaluated every login. Stale posture from old session can block legitimate access.
- Some posture check modules fail-open on crash (allow access). **Verify fail-closed behavior.**

**Policy Rule Gotchas:**
- First-matching rule wins. Contradictory rules fail silently — the first one matched applies.
- Bypass rules inherit all previous rules. Narrow bypass scope to specific segments only.
- Policy grants access but servers not in connector group = connection timeout, no clear error
```

- [ ] **Step 2: Verify the edit is clean**

Run: `tail -60 skills/zscaler-zpa/SKILL.md` to verify the new section appends cleanly.

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-zpa/SKILL.md
git commit -m "feat(zpa): add field gotchas from zstack — connector sizing, FQDN vs IP matrix, SCIM sync, posture fail-open"
```

---

### Task 3: Enrich ZTB skill with field gotchas

**Files:**
- Modify: `skills/zscaler-ztb/SKILL.md` (append after `## Known Limitations` section)

- [ ] **Step 1: Add Field Gotchas section to ZTB skill**

Insert after `## Known Limitations` item 7:

```markdown

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
```

- [ ] **Step 2: Verify the edit is clean**

Run: `grep -n "## Field Gotchas\|## Known Limitations\|## API Reference" skills/zscaler-ztb/SKILL.md | tail -5` to verify section ordering.

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-ztb/SKILL.md
git commit -m "feat(ztb): add field gotchas from zstack — ZTP enrollment, MTU mismatch, ARP storms, rollback procedure"
```

---

### Task 4: Enrich ZCC skill with field gotchas

**Files:**
- Modify: `skills/zscaler-zcc/SKILL.md` (append after last section)

- [ ] **Step 1: Read current ZCC skill to find insertion point**

Run: `cat -n skills/zscaler-zcc/SKILL.md | tail -20` to find the end of the file.

- [ ] **Step 2: Add Field Gotchas section to ZCC skill**

Append at end of file:

```markdown

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
```

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-zcc/SKILL.md
git commit -m "feat(zcc): add field gotchas from zstack — Z-Tunnel EOL, app profiles, deployment waves, GlobalProtect conflict"
```

---

### Task 5: Enrich Deploy skill with cutover best practices

**Files:**
- Modify: `skills/zscaler-deploy/SKILL.md` (add new section before `## Common Mistakes`)

- [ ] **Step 1: Read current deploy skill to find insertion point**

Run: `grep -n "## Common Mistakes" skills/zscaler-deploy/SKILL.md` to find the line number.

- [ ] **Step 2: Add Cutover Best Practices section**

Insert before `## Common Mistakes`:

```markdown

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

```

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-deploy/SKILL.md
git commit -m "feat(deploy): add cutover best practices from zstack — timeline, staggered rollout, rollback triggers, war room"
```

---

### Task 6: Create migration skill (`/zscaler-migrate`)

**Files:**
- Create: `skills/zscaler-migrate/SKILL.md`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p skills/zscaler-migrate
```

- [ ] **Step 2: Write the migration skill**

Create `skills/zscaler-migrate/SKILL.md` with the following content:

```markdown
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
```

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-migrate/SKILL.md
git commit -m "feat: add zscaler-migrate skill — competitive displacement with assessment, 6 vendor playbooks, API execution"
```

---

### Task 7: Create bridge skill (`/zscaler-bridge`)

**Files:**
- Create: `skills/zscaler-bridge/SKILL.md`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p skills/zscaler-bridge
```

- [ ] **Step 2: Write the bridge skill**

Create `skills/zscaler-bridge/SKILL.md` with the following content:

```markdown
---
name: zscaler-bridge
description: Use when translating a Zscaler design document (from zstack or manual planning) into executable API calls. Takes architecture docs, policy matrices, or deployment plans and maps them to MCP tool sequences.
---

# Zscaler Bridge — Plan-to-Execute

Translates Zscaler design documents into executable API call sequences. Works with outputs from zstack (PS planning skills) or any structured design document.

## When to Use

- After running zstack design skills (`/zia-policy`, `/zpa-segments`, `/ztb-design`, etc.) and wanting to execute the design
- When you have a policy matrix, architecture doc, or deployment plan and need to configure the tenant
- When a PS consultant has produced a design and an engineer needs to implement it

## Entry Point

Ask the user:

> **Provide the design document or paste the relevant section.**
> This can be:
> - A zstack skill output (policy matrix, segment design, config artifact)
> - A manual design document (architecture doc, SOW scope)
> - A specific configuration request with structured requirements

## Phase 1: Parse Design

### Step 1 — Identify Components

Read the design document and extract all Zscaler components mentioned:

| Component | Product | Count | Action |
|-----------|---------|-------|--------|
| (e.g., "SSL inspection with custom CA") | ZIA | 1 | Create SSL inspection rule + bypass list |
| (e.g., "App segment for CRM") | ZPA | 1 | Create segment + access rule |

### Step 2 — Map to API Calls

For each component, determine the execution sequence:

| # | Component | MCP Tool / API | Dependencies | Notes |
|---|-----------|---------------|-------------|-------|
| 1 | IP source group | `zia_create_ip_source_group` | None | Create first (referenced by rules) |
| 2 | Firewall rule | `zia_create_cloud_firewall_rule` | #1 | References IP group |
| 3 | Activate | `zia_activate_configuration` | #2 | After all ZIA writes |

**Dependency rules:**
- Groups/categories before rules (rules reference groups)
- Segments before policies (policies reference segments)
- Connectors before segments (segments need a server group with connectors)
- ZIA activation after all ZIA changes (batch, not per-change)
- ZPA needs no activation

### Step 3 — Present Execution Plan

Show the user the complete execution plan as a numbered checklist:

```
Execution Plan:
1. [ZIA] Create IP source group "Branch-Offices" — zia_create_ip_source_group
2. [ZIA] Create URL category "Blocked-Sites" — zia_create_url_category
3. [ZIA] Create firewall rule "Block-Torrents" — zia_create_cloud_firewall_rule
4. [ZIA] Activate configuration — zia_activate_configuration
5. [ZPA] Create segment group "CRM-Apps" — zpa_create_segment_group
6. [ZPA] Create app segment "CRM-Portal" — zpa_create_application_segment
7. [ZPA] Create access policy rule — zpa_create_access_policy_rule

Proceed? (yes / modify / abort)
```

**Wait for user confirmation before executing.**

## Phase 2: Pre-Flight

Before executing ANY changes:

1. **Verify connectivity:** `zscaler_check_connectivity`
2. **Take snapshot:** Use `@zscaler-snapshot` to capture current state
3. **Discover current state:** Check for conflicts (duplicate domains, overlapping rules, existing groups with same names)
4. **Validate IDs:** Fetch all referenced IDs (segment groups, server groups, SCIM groups, IdP ID, policy set IDs)

## Phase 3: Execute

Execute the plan step by step:

1. **Run each step in order** (respecting dependencies)
2. **After each step:** Verify the resource was created (re-read and confirm)
3. **On error:** Stop, report the error, ask user whether to continue or rollback
4. **After all ZIA steps:** Run `zia_activate_configuration`
5. **After all steps:** Run a summary verification — list all created resources

### Execution Pattern

```
For each step in the execution plan:
  1. Announce: "Step N: Creating [component]..."
  2. Execute the MCP tool call
  3. Verify: Read back the created resource to confirm
  4. Report: "Step N complete — [resource name] created (ID: xxx)"
  5. If error: "Step N FAILED — [error]. Stop here? (yes/skip/abort)"
```

## Phase 4: Validate

After execution:

1. **Run audit:** Use `@zscaler-audit` for the affected products
2. **Compare snapshot:** Use `@zscaler-snapshot` to diff pre vs post
3. **Verify against design:** For each component in the design doc, confirm it exists in the tenant
4. **Report:** Summary table showing design intent vs actual configuration

| Design Component | Status | Zscaler Resource | ID |
|-----------------|--------|------------------|----|
| SSL inspection rule | Created | "SSL-Inspect-All" | 12345 |
| CRM app segment | Created | "CRM-Portal" | 67890 |

## Rollback

If the user wants to undo changes:

1. Load the pre-execution snapshot
2. Identify all resources created during this session
3. Delete them in reverse dependency order (rules before groups, segments before segment groups)
4. For ZIA: activate after all deletes
5. Verify snapshot matches pre-execution state

## Design Document Formats Supported

This skill can parse:

1. **zstack policy matrices** — Tables with columns for rule name, action, source, destination, ports
2. **zstack architecture docs** — Structured markdown with component lists and configuration details
3. **Manual spreadsheets** — Pasted CSV/table with component definitions
4. **SOW scope sections** — Extract configurable components from SOW module descriptions
5. **Free-form requirements** — Natural language design requirements (least precise, will ask clarifying questions)

## Known Limitations

1. **ZTB has no MCP tools** — ZTB components require AirGap API calls (Python urllib). The skill will generate the Python code but cannot execute via MCP.
2. **ZIdentity writes require Python SDK** — User/group creation not available via MCP. Will generate SDK code.
3. **Rule reordering** — ZPA rule reorder not in MCP. Will use direct API call.
4. **Complex designs** — Designs with 50+ components should be split into phases. Executing all at once risks partial failure states.
5. **Design ambiguity** — Vague designs ("set up SSL inspection") require clarifying questions. The more specific the design doc, the more precise the execution.
```

- [ ] **Step 3: Commit**

```bash
git add skills/zscaler-bridge/SKILL.md
git commit -m "feat: add zscaler-bridge skill — translates design documents into executable MCP tool sequences"
```

---

### Task 8: Update router, installer, and README

**Files:**
- Modify: `skills/zscaler/SKILL.md` (~line 36)
- Modify: `install.sh` (~line 23)
- Modify: `README.md`

- [ ] **Step 1: Read current router skill operational section**

Run: `grep -n "Operational Skills\|@zscaler-migrate\|@zscaler-bridge" skills/zscaler/SKILL.md` to find insertion points.

- [ ] **Step 2: Add new skills to router**

In `skills/zscaler/SKILL.md`, add to the **Operational Skills** table (after the `@zscaler-troubleshoot` row):

```markdown
| @zscaler-migrate | Competitive migration (assessment, 6 vendor playbooks, API execution) |
| @zscaler-bridge | Translate design documents into executable API call sequences |
```

- [ ] **Step 3: Update install.sh**

In `install.sh`, update the `OPERATIONAL` variable (line 22) to include the new skills:

Change:
```bash
OPERATIONAL="zscaler zscaler-setup zscaler-onboard zscaler-discover zscaler-audit zscaler-troubleshoot zscaler-snapshot zscaler-deploy"
```

To:
```bash
OPERATIONAL="zscaler zscaler-setup zscaler-onboard zscaler-discover zscaler-audit zscaler-troubleshoot zscaler-snapshot zscaler-deploy zscaler-migrate zscaler-bridge"
```

Also add to the help text (after the deploy line, ~line 64):

```bash
echo "  /zscaler-migrate      Competitive migration (6 vendor playbooks + API execution)"
echo "  /zscaler-bridge       Translate design docs into API call sequences"
```

- [ ] **Step 4: Read current README**

Run: `cat -n README.md` to see full content and find the skills table.

- [ ] **Step 5: Update README**

Update the skills count (from 19 to 21) and add the two new skills to the appropriate table.

Add to the operational skills section:

```markdown
| `/zscaler-migrate` | zscaler-migrate | — | Competitive migration — assessment, 6 vendor playbooks, cutover with API execution |
| `/zscaler-bridge` | zscaler-bridge | — | Translate design docs (from zstack or manual) into executable API sequences |
```

Update the total endpoint count header to reflect "21 modular skills".

- [ ] **Step 6: Commit**

```bash
git add skills/zscaler/SKILL.md install.sh README.md
git commit -m "feat: register zscaler-migrate and zscaler-bridge in router, installer, and README"
```

---

### Task 9: Verify everything works

**Files:**
- All modified files

- [ ] **Step 1: Run install script in dry-run mode**

```bash
bash -n install.sh  # syntax check only
```

- [ ] **Step 2: Verify all skill frontmatter is valid**

```bash
for f in skills/*/SKILL.md; do
  name=$(head -5 "$f" | grep "^name:" | cut -d' ' -f2-)
  desc=$(head -5 "$f" | grep "^description:" | head -c 80)
  if [ -z "$name" ]; then
    echo "MISSING name: $f"
  else
    echo "OK: $name"
  fi
done
```

- [ ] **Step 3: Verify no broken markdown**

```bash
# Check all new/modified skills have required sections
for skill in zscaler-migrate zscaler-bridge; do
  echo "=== $skill ==="
  grep "^## " "skills/$skill/SKILL.md"
done
```

- [ ] **Step 4: Verify skill count matches README**

```bash
echo "Skill directories: $(ls -d skills/*/ | wc -l)"
echo "README claims: $(grep -o '[0-9]* modular skills' README.md)"
```

- [ ] **Step 5: Final commit if any fixes needed**

Only if Steps 1-4 revealed issues. Fix and commit with descriptive message.
