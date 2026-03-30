# Skill Versioning + Postman Drift Detection — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add semver versioning to all 21 skills, split API Reference sections into separate ENDPOINTS.md files, and create a bi-monthly GitHub Action that detects Postman collection changes and opens PRs with updated endpoints.

**Architecture:** Each product skill gets split into human-edited SKILL.md + auto-generated ENDPOINTS.md. A Python script downloads Postman collections and generates ENDPOINTS.md files. A GitHub Action runs bi-monthly, compares collections against stored metadata, and opens PRs when drift is detected.

**Tech Stack:** Python 3.10+ (urllib, json, re — no external deps), GitHub Actions, Postman public API (no auth).

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `tools/postman_sources.json` | Collection UIDs, URLs, folder→skill mappings, last_updated timestamps |
| Create | `tools/generate_endpoints.py` | Download Postman collections, generate ENDPOINTS.md files, report diff |
| Create | `tools/split_endpoints.py` | One-time migration: extract API Reference from SKILL.md into ENDPOINTS.md |
| Create | `tests/test_generate_endpoints.py` | Tests for endpoint generation logic |
| Create | `.github/workflows/postman-drift.yml` | Bi-monthly scheduled action |
| Create | `skills/zscaler-zia/ENDPOINTS.md` | Generated: ZIA API Reference |
| Create | `skills/zscaler-zpa/ENDPOINTS.md` | Generated: ZPA API Reference |
| Create | `skills/zscaler-ztb/ENDPOINTS.md` | Generated: ZTB API Reference |
| Create | `skills/zscaler-zcbc/ENDPOINTS.md` | Generated: ZCBC API Reference |
| Create | `skills/zscaler-zcc/ENDPOINTS.md` | Generated: ZCC API Reference |
| Create | `skills/zscaler-zdx/ENDPOINTS.md` | Generated: ZDX API Reference |
| Create | `skills/zscaler-zid/ENDPOINTS.md` | Generated: ZID API Reference |
| Create | `skills/zscaler-easm/ENDPOINTS.md` | Generated: EASM API Reference |
| Create | `skills/zscaler-zwa/ENDPOINTS.md` | Generated: ZWA API Reference |
| Create | `skills/zscaler-aiguard/ENDPOINTS.md` | Generated: AI Guard API Reference |
| Create | `skills/zscaler-zinsights/ENDPOINTS.md` | Generated: ZInsights API Reference |
| Modify | `skills/*/SKILL.md` (all 21) | Add version frontmatter, remove API Reference section (product skills) |
| Modify | `install.sh` | Copy ENDPOINTS.md alongside SKILL.md |
| Modify | `README.md` | Comprehensive update for all today's changes |

---

### Task 1: Create postman_sources.json

**Files:**
- Create: `tools/postman_sources.json`

- [ ] **Step 1: Write the source config**

Create `tools/postman_sources.json`:

```json
{
  "collections": {
    "oneapi": {
      "uid": "43028424-f276a17d-1778-46a9-8c61-ac3ef1d79de8",
      "url": "https://www.postman.com/collections/43028424-f276a17d-1778-46a9-8c61-ac3ef1d79de8",
      "metadata_url": "https://www.postman.com/_api/collection/43028424-f276a17d-1778-46a9-8c61-ac3ef1d79de8",
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
      "metadata_url": "https://www.postman.com/_api/collection/43028424-f74b4e07-08e1-4744-8d55-e64b0de87d0f",
      "last_updated": "2026-02-26",
      "skill": "zscaler-ztb"
    },
    "zwa": {
      "uid": "43028424-bfb895d7-5865-4586-8907-6bdc2bd222e5",
      "url": "https://www.postman.com/collections/43028424-bfb895d7-5865-4586-8907-6bdc2bd222e5",
      "metadata_url": "https://www.postman.com/_api/collection/43028424-bfb895d7-5865-4586-8907-6bdc2bd222e5",
      "last_updated": "2025-06-13",
      "skill": "zscaler-zwa"
    },
    "aiguard": {
      "uid": "43028424-c00ef572-af61-410e-bdbd-ab84ea34d599",
      "url": "https://www.postman.com/collections/43028424-c00ef572-af61-410e-bdbd-ab84ea34d599",
      "metadata_url": "https://www.postman.com/_api/collection/43028424-c00ef572-af61-410e-bdbd-ab84ea34d599",
      "last_updated": "2026-02-26",
      "skill": "zscaler-aiguard"
    }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add tools/postman_sources.json
git commit -m "feat: add Postman collection source config for drift detection"
```

