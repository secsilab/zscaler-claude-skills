# Zscaler Skills Suite for Claude Code

21 modular [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for managing Zscaler infrastructure across all products. Covers **1,677 API endpoints** with natural language commands.

## What are Claude Code Skills?

[Skills](https://docs.anthropic.com/en/docs/claude-code/skills) are reusable prompt files that teach Claude Code domain-specific knowledge. Type `/zscaler-audit` and Claude knows every API endpoint, every parameter, every workflow to audit your Zscaler tenant — no coding required.

## Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [Zscaler MCP Server](https://github.com/zscaler/zscaler-mcp) installed (`uv tool install zscaler-mcp`)
- Zscaler API credentials (Client ID, Client Secret, Customer ID)

### Install

```bash
git clone https://github.com/secsilab/zscaler-claude-skills.git
cd zscaler-claude-skills
bash install.sh
```

Options:
```bash
bash install.sh                    # Install all 21 skills
bash install.sh --operational-only # Install 10 operational skills only
bash install.sh --product-only     # Install 11 product skills only
```

### Configure MCP

Copy the example config to your project:

```bash
cp .mcp.json.example /path/to/your/project/.mcp.json
```

Edit `.mcp.json` with your credentials, then run Claude Code and type:

```
/zscaler-setup
```

The interactive wizard validates your connectivity and generates the config.

### First Run

For a new tenant, use the onboarding flow:

```
/zscaler-onboard
```

This chains: setup -> discover -> audit -> snapshot — giving you a complete picture of your tenant in one command.

## Skills

### Operational Skills (10)

Start here. These guide workflows and chain product skills automatically.

| Skill | Command | Version | Description |
|-------|---------|---------|-------------|
| **Router** | `/zscaler` | 1.0.0 | Routes requests to the right product skill automatically |
| **Setup** | `/zscaler-setup` | 1.0.0 | Interactive credential wizard — installs MCP, validates connectivity |
| **Onboard** | `/zscaler-onboard` | 1.0.0 | Full onboarding flow (setup + discover + audit + snapshot) |
| **Discover** | `/zscaler-discover` | 1.0.0 | Scans tenant, generates full inventory |
| **Audit** | `/zscaler-audit` | 1.0.0 | Security and hygiene audit (22 checks across ZIA/ZPA/ZDX) |
| **Troubleshoot** | `/zscaler-troubleshoot` | 1.0.0 | Interactive diagnostics (6 flows: connectivity, access, DNS, ...) |
| **Snapshot** | `/zscaler-snapshot` | 1.0.0 | Config backup, drift detection, point-in-time comparison |
| **Deploy** | `/zscaler-deploy` | 1.0.0 | Deployment templates (6 recipes: app, server, location, DLP, ...) |
| **Migrate** | `/zscaler-migrate` | 1.0.0 | Competitive migration — assessment, 6 vendor playbooks, API execution |
| **Bridge** | `/zscaler-bridge` | 1.0.0 | Translate design docs (from zstack or manual) into API call sequences |

### Product Skills (11)

Deep API knowledge for each Zscaler product. Loaded automatically by the router when needed.

| Skill | Command | Version | Endpoints | Covers |
|-------|---------|---------|-----------|--------|
| **ZIA** | `/zscaler-zia` | 1.1.0 | 428 | Firewall, URL filtering, DLP, SSL inspection, cloud apps, locations, GRE, sandbox, ATP |
| **ZPA** | `/zscaler-zpa` | 1.1.0 | 328 | App segments, access policies, PRA/BA, connectors, service edges, SCIM, isolation |
| **ZTB** | `/zscaler-ztb` | 1.1.0 | 674 | AirGap API — sites, gateways, VLANs, PBR, VRRP, IPsec, GRE, WireGuard, BGP, OSPF |
| **ZCBC** | `/zscaler-zcbc` | 1.0.0 | 97 | Cloud & Branch Connector via OneAPI — partner integrations, connector groups |
| **ZCC** | `/zscaler-zcc` | 1.1.0 | 33 | Client Connector — devices, forwarding profiles, trusted networks, enrollment |
| **ZDX** | `/zscaler-zdx` | 1.0.0 | 42 | Digital Experience — app monitoring, device metrics, alerts, deep traces |
| **ZID** | `/zscaler-zid` | 1.0.0 | 31 | ZIdentity — users, groups, API clients, resource servers, directory sync |
| **EASM** | `/zscaler-easm` | 1.0.0 | 7 | External Attack Surface Management — findings, lookalike domains |
| **ZWA** | `/zscaler-zwa` | 1.0.0 | 19 | Workflow Automation — DLP incidents, evidence, closure, audit logs |
| **AI Guard** | `/zscaler-aiguard` | 1.0.0 | 2 | AI/ML content detection and policy execution |
| **ZInsights** | `/zscaler-zinsights` | 1.0.0 | 16 | Analytics — web traffic, firewall stats, cyber incidents, shadow IT, IoT |

## Skill Versioning

Every skill has a `version` field (semver) in its YAML frontmatter. Product skills also have `postman_revision` tracking which Postman collection version they were built from.

```yaml
---
name: zscaler-zia
version: 1.1.0
postman_revision: 2026-03-30
description: Use when working with ZIA...
---
```

- **`version`** — bumped manually when the skill's human-written content changes
- **`postman_revision`** — bumped automatically by CI when Postman endpoints are updated

## ENDPOINTS.md — API Reference Files

Product skills are split into two files:

```
skills/zscaler-zia/
├── SKILL.md       — Human-written: overview, MCP tools, gotchas, patterns, limitations
└── ENDPOINTS.md   — Auto-generated: full API endpoint reference tables
```

- `SKILL.md` contains domain expertise, field gotchas, and workflow guidance
- `ENDPOINTS.md` contains comprehensive API endpoint tables generated from Zscaler's official Postman collections
- Both files are installed to `~/.claude/skills/<skill>/` and Claude reads both when the skill is invoked
- Only the 11 product skills have ENDPOINTS.md; operational skills remain single-file

## Postman Drift Detection

A GitHub Action runs bi-monthly (1st and 15th) to detect changes in Zscaler's official Postman collections:

1. Fetches metadata from the [Zscaler Developers workspace](https://www.postman.com/zscaler/zscaler-developers/)
2. Compares `updatedAt` timestamps against stored values
3. If changes detected: downloads full collection, regenerates ENDPOINTS.md files, opens a PR

Collections tracked:
- **OneAPI** (ZIA, ZPA, ZCBC, ZDX, ZCC, ZID, EASM)
- **ZTB** (AirGap API)
- **ZWA** (Workflow Automation)
- **AI Guard**

You can also run the check locally:

```bash
python3 tools/generate_endpoints.py --check   # Check for drift only
python3 tools/generate_endpoints.py            # Regenerate all ENDPOINTS.md
```

## Architecture

```
User types /zscaler "list all DLP rules"
       |
       v
  [zscaler] Router skill
       |  Identifies: this is a ZIA DLP question
       v
  [zscaler-zia] Product skill
       |  SKILL.md: MCP tools, gotchas, workflows
       |  ENDPOINTS.md: Full API reference (auto-generated)
       v
  [Zscaler MCP Server] Executes the API call
       |
       v
  Claude formats and presents the results
```

The router (`/zscaler`) detects which product is relevant and loads the right skill. You can also invoke product skills directly if you know which product you need.

### Using with zstack (Planning + Execution)

This project works alongside [zstack](https://github.com/pganti/zstack) for a complete plan-to-execute workflow:

```
 zstack (91 skills)              zscaler-claude-skills (21 skills)
 ┌─────────────────┐             ┌─────────────────────┐
 │ /zia-ssl         │──design──>│ /zscaler-bridge      │──execute──> Zscaler API
 │ /migrate-palo    │           │ /zscaler-migrate     │
 │ /ps-scoping      │           │ /zscaler-deploy      │
 │ /dlp-design      │           │ /zscaler-audit       │
 └─────────────────┘             └─────────────────────┘
   WHAT to build                   HOW to execute
```

Install both:
```bash
# zstack (planning/design skills)
git clone https://github.com/pganti/zstack ~/.claude/skills/zstack

# zscaler-claude-skills (execution skills)
git clone https://github.com/secsilab/zscaler-claude-skills.git
cd zscaler-claude-skills && bash install.sh
```

## Tools

### `tools/generate_endpoints.py`

Downloads Zscaler's official Postman collections and generates ENDPOINTS.md files for each product skill. Used by the Postman drift detection GitHub Action.

```bash
python3 tools/generate_endpoints.py                     # Generate all from Postman
python3 tools/generate_endpoints.py --check              # Check for drift only
python3 tools/generate_endpoints.py --skill zscaler-zia  # Generate for one skill
```

### `tools/split_endpoints.py`

One-time migration script that extracts API Reference sections from SKILL.md into separate ENDPOINTS.md files.

### `tools/extract_postman.py`

Converts Zscaler's official Postman collection JSON files into Markdown endpoint tables. Legacy tool, superseded by `generate_endpoints.py` for most use cases.

```bash
python3 tools/extract_postman.py collection.json
python3 tools/extract_postman.py collection.json --folder "DLP Policies"
```

### `tools/postman_sources.json`

Configuration file tracking Postman collection UIDs, download URLs, folder-to-skill mappings, and last update timestamps.

## Requirements

- **Claude Code** v1.0+ (Claude Pro, Max, or Team plan)
- **Zscaler MCP Server** (`zscaler-mcp`) — the official Zscaler MCP integration
- **Zscaler API access** — OAuth2 client credentials with appropriate permissions
- **Python 3.10+** (for the tools)

## License

MIT
