---
name: zscaler-setup
version: 1.1.0
description: Use when setting up Zscaler MCP integration from scratch, when .mcp.json is missing, or when a colleague needs to configure their Zscaler API access. Interactive wizard that installs dependencies, collects credentials, and validates connectivity.
---

# Zscaler Setup Wizard

Interactive setup for Zscaler MCP integration. Installs dependencies, collects credentials, creates config files, and validates connectivity.

## Process

Run each step sequentially. Use AskUserQuestion for any missing information. Skip steps that are already satisfied.

### Step 1: Check Prerequisites

```bash
# Check uv
which uv 2>/dev/null && uv --version

# Check zscaler-mcp
which zscaler-mcp 2>/dev/null && zscaler-mcp --version 2>/dev/null
```

**If `uv` missing:** Ask user to install it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**If `zscaler-mcp` missing:**
```bash
uv tool install zscaler-mcp
```

Confirm each installation succeeded before proceeding.

### Step 2: Check Existing Config

```bash
# Check for existing .mcp.json
test -f .mcp.json && echo "EXISTS" || echo "MISSING"

# Check for existing .env
test -f .env && echo "EXISTS" || echo "MISSING"

# Check .gitignore covers secrets
grep -q ".mcp.json" .gitignore 2>/dev/null && echo ".mcp.json gitignored" || echo "WARNING: .mcp.json NOT in .gitignore"
grep -q ".env" .gitignore 2>/dev/null && echo ".env gitignored" || echo "WARNING: .env NOT in .gitignore"
```

If `.mcp.json` already exists, ask: "A Zscaler MCP config already exists. Do you want to reconfigure it? (yes/no)"
If no, skip to Step 4 (validation).

### Step 3: Collect Credentials

Ask these questions **one at a time**, explaining where to find each value:

**Q1: Vanity Domain**
> What is your Zscaler vanity domain? This is the subdomain in your Zscaler login URL.
> Example: if you log in at `https://acme.zslogin.net`, your vanity domain is `acme`.

**Q2: Client ID**
> What is your API Client ID?
> Find it in: ZIdentity Portal > Settings > API Keys > Client ID
> (Or: Administration > API Key Management in older portals)

**Q3: Client Secret**
> What is your API Client Secret?
> This was shown when you created the API key. If lost, generate a new key.

**Q4: Customer ID**
> What is your Zscaler Customer ID?
> Find it in: Administration > Company Profile > Customer ID
> It's a long number like `12345678901234567`.

**Q5: Write Mode**
> Do you want to enable write operations (create/update/delete) via MCP?
> - **yes** — full read+write access (recommended for admins)
> - **read-only** — safe mode, only read operations
> Default: read-only

**Q6: ZTB AirGap (optional)**
> Do you have a Zero Trust Branch (ZTB) deployment with AirGap?
> If yes, what is your AirGap site name? (the prefix in `<site>-api.goairgap.com`)
> If no or unsure, just say no.

### Step 4: Create Config Files

**Create `.mcp.json`:**

If write mode = yes:
```json
{
  "mcpServers": {
    "zscaler": {
      "command": "zscaler-mcp",
      "args": ["--enable-write-tools", "--write-tools", "*"],
      "env": {
        "ZSCALER_CLIENT_ID": "<collected>",
        "ZSCALER_CLIENT_SECRET": "<collected>",
        "ZSCALER_CUSTOMER_ID": "<collected>",
        "ZSCALER_VANITY_DOMAIN": "<collected>"
      }
    }
  }
}
```

If read-only:
```json
{
  "mcpServers": {
    "zscaler": {
      "command": "zscaler-mcp",
      "env": {
        "ZSCALER_CLIENT_ID": "<collected>",
        "ZSCALER_CLIENT_SECRET": "<collected>",
        "ZSCALER_CUSTOMER_ID": "<collected>",
        "ZSCALER_VANITY_DOMAIN": "<collected>"
      }
    }
  }
}
```

