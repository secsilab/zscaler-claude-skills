---
name: zscaler-zia
version: 1.2.0
postman_revision: 2026-03-30
description: Use when working with ZIA — firewall rules, URL filtering, DLP policies, SSL inspection, cloud apps, locations, GRE tunnels, sandbox, ATP, bandwidth, DNS control, forwarding, NAT, PAC files, admin audit logs, traffic management, AppTotal, Cloud NSS, VZEN, shadow IT, IoT, traffic capture, policy export.
---

# Zscaler Internet Access (ZIA)

## Overview

ZIA is Zscaler's cloud-based secure web gateway. Use this skill for firewall policies, URL filtering, DLP, SSL inspection, cloud app control, location management, traffic forwarding (GRE, VPN, static IPs), sandbox analysis, and advanced threat protection.

## MCP Tools

### Locations & Tunnels

| Operation | MCP Tool |
|-----------|----------|
| List locations | `zia_list_locations` |
| Get/Create/Update/Delete location | `zia_get_location` / `zia_create_location` / `zia_update_location` / `zia_delete_location` |
| List/Get/Create/Delete GRE tunnels | `zia_list_gre_tunnels` / `zia_get_gre_tunnel` / `zia_create_gre_tunnel` / `zia_delete_gre_tunnel` |
| List GRE ranges | `zia_list_gre_ranges` |
| List/Get/Create/Update/Delete static IPs | `zia_list_static_ips` / `zia_get_static_ip` / `zia_create_static_ip` / `zia_update_static_ip` / `zia_delete_static_ip` |
| List/Get/Create/Update/Delete VPN credentials | `zia_list_vpn_credentials` / `zia_get_vpn_credential` / `zia_create_vpn_credential` / `zia_update_vpn_credential` / `zia_delete_vpn_credential` |

### Cloud Firewall

| Operation | MCP Tool |
|-----------|----------|
| List/Get/Create/Update/Delete rules | `zia_list_cloud_firewall_rules` / `zia_get_cloud_firewall_rule` / `zia_create_cloud_firewall_rule` / `zia_update_cloud_firewall_rule` / `zia_delete_cloud_firewall_rule` |
| List/Get/Create/Update/Delete IP source groups | `zia_list_ip_source_groups` / `zia_get_ip_source_group` / `zia_create_ip_source_group` / `zia_update_ip_source_group` / `zia_delete_ip_source_group` |
| List/Get/Create/Update/Delete IP destination groups | `zia_list_ip_destination_groups` / `zia_get_ip_destination_group` / `zia_create_ip_destination_group` / `zia_update_ip_destination_group` / `zia_delete_ip_destination_group` |
| List/Get/Create/Update/Delete network app groups | `zia_list_network_app_groups` / `zia_get_network_app_group` / `zia_create_network_app_group` / `zia_update_network_app_group` / `zia_delete_network_app_group` |
| List/Get/Create/Update/Delete rule labels | `zia_list_rule_labels` / `zia_get_rule_label` / `zia_create_rule_label` / `zia_update_rule_label` / `zia_delete_rule_label` |

### URL Filtering

| Operation | MCP Tool |
|-----------|----------|
| List/Get/Create/Update/Delete URL filtering rules | `zia_list_url_filtering_rules` / `zia_get_url_filtering_rule` / `zia_create_url_filtering_rule` / `zia_update_url_filtering_rule` / `zia_delete_url_filtering_rule` |
| List/Get/Create/Update/Delete URL categories | `zia_list_url_categories` / `zia_get_url_category` / `zia_create_url_category` / `zia_update_url_category` / `zia_delete_url_category` |
| Add/Remove URLs from category | `zia_add_urls_to_category` / `zia_remove_urls_from_category` |

### SSL Inspection

