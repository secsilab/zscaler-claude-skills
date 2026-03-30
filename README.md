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

| Skill | Command | Description |
|-------|---------|-------------|
| **Router** | `/zscaler` | Routes requests to the right product skill automatically |
| **Setup** | `/zscaler-setup` | Interactive credential wizard — installs MCP, validates connectivity |
| **Onboard** | `/zscaler-onboard` | Full onboarding flow (setup + discover + audit + snapshot) |
| **Discover** | `/zscaler-discover` | Scans tenant, generates full inventory |
| **Audit** | `/zscaler-audit` | Security and hygiene audit (22 checks across ZIA/ZPA/ZDX) |
| **Troubleshoot** | `/zscaler-troubleshoot` | Interactive diagnostics (6 flows: connectivity, access, DNS, ...) |
| **Snapshot** | `/zscaler-snapshot` | Config backup, drift detection, point-in-time comparison |
| **Deploy** | `/zscaler-deploy` | Deployment templates (6 recipes: app, server, location, DLP, ...) |
| **Migrate** | `/zscaler-migrate` | Competitive migration — assessment, 6 vendor playbooks, API execution |
| **Bridge** | `/zscaler-bridge` | Translate design docs (from zstack or manual) into API call sequences |

### Product Skills (11)

Deep API knowledge for each Zscaler product. Loaded automatically by the router when needed.

| Skill | Command | Endpoints | Covers |
|-------|---------|-----------|--------|
| **ZIA** | `/zscaler-zia` | 428 | Firewall, URL filtering, DLP, SSL inspection, cloud apps, locations, GRE, sandbox, ATP |
| **ZPA** | `/zscaler-zpa` | 328 | App segments, access policies, PRA/BA, connectors, service edges, SCIM, isolation |
| **ZTB** | `/zscaler-ztb` | 674 | AirGap API — sites, gateways, VLANs, PBR, VRRP, IPsec, GRE, WireGuard, BGP, OSPF |
| **ZCBC** | `/zscaler-zcbc` | 97 | Cloud & Branch Connector via OneAPI — partner integrations, connector groups |
| **ZCC** | `/zscaler-zcc` | 33 | Client Connector — devices, forwarding profiles, trusted networks, enrollment |
| **ZDX** | `/zscaler-zdx` | 42 | Digital Experience — app monitoring, device metrics, alerts, deep traces |
| **ZID** | `/zscaler-zid` | 31 | ZIdentity — users, groups, API clients, resource servers, directory sync |
| **EASM** | `/zscaler-easm` | 7 | External Attack Surface Management — findings, lookalike domains |
| **ZWA** | `/zscaler-zwa` | 19 | Workflow Automation — DLP incidents, evidence, closure, audit logs |
| **AI Guard** | `/zscaler-aiguard` | 2 | AI/ML content detection and policy execution |
| **ZInsights** | `/zscaler-zinsights` | 16 | Analytics — web traffic, firewall stats, cyber incidents, shadow IT, IoT |

## Architecture

```
User types /zscaler "list all DLP rules"
       |
       v
  [zscaler] Router skill
       |  Identifies: this is a ZIA DLP question
       v
  [zscaler-zia] Product skill
       |  Knows: GET /zia/api/v1/webDlpRules (params, response shape)
       v
  [Zscaler MCP Server] Executes the API call
       |
       v
  Claude formats and presents the results
```

The router (`/zscaler`) detects which product is relevant and loads the right skill. You can also invoke product skills directly if you know which product you need.

## Tools

### `tools/extract_postman.py`

Converts Zscaler's official Postman collection JSON files into Markdown endpoint tables. Used to maintain the product skills.

```bash
python3 tools/extract_postman.py collection.json
python3 tools/extract_postman.py collection.json --folder "DLP Policies"
```

## Requirements

- **Claude Code** v1.0+ (Claude Pro, Max, or Team plan)
- **Zscaler MCP Server** (`zscaler-mcp`) — the official Zscaler MCP integration
- **Zscaler API access** — OAuth2 client credentials with appropriate permissions
- **Python 3.10+** (for the extract tool only)

## License

MIT
