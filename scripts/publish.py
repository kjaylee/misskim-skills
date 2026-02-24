#!/usr/bin/env python3
"""Regenerate cross-agent compatibility indexes from skills/*/SKILL.md.

Parses YAML frontmatter with regex-only logic (no external dependencies).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
AGENTS_FILE = ROOT / "agents" / "AGENTS.md"
MARKETPLACE_FILE = ROOT / ".claude-plugin" / "marketplace.json"
MCP_FILE = ROOT / ".mcp.json"
GEMINI_FILE = ROOT / "gemini-extension.json"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_frontmatter(skill_file: Path) -> tuple[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        raise ValueError("Missing YAML frontmatter (--- ... ---) at top of file")

    fm = fm_match.group(1)

    name_match = re.search(r"(?m)^name\s*:\s*(.+?)\s*$", fm)
    if not name_match:
        raise ValueError("Missing required frontmatter field: name")
    name = strip_yaml_scalar(name_match.group(1))

    desc_match = re.search(r"(?m)^description\s*:\s*(.*)$", fm)
    if not desc_match:
        raise ValueError("Missing required frontmatter field: description")

    raw_desc = desc_match.group(1).strip()
    if raw_desc in {"|", ">", "|-", ">-", "|+", ">+"}:
        rest = fm[desc_match.end() :]
        collected: list[str] = []
        for line in rest.splitlines():
            if line.startswith(" ") or line.startswith("\t"):
                collected.append(line[1:] if line.startswith(" ") else line.lstrip("\t"))
                continue
            if line.strip() == "":
                collected.append("")
                continue
            break
        description = "\n".join(collected).strip()
    else:
        description = strip_yaml_scalar(raw_desc)

    if not description:
        raise ValueError("Frontmatter description is empty")

    return name, normalize_spaces(description)


def to_human_description(agent_description: str) -> str:
    text = agent_description
    text = re.sub(r"(?i)\bTriggers? on\b.*$", "", text).strip(" .;")
    text = re.split(r"(?i)\bUse when\b", text, maxsplit=1)[0].strip(" .;")
    text = normalize_spaces(text)
    return text or agent_description


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"ERROR: skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_dirs = sorted([p for p in SKILLS_DIR.iterdir() if p.is_dir()])
    entries = []
    errors: list[str] = []

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"[{skill_dir.name}] Missing SKILL.md")
            continue

        try:
            name, agent_desc = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"[{skill_dir.name}] {exc}")
            continue

        if name != skill_dir.name:
            errors.append(
                f"[{skill_dir.name}] name mismatch: frontmatter name='{name}' must equal directory name='{skill_dir.name}'"
            )
            continue

        entries.append(
            {
                "name": name,
                "path": f"skills/{name}",
                "agent_description": agent_desc,
                "human_description": to_human_description(agent_desc),
            }
        )

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    AGENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    MARKETPLACE_FILE.parent.mkdir(parents=True, exist_ok=True)

    agent_lines = [
        "<skills>",
        'You have additional SKILLs documented in directories containing a "SKILL.md" file.',
        "These skills are:",
    ]
    for entry in entries:
        agent_lines.append(f' - {entry["name"]} -> "{entry["path"]}/SKILL.md"')
    agent_lines.extend(["", "<available_skills>"])
    for entry in entries:
        agent_lines.append(f'{entry["name"]}: `{entry["agent_description"]}`')
    agent_lines.extend(["</available_skills>", "</skills>", ""])
    AGENTS_FILE.write_text("\n".join(agent_lines), encoding="utf-8")

    marketplace_payload = {
        "skills": [
            {
                "name": entry["name"],
                "path": entry["path"],
                "description": entry["human_description"],
            }
            for entry in entries
        ]
    }
    MARKETPLACE_FILE.write_text(
        json.dumps(marketplace_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if not MCP_FILE.exists():
        MCP_FILE.write_text(json.dumps({"mcpServers": {}}, indent=2) + "\n", encoding="utf-8")

    gemini_payload = {
        "name": "misskim-skills",
        "version": "1.0.0",
        "skills": [
            {
                "name": entry["name"],
                "path": entry["path"],
                "description": entry["human_description"],
            }
            for entry in entries
        ],
    }
    GEMINI_FILE.write_text(
        json.dumps(gemini_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated {AGENTS_FILE.relative_to(ROOT)} ({len(entries)} skills)")
    print(f"Generated {MARKETPLACE_FILE.relative_to(ROOT)} ({len(entries)} skills)")
    print(f"Ensured {MCP_FILE.relative_to(ROOT)}")
    print(f"Generated {GEMINI_FILE.relative_to(ROOT)} ({len(entries)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
