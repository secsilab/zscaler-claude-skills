#!/bin/bash
# Zscaler Skills Suite — Installer for Claude Code
# https://github.com/secsilab/zscaler-claude-skills

set -e

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Zscaler Skills Suite — Installer for Claude Code ==="
echo ""

# Check Claude Code is installed
if ! command -v claude &>/dev/null; then
    echo "ERROR: Claude Code not found. Install it first:"
    echo "  npm install -g @anthropic-ai/claude-code"
    exit 1
fi
echo "[OK] Claude Code found"

# All skills to install
OPERATIONAL="zscaler zscaler-setup zscaler-onboard zscaler-discover zscaler-audit zscaler-troubleshoot zscaler-snapshot zscaler-deploy zscaler-migrate zscaler-bridge"
PRODUCT="zscaler-zia zscaler-zpa zscaler-ztb zscaler-zcbc zscaler-zcc zscaler-zdx zscaler-zid zscaler-easm zscaler-zwa zscaler-aiguard zscaler-zinsights"

ALL_SKILLS="$OPERATIONAL $PRODUCT"

# Allow selective install
if [ "$1" = "--operational-only" ]; then
    SKILLS="$OPERATIONAL"
    echo "[*] Installing operational skills only"
elif [ "$1" = "--product-only" ]; then
    SKILLS="$PRODUCT"
    echo "[*] Installing product skills only"
else
    SKILLS="$ALL_SKILLS"
    echo "[*] Installing all skills"
fi

echo ""

INSTALLED=0
for skill in $SKILLS; do
    src="$SCRIPT_DIR/skills/$skill/SKILL.md"
    if [ ! -f "$src" ]; then
        echo "[SKIP] $skill (not found)"
        continue
    fi
    mkdir -p "$SKILLS_DIR/$skill"
    cp "$src" "$SKILLS_DIR/$skill/SKILL.md"
    # Copy ENDPOINTS.md if it exists (product skills with API reference)
    endpoints_src="$SCRIPT_DIR/skills/$skill/ENDPOINTS.md"
    if [ -f "$endpoints_src" ]; then
        cp "$endpoints_src" "$SKILLS_DIR/$skill/ENDPOINTS.md"
    fi
    echo "[OK] $skill"
    INSTALLED=$((INSTALLED + 1))
done

echo ""
echo "=== Installation complete — $INSTALLED skills installed ==="
echo ""
echo "Operational skills (start here):"
echo "  /zscaler-onboard      Full onboarding (setup + discover + audit + snapshot)"
echo "  /zscaler-setup        Configure Zscaler MCP credentials"
echo "  /zscaler-discover     Scan tenant and generate inventory"
echo "  /zscaler-audit        Security and hygiene audit (22 checks)"
echo "  /zscaler-troubleshoot Interactive diagnostics (6 flows)"
echo "  /zscaler-snapshot     Config snapshots and drift detection"
echo "  /zscaler-deploy       Deployment templates (6 recipes)"
echo "  /zscaler-migrate      Competitive migration (6 vendor playbooks + API execution)"
echo "  /zscaler-bridge       Translate design docs into API call sequences"
echo ""
echo "Product skills (loaded automatically by the router):"
echo "  /zscaler-zia   /zscaler-zpa   /zscaler-ztb   /zscaler-zcbc"
echo "  /zscaler-zcc   /zscaler-zdx   /zscaler-zid   /zscaler-easm"
echo "  /zscaler-zwa   /zscaler-aiguard /zscaler-zinsights"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code in your project directory"
echo "  2. Type: /zscaler-setup"
echo "  3. Follow the interactive wizard to configure your credentials"
echo ""
