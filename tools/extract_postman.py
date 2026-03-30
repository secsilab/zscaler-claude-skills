#!/usr/bin/env python3
"""Extract API endpoints from Postman collection JSON to Markdown.

Usage:
    python3 extract_postman.py <collection.json> [--folder "Folder Name"]

    --folder: Extract only a specific top-level folder
    Without --folder: Extract entire collection.

Output: Markdown tables grouped by category, printed to stdout.
"""
import json
import sys


def parse_url(url_obj):
    """Extract clean URL path from Postman URL object."""
    if isinstance(url_obj, str):
        return url_obj.split("?")[0]
    parts = url_obj.get("path", [])
    if parts:
        path = "/" + "/".join(
            f"{{{{{p[1:]}}}}}" if p.startswith(":") else p
            for p in parts
        )
    else:
        path = url_obj.get("raw", "")
    return path.split("?")[0]


def extract_items(node):
    """Recursively extract request items from Postman folder tree."""
    results = []
    for item in node.get("item", []):
        if "request" in item:
            req = item["request"]
            method = req.get("method", "GET")
            path = parse_url(req.get("url", {}))
            results.append({"method": method, "path": path, "name": item.get("name", "")})
        if "item" in item:
            results.extend(extract_items(item))
    return results


def extract_tree(node):
    """Extract folder tree with endpoints at each level."""
    tree = []
    for item in node.get("item", []):
        if "item" in item:
            # Folder
            endpoints = []
            subfolders = []
            for sub in item.get("item", []):
                if "request" in sub and "item" not in sub:
                    req = sub["request"]
                    endpoints.append({
                        "method": req.get("method", "GET"),
                        "path": parse_url(req.get("url", {})),
                        "name": sub.get("name", ""),
                    })
                if "item" in sub:
                    sub_eps = extract_items(sub)
                    if sub_eps:
                        subfolders.append({"name": sub.get("name", ""), "endpoints": sub_eps})
                    elif "request" in sub:
                        req = sub["request"]
                        endpoints.append({
                            "method": req.get("method", "GET"),
                            "path": parse_url(req.get("url", {})),
                            "name": sub.get("name", ""),
                        })
            total = len(endpoints) + sum(len(sf["endpoints"]) for sf in subfolders)
            tree.append({
                "name": item.get("name", ""),
                "total": total,
                "endpoints": endpoints,
                "subfolders": subfolders,
            })
        elif "request" in item:
            req = item["request"]
            tree.append({
                "name": item.get("name", ""),
                "total": 1,
                "endpoints": [{
                    "method": req.get("method", "GET"),
                    "path": parse_url(req.get("url", {})),
                    "name": item.get("name", ""),
                }],
                "subfolders": [],
            })
    return tree


def print_table(endpoints):
    """Print an endpoint table."""
    if not endpoints:
        return
    print("| Method | Endpoint | Description |")
    print("|--------|----------|-------------|")
    for ep in endpoints:
        print(f"| {ep['method']} | `{ep['path']}` | {ep['name']} |")


def print_tree(tree):
    """Print the folder tree as markdown."""
    for folder in tree:
        name = folder["name"]
        total = folder["total"]
        endpoints = folder["endpoints"]
        subfolders = folder["subfolders"]

        if total == 0 and not endpoints:
            continue

        print(f"\n### {name} ({total} endpoints)\n")

        if endpoints and not subfolders:
            print_table(endpoints)
        elif endpoints:
            print(f"\n#### General\n")
            print_table(endpoints)

        for sf in subfolders:
            print(f"\n#### {sf['name']}\n")
            print_table(sf["endpoints"])


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_postman.py <collection.json> [--folder 'Name']")
        sys.exit(1)

    collection_path = sys.argv[1]
    target_folder = None
    if "--folder" in sys.argv:
        idx = sys.argv.index("--folder")
        target_folder = sys.argv[idx + 1]

    with open(collection_path) as f:
        collection = json.load(f)

    if target_folder:
        for item in collection.get("item", []):
            if item.get("name") == target_folder:
                tree = extract_tree(item)
                print_tree(tree)
                return
        print(f"Folder '{target_folder}' not found.", file=sys.stderr)
        # List available folders
        for item in collection.get("item", []):
            print(f"  - {item.get('name', '?')}", file=sys.stderr)
        sys.exit(1)
    else:
        tree = extract_tree(collection)
        print_tree(tree)


if __name__ == "__main__":
    main()
