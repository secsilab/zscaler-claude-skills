# Skill Versioning + Postman Drift Detection — Design Spec

**Date:** 2026-03-30
**Status:** Approved

## Goal

Add versioning to all skills (semver + Postman source revision) and automate detection of Postman collection changes via a bi-monthly GitHub Action that opens PRs with regenerated endpoint tables.

## 1. Skill Versioning

### Frontmatter Changes

All SKILL.md files get a `version` field. Product skills with Postman-sourced endpoints also get `postman_revision`.

```yaml
---
name: zscaler-zia
version: 1.1.0
postman_revision: 2026-03-05
description: Use when...
---
```

- `version`: semver, bumped manually on human edits
- `postman_revision`: date of last integrated Postman update, bumped by CI
- Operational skills (deploy, troubleshoot, audit, bridge, migrate, etc.) only have `version`

### Version Mapping

| Skill | Initial Version | Has postman_revision |
|-------|----------------|---------------------|
| zscaler | 1.0.0 | No |
| zscaler-setup | 1.0.0 | No |
| zscaler-onboard | 1.0.0 | No |
| zscaler-discover | 1.0.0 | No |
| zscaler-audit | 1.0.0 | No |
| zscaler-troubleshoot | 1.0.0 | No |
| zscaler-snapshot | 1.0.0 | No |
| zscaler-deploy | 1.0.0 | No |
| zscaler-migrate | 1.0.0 | No |
| zscaler-bridge | 1.0.0 | No |
| zscaler-zia | 1.1.0 | Yes |
| zscaler-zpa | 1.1.0 | Yes |
| zscaler-ztb | 1.1.0 | Yes |
| zscaler-zcbc | 1.0.0 | Yes |
| zscaler-zcc | 1.1.0 | Yes |
| zscaler-zdx | 1.0.0 | Yes |
| zscaler-zid | 1.0.0 | Yes |
| zscaler-easm | 1.0.0 | Yes |
| zscaler-zwa | 1.0.0 | Yes |
| zscaler-aiguard | 1.0.0 | Yes |
| zscaler-zinsights | 1.0.0 | No (analytics API, not in Postman) |

Skills with field gotchas added today start at 1.1.0. Others at 1.0.0.

## 2. File Separation: SKILL.md + ENDPOINTS.md

### Before
```
skills/zscaler-zia/SKILL.md  (44KB — everything)
```

### After
```
skills/zscaler-zia/
├── SKILL.md       (~15KB — human: overview, MCP Tools, gotchas, patterns, limitations)
└── ENDPOINTS.md   (~30KB — generated: API Reference tables)
```

### Rules
- `SKILL.md` contains a reference: `For full API endpoint reference, see ENDPOINTS.md in this skill directory.`
- `ENDPOINTS.md` has auto-generated header with timestamp and source revision
- `install.sh` copies both files to `~/.claude/skills/<skill>/`
- 10 skills get ENDPOINTS.md: ZIA, ZPA, ZTB, ZCBC, ZCC, ZDX, ZID, EASM, ZWA, AI Guard
- 11 other skills remain single-file

### ENDPOINTS.md Format
```markdown
<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->
<!-- Source: OneAPI collection | Updated: 2026-03-05 | Revision: 12345 -->

# ZIA API Reference

## Activation (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/status` | Get activation status |
| POST | `/status/activate` | Activate configuration changes |

