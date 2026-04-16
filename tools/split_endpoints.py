#!/usr/bin/env python3
"""
split_endpoints.py

For each of the 11 product skills:
  1. Reads SKILL.md
  2. Finds the line starting with "## API Reference" (any suffix after that)
  3. Finds the next "## " line after it (or end of file)
  4. Extracts everything between those two points into ENDPOINTS.md
  5. Replaces the extracted section in SKILL.md with a reference line

Usage:
    python3 tools/split_endpoints.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Repo root is one level up from tools/
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Skills to process and their display names
SKILLS = {
    "zscaler-zia":      "Zscaler Internet Access (ZIA)",
    "zscaler-zpa":      "Zscaler Private Access (ZPA)",
    "zscaler-ztb":      "Zero Trust Branch (ZTB)",
    "zscaler-zcbc":     "Zscaler Cloud & Branch Connector (ZCBC)",
    "zscaler-zcc":      "Zscaler Client Connector (ZCC)",
    "zscaler-zdx":      "Zscaler Digital Experience (ZDX)",
    "zscaler-zid":      "ZIdentity (ZID)",
    "zscaler-easm":     "External Attack Surface Management (EASM)",
    "zscaler-zwa":      "Zscaler Workflow Automation (ZWA)",
    "zscaler-aiguard":  "Zscaler AI Guard",
    "zscaler-zinsights": "Zscaler Insights (ZInsights)",
}

UPDATED_DATE = datetime.now().strftime("%Y-%m-%d")

REFERENCE_LINE = "\nFor full API endpoint reference, see ENDPOINTS.md in this skill directory.\n\n"


def split_skill(skill_dir: str, product_name: str) -> dict:
    """
    Split SKILL.md for one skill. Returns a result dict with:
      - skill: skill directory name
      - extracted_lines: number of lines extracted into ENDPOINTS.md
      - status: "ok" or "error"
      - message: details
    """
    skill_path = SKILLS_DIR / skill_dir
    skill_md = skill_path / "SKILL.md"
    endpoints_md = skill_path / "ENDPOINTS.md"

    if not skill_md.exists():
        return {"skill": skill_dir, "extracted_lines": 0, "status": "error",
                "message": f"SKILL.md not found at {skill_md}"}

    lines = skill_md.read_text(encoding="utf-8").splitlines(keepends=True)

    # Find the "## API Reference" line (any suffix allowed)
    api_ref_idx = None
    for i, line in enumerate(lines):
        if line.startswith("## API Reference"):
            api_ref_idx = i
            break

    if api_ref_idx is None:
        return {"skill": skill_dir, "extracted_lines": 0, "status": "error",
                "message": "Could not find '## API Reference' heading"}

    # Find the next "## " heading after the API Reference line
    next_section_idx = None
    for i in range(api_ref_idx + 1, len(lines)):
        if lines[i].startswith("## "):
            next_section_idx = i
            break

    # Extract the body lines (everything after the ## API Reference heading,
    # up to but not including the next ## heading, or end of file)
    if next_section_idx is not None:
        body_lines = lines[api_ref_idx + 1 : next_section_idx]
    else:
        body_lines = lines[api_ref_idx + 1 :]

    # Build ENDPOINTS.md content
    endpoints_header = (
        f"<!-- AUTO-GENERATED from Zscaler Postman collection. Do not edit manually. -->\n"
        f"<!-- Source: Extracted from SKILL.md | Updated: {UPDATED_DATE} -->\n"
        f"# {product_name} API Reference\n"
    )
    endpoints_content = endpoints_header + "".join(body_lines)

    # Write ENDPOINTS.md
    endpoints_md.write_text(endpoints_content, encoding="utf-8")

    # Build updated SKILL.md: replace the extracted section with a reference line
    if next_section_idx is not None:
        new_lines = (
            lines[:api_ref_idx]
            + [REFERENCE_LINE]
            + lines[next_section_idx:]
        )
    else:
        new_lines = lines[:api_ref_idx] + [REFERENCE_LINE]

    skill_md.write_text("".join(new_lines), encoding="utf-8")

    extracted_lines = len(body_lines)
    return {
        "skill": skill_dir,
        "extracted_lines": extracted_lines,
        "status": "ok",
        "message": f"Extracted {extracted_lines} lines into ENDPOINTS.md",
    }


def verify_results() -> list[str]:
    """
    Verification checks:
    - All 11 ENDPOINTS.md files exist and are non-empty
    - All 11 SKILL.md files have the reference line
    - No SKILL.md has '| Method | Endpoint |' tables left
    """
    issues = []
    for skill_dir in SKILLS:
        skill_path = SKILLS_DIR / skill_dir
        endpoints_md = skill_path / "ENDPOINTS.md"
        skill_md = skill_path / "SKILL.md"

        if not endpoints_md.exists():
            issues.append(f"{skill_dir}: ENDPOINTS.md missing")
        elif endpoints_md.stat().st_size == 0:
            issues.append(f"{skill_dir}: ENDPOINTS.md is empty")

        if not skill_md.exists():
            issues.append(f"{skill_dir}: SKILL.md missing after split")
        else:
            text = skill_md.read_text(encoding="utf-8")
            if "For full API endpoint reference, see ENDPOINTS.md" not in text:
                issues.append(f"{skill_dir}: reference line not found in SKILL.md")
            if "| Method | Endpoint |" in text:
                issues.append(f"{skill_dir}: SKILL.md still contains endpoint tables")

    return issues


def main():
    print(f"split_endpoints.py — splitting {len(SKILLS)} product skills\n")
    print(f"{'Skill':<25} {'Status':<8} {'Lines extracted'}")
    print("-" * 55)

    total_extracted = 0
    results = []

    for skill_dir, product_name in SKILLS.items():
        result = split_skill(skill_dir, product_name)
        results.append(result)
        status_icon = "OK" if result["status"] == "ok" else "ERROR"
        print(f"{skill_dir:<25} {status_icon:<8} {result['extracted_lines']:>6}  {result['message']}")
        if result["status"] == "ok":
            total_extracted += result["extracted_lines"]

    errors = [r for r in results if r["status"] == "error"]
    successes = [r for r in results if r["status"] == "ok"]

    print("\n" + "=" * 55)
    print(f"Skills split successfully : {len(successes)}/{len(SKILLS)}")
    print(f"Total lines extracted     : {total_extracted}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for r in errors:
            print(f"  {r['skill']}: {r['message']}")

    # Run verification
    print("\nRunning verification checks...")
    issues = verify_results()
    if issues:
        print(f"VERIFICATION FAILED — {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("All verification checks passed.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
