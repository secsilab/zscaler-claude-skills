---
name: zscaler-terraformer
version: 1.0.0
description: Use when importing existing ZIA or ZPA infrastructure into Terraform (brownfield). Zscaler Terraformer is a CLI tool that generates .tf configuration files and .tfstate from live Zscaler tenants.
---

# Zscaler Terraformer

## Overview

Zscaler Terraformer is a CLI utility for brownfield Terraform adoption. It connects to your live ZIA, ZPA, or ZTC (ZCBC) tenant and generates ready-to-use `.tf` configuration files and a `.tfstate` file, letting you bring existing infrastructure under Terraform management without manual rewriting.

**This is a CLI tool, not an API skill.** There are no MCP tools. Use this skill when a user wants to:
- Import existing Zscaler config into Terraform for the first time
- Generate a Terraform baseline before making infrastructure-as-code changes
- Migrate from manual admin portal configuration to code-managed infrastructure

## Installation

### macOS (Homebrew)
```bash
brew tap zscaler/tap
brew install zscaler-terraformer
```

### Windows (Chocolatey)
```powershell
choco install zscaler-terraformer
```

### Linux (manual)
```bash
# Download the latest release from GitHub releases
curl -LO https://github.com/zscaler/zscaler-terraformer/releases/latest/download/zscaler-terraformer_linux_amd64.tar.gz
tar -xzf zscaler-terraformer_linux_amd64.tar.gz
sudo mv zscaler-terraformer /usr/local/bin/
```

### Verify installation
```bash
zscaler-terraformer --version
```

## Authentication

Terraformer supports both modern OneAPI and legacy per-product credentials.

### OneAPI (Recommended)
```bash
export ZSCALER_CLIENT_ID="<client-id>"
export ZSCALER_CLIENT_SECRET="<client-secret>"
export ZSCALER_VANITY_DOMAIN="<vanity>"
```

### Legacy — ZPA
```bash
export ZPA_CLIENT_ID="<client-id>"
export ZPA_CLIENT_SECRET="<client-secret>"
export ZPA_CUSTOMER_ID="<customer-id>"
export ZPA_CLOUD="PRODUCTION"    # PRODUCTION | BETA | GOV | PREVIEW
```

### Legacy — ZIA
```bash
export ZIA_USERNAME="<admin@domain>"
export ZIA_PASSWORD="<password>"
export ZIA_API_KEY="<api-key>"
export ZIA_CLOUD="<cloud>"       # e.g. zscaler.net, zscalerone.net, zscloud.net
```

## Supported Resources

### ZPA Resources (30+)

| Category | Resources |
|----------|-----------|
| Applications | `zpa_application_segment`, `zpa_application_segment_browser_access`, `zpa_application_segment_pra`, `zpa_application_segment_inspection`, `zpa_ba_certificate` |
| Groups | `zpa_segment_group`, `zpa_server_group`, `zpa_app_connector_group`, `zpa_service_edge_group` |
| Policy | `zpa_policy_access_rule`, `zpa_policy_forwarding_rule`, `zpa_policy_timeout_rule`, `zpa_policy_isolation_rule`, `zpa_policy_inspection_rule` |
| PRA / BA | `zpa_pra_portal`, `zpa_pra_credential`, `zpa_pra_console` |
| Connectors | `zpa_app_connector`, `zpa_service_edge` |
| Identity | `zpa_idp_controller`, `zpa_provisioning_key` |
| Other | `zpa_lss_config_controller`, `zpa_inspection_profile`, `zpa_inspection_custom_controls`, `zpa_microtenant_controller` |

### ZIA Resources (50+)

| Category | Resources |
|----------|-----------|
| Locations | `zia_location_management`, `zia_gre_tunnel`, `zia_vpn_credentials`, `zia_static_ip` |
| Firewall | `zia_firewall_filtering_rule`, `zia_firewall_filtering_ip_source_groups`, `zia_firewall_filtering_ip_destination_groups`, `zia_firewall_filtering_network_application_groups`, `zia_firewall_dns_rule`, `zia_firewall_ips_rule` |
| URL Filtering | `zia_url_filtering_rules`, `zia_url_categories` |
| DLP | `zia_dlp_web_rules`, `zia_dlp_dictionaries`, `zia_dlp_engines`, `zia_dlp_notification_templates` |
| SSL | `zia_ssl_inspection_rules` |
| Cloud Apps | `zia_cloud_app_control_rule` |
| Forwarding | `zia_forwarding_control_rule`, `zia_zpa_gateway` |
| Admin | `zia_admin_users`, `zia_rule_labels` |
| ATP | `zia_advanced_threat_settings`, `zia_malware_protection` |
| Bandwidth | `zia_bandwidth_classes`, `zia_bandwidth_control_rules` |
| Other | `zia_auth_settings_urls`, `zia_sandbox_behavioral_analysis`, `zia_traffic_forwarding_static_ip` |