...
```

## 3. Endpoint Generator: `tools/generate_endpoints.py`

Replaces/evolves `extract_postman.py`. New capabilities:

1. Downloads Postman collections from public URLs (no auth)
2. Splits OneAPI by product folder → per-skill ENDPOINTS.md
3. Generates markdown with auto-generated header
4. Compares with existing ENDPOINTS.md, reports diff
5. Updates `postman_revision` in corresponding SKILL.md frontmatter

### Collections Tracked

| Collection | Postman UID | Download URL | Target Skills |
|---|---|---|---|
| OneAPI | 43028424-f276a17d-1778-46a9-8c61-ac3ef1d79de8 | `postman.com/collections/43028424-f276a17d-...` | ZIA, ZPA, ZCBC, ZDX, ZCC, ZID, EASM |
| ZTB | 43028424-f74b4e07-08e1-4744-8d55-e64b0de87d0f | `postman.com/collections/43028424-f74b4e07-...` | ZTB |
| ZWA | 43028424-bfb895d7-5865-4586-8907-6bdc2bd222e5 | `postman.com/collections/43028424-bfb895d7-...` | ZWA |
| AI Guard | 43028424-c00ef572-af61-410e-bdbd-ab84ea34d599 | `postman.com/collections/43028424-c00ef572-...` | AI Guard |

### Source Config: `tools/postman_sources.json`

```json
{
  "collections": {
    "oneapi": {
      "uid": "43028424-f276a17d-1778-46a9-8c61-ac3ef1d79de8",
      "url": "https://www.postman.com/collections/43028424-f276a17d-1778-46a9-8c61-ac3ef1d79de8",
      "last_updated": "2026-03-05",
      "product_folders": {
        "Zscaler Internet Access (ZIA)": "zscaler-zia",
        "Zscaler Private Access (ZPA)": "zscaler-zpa",
        "Zscaler Cloud & Branch Connector (ZCBC)": "zscaler-zcbc",
        "Zscaler Digital Experience (ZDX)": "zscaler-zdx",
        "Zscaler Client Connector (ZCC)": "zscaler-zcc",
        "ZIdentity (ZID)": "zscaler-zid",
        "EASM": "zscaler-easm"
      }
    },
    "ztb": {
      "uid": "43028424-f74b4e07-08e1-4744-8d55-e64b0de87d0f",
      "url": "https://www.postman.com/collections/43028424-f74b4e07-08e1-4744-8d55-e64b0de87d0f",
      "last_updated": "2026-02-26",
      "skill": "zscaler-ztb"
    },
    "zwa": {
      "uid": "43028424-bfb895d7-5865-4586-8907-6bdc2bd222e5",
      "url": "https://www.postman.com/collections/43028424-bfb895d7-5865-4586-8907-6bdc2bd222e5",
      "last_updated": "2025-06-13",
      "skill": "zscaler-zwa"
    },
    "aiguard": {
      "uid": "43028424-c00ef572-af61-410e-bdbd-ab84ea34d599",
      "url": "https://www.postman.com/collections/43028424-c00ef572-af61-410e-bdbd-ab84ea34d599",
      "last_updated": "2026-02-26",
      "skill": "zscaler-aiguard"
    }
  }
}
```

## 4. GitHub Action: `.github/workflows/postman-drift.yml`

### Schedule
Bi-monthly: cron `0 9 1,15 * *` (1st and 15th at 09:00 UTC)

### Flow
1. Checkout repo
2. For each collection in `postman_sources.json`:
   a. Fetch metadata via `https://www.postman.com/_api/collection/<uid>`
   b. Compare `updatedAt` with stored `last_updated`
   c. If unchanged → skip
3. If any collection changed:
   a. Download full collection JSON
   b. Run `generate_endpoints.py` to regenerate ENDPOINTS.md files
   c. Update `postman_revision` in affected SKILL.md frontmatter
   d. Update `last_updated` in `postman_sources.json`
   e. Create branch `postman-update/YYYY-MM-DD`
   f. Commit changes
   g. Open PR with summary

### PR Body Format
```markdown
## Postman Collection Update — 2026-04-15

### ZIA (3 changes)
- Added: `POST /cloudBrowserIsolation/profiles`
- Added: `GET /cloudBrowserIsolation/profiles/{id}`
- Removed: `GET /obsoleteEndpoint`

### ZPA (no changes)

### ZTB (1 change)
- Added: `GET /api/v3/newEndpoint`

---
Auto-generated by postman-drift workflow.
```

### If No Changes
Action exits cleanly with no PR.

## 5. README Update

README.md updated to reflect:
- 21 skills with versioning
- ENDPOINTS.md separation explained
- Postman drift detection explained
- Updated architecture diagram
- Updated install instructions (both files copied)

## Non-Goals
- No automatic merge of PRs (human review required)
- No OpenAPI spec generation (Postman JSON is the source of truth)
- No backward compatibility with old single-file format (clean migration)
