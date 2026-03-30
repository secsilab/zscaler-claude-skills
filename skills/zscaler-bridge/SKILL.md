---
name: zscaler-bridge
version: 1.0.0
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
