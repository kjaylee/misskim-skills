---
name: skill-intake-sandbox-gate
description: Intake gate for external AgentSkills/MCP tools. Use when reviewing, importing, or rewriting third-party skills (ClawHub/MCP Market/GitHub) into misskim-skills. Produces a risk report (exec/network/fs/secrets/persistence), recommends accept/quarantine/rewrite, and standardizes logging into INTAKE_LOG.
---

# Skill Intake Sandbox Gate

Use this workflow to **safely intake** any third-party skill/tool package before it touches production automation.

## Workflow (default)

### 0) Collect source
- Prefer **source tree** (git repo / skill folder) over “install and run”.
- Put the candidate under a temp path (do not run it yet).

### 1) Run the gate (static scan)
From the skill folder:

```bash
python3 scripts/gate.py --path <skill-folder> --out /tmp/skill-gate-report.json --md /tmp/skill-gate-report.md
```

Interpretation:
- `risk_level=low`: likely safe to rewrite/import
- `risk_level=medium`: quarantine + manual audit + limited-scope rewrite
- `risk_level=high/critical`: reject or rewrite from scratch (no execution)

### 2) Decide
Use the report to choose one:
- **ACCEPT**: Only if low risk + clear value + minimal capabilities.
- **QUARANTINE**: Keep for reference, do not execute in automation.
- **REWRITE (preferred)**: Rebuild the skill internally with minimal permissions and deterministic scripts.

### 3) Rewrite pattern (recommended)
- Create a new internal skill folder under `misskim-skills/skills/<name>/`.
- Copy only:
  - essential procedural instructions
  - deterministic scripts (no hidden downloads)
  - explicit allowlisted network endpoints (if any)
- Remove:
  - auto-updaters, telemetry, “curl | bash”, arbitrary shell execution
  - credential handling or implicit secret reads

### 4) Log the intake
Append the decision + rationale to the intake log files:
- `misskim-skills/INTAKE_LOG.md`
- `misskim-skills/intake-log.md`
- `misskim-skills/intake-log/<date>-*-trend-raw.json` (if applicable)

## What the gate checks (summary)
- **Process execution**: `subprocess/child_process/os.system/exec/spawn`, shell pipelines
- **Network**: `requests/httpx/aiohttp/fetch/axios/socket`, hardcoded domains
- **File write/destructive ops**: `rm -rf`, recursive deletes, chmod/chown, persistence
- **Privilege**: `sudo`, system service edits, launchd/systemd, firewall rules
- **Secrets indicators**: env/key file reads, token patterns, `.npmrc`, `.env`

## Resources
- `scripts/gate.py`: static scanner + JSON/MD report generator
- `references/policy.md`: allow/deny rules + decision rubric
- `references/threat-model.md`: threat model for skill intake