| Operation | MCP Tool |
|-----------|----------|
| List/Get/Create/Update/Delete SSL inspection rules | `zia_list_ssl_inspection_rules` / `zia_get_ssl_inspection_rule` / `zia_create_ssl_inspection_rule` / `zia_update_ssl_inspection_rule` / `zia_delete_ssl_inspection_rule` |

### DLP

| Operation | MCP Tool |
|-----------|----------|
| List/Get/Create/Update/Delete Web DLP rules | `zia_list_web_dlp_rules` / `zia_get_web_dlp_rule` / `zia_create_web_dlp_rule` / `zia_update_web_dlp_rule` / `zia_delete_web_dlp_rule` |
| List DLP rules (lite) | `zia_list_web_dlp_rules_lite` |
| Get DLP dictionaries (read-only) | `get_zia_dlp_dictionaries` |
| Get DLP engines (read-only) | `get_zia_dlp_engines` |

### Sandbox

| Operation | MCP Tool |
|-----------|----------|
| Get sandbox report | `zia_get_sandbox_report` |
| Get behavioral analysis | `zia_get_sandbox_behavioral_analysis` |
| Get sandbox quota | `zia_get_sandbox_quota` |
| Get file hash count | `zia_get_sandbox_file_hash_count` |

### ATP & Auth

| Operation | MCP Tool |
|-----------|----------|
| List/Add/Delete ATP malicious URLs | `zia_list_atp_malicious_urls` / `zia_add_atp_malicious_urls` / `zia_delete_atp_malicious_urls` |
| List/Add/Delete auth exempt URLs | `zia_list_auth_exempt_urls` / `zia_add_auth_exempt_urls` / `zia_delete_auth_exempt_urls` |

### Cloud Applications

| Operation | MCP Tool |
|-----------|----------|
| List cloud apps | `zia_list_cloud_applications` |
| List custom tags | `zia_list_cloud_application_custom_tags` |
| Bulk update | `zia_bulk_update_cloud_applications` |

### Users (read-only)

| Operation | MCP Tool |
|-----------|----------|
| List users | `get_zia_users` |
| List groups | `get_zia_user_groups` |
| List departments | `get_zia_user_departments` |

### Activation

| Operation | MCP Tool |
|-----------|----------|
| Get activation status | `zia_get_activation_status` |
| Activate configuration | `zia_activate_configuration` |

### Geo Search

| Operation | MCP Tool |
|-----------|----------|
| Geo search (city/region lookup) | `zia_geo_search` |


For full API endpoint reference, see ENDPOINTS.md in this skill directory.

## Authentication

OneAPI OAuth2: `POST https://<vanity>.zslogin.net/oauth2/v1/token` with `client_credentials` grant.

Base URL: `https://api.zsapi.net/zia/api/v1`

Legacy API: `https://zsapi.<cloud>.net/api/v1` (only needed for specific fields not exposed by OneAPI).

Cloud domains: `zscaler.net`, `zscalerone.net`, `zscalertwo.net`, `zscalerthree.net`, `zscloud.net`, `zscalerbeta.net`, `zscalergov.net`

## IMPORTANT: Activation Required

**Every ZIA write operation requires activation to take effect.**

After any ZIA create/update/delete, call `zia_activate_configuration` (MCP) or `POST /status/activate` (API). Changes are staged and invisible to users until activated.

## Common Patterns

### Create firewall rule with activation
1. Create IP source/destination groups if needed
2. Create network application group if needed
3. `zia_create_cloud_firewall_rule` with references to groups
4. `zia_activate_configuration`

### Create DLP policy (dictionary + engine + rule)
1. `POST /dlpDictionaries` to create custom dictionary (API, no MCP tool for create)
2. `POST /dlpEngines` to create engine referencing the dictionary (API)
3. `zia_create_web_dlp_rule` referencing the engine (MCP)
4. `zia_activate_configuration`

### Add location with VPN credentials and static IP
1. `zia_create_static_ip` for the location's public IP
2. `zia_create_vpn_credential` with the static IP reference
3. `zia_create_location` referencing the VPN credential
4. `zia_activate_configuration`