---

### Task 2: Create generate_endpoints.py with tests

**Files:**
- Create: `tools/generate_endpoints.py`
- Create: `tests/test_generate_endpoints.py`

- [ ] **Step 1: Write tests**

Create `tests/test_generate_endpoints.py`:

```python
#!/usr/bin/env python3
"""Tests for generate_endpoints.py"""
import json
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from generate_endpoints import (
    parse_url,
    extract_endpoints,
    format_endpoints_md,
    diff_endpoints,
)


def test_parse_url_string():
    assert parse_url("https://example.com/api/v1/users?limit=10") == "/api/v1/users"


def test_parse_url_object():
    url_obj = {
        "raw": "{{baseUrl}}/api/v1/users/:userId",
        "path": ["api", "v1", "users", ":userId"],
    }
    assert parse_url(url_obj) == "/api/v1/users/{{userId}}"


def test_parse_url_empty():
    assert parse_url({}) == ""


def test_extract_endpoints_flat():
    collection = {
        "item": [
            {
                "name": "Get User",
                "request": {"method": "GET", "url": {"path": ["users", ":id"]}},
            },
            {
                "name": "Create User",
                "request": {"method": "POST", "url": {"path": ["users"]}},
            },
        ]
    }
    eps = extract_endpoints(collection)
    assert len(eps) == 2
    assert eps[0]["method"] == "GET"
    assert eps[0]["path"] == "/users/{{id}}"
    assert eps[1]["method"] == "POST"


def test_extract_endpoints_nested():
    collection = {
        "item": [
            {
                "name": "Users",
                "item": [
                    {
                        "name": "List Users",
                        "request": {"method": "GET", "url": {"path": ["users"]}},
                    }
                ],
            }
        ]
    }
    result = extract_endpoints(collection)
    assert len(result) == 1
    assert result[0]["name"] == "List Users"


def test_format_endpoints_md():
    endpoints = [
        {"method": "GET", "path": "/users", "name": "List Users", "folder": "Users"},
        {"method": "POST", "path": "/users", "name": "Create User", "folder": "Users"},
        {"method": "GET", "path": "/roles", "name": "List Roles", "folder": "Roles"},
    ]
    md = format_endpoints_md("ZIA", endpoints, "2026-03-05")
    assert "<!-- AUTO-GENERATED" in md
    assert "2026-03-05" in md
    assert "### Users (2 endpoints)" in md
    assert "### Roles (1 endpoints)" in md
    assert "| GET | `/users` | List Users |" in md


def test_diff_endpoints():
    old = [
        {"method": "GET", "path": "/users", "name": "List Users"},
        {"method": "DELETE", "path": "/old", "name": "Old Endpoint"},
    ]
    new = [
        {"method": "GET", "path": "/users", "name": "List Users"},
        {"method": "POST", "path": "/new", "name": "New Endpoint"},
    ]
    added, removed = diff_endpoints(old, new)
    assert len(added) == 1
    assert added[0]["path"] == "/new"
    assert len(removed) == 1
    assert removed[0]["path"] == "/old"


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            try:
                func()
                print(f"PASS: {name}")
            except AssertionError as e:
                print(f"FAIL: {name} — {e}")
                sys.exit(1)
    print("\nAll tests passed.")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python3 tests/test_generate_endpoints.py
```

