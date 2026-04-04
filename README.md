# Zscaler Skills Suite for Claude Code

115 skills for Zscaler — plan with [zstack](https://github.com/pganti/zstack), execute with API. **1,677 endpoints** covered.

## Install

```bash
git clone https://github.com/secsilab/zscaler-claude-skills.git
cd zscaler-claude-skills
bash install.sh
```

This installs 24 execution skills + 91 planning skills ([zstack](https://github.com/pganti/zstack)). Use `--skills-only` to skip zstack.

**Prerequisites:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Zscaler MCP Server](https://github.com/zscaler/zscaler-mcp) (`uv tool install zscaler-mcp`), API credentials.

## Get Started

```
/zscaler-setup       Configure credentials (interactive wizard)
/zscaler-onboard     Full onboarding: setup → discover → audit → snapshot
```

**Typical workflow:**
1. `/zia-ssl` — design SSL inspection with zstack (CA model, bypass list, compliance)
2. `/zscaler-bridge` — translate the design into API calls
3. `/zscaler-audit` — validate with 22 security checks
4. `/zscaler-snapshot` — backup the config

## Execution Skills (24)

### Operational (10)

| Command | Description |
|---------|-------------|
| `/zscaler` | Routes to the right product skill |
| `/zscaler-setup` | Credential wizard — installs MCP, validates connectivity |
| `/zscaler-onboard` | Full onboarding (setup + discover + audit + snapshot) |
| `/zscaler-discover` | Scan tenant, generate inventory |
| `/zscaler-audit` | Security audit — 22 checks across ZIA/ZPA/ZDX |
| `/zscaler-troubleshoot` | Interactive diagnostics (6 flows) |
| `/zscaler-snapshot` | Config backup, drift detection, rollback |
| `/zscaler-deploy` | Deployment templates (6 recipes) |
| `/zscaler-migrate` | Competitive migration — 6 vendor playbooks + API execution |
| `/zscaler-bridge` | Translate design docs into API call sequences |

### Product (14)

Loaded automatically by the router. Each skill has a `SKILL.md` (human-written expertise) and, where available, an `ENDPOINTS.md` (auto-generated API reference).

| Command | Endpoints | Covers |
|---------|-----------|--------|
| `/zscaler-zia` | 428 | Firewall, URL filtering, DLP, SSL, cloud apps, locations, GRE, sandbox |
| `/zscaler-zpa` | 328 | App segments, access policies, PRA/BA, connectors, SCIM, isolation |
| `/zscaler-ztb` | 674 | Sites, gateways, VLANs, PBR, VRRP, IPsec, GRE, WireGuard, BGP, OSPF |
| `/zscaler-zcbc` | 97 | Cloud & Branch Connector — partner integrations, connector groups (also ZTC/ZTW) |
| `/zscaler-zcc` | 33 | Client Connector — devices, forwarding profiles, web policy, entitlements |
| `/zscaler-zdx` | 42 | Digital Experience — app monitoring, alerts, deep traces |
| `/zscaler-zid` | 31 | ZIdentity — users, groups, API clients, directory sync |
| `/zscaler-easm` | 7 | External Attack Surface — findings, lookalike domains |
| `/zscaler-zwa` | 19 | Workflow Automation — DLP incidents, evidence, closure |
| `/zscaler-aiguard` | 2 | AI/ML content detection, policy execution, AI Gateway, n8n, NeMo |
| `/zscaler-zinsights` | 16 | Analytics — traffic, firewall stats, shadow IT, IoT |
| `/zscaler-zms` | — | Microsegmentation — agents, resource groups, policy rules, app zones |
| `/zscaler-zbi` | — | Business Insights — custom app definitions, reports |
| `/zscaler-terraformer` | CLI | Brownfield Terraform import for ZIA, ZPA, and ZTC |

## Planning Skills (91 — zstack)

Installed by default via `bash install.sh`. [zstack](https://github.com/pganti/zstack) provides PS consulting expertise:

| Category | Examples | Skills |
|----------|---------|--------|
| PS Lifecycle | `/ps-scoping`, `/isp`, `/ps-sow`, `/ps-handoff` | 6 |
| ZIA Design | `/zia-ssl`, `/zia-policy`, `/zia-firewall`, `/zia-dlp-inline` | 6 |
| ZPA Design | `/zpa-connectors`, `/zpa-segments`, `/vpn-migration` | 6 |
| Data Protection | `/dlp-design`, `/casb-inline`, `/ai-guard` | 7 |
| Migrations | `/migrate-palo-alto`, `/migrate-checkpoint`, `/migrate-cisco` | 8 |
| ZTB / ZDX / ZCC | `/ztb-design`, `/zdx-deployment`, `/zcc-deployment` | 14 |
| SecOps / ITDR | `/secops-incident-response`, `/itdr-setup` | 9 |
| Other | `/bc-design`, `/sovereign-cloud`, `/microsegmentation` | 35 |

Full list: see [zstack CLAUDE.md](https://github.com/pganti/zstack/blob/main/CLAUDE.md)

## How It Works

```
/zscaler "list all DLP rules"
    → [Router] identifies ZIA
    → [zscaler-zia] SKILL.md (tools, gotchas) + ENDPOINTS.md (API reference)
    → [Zscaler MCP Server] executes API call
    → Claude presents results
```

**Two layers, one workflow:**
- **zstack** = consulting brain (what to build, why, gotchas from field experience)
- **This project** = execution hands (API calls via MCP, audit, snapshot, deploy)

## Keeping Endpoints Up to Date

A [GitHub Action](.github/workflows/postman-drift.yml) runs bi-monthly to detect changes in Zscaler's [Postman collections](https://www.postman.com/zscaler/zscaler-developers/). When drift is found, it regenerates `ENDPOINTS.md` files and opens a PR.

```bash
python3 tools/generate_endpoints.py --check   # Check for drift locally
python3 tools/generate_endpoints.py            # Regenerate all ENDPOINTS.md
```

## Versioning

Skills use semver in their YAML frontmatter:

```yaml
name: zscaler-zia
version: 1.1.0
postman_revision: 2026-03-30
```

- `version` — bumped on human edits
- `postman_revision` — bumped by CI when Postman endpoints update

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) v1.0+
- [Zscaler MCP Server](https://github.com/zscaler/zscaler-mcp) (`uv tool install zscaler-mcp`)
- Zscaler API credentials (OAuth2 client credentials)
- Python 3.10+ (for tools only)

## License

MIT