### URL filtering with custom category
1. `zia_create_url_category` with URLs to match
2. `zia_create_url_filtering_rule` referencing the category
3. `zia_activate_configuration`

## MCP Tool Gaps (Use API Directly)

| Feature | MCP Available? | API Endpoint |
|---------|---------------|-------------|
| DNS Control rules | NO | `GET/POST/PUT/DELETE /firewallDnsRules` |
| IPS Control rules | NO | `GET/POST/PUT/DELETE /firewallIpsRules` |
| Bandwidth Control | NO | `/bandwidthClasses`, `/bandwidthControlRules` |
| File Type Control | NO | `/fileTypeRules` (not in Postman collection but exists) |
| Malware Protection | NO | `/cyberThreatProtection/malware*` |
| Advanced Threat Protection settings | NO | `/cyberThreatProtection/advancedThreatSettings` |
| Forwarding Control rules | NO | `/forwardingRules`, `/zpaGateways` |
| PAC files | NO | `/pacFiles` |
| Admin management | NO | `/adminUsers`, `/adminRoles/lite` |
| DLP dictionary/engine CRUD | NO | `/dlpDictionaries`, `/dlpEngines` (MCP is read-only) |
| DLP notification templates | NO | `/dlpNotificationTemplates` |
| NSS feeds/servers | NO | `/nssFeeds`, `/nssServers` |
| Intermediate CA certificates | NO | `/intermediateCaCertificate` |
| NAT control rules | NO | `/dnatRules` |
| Traffic capture rules | NO | `/trafficCaptureRules` |
| CASB DLP/Malware rules | NO | `/casbDlpRules`, `/casbMalwareRules` |
| Service Edges | NO | `/virtualZenNodes`, `/virtualZenClusters` |

## Known Limitations

1. **`receiver` field on webDlpRules** only exposed by Legacy API (`https://zsapi.<cloud>.net/api/v1`), not OneAPI
2. **DLP dictionary/engine CRUD**: MCP tools are read-only (`get_zia_dlp_dictionaries`, `get_zia_dlp_engines`). Use API directly for create/update/delete.
3. **`zia_list_cloud_firewall_rules` with search parameter** returns 400. List all rules and filter client-side.
4. **DLP rule PUT requires full body**: Cannot send partial updates. Clone the original, remove read-only fields (`modifiedTime`, `modifiedBy`, `creationTime`, `lastModifiedTime`), then modify.
5. **DLP `fileTypes` vs `fileTypeCategories`**: PUT accepts ONLY `fileTypeCategories` (objects with `id`). If both fields are present, API returns 400.
6. **DLP notification template**: Requires `auditor` to also be set (both null or both non-null).
7. **File Type Control**: POST uses `fileTypes` (string list), PUT uses `fileTypeCategories` (object list with `id`). ~13 DLP file type category IDs are invalid for FTC.
8. **URL filtering rule update**: MCP `zia_update_url_filtering_rule` requires ALL mandatory fields (`name`, `rank`, `order`, `rule_action`) even for simple state changes.
9. **Location profiles**: SERVER profiles don't inspect DNS. Use CORPORATE for full DNS inspection and logging.
10. **WebSocket/AI apps**: ZIA cannot inspect WebSocket content to distinguish chat vs file upload (e.g., Manus uses socket.io for both).

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

## Location Profiles

| Profile | DNS Inspection | Web Inspection | Use Case |
|---------|---------------|----------------|----------|
| **CORPORATE** | Full (DNS proxy + logging) | Full | User traffic, branch offices |
| **SERVER** | Minimal (no DNS proxy) | Limited | Server workloads, automated traffic |
| **WORKLOAD** | Via Branch Connector | Via Branch Connector | Cloud/ZTB workloads |
| **EXTRANET** | Extranet-specific | Extranet | Partner/extranet traffic |

