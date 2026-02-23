#!/usr/bin/env python3
"""skill-intake-sandbox-gate: static scanner

Purpose:
- Scan a candidate skill/tool directory without executing it.
- Detect risky patterns (exec/network/fs/persistence/secrets).
- Output JSON report (+ optional Markdown summary).

This is intentionally dependency-free.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "target",
    ".venv",
    "venv",
    "__pycache__",
}

TEXT_EXTS = {
    ".md",
    ".txt",
    ".py",
    ".js",
    ".ts",
    ".sh",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}


@dataclasses.dataclass
class Match:
    file: str
    line: int
    category: str
    pattern: str
    snippet: str


PATTERNS: Dict[str, List[re.Pattern]] = {
    "proc_exec": [
        re.compile(r"\bsubprocess\b"),
        re.compile(r"\bos\.system\b"),
        re.compile(r"\bPopen\b"),
        re.compile(r"\bexecSync\b"),
        re.compile(r"\bspawn\b"),
        re.compile(r"\bchild_process\b"),
        re.compile(r"\beval\s*\("),
        re.compile(r"\bexec\s*\("),
        re.compile(r"\bbash\s+-c\b"),
        re.compile(r"\bsh\s+-c\b"),
    ],
    "network": [
        re.compile(r"\brequests\b"),
        re.compile(r"\bhttpx\b"),
        re.compile(r"\baiohttp\b"),
        re.compile(r"\burllib\b"),
        re.compile(r"\bsocket\b"),
        re.compile(r"\bfetch\s*\("),
        re.compile(r"\baxios\b"),
        re.compile(r"https?://"),
        re.compile(r"\bws://|\bwss://"),
    ],
    "fs_write": [
        re.compile(r"\bwriteFile\b"),
        re.compile(r"\bappendFile\b"),
        re.compile(r"\bfs\.rm\b"),
        re.compile(r"\bfs\.rmdir\b"),
        re.compile(r"\bos\.remove\b"),
        re.compile(r"\bshutil\.rmtree\b"),
        re.compile(r"rm\s+-rf\b"),
        re.compile(r"\bchmod\b"),
        re.compile(r"\bchown\b"),
    ],
    "privilege": [
        re.compile(r"\bsudo\b"),
        re.compile(r"\blaunchctl\b"),
        re.compile(r"\bsystemctl\b"),
        re.compile(r"\bcrontab\b"),
        re.compile(r"\biptables\b"),
        re.compile(r"\bufw\b"),
    ],
    "secrets": [
        re.compile(r"\.env\b"),
        re.compile(r"\.npmrc\b"),
        re.compile(r"AWS_SECRET_ACCESS_KEY"),
        re.compile(r"OPENAI_API_KEY"),
        re.compile(r"ANTHROPIC_API_KEY"),
        re.compile(r"PRIVATE_KEY"),
        re.compile(r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"),
        re.compile(r"_authToken"),
    ],
    "persistence": [
        re.compile(r"launchd\b"),
        re.compile(r"plist\b"),
        re.compile(r"systemd\b"),
        re.compile(r"~/\.config"),
        re.compile(r"/etc/"),
    ],
}

RISK_WEIGHTS = {
    "proc_exec": 5,
    "privilege": 5,
    "persistence": 4,
    "network": 3,
    "secrets": 4,
    "fs_write": 3,
}


def is_text_file(p: Path) -> bool:
    return p.suffix.lower() in TEXT_EXTS


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_file(path: Path, root: Path) -> List[Match]:
    rel = str(path.relative_to(root))
    matches: List[Match] = []

    # Reduce false-positives from documentation.
    # Markdown often *mentions* risky terms (subprocess, rm -rf) without executing them.
    # For markdown, we only record outbound URLs as an informational signal.
    is_markdown = path.suffix.lower() == ".md"
    md_url_patterns = [re.compile(r"https?://"), re.compile(r"\bws://|\bwss://")]

    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return matches

    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        if is_markdown:
            for pat in md_url_patterns:
                if pat.search(line):
                    matches.append(
                        Match(
                            file=rel,
                            line=idx,
                            category="doc_url",
                            pattern=pat.pattern,
                            snippet=line.strip()[:400],
                        )
                    )
            continue

        for category, patterns in PATTERNS.items():
            for pat in patterns:
                if pat.search(line):
                    stripped = line.strip()
                    # Reduce false positives from comments/documentation inside code.
                    if stripped.startswith("#") or stripped.startswith("//"):
                        if category != "network":
                            continue

                    # Reduce false positives from scanners/linters that merely *mention* risky terms.
                    # If the line is defining regex patterns (re.compile), it's usually not executing the behavior.
                    if "re.compile" in line and category != "network":
                        continue
                    snippet = stripped[:400]
                    matches.append(
                        Match(
                            file=rel,
                            line=idx,
                            category=category,
                            pattern=pat.pattern,
                            snippet=snippet,
                        )
                    )
    return matches


def compute_risk(matches: List[Match]) -> Tuple[int, str]:
    # basic score: unique category hits weighted + small per-hit bonus
    # NOTE: doc_url is informational only and does not affect risk.
    cats = {}
    for m in matches:
        if m.category == "doc_url":
            continue
        cats[m.category] = cats.get(m.category, 0) + 1

    score = 0
    for cat, count in cats.items():
        score += RISK_WEIGHTS.get(cat, 1)
        score += min(10, count)  # cap runaway

    if score >= 35:
        level = "critical"
    elif score >= 22:
        level = "high"
    elif score >= 10:
        level = "medium"
    else:
        level = "low"

    return score, level


def recommend(level: str) -> str:
    if level in ("critical", "high"):
        return "reject_or_rewrite"
    if level == "medium":
        return "quarantine_then_rewrite"
    return "accept_or_rewrite"


def walk_files(root: Path) -> List[Path]:
    paths: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored dirs
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            paths.append(p)
    return paths


def render_md(report: dict) -> str:
    lines = []
    lines.append(f"# Skill Intake Gate Report")
    lines.append("")
    lines.append(f"- Path: `{report['path']}`")
    lines.append(f"- Risk: **{report['risk_level']}** (score={report['risk_score']})")
    lines.append(f"- Recommendation: `{report['recommendation']}`")
    lines.append("")

    by_cat = report.get("matches_by_category", {})
    if by_cat:
        lines.append("## Matches by category")
        for cat, count in sorted(by_cat.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {cat}: {count}")
        lines.append("")

    matches = report.get("matches", [])
    if matches:
        lines.append("## Top findings")
        for m in matches[:50]:
            lines.append(f"- `{m['file']}:{m['line']}` [{m['category']}] `{m['snippet']}`")
        if len(matches) > 50:
            lines.append(f"- ... ({len(matches)-50} more)")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="Candidate skill/tool directory")
    ap.add_argument("--out", required=True, help="Output JSON path")
    ap.add_argument("--md", default=None, help="Optional markdown output path")
    args = ap.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    matches: List[Match] = []
    files = walk_files(root)

    file_hashes = {}
    for p in files:
        if p.is_file() and is_text_file(p):
            matches.extend(scan_file(p, root))
        # hash small files only (avoid huge blobs)
        try:
            if p.is_file() and p.stat().st_size <= 2_000_000:
                file_hashes[str(p.relative_to(root))] = sha256_file(p)
        except Exception:
            pass

    risk_score, risk_level = compute_risk(matches)
    by_cat = {}
    for m in matches:
        by_cat[m.category] = by_cat.get(m.category, 0) + 1

    report = {
        "path": str(root),
        "file_count": len([p for p in files if p.is_file()]),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommend(risk_level),
        "matches_by_category": by_cat,
        "matches": [dataclasses.asdict(m) for m in matches],
        "file_sha256": file_hashes,
    }

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True))

    if args.md:
        md_path = Path(args.md).expanduser().resolve()
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_md(report))

    print(f"wrote: {out_path}")
    if args.md:
        print(f"wrote: {Path(args.md).expanduser().resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