### ZTC Resources (14 — Cloud & Branch Connector)

| Resources |
|-----------|
| `ztc_ip_groups`, `ztc_network_services`, `ztc_account_groups`, `ztc_admin_roles`, `ztc_location_management`, `ztc_partner_integration`, `ztc_ecgroup`, `ztc_connector_group`, `ztc_policy_rule`, `ztc_forwarding_rules` and 4 more |

## Usage Examples

### Full ZPA Import
```bash
# Generate all ZPA resources as Terraform
zscaler-terraformer generate --product zpa --resources "*" --output ./terraform/zpa/
```

### Full ZIA Import
```bash
zscaler-terraformer generate --product zia --resources "*" --output ./terraform/zia/
```

### Selective Import (Single Resource Type)
```bash
# Import only application segments
zscaler-terraformer generate --product zpa --resources zpa_application_segment --output ./terraform/

# Import only firewall rules
zscaler-terraformer generate --product zia --resources zia_firewall_filtering_rule --output ./terraform/
```

### Import by Resource ID
```bash
# Import a specific app segment by ID
zscaler-terraformer generate --product zpa --resources zpa_application_segment --id <segment-id>
```

### List Available Resources
```bash
zscaler-terraformer list --product zpa
zscaler-terraformer list --product zia
```

### Debug Mode
```bash
zscaler-terraformer generate --product zpa --resources "*" --verbose
```

## Common Workflows

### Brownfield Onboarding (First-Time Import)

1. Install and authenticate (see above)
2. Create output directory: `mkdir -p terraform/zpa terraform/zia`
3. Generate ZPA resources:
   ```bash
   zscaler-terraformer generate --product zpa --resources "*" --output terraform/zpa/
   ```
4. Generate ZIA resources:
   ```bash
   zscaler-terraformer generate --product zia --resources "*" --output terraform/zia/
   ```
5. Initialize Terraform: `terraform init`
6. **Review the generated `.tf` files before running** — always check references and naming
7. Validate: `terraform plan` — should show 0 changes if import is correct
8. Commit to version control

### Selective Import (Add One Resource Type to Existing State)

1. Identify the resource type to import
2. Generate only that resource:
   ```bash
   zscaler-terraformer generate --product zia --resources zia_url_filtering_rules --output ./
   ```
3. Merge generated files into your existing Terraform directory
4. Run `terraform plan` — confirm expected state matches live config

### Pre-Migration Baseline

Before making changes to a production tenant, capture the full Terraform representation as a baseline:
```bash
# Snapshot current state
zscaler-terraformer generate --product zpa --resources "*" --output ./baseline-$(date +%Y%m%d)/zpa/
zscaler-terraformer generate --product zia --resources "*" --output ./baseline-$(date +%Y%m%d)/zia/
git add baseline-*/
git commit -m "Pre-migration Terraform baseline $(date +%Y-%m-%d)"
```

## Known Limitations

- **Not 100% idempotent** — some resources require manual `terraform import` for computed fields
- **Hard-coded IDs are converted to references** automatically, but complex cross-resource references may need manual review
- **ZTC resources** require the `terraform-provider-ztc` provider (renamed from `terraform-provider-zcbc`)
- **Read-only resources** (computed-only fields like connector health status) are excluded from generated configs
- **ZIA activation** — Terraformer imports current state; changes applied via `terraform apply` still require ZIA activation (`zia_activate_configuration`)
- **Sensitive fields** (secrets, passwords) are placeholders in generated `.tf` — fill them from a secrets manager before applying

## Related

- Terraform provider for ZPA: `terraform-provider-zpa`
- Terraform provider for ZIA: `terraform-provider-zia`
- Terraform provider for ZTC (ZCBC): `terraform-provider-ztc`
- For live API management (non-Terraform), use @zscaler-zia and @zscaler-zpa skills