## Advanced Services (SDK-Available, MCP Gaps)

These services are available via the ZIA API and SDK but are not yet exposed through MCP tools. Use OneAPI direct calls for all of them.

### AppTotal

AppTotal provides deep inspection and risk scoring for cloud applications beyond standard CASB categories. Use it to get risk metadata for specific apps and inform cloud app control policy.

| Operation | Endpoint |
|-----------|----------|
| Get app report | `GET /appTotal/report?appUrl=<url>` |
| Get app review | `GET /appTotal/review?appUrl=<url>` |

### Cloud NSS (Network Security Service)

Cloud NSS streams ZIA logs to external SIEMs and SOC platforms without requiring on-premises NSS appliances.

| Operation | Endpoint |
|-----------|----------|
| List NSS feeds | `GET /cloudNssFeeds` |
| Get NSS feed | `GET /cloudNssFeeds/{id}` |
| Create NSS feed | `POST /cloudNssFeeds` |
| Update NSS feed | `PUT /cloudNssFeeds/{id}` |
| Delete NSS feed | `DELETE /cloudNssFeeds/{id}` |
| List NSS servers | `GET /nssServers` |

Supported output formats: CEF, LEEF, JSON. Supported destinations: Splunk, QRadar, Azure Sentinel, generic syslog.

### VZEN Clusters and Nodes (Virtual ZEN)

VZEN (Virtual ZEN / `virtualZenClusters`, `virtualZenNodes`) allows deploying Zscaler enforcement nodes in private or sovereign cloud environments.

| Operation | Endpoint |
|-----------|----------|
| List VZEN clusters | `GET /virtualZenClusters` |
| Get VZEN cluster | `GET /virtualZenClusters/{id}` |
| Create VZEN cluster | `POST /virtualZenClusters` |
| List VZEN nodes | `GET /virtualZenNodes` |
| Get VZEN node | `GET /virtualZenNodes/{id}` |

Use VZEN for government or regulated environments where traffic cannot egress to Zscaler's public cloud.

### Bandwidth Control

Bandwidth control throttles traffic by category, application, or user group to prevent bandwidth monopolization.

| Operation | Endpoint |
|-----------|----------|
| List bandwidth classes | `GET /bandwidthClasses` |
| Create bandwidth class | `POST /bandwidthClasses` |
| List bandwidth control rules | `GET /bandwidthControlRules` |
| Create bandwidth control rule | `POST /bandwidthControlRules` |

### IoT Report

IoT report provides visibility into IoT device traffic patterns and risk.

| Operation | Endpoint |
|-----------|----------|
| Get IoT report | `GET /iotReport` |

### Shadow IT Report

Shadow IT discovery report surfaces unauthorized cloud app usage across the tenant.

| Operation | Endpoint |
|-----------|----------|
| Get shadow IT report | `GET /shadowIT/applications` |
| Export shadow IT CSV | `GET /shadowIT/applications/export` |

### Traffic Capture

Traffic capture rules define packet capture triggers for diagnostic and forensic purposes.

| Operation | Endpoint |
|-----------|----------|
| List capture rules | `GET /trafficCaptureRules` |
| Create capture rule | `POST /trafficCaptureRules` |
| Update capture rule | `PUT /trafficCaptureRules/{id}` |
| Delete capture rule | `DELETE /trafficCaptureRules/{id}` |

### Policy Export

Export the full ZIA policy configuration as a structured snapshot for backup or audit.

| Operation | Endpoint |
|-----------|----------|
| Export all policies | `GET /policyExport` |
| Export by type | `GET /policyExport?policyType=<type>` |

## MCP Server

Live CRUD operations for ZIA are available via the [zscaler-mcp-server](https://github.com/zscaler/zscaler-mcp-server). This skill provides workflow guidance and field gotchas; the MCP server executes the actual API calls via `zia_*` tools. See the MCP server repository for the full list of available tools and required parameters.
