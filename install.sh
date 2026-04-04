#!/bin/bash
# Zscaler Skills Suite — Installer for Claude Code
# https://github.com/secsilab/zscaler-claude-skills

set -e

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ZSTACK_DIR="$SKILLS_DIR/zstack"
ZSTACK_REPO="https://github.com/pganti/zstack.git"

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
PRODUCT="zscaler-zia zscaler-zpa zscaler-ztb zscaler-zcbc zscaler-zcc zscaler-zdx zscaler-zid zscaler-easm zscaler-zwa zscaler-aiguard zscaler-zinsights zscaler-zms zscaler-zbi zscaler-terraformer"

ALL_SKILLS="$OPERATIONAL $PRODUCT"

# Parse options
SKILLS="$ALL_SKILLS"
SKIP_ZSTACK=false
SKILL_MODE=""

for arg in "$@"; do
    case "$arg" in
        --operational-only)
            SKILLS="$OPERATIONAL"
            SKILL_MODE="operational"
            ;;
        --product-only)
            SKILLS="$PRODUCT"
            SKILL_MODE="product"
            ;;
        --skills-only)
            SKIP_ZSTACK=true
            ;;
        --help|-h)
            echo "Usage: bash install.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  (default)            Install all 24 execution skills + zstack (91 planning skills)"
            echo "  --skills-only        Install execution skills only (skip zstack)"
            echo "  --operational-only   Install 10 operational skills only"
            echo "  --product-only       Install 14 product skills only"
            echo "  --help, -h           Show this help"
            echo ""
            echo "By default, the installer also clones zstack (PS planning/design skills)"
            echo "alongside the execution skills for a complete plan-to-execute workflow."
            exit 0
            ;;
    esac
done

if [ -n "$SKILL_MODE" ]; then
    echo "[*] Installing $SKILL_MODE skills only"
else
    echo "[*] Installing all 24 execution skills"
fi

echo ""

# --- Install execution skills ---
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
echo "[*] $INSTALLED execution skills installed"

# --- Install zstack (planning/design skills) ---
ZSTACK_COUNT=0
if [ "$SKIP_ZSTACK" = false ]; then
    echo ""
    if [ -d "$ZSTACK_DIR/.git" ]; then
        echo "[*] Updating zstack..."
        git -C "$ZSTACK_DIR" pull --quiet 2>/dev/null && echo "[OK] zstack updated" || echo "[OK] zstack (already up to date)"
    else
        echo "[*] Installing zstack (91 planning/design skills)..."
        git clone --quiet "$ZSTACK_REPO" "$ZSTACK_DIR" 2>/dev/null
        echo "[OK] zstack installed"
    fi
    ZSTACK_COUNT=$(find "$ZSTACK_DIR" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    echo "[*] $ZSTACK_COUNT zstack planning skills available"
fi

# --- Summary ---
echo ""
echo "========================================="
if [ "$SKIP_ZSTACK" = false ] && [ "$ZSTACK_COUNT" -gt 0 ]; then
    TOTAL=$((INSTALLED + ZSTACK_COUNT))
    echo "  $TOTAL total skills installed"
    echo "  ├── $INSTALLED execution skills (this project)"
    echo "  └── $ZSTACK_COUNT planning skills (zstack)"
else
    echo "  $INSTALLED execution skills installed"
fi
echo "========================================="
echo ""
echo "Execution skills (manage live infrastructure):"
echo "  /zscaler-onboard      Full onboarding (setup + discover + audit + snapshot)"
echo "  /zscaler-setup        Configure Zscaler MCP credentials"
echo "  /zscaler-discover     Scan tenant and generate inventory"
echo "  /zscaler-audit        Security and hygiene audit (22 checks)"
echo "  /zscaler-troubleshoot Interactive diagnostics (6 flows)"
echo "  /zscaler-snapshot     Config snapshots and drift detection"
echo "  /zscaler-deploy       Deployment templates (6 recipes)"
echo "  /zscaler-migrate      Competitive migration (6 vendor playbooks)"
echo "  /zscaler-bridge       Translate design docs into API calls"
if [ "$SKIP_ZSTACK" = false ] && [ "$ZSTACK_COUNT" -gt 0 ]; then
    echo ""
    echo "Planning skills from zstack (design, SOWs, migrations):"
    echo "  /zia-ssl              SSL inspection design + CA selection"
    echo "  /zpa-connectors       Connector sizing + HA design"
    echo "  /dlp-design           DLP policy design + EDM"
    echo "  /migrate-palo-alto    Palo Alto migration playbook"
    echo "  /ps-scoping           PS engagement scoping"
    echo "  /best-practices-qa    Query Zscaler best practices KB"
    echo "  ... and $(( ZSTACK_COUNT - 6 )) more (see zstack CLAUDE.md)"
fi
echo ""
echo "Product skills (loaded automatically by the router):"
echo "  /zscaler-zia   /zscaler-zpa   /zscaler-ztb   /zscaler-zcbc"
echo "  /zscaler-zcc   /zscaler-zdx   /zscaler-zid   /zscaler-easm"
echo "  /zscaler-zwa   /zscaler-aiguard /zscaler-zinsights"
echo "  /zscaler-zms   /zscaler-zbi   /zscaler-terraformer"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code in your project directory"
echo "  2. Type: /zscaler-setup"
echo "  3. Follow the interactive wizard to configure your credentials"
if [ "$SKIP_ZSTACK" = false ] && [ "$ZSTACK_COUNT" -gt 0 ]; then
    echo ""
    echo "Typical workflow (plan then execute):"
    echo "  /zia-ssl             Design SSL inspection (zstack)"
    echo "  /zscaler-bridge      Execute the design via API (this project)"
    echo "  /zscaler-audit       Validate post-deployment"
fi
echo ""
