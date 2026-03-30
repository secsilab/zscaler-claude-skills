---
name: zscaler-onboard
version: 1.0.0
description: Use when onboarding a new Zscaler tenant from scratch, when a colleague starts using the Zscaler skills for the first time, or when setting up a fresh project with Zscaler integration. Chains setup, discover, audit, and snapshot into a single flow.
---

# Zscaler Tenant Onboarding

Single-command orchestration that runs: **setup > discover > audit > snapshot**. A new colleague types `/zscaler-onboard` and in 5 minutes everything is configured, inventoried, audited, and snapshotted.

## Pre-flight: Check If Already Onboarded

```bash
test -f .mcp.json && echo "MCP_EXISTS" || echo "MCP_MISSING"
# Check for tenant inventory in project memory
ls memory/zscaler-tenant.md 2>/dev/null && echo "TENANT_EXISTS" || echo "TENANT_MISSING"
```

**If both exist:** Ask the user:
> "Tenant already onboarded. What would you like to do?"
> - **full** — re-run everything from scratch
> - **audit-only** — skip setup+discover, just run audit+snapshot
> - **skip** — nothing to do, exit

- If `full`: continue with all steps below
- If `audit-only`: jump to Step 3
- If `skip`: print "Already onboarded. Use individual skills (/zscaler-discover, /zscaler-audit, /zscaler-snapshot) as needed." and stop

## Step 1: Setup

Check if MCP is already configured and working:

1. Check if `.mcp.json` exists
2. If yes: run `zscaler_check_connectivity` to verify it works
3. If connectivity succeeds: print `[OK] MCP already configured` and skip to Step 2
4. If `.mcp.json` missing OR connectivity fails: invoke the `/zscaler-setup` skill (the interactive wizard)

**On failure:** Report the error. Ask: "Setup failed. Do you want to retry, or skip and continue with remaining steps? (retry/skip/stop)"
- `retry`: re-run Step 1
- `skip`: continue to Step 2 (will likely fail without MCP)
- `stop`: abort onboarding

## Step 2: Discover

Run the `/zscaler-discover` flow to scan all services and generate `memory/zscaler-tenant.md`.

Print progress as the scan runs:
```
Scanning ZIA... done (X locations, Y rules)
Scanning ZPA... done (X app segments, Y access rules)
Scanning ZTB... done / skipped (no AirGap configured)
Scanning ZIdentity... done (X users, Y groups)
Scanning ZCC/ZDX... done
```

**On failure:** Report the error. Ask: "Discovery failed. Do you want to continue with audit+snapshot anyway? (yes/no)"

## Step 3: Audit

Run the `/zscaler-audit` flow to execute all security checks.

After the audit completes, print the findings summary:
```
Audit Results:
  CRITICAL: X    HIGH: X    MEDIUM: X    LOW: X    INFO: X
```

**Do NOT auto-fix.** Ask the user:
> "Do you want to review and fix findings now? (yes/no)"

- If `yes`: show detailed findings and offer auto-fix per the `/zscaler-audit` skill's auto-fix flow
- If `no`: save the report and continue to Step 4

**On failure:** Report the error. Ask: "Audit failed. Do you want to continue with snapshot? (yes/no)"

## Step 4: Snapshot

Run `/zscaler-snapshot take` to capture the initial baseline snapshot.

This becomes the reference point for future drift detection via `/zscaler-snapshot diff`.

**On failure:** Report the error. The onboarding is still considered successful if Steps 1-3 completed.

## Final Summary

After all steps complete (or partially complete), print:

```
=== Zscaler Onboarding Complete ===

Tenant:      <vanity domain from .mcp.json or .env>
Customer ID: <customer id>

Services Connected:
  ZIA: <Y/N>    ZPA: <Y/N>    ZTB: <Y/N>    ZDX: <Y/N>    ZCC: <Y/N>

Inventory:
  <count> locations, <count> app segments, <count> firewall rules, ...
  (from memory/zscaler-tenant.md)

Audit:
  <count> CRITICAL, <count> HIGH, <count> MEDIUM findings
  Report: zscaler/audits/<date>-audit.md

Baseline Snapshot:
  zscaler/snapshots/<timestamp>/

Available Skills:
  /zscaler-discover     Re-scan tenant inventory
  /zscaler-audit        Run security audit
  /zscaler-troubleshoot Diagnose issues
  /zscaler-snapshot     Take/diff/restore snapshots
  /zscaler-deploy       Deploy new resources

Recommended next steps:
  1. Review audit findings: cat zscaler/audits/<date>-audit.md
  2. Fix CRITICAL/HIGH issues
  3. Set up drift monitoring: /loop 24h /zscaler-snapshot take
```

Adapt the summary based on what actually completed:
- If a step was skipped or failed, note it (e.g., "Audit: SKIPPED (MCP connectivity issue)")
- If no ZTB is configured, show `ZTB: N/A` instead of `N`
- Pull inventory counts from `memory/zscaler-tenant.md` if it exists

## Error Handling

- Each step is independent enough to continue if a previous step fails (except Step 2-4 all need MCP)
- If Step 1 (setup) fails and user chooses to continue, warn that remaining steps will likely fail
- Never fail the entire onboarding silently — always report what succeeded and what failed
- If any step fails, include the error in the final summary under a "Issues" section

## Related API Reference

Onboarding chains multiple skills. For detailed API docs:
- Setup → See @zscaler-setup skill
- Discovery endpoints → See @zscaler-discover and individual product skills
- Audit endpoints → See @zscaler-audit skill
- Full product API map → See @zscaler orchestrator skill