**Create/update `.env`** (append, don't overwrite existing content):
```bash
ZSCALER_CLIENT_ID=<collected>
ZSCALER_CLIENT_SECRET=<collected>
```

If ZTB: also add `ZSCALER_AIRGAP_SITE=<site-name>` to `.env`.

**Ensure `.gitignore` covers secrets:**
If `.mcp.json` or `.env` not in `.gitignore`, add them and warn the user.

### Step 5: Validate Connectivity

Ask Claude Code to restart MCP servers to pick up the new config, then test:

**5a. MCP services:**
```
Use the `zscaler_check_connectivity` MCP tool to verify API access.
Then use `zscaler_get_available_services` to show which services are accessible.
```

**5b. ZTB AirGap (if configured):**
Test ZTB connectivity separately — the MCP does NOT cover ZTB. Use a direct API call:
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

# Get token
token_data = urllib.parse.urlencode({
    "client_id": env["ZSCALER_CLIENT_ID"],
    "client_secret": env["ZSCALER_CLIENT_SECRET"],
    "grant_type": "client_credentials"
}).encode()
req = urllib.request.Request(f"https://{env.get('ZSCALER_VANITY_DOMAIN', '<vanity>')}.zslogin.net/oauth2/v1/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
token = json.loads(urllib.request.urlopen(req, context=ctx).read())["access_token"]

# Test AirGap API
site = env.get("ZSCALER_AIRGAP_SITE", "<site>")
req = urllib.request.Request(f"https://{site}-api.goairgap.com/api/v2/Site/")
req.add_header("Authorization", f"Bearer {token}")
resp = urllib.request.urlopen(req, context=ctx)
sites = json.loads(resp.read())
print(f"ZTB connected: {len(sites)} site(s) found")
for s in sites:
    print(f"  - {s.get('name', '?')} (ID: {s.get('id', '?')})")
```

**If connectivity fails:**
- Check credentials (typo in client_id/secret?)
- Check network (proxy, firewall?)
- Check API key permissions in ZIdentity portal
- ZTB: verify AirGap site name matches your portal URL
- Ask user to verify and re-enter credentials

### Step 6: Show Summary

Print a summary of what was configured:

```
=== Zscaler MCP Setup Complete ===

Vanity Domain:  <domain>
Customer ID:    <id>
Write Mode:     <yes/read-only>
ZTB AirGap:     <site or N/A>

Services Available (MCP):
  - ZIA:        <connected/not available>
  - ZPA:        <connected/not available>
  - ZDX:        <connected/not available>
  - ZCC:        <connected/not available>
  - ZIdentity:  <connected/not available>
  - ZTW:        <connected/not available>
  - ZEASM:      <connected/not available>
  - ZInsights:  <connected/not available>

Services Available (Direct API):
  - ZTB AirGap: <connected/not available/not configured>

Files Created:
  - .mcp.json (MCP server config)
  - .env (API credentials for direct calls)

Next Steps:
  1. The `zscaler` skill is now active — ask Claude to manage any Zscaler component
  2. Try: "list my ZIA locations" or "show ZPA app segments"
  3. For ZTB management, Claude will use the AirGap API directly
  4. Run `/zscaler-setup` again anytime to reconfigure
```

### Step 7: Install the Zscaler Skill (if missing)

Check if the `zscaler` skill exists:
```bash
test -f ~/.claude/skills/zscaler/SKILL.md && echo "EXISTS" || echo "MISSING"
```

If missing, inform the user they need the `zscaler` skill for full functionality and ask if they want to install it now. If yes, copy it from the shared location or create it.

## Error Recovery

| Error | Fix |
|-------|-----|
| `uv: command not found` | Run install script, then `source ~/.bashrc` or restart shell |
| `zscaler-mcp: command not found` | `uv tool install zscaler-mcp`, check PATH |
| `401 Unauthorized` | Wrong client_id or client_secret — re-enter |
| `403 Forbidden` | API key lacks permissions — check ZIdentity portal |
| `Connection refused` | Network issue — check proxy/firewall settings |
| `.mcp.json` not picked up | Restart Claude Code (`/mcp` to check MCP server status) |

## Authentication Reference

### OneAPI (OAuth2) — Recommended

OneAPI is the recommended authentication method for all Zscaler products (ZIA, ZPA, ZCC, ZDX, ZID, ZCBC, EASM, ZWA, AI Guard, ZInsights, ZMS, ZBI).

| Field | Value |
|-------|-------|
| Grant type | `client_credentials` |
| Token endpoint | `https://<vanity>.zslogin.net/oauth2/v1/token` |
| API base | `https://api.zsapi.net/<product>/api/v1` |
| Credentials | `ZSCALER_CLIENT_ID`, `ZSCALER_CLIENT_SECRET`, `ZSCALER_VANITY_DOMAIN` |

Create API credentials in the ZIdentity portal: **Settings > API Keys**.

OneAPI credentials are product-agnostic — one client ID/secret pair accesses all products your role permits.

### Legacy Per-Product Auth — Fallback

Some features are only accessible via the legacy API (e.g., the ZIA `receiver` field on DLP rules). Legacy auth uses per-product credentials:

| Product | Credentials |
|---------|-------------|
| ZIA | `ZIA_USERNAME`, `ZIA_PASSWORD`, `ZIA_API_KEY`, `ZIA_CLOUD` |
| ZPA | `ZPA_CLIENT_ID`, `ZPA_CLIENT_SECRET`, `ZPA_CUSTOMER_ID`, `ZPA_CLOUD` |

Legacy base URL: `https://zsapi.<cloud>.net/api/v1` (ZIA) or `https://config.private.zscaler.com/...` (ZPA)

Use legacy only when a specific field or endpoint is not available via OneAPI.

### SCIM Auth — ZIA and ZPA User Provisioning

For automated user/group provisioning from an IdP (Okta, Azure AD, etc.), SCIM uses a separate bearer token:

| Product | SCIM Base URL | Notes |
|---------|--------------|-------|
| ZIA | `https://scim.zscaler.com/zia/<tenant-id>/scim/v2` | Enable SCIM in ZIA admin portal |
| ZPA | `https://scim.zscaler.com/zpa/<tenant-id>/scim/v2` | Enable SCIM in ZPA admin portal |

SCIM tokens are generated in the respective admin portal (not ZIdentity). They are separate from OneAPI credentials.

## Related API Reference

After setup, use product skills for detailed API documentation:
- Full product map → See @zscaler orchestrator skill
- MCP tool reference by product → See @zscaler-zia, @zscaler-zpa, etc.
