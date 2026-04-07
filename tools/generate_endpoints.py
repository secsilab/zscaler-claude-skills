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
        no_query = url_obj.split("?")[0]
        # Strip scheme and host if present (e.g. https://example.com/path -> /path)
        if "{{baseUrl}}" in no_query:
            return no_query.split("{{baseUrl}}")[-1] or ""
        m = re.match(r"https?://[^/]+(/.*)$", no_query)
        if m:
            return m.group(1)
        return no_query or ""
    parts = url_obj.get("path", [])
    if parts:
        path = "/" + "/".join(
            f"{{{{{p[1:]}}}}}" if p.startswith(":") else p for p in parts
        )
        return path.split("?")[0]
    raw = url_obj.get("raw", "")
    if raw:
        clean = raw.split("?")[0]
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


def apply_overrides(endpoints, overrides):
    """Apply manual corrections to fix known upstream Postman bugs.

    Each override entry matches by request `name` and replaces `path` and/or
    `method`. Use sparingly — only for confirmed bugs in the source collection.
    """
    if not overrides:
        return endpoints
    by_name = {o["name"]: o for o in overrides}
    for ep in endpoints:
        override = by_name.get(ep["name"])
        if override is None:
            continue
        if "path" in override:
            ep["path"] = override["path"]
        if "method" in override:
            ep["method"] = override["method"]
    return endpoints


def format_endpoints_md(product_name, endpoints, source_date):
    """Format endpoints as a Markdown document."""
    lines = [
        "<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->",
        f"<!-- Source: Postman | Updated: {source_date} -->",
        "",
        f"# {product_name} API Reference",
        "",
    ]
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
    return True, stored_date


def update_skill_frontmatter(skill_dir, postman_date):
    """Update postman_revision in SKILL.md frontmatter."""
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_path):
        return
    with open(skill_path) as f:
        content = f.read()
    if "postman_revision:" in content:
        content = re.sub(r"postman_revision: .+", f"postman_revision: {postman_date}", content)
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
    collection = fetch_json(config["url"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    overrides_by_skill = config.get("overrides", {})
    if "product_folders" in config:
        for item in collection.get("item", []):
            folder_name = item.get("name", "")
            skill_name = config["product_folders"].get(folder_name)
            if not skill_name:
                continue
            if target_skill and skill_name != target_skill:
                continue
            endpoints = extract_endpoints(item)
            endpoints = apply_overrides(endpoints, overrides_by_skill.get(skill_name, []))
            skill_dir = os.path.join(SKILLS_DIR, skill_name)
            endpoints_path = os.path.join(skill_dir, "ENDPOINTS.md")
            old_endpoints = parse_existing_endpoints(endpoints_path)
            added, removed = diff_endpoints(old_endpoints, endpoints)
            if added or removed:
                report[skill_name] = {"added": added, "removed": removed}
            if not check_only:
                md = format_endpoints_md(folder_name, endpoints, today)
                os.makedirs(skill_dir, exist_ok=True)
                with open(endpoints_path, "w") as f:
                    f.write(md)
                update_skill_frontmatter(skill_dir, today)
                print(f"  Generated {skill_name}/ENDPOINTS.md ({len(endpoints)} endpoints)")
    else:
        skill_name = config["skill"]
        if target_skill and skill_name != target_skill:
            return report
        endpoints = extract_endpoints(collection)
        endpoints = apply_overrides(endpoints, overrides_by_skill.get(skill_name, []))
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
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
