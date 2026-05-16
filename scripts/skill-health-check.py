#!/usr/bin/env python3
"""Lend.Ai - Ecosystem Health Check.

Validates consistency between AGENTS.md, skills/ folders, agent manifests,
and opencode.json. Exits 0 if all pass, 1 if any fail.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_MD = REPO_ROOT / "AGENTS.md"
SKILLS_DIR = REPO_ROOT / "skills"
MANIFESTS_DIR = REPO_ROOT / "agents" / "manifests"
OPENCODE_JSON = REPO_ROOT / "opencode.json"

N1_REQUIRED = {"lend-ai-engram", "commits-real", "lend-ai-testing", "lend-ai-docs"}

# Skills that live outside skills/ dir (e.g. profiles/)
NON_SKILL_DIR_EXCEPTIONS = {"lend-ai-workflow"}

errors = 0


def extract_skill_names_from_md(text: str) -> set[str]:
    """Extract backtick skill names from markdown table rows."""
    names: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            continue
        cell = parts[1]
        m = re.match(r"^`(.+?)`$", cell)
        if m:
            names.add(m.group(1))
    return names


def get_section(text: str, heading: str) -> str:
    """Get content of a markdown section given its heading (regex-escaped)."""
    lines = text.splitlines()
    start = -1
    for i, line in enumerate(lines):
        if re.match(r"^#{2,3}\s+" + heading + r"\s*$", line.strip()):
            start = i
            break
    if start == -1:
        return ""
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^#{2,3}\s+", lines[i].strip()):
            end = i
            break
    return "\n".join(lines[start:end])


def check_skill_bi_directional(agents_skills: set[str], disk_skills: set[str]):
    global errors
    pass_count = 0
    fail_count = 0
    orphan_skills: list[str] = []
    missing_skills: list[str] = []

    for folder in sorted(disk_skills):
        if folder in agents_skills:
            print(f"  [OK] skills/{folder}/SKILL.md -> referenced in AGENTS.md")
            pass_count += 1
        else:
            print(f"  [FAIL] skills/{folder}/SKILL.md -> NOT in AGENTS.md")
            orphan_skills.append(folder)
            fail_count += 1
            errors += 1

    for name in sorted(agents_skills):
        if name not in disk_skills:
            if name in NON_SKILL_DIR_EXCEPTIONS:
                print(f"  [OK] {name} listed in AGENTS.md -> external (profiles/)")
                pass_count += 1
            else:
                print(f"  [FAIL] {name} listed in AGENTS.md -> NO skill folder found")
                missing_skills.append(name)
                fail_count += 1
                errors += 1

    return pass_count, fail_count, orphan_skills, missing_skills


def check_manifests() -> tuple[int, int, list[str]]:
    global errors
    import yaml

    yaml_files = sorted(MANIFESTS_DIR.glob("*.yaml"))
    required_fields = ["agent.name", "agent.layer", "agent.description"]
    total = len(yaml_files)
    broken: list[str] = []

    for yf in yaml_files:
        try:
            with open(yf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"  [FAIL] {yf.relative_to(REPO_ROOT)} -> parse error: {e}")
            broken.append(yf.name)
            errors += 1
            continue

        missing: list[str] = []
        for field in required_fields:
            parts = field.split(".")
            val = data
            for p in parts:
                if isinstance(val, dict):
                    val = val.get(p)
                else:
                    val = None
                    break
            if val is None:
                missing.append(field)

        if missing:
            print(f"  [FAIL] {yf.relative_to(REPO_ROOT)} -> missing field(s): {', '.join(missing)}")
            broken.append(yf.name)
            errors += 1
        else:
            print(f"  [OK] {yf.relative_to(REPO_ROOT)} -> valid")

    return total, len(broken), broken


def check_opencode_json_agents(json_path: Path) -> tuple[int, int, list[str]]:
    global errors
    with open(json_path, encoding="utf-8") as f:
        config = json.load(f)

    agent_names = set(config.get("agent", {}).keys())
    yaml_names = {p.stem for p in MANIFESTS_DIR.glob("*.yaml")}
    unmatched: list[str] = []

    for name in sorted(agent_names):
        if name not in yaml_names:
            print(f"  [FAIL] opencode.json agent '{name}' -> no matching YAML manifest")
            unmatched.append(name)
            errors += 1

    return len(agent_names), len(unmatched), unmatched


def check_n1_skills(text: str):
    global errors
    heading = r"N1 \u2014 Skills de Sistema \(SIEMPRE ACTIVAS en el chat principal\)"
    n1_section = get_section(text, heading)
    n1_skills = extract_skill_names_from_md(n1_section)

    print("\n=== N1 CROSS-REFERENCE CHECK ===")
    for skill in sorted(N1_REQUIRED):
        if skill in n1_skills:
            print(f"  [OK] {skill} -> listed in N1 table")
        else:
            print(f"  [FAIL] {skill} -> MISSING from N1 table")
            errors += 1


def main():
    global errors
    agents_md_text = AGENTS_MD.read_text(encoding="utf-8")

    skills_section = get_section(agents_md_text, r"Skills")
    skills_table = extract_skill_names_from_md(skills_section)

    sdd_section = get_section(agents_md_text, r"Skills SDD \(Spec-Driven Development\)")
    sdd_table = extract_skill_names_from_md(sdd_section)

    trans_section = get_section(agents_md_text, r"Skills Transversales \(PRs, Issues, Docs\)")
    trans_table = extract_skill_names_from_md(trans_section)

    all_agents_skills = skills_table | sdd_table | trans_table

    disk_skills_raw = set()
    for sk_dir in SKILLS_DIR.iterdir():
        if sk_dir.name.startswith("_"):
            continue
        if sk_dir.is_dir() and (sk_dir / "SKILL.md").exists():
            disk_skills_raw.add(sk_dir.name)
    total_disk = len(disk_skills_raw)

    print("=== SKILL HEALTH CHECK ===")
    pass_b, fail_b, orphans, missing = check_skill_bi_directional(
        all_agents_skills, disk_skills_raw
    )

    print("\n=== MANIFEST CHECK ===")
    total_manifests, broken_manifests, broken_list = check_manifests()

    print("\n=== OPENCODE.JSON AGENT CROSS-REFERENCE ===")
    total_json_agents, unmatched_json, unmatched_list = check_opencode_json_agents(OPENCODE_JSON)

    check_n1_skills(agents_md_text)

    status = "[PASS]" if errors == 0 else "[FAIL]"

    print("\n=== SUMMARY ===")
    print(
        f"Skills: {total_disk} total, {len(missing)} missing from disk, "
        f"{len(orphans)} orphans (no AGENTS.md entry)"
    )
    print(f"Manifests: {total_manifests} total, {broken_manifests} broken")
    print(
        f"opencode.json agents: {total_json_agents} total, {unmatched_json} missing YAML manifests"
    )
    print(f"Status: {status}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