Expected: ImportError (module doesn't exist yet).

- [ ] **Step 3: Write generate_endpoints.py**

Create `tools/generate_endpoints.py`:

```python
#!/usr/bin/env python3
"""Download Zscaler Postman collections and generate ENDPOINTS.md files.

Usage:
    python3 generate_endpoints.py                    # Generate all from Postman
    python3 generate_endpoints.py --check            # Check for drift only (no file writes)
    python3 generate_endpoints.py --skill zscaler-zia # Generate for one skill only
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
SOURCES_FILE = os.path.join(SCRIPT_DIR, "postman_sources.json")


def parse_url(url_obj):
    """Extract clean URL path from Postman URL object or string."""
    if isinstance(url_obj, str):
        return url_obj.split("?")[0].split("{{baseUrl}}")[-1] or ""
    parts = url_obj.get("path", [])
    if parts:
        path = "/" + "/".join(
            f"{{{{{p[1:]}}}}}" if p.startswith(":") else p for p in parts
        )
        return path.split("?")[0]
    raw = url_obj.get("raw", "")
    if raw:
        clean = raw.split("?")[0]
        # Remove base URL variable
        clean = re.sub(r"\{\{[^}]+\}\}", "", clean, count=1)
        return clean or ""
    return ""


def extract_endpoints(node, folder=None):
    """Recursively extract request items from Postman folder tree."""
    results = []
    for item in node.get("item", []):
        current_folder = folder or item.get("name", "")
        if "request" in item and "item" not in item:
            req = item["request"]
            results.append({
                "method": req.get("method", "GET"),
                "path": parse_url(req.get("url", {})),
                "name": item.get("name", ""),
                "folder": current_folder,
            })
        if "item" in item:
            subfolder = item.get("name", "") if not folder else folder
            results.extend(extract_endpoints(item, subfolder))
    return results


def format_endpoints_md(product_name, endpoints, source_date):
    """Format endpoints as a Markdown document."""
    lines = [
        f"<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->",
        f"<!-- Source: Postman | Updated: {source_date} -->",
        "",
        f"# {product_name} API Reference",
        "",
    ]

    # Group by folder
    folders = {}
    for ep in endpoints:
        folder = ep.get("folder", "General")
        folders.setdefault(folder, []).append(ep)

    for folder_name, eps in folders.items():
        lines.append(f"### {folder_name} ({len(eps)} endpoints)")
        lines.append("")
        lines.append("| Method | Endpoint | Description |")
        lines.append("|--------|----------|-------------|")
        for ep in eps:
            lines.append(f"| {ep['method']} | `{ep['path']}` | {ep['name']} |")
        lines.append("")

    return "\n".join(lines)


def diff_endpoints(old_endpoints, new_endpoints):
    """Compare two endpoint lists. Returns (added, removed)."""
    old_set = {(ep["method"], ep["path"]) for ep in old_endpoints}
    new_set = {(ep["method"], ep["path"]) for ep in new_endpoints}

    added = [ep for ep in new_endpoints if (ep["method"], ep["path"]) not in old_set]
    removed = [ep for ep in old_endpoints if (ep["method"], ep["path"]) not in new_set]
    return added, removed


def parse_existing_endpoints(filepath):
    """Parse an existing ENDPOINTS.md back into endpoint list."""
    endpoints = []
    if not os.path.exists(filepath):
        return endpoints
    with open(filepath) as f:
        current_folder = "General"
        for line in f:
            line = line.rstrip()
            if line.startswith("### "):
                current_folder = re.sub(r"\s*\(\d+ endpoints?\)", "", line[4:])
            m = re.match(r"\| (\w+) \| `([^`]+)` \| (.+) \|", line)
            if m:
                endpoints.append({
                    "method": m.group(1),
                    "path": m.group(2),
                    "name": m.group(3).strip(),
                    "folder": current_folder,
                })
    return endpoints


def fetch_json(url):
    """Fetch JSON from a URL."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "zscaler-claude-skills/1.0")
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())


def fetch_collection(url):
    """Download a full Postman collection."""
    print(f"  Downloading collection from {url[:60]}...")
    return fetch_json(url)


def check_collection_updated(metadata_url, stored_date):
    """Check if a collection has been updated since stored_date."""
    try:
        data = fetch_json(metadata_url)
        updated_at = data.get("data", {}).get("updatedAt", "")
        if updated_at:
            remote_date = updated_at[:10]
            return remote_date > stored_date, remote_date
    except urllib.error.URLError as e:
        print(f"  Warning: could not check metadata: {e}")
    return True, stored_date  # Assume changed if we can't check


def update_skill_frontmatter(skill_dir, postman_date):
    """Update postman_revision in SKILL.md frontmatter."""
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_path):
        return
    with open(skill_path) as f:
        content = f.read()
    if "postman_revision:" in content:
        content = re.sub(
            r"postman_revision: .+",
            f"postman_revision: {postman_date}",
            content,
        )
    with open(skill_path, "w") as f:
        f.write(content)


def load_sources():
    """Load postman_sources.json."""
    with open(SOURCES_FILE) as f:
        return json.load(f)


def save_sources(sources):
    """Save postman_sources.json."""
    with open(SOURCES_FILE, "w") as f:
        json.dump(sources, f, indent=2)
        f.write("\n")


def generate_for_collection(name, config, check_only=False, target_skill=None):
    """Generate ENDPOINTS.md for all skills in a collection. Returns diff report."""
    report = {}
    collection = fetch_collection(config["url"])

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if "product_folders" in config:
        # Multi-product collection (OneAPI)
        for item in collection.get("item", []):
            folder_name = item.get("name", "")
            skill_name = config["product_folders"].get(folder_name)
            if not skill_name:
                continue
            if target_skill and skill_name != target_skill:
                continue

            endpoints = extract_endpoints(item)
            skill_dir = os.path.join(SKILLS_DIR, skill_name)
            endpoints_path = os.path.join(skill_dir, "ENDPOINTS.md")

            old_endpoints = parse_existing_endpoints(endpoints_path)
            added, removed = diff_endpoints(old_endpoints, endpoints)

            if added or removed:
                report[skill_name] = {"added": added, "removed": removed}

            if not check_only:
                product_name = folder_name
                md = format_endpoints_md(product_name, endpoints, today)
                os.makedirs(skill_dir, exist_ok=True)
                with open(endpoints_path, "w") as f:
                    f.write(md)
                update_skill_frontmatter(skill_dir, today)
                print(f"  Generated {skill_name}/ENDPOINTS.md ({len(endpoints)} endpoints)")
    else:
        # Single-product collection
        skill_name = config["skill"]
        if target_skill and skill_name != target_skill:
            return report

        endpoints = extract_endpoints(collection)
        skill_dir = os.path.join(SKILLS_DIR, skill_name)
        endpoints_path = os.path.join(skill_dir, "ENDPOINTS.md")

        old_endpoints = parse_existing_endpoints(endpoints_path)
        added, removed = diff_endpoints(old_endpoints, endpoints)

        if added or removed:
            report[skill_name] = {"added": added, "removed": removed}

        if not check_only:
            product_name = collection.get("info", {}).get("name", skill_name)
            md = format_endpoints_md(product_name, endpoints, today)
            os.makedirs(skill_dir, exist_ok=True)
            with open(endpoints_path, "w") as f:
                f.write(md)
            update_skill_frontmatter(skill_dir, today)
            print(f"  Generated {skill_name}/ENDPOINTS.md ({len(endpoints)} endpoints)")

    return report


def format_report(all_reports):
    """Format a human-readable diff report."""
    lines = []
    for skill, diff in sorted(all_reports.items()):
        added = diff["added"]
        removed = diff["removed"]
        lines.append(f"\n### {skill} ({len(added)} added, {len(removed)} removed)")
        for ep in added:
            lines.append(f"- Added: `{ep['method']} {ep['path']}`")
        for ep in removed:
            lines.append(f"- Removed: `{ep['method']} {ep['path']}`")
    if not lines:
        return "No changes detected."
    return "\n".join(lines)


def main():
    check_only = "--check" in sys.argv
    target_skill = None
    if "--skill" in sys.argv:
        idx = sys.argv.index("--skill")
        target_skill = sys.argv[idx + 1]

    sources = load_sources()
    all_reports = {}

    for name, config in sources["collections"].items():
        print(f"\n[{name}]")

        if check_only:
            changed, remote_date = check_collection_updated(
                config["metadata_url"], config["last_updated"]
            )
            if not changed:
                print(f"  No changes (last updated: {config['last_updated']})")
                continue
            print(f"  Changed! Remote: {remote_date}, Stored: {config['last_updated']}")

        report = generate_for_collection(name, config, check_only, target_skill)
        all_reports.update(report)

        if not check_only:
            config["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not check_only:
        save_sources(sources)

    print("\n" + "=" * 50)
    print(format_report(all_reports))

    if all_reports:
        sys.exit(2)  # Signal that changes were found
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python3 tests/test_generate_endpoints.py
```

Expected: All tests passed.

- [ ] **Step 5: Commit**

```bash
git add tools/generate_endpoints.py tests/test_generate_endpoints.py
git commit -m "feat: add Postman endpoint generator with tests"
```

---

### Task 3: Create split_endpoints.py and run the initial split

**Files:**
- Create: `tools/split_endpoints.py`
- Modify: 11 skills (SKILL.md split + ENDPOINTS.md created)

This is the one-time migration script that extracts the `## API Reference` section from each SKILL.md into a separate ENDPOINTS.md.

- [ ] **Step 1: Write the split script**

Create `tools/split_endpoints.py`:

```python
#!/usr/bin/env python3
"""One-time migration: split API Reference sections from SKILL.md into ENDPOINTS.md.

Usage:
    python3 split_endpoints.py              # Split all product skills
    python3 split_endpoints.py zscaler-zia  # Split one skill only
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "skills")

# Skills and their API Reference section boundaries (start heading text)
SKILLS_TO_SPLIT = {
    "zscaler-zia": {"start": "## API Reference", "product": "Zscaler Internet Access (ZIA)"},
    "zscaler-zpa": {"start": "## API Reference (328 endpoints, 66 controllers)", "product": "Zscaler Private Access (ZPA)"},
    "zscaler-ztb": {"start": "## API Reference (674 endpoints)", "product": "Zero Trust Branch (ZTB)"},
    "zscaler-zcbc": {"start": "## API Reference", "product": "Zscaler Cloud & Branch Connector (ZCBC)"},
    "zscaler-zcc": {"start": "## API Reference", "product": "Zscaler Client Connector (ZCC)"},
    "zscaler-zdx": {"start": "## API Reference", "product": "Zscaler Digital Experience (ZDX)"},
    "zscaler-zid": {"start": "## API Reference", "product": "ZIdentity (ZID)"},
    "zscaler-easm": {"start": "## API Reference", "product": "External Attack Surface Management (EASM)"},
    "zscaler-zwa": {"start": "## API Reference", "product": "Zscaler Workflow Automation (ZWA)"},
    "zscaler-aiguard": {"start": "## API Reference", "product": "Zscaler AI Guard"},
    "zscaler-zinsights": {"start": "## API Reference", "product": "Zscaler Insights (ZInsights)"},
}


def split_skill(skill_name, config):
    """Extract API Reference section from SKILL.md into ENDPOINTS.md."""
    skill_dir = os.path.join(SKILLS_DIR, skill_name)
    skill_path = os.path.join(skill_dir, "SKILL.md")
    endpoints_path = os.path.join(skill_dir, "ENDPOINTS.md")

    if not os.path.exists(skill_path):
        print(f"  SKIP: {skill_path} not found")
        return False

    with open(skill_path) as f:
        lines = f.readlines()

    # Find the API Reference section
    start_line = None
    end_line = None
    start_text = config["start"]

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped.startswith("## API Reference") and start_line is None:
            start_line = i
        elif start_line is not None and stripped.startswith("## ") and i > start_line:
            end_line = i
            break

    if start_line is None:
        print(f"  SKIP: no API Reference section found in {skill_name}")
        return False

    if end_line is None:
        end_line = len(lines)

    # Extract API Reference content
    api_lines = lines[start_line:end_line]

    # Write ENDPOINTS.md
    header = [
        "<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->\n",
        "<!-- Source: Extracted from SKILL.md | Updated: 2026-03-30 -->\n",
        "\n",
        f"# {config['product']} API Reference\n",
        "\n",
    ]
    # Skip the "## API Reference..." heading from extracted content, keep subheadings
    body = []
    for line in api_lines[1:]:  # Skip first line (the ## heading)
        if line.strip() == "":
            body.append(line)
        else:
            body.append(line)

    with open(endpoints_path, "w") as f:
        f.writelines(header)
        f.writelines(body)

    # Replace API Reference section in SKILL.md with a reference
    reference = f"\nFor full API endpoint reference, see ENDPOINTS.md in this skill directory.\n\n"
    new_lines = lines[:start_line] + [reference] + lines[end_line:]

    with open(skill_path, "w") as f:
        f.writelines(new_lines)

    extracted = end_line - start_line
    print(f"  OK: {skill_name} — extracted {extracted} lines into ENDPOINTS.md")
    return True


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None

    skills = SKILLS_TO_SPLIT
    if target:
        if target not in skills:
            print(f"Unknown skill: {target}")
            sys.exit(1)
        skills = {target: skills[target]}

    print("Splitting API Reference sections into ENDPOINTS.md...\n")
    count = 0
    for skill_name, config in skills.items():
        if split_skill(skill_name, config):
            count += 1

    print(f"\nDone. Split {count} skills.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the split**

```bash
python3 tools/split_endpoints.py
```

Expected output:
```
Splitting API Reference sections into ENDPOINTS.md...

  OK: zscaler-zia — extracted 819 lines into ENDPOINTS.md
  OK: zscaler-zpa — extracted 670 lines into ENDPOINTS.md
  OK: zscaler-ztb — extracted 1011 lines into ENDPOINTS.md
  ...

Done. Split 11 skills.
```

- [ ] **Step 3: Verify all ENDPOINTS.md files exist**

```bash
for skill in zscaler-zia zscaler-zpa zscaler-ztb zscaler-zcbc zscaler-zcc zscaler-zdx zscaler-zid zscaler-easm zscaler-zwa zscaler-aiguard zscaler-zinsights; do
  if [ -f "skills/$skill/ENDPOINTS.md" ]; then
    echo "OK: $skill/ENDPOINTS.md ($(wc -l < skills/$skill/ENDPOINTS.md) lines)"
  else
    echo "MISSING: $skill/ENDPOINTS.md"
  fi
done
```

- [ ] **Step 4: Verify SKILL.md files have the reference line**

```bash
grep -l "see ENDPOINTS.md" skills/*/SKILL.md | wc -l
```

Expected: 11

- [ ] **Step 5: Verify SKILL.md files no longer have API Reference tables**

```bash
grep -c "^| Method | Endpoint |" skills/zscaler-zia/SKILL.md
```

Expected: 0 (all tables moved to ENDPOINTS.md)

- [ ] **Step 6: Commit**

```bash
git add tools/split_endpoints.py skills/*/ENDPOINTS.md skills/*/SKILL.md
git commit -m "feat: split API Reference sections into ENDPOINTS.md for 11 product skills"
```

---

### Task 4: Add version frontmatter to all 21 skills

**Files:**
- Modify: All 21 `skills/*/SKILL.md` files

- [ ] **Step 1: Write a version injection script**

This is simpler as an inline bash loop than a separate script:

```bash
# Skills with field gotchas (version 1.1.0) and postman_revision
for skill in zscaler-zia zscaler-zpa zscaler-ztb zscaler-zcc; do
  sed -i '' 's/^name: '"$skill"'$/name: '"$skill"'\nversion: 1.1.0\npostman_revision: 2026-03-30/' "skills/$skill/SKILL.md"
done

# Product skills at 1.0.0 with postman_revision
for skill in zscaler-zcbc zscaler-zdx zscaler-zid zscaler-easm zscaler-zwa zscaler-aiguard; do
  sed -i '' 's/^name: '"$skill"'$/name: '"$skill"'\nversion: 1.0.0\npostman_revision: 2026-03-30/' "skills/$skill/SKILL.md"
done

# ZInsights (no postman_revision — analytics API not in Postman)
sed -i '' 's/^name: zscaler-zinsights$/name: zscaler-zinsights\nversion: 1.0.0/' "skills/zscaler-zinsights/SKILL.md"

# Operational skills at 1.0.0 (no postman_revision)
for skill in zscaler zscaler-setup zscaler-onboard zscaler-discover zscaler-audit zscaler-troubleshoot zscaler-snapshot zscaler-deploy zscaler-migrate zscaler-bridge; do
  sed -i '' 's/^name: '"$skill"'$/name: '"$skill"'\nversion: 1.0.0/' "skills/$skill/SKILL.md"
done
```

**Note:** On Linux, use `sed -i` instead of `sed -i ''`.

- [ ] **Step 2: Verify all skills have version field**

```bash
for f in skills/*/SKILL.md; do
  name=$(grep "^name:" "$f" | head -1 | cut -d' ' -f2-)
  version=$(grep "^version:" "$f" | head -1 | cut -d' ' -f2-)
  if [ -z "$version" ]; then
    echo "MISSING version: $name ($f)"
  else
    echo "OK: $name v$version"
  fi
done
```

Expected: 21 lines, all "OK".

- [ ] **Step 3: Verify postman_revision on product skills**

```bash
grep -l "postman_revision:" skills/*/SKILL.md | wc -l
```

Expected: 10

- [ ] **Step 4: Commit**

```bash
git add skills/*/SKILL.md
git commit -m "feat: add semver versioning to all 21 skills"
```

---

### Task 5: Update install.sh to copy ENDPOINTS.md

**Files:**
- Modify: `install.sh`

- [ ] **Step 1: Update the install loop**

In `install.sh`, replace the file copy loop (lines 42-51):

```bash
# Old:
for skill in $SKILLS; do
    src="$SCRIPT_DIR/skills/$skill/SKILL.md"
    if [ ! -f "$src" ]; then
        echo "[SKIP] $skill (not found)"
        continue
    fi
    mkdir -p "$SKILLS_DIR/$skill"
    cp "$src" "$SKILLS_DIR/$skill/SKILL.md"
    echo "[OK] $skill"
    INSTALLED=$((INSTALLED + 1))
done

# New:
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
```

- [ ] **Step 2: Verify syntax**

```bash
bash -n install.sh && echo "SYNTAX OK"
```

- [ ] **Step 3: Commit**

```bash
git add install.sh
git commit -m "feat: install.sh now copies ENDPOINTS.md alongside SKILL.md"
```

---

### Task 6: Create GitHub Action for Postman drift detection

**Files:**
- Create: `.github/workflows/postman-drift.yml`

- [ ] **Step 1: Write the workflow**

Create `.github/workflows/postman-drift.yml`:

```yaml
name: Postman Collection Drift Detection

on:
  schedule:
    # Bi-monthly: 1st and 15th of each month at 09:00 UTC
    - cron: '0 9 1,15 * *'
  workflow_dispatch: # Allow manual trigger

permissions:
  contents: write
  pull-requests: write

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Check for collection updates
        id: check
        run: |
          python3 tools/generate_endpoints.py --check > drift_report.txt 2>&1 || true
          EXIT_CODE=${PIPESTATUS[0]}
          echo "exit_code=$EXIT_CODE" >> "$GITHUB_OUTPUT"
          cat drift_report.txt

      - name: Generate updated endpoints
        if: steps.check.outputs.exit_code == '2'
        run: |
          python3 tools/generate_endpoints.py > generate_report.txt 2>&1
          cat generate_report.txt

      - name: Create Pull Request
        if: steps.check.outputs.exit_code == '2'
        run: |
          DATE=$(date +%Y-%m-%d)
          BRANCH="postman-update/$DATE"

          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          git checkout -b "$BRANCH"
          git add skills/*/ENDPOINTS.md skills/*/SKILL.md tools/postman_sources.json
          git commit -m "chore: update endpoints from Postman collections ($DATE)"
          git push origin "$BRANCH"

          # Build PR body from drift report
          REPORT=$(cat drift_report.txt | tail -n +3)
          gh pr create \
            --title "Postman Collection Update — $DATE" \
            --body "$(cat <<EOF
          ## Postman Collection Drift Detected

          $REPORT

          ---
          Auto-generated by [postman-drift](.github/workflows/postman-drift.yml) workflow.
          EOF
          )" \
            --base main \
            --head "$BRANCH"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: No changes detected
        if: steps.check.outputs.exit_code != '2'
        run: echo "No Postman collection changes detected. Nothing to do."
```

- [ ] **Step 2: Verify YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/postman-drift.yml'))" 2>/dev/null || python3 -c "
import json, sys
# Basic YAML structure check without PyYAML
with open('.github/workflows/postman-drift.yml') as f:
    content = f.read()
    if 'on:' in content and 'jobs:' in content and 'steps:' in content:
        print('YAML structure looks valid')
    else:
        print('YAML structure may be invalid')
        sys.exit(1)
"
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/postman-drift.yml
git commit -m "feat: add bi-monthly GitHub Action for Postman drift detection"
```

---

### Task 7: Comprehensive README update

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README.md**

Replace the entire README with an updated version that covers all of today's changes. The new README must include:

1. Updated header (21 skills, 1,677 endpoints)
2. Quick Start (unchanged)
3. Skills tables (10 operational + 11 product, with version column)
4. New section: "Skill Versioning" explaining the version + postman_revision fields
5. New section: "ENDPOINTS.md — API Reference Files" explaining the split
6. New section: "Postman Drift Detection" explaining the GitHub Action
7. Architecture diagram (updated with zstack integration + ENDPOINTS.md)
8. New section: "Using with zstack" explaining side-by-side usage
9. Tools section (updated with generate_endpoints.py and split_endpoints.py)
10. Requirements (unchanged)

Write the full new README.md content — see the full file in Step 2.

- [ ] **Step 2: Write the README**

Full content for `README.md`:

```markdown
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

Converts Zscaler's official Postman collection JSON files into Markdown endpoint tables. Used to maintain the product skills.

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
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: comprehensive README update — versioning, ENDPOINTS.md, drift detection, zstack integration"
```

---

### Task 8: Final verification

**Files:**
- All modified files

- [ ] **Step 1: Run the test suite**

```bash
python3 tests/test_generate_endpoints.py
```

Expected: All tests passed.

- [ ] **Step 2: Verify all 21 skills have version**

```bash
for f in skills/*/SKILL.md; do
  name=$(grep "^name:" "$f" | head -1 | cut -d' ' -f2-)
  version=$(grep "^version:" "$f" | head -1 | cut -d' ' -f2-)
  echo "$name v$version"
done
```

- [ ] **Step 3: Verify 11 ENDPOINTS.md files exist and are non-empty**

```bash
for f in skills/*/ENDPOINTS.md; do
  lines=$(wc -l < "$f")
  skill=$(basename $(dirname "$f"))
  echo "$skill: $lines lines"
done
```

- [ ] **Step 4: Verify install.sh works**

```bash
bash -n install.sh && echo "SYNTAX OK"
```

- [ ] **Step 5: Verify no API Reference tables remain in SKILL.md (product skills)**

```bash
for skill in zscaler-zia zscaler-zpa zscaler-ztb zscaler-zcbc zscaler-zcc zscaler-zdx zscaler-zid zscaler-easm zscaler-zwa zscaler-aiguard zscaler-zinsights; do
  count=$(grep -c "^| Method | Endpoint |" "skills/$skill/SKILL.md" 2>/dev/null || echo 0)
  if [ "$count" -gt 0 ]; then
    echo "WARNING: $skill still has $count endpoint tables in SKILL.md"
  fi
done
echo "Check complete."
```

- [ ] **Step 6: Verify GitHub Action YAML is valid**

```bash
python3 -c "
with open('.github/workflows/postman-drift.yml') as f:
    content = f.read()
assert 'on:' in content
assert 'schedule:' in content
assert 'cron:' in content
assert 'generate_endpoints.py' in content
print('GitHub Action structure valid')
"
```

- [ ] **Step 7: Run install.sh to deploy**

```bash
bash install.sh
```

Verify output shows 21 skills installed.

- [ ] **Step 8: Push everything**

```bash
git push origin main
```
