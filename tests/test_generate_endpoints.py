#!/usr/bin/env python3
"""Tests for generate_endpoints.py"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from generate_endpoints import (
    parse_url,
    extract_endpoints,
    format_endpoints_md,
    diff_endpoints,
    parse_existing_endpoints,
    apply_overrides,
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


def test_parse_existing_endpoints(tmp_path):
    content = """<!-- AUTO-GENERATED -->
# ZIA API Reference

### Users (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List Users |
| POST | `/users` | Create User |

### Roles (1 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/roles` | List Roles |
"""
    f = tmp_path / "ENDPOINTS.md"
    f.write_text(content)
    eps = parse_existing_endpoints(str(f))
    assert len(eps) == 3
    assert eps[0]["folder"] == "Users"
    assert eps[2]["folder"] == "Roles"


def test_parse_existing_endpoints_missing():
    eps = parse_existing_endpoints("/nonexistent/path.md")
    assert eps == []


def test_apply_overrides_path():
    endpoints = [
        {"method": "PUT", "path": "/v1/wrongPath", "name": "fixMe", "folder": "F"},
        {"method": "GET", "path": "/v1/keep", "name": "leaveAlone", "folder": "F"},
    ]
    overrides = [{"name": "fixMe", "path": "/v1/correctPath"}]
    apply_overrides(endpoints, overrides)
    assert endpoints[0]["path"] == "/v1/correctPath"
    assert endpoints[1]["path"] == "/v1/keep"


def test_apply_overrides_method():
    endpoints = [{"method": "GET", "path": "/v1/x", "name": "wrongMethod", "folder": "F"}]
    apply_overrides(endpoints, [{"name": "wrongMethod", "method": "POST"}])
    assert endpoints[0]["method"] == "POST"


def test_apply_overrides_empty():
    endpoints = [{"method": "GET", "path": "/v1/x", "name": "x", "folder": "F"}]
    apply_overrides(endpoints, [])
    assert endpoints[0]["path"] == "/v1/x"
    apply_overrides(endpoints, None)
    assert endpoints[0]["path"] == "/v1/x"


def test_apply_overrides_no_match():
    endpoints = [{"method": "GET", "path": "/v1/x", "name": "x", "folder": "F"}]
    apply_overrides(endpoints, [{"name": "doesNotExist", "path": "/v1/never"}])
    assert endpoints[0]["path"] == "/v1/x"


if __name__ == "__main__":
    import tempfile, pathlib
    failures = 0
    for name, func in sorted(globals().items()):
        if not name.startswith("test_"):
            continue
        try:
            import inspect
            sig = inspect.signature(func)
            if "tmp_path" in sig.parameters:
                with tempfile.TemporaryDirectory() as td:
                    func(pathlib.Path(td))
            else:
                func()
            print(f"PASS: {name}")
        except Exception as e:
            print(f"FAIL: {name} — {e}")
            failures += 1
    if failures:
        print(f"\n{failures} test(s) failed.")
        sys.exit(1)
    print("\nAll tests passed.")
