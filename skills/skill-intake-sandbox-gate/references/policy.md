# Skill Intake Gate — Policy (v0)

## Goal
Minimize risk from third-party skills by enforcing: **least capability + deterministic behavior + explicit logging**.

## Decision rubric
- **ACCEPT (low)**: no process exec, no privileged ops, no persistence, network either absent or explicitly allowlisted.
- **QUARANTINE (medium)**: ambiguous behavior, broad dependencies, dynamic downloads, indirect execution paths.
- **REJECT / REWRITE (high/critical)**: any of:
  - arbitrary shell execution (`bash -c`, `curl|bash`, `eval`, `exec`)
  - filesystem destructive patterns (`rm -rf`, recursive deletes outside a temp dir)
  - privilege escalation (`sudo`, service install, firewall changes)
  - secret harvesting indicators (reading `.env`, `.npmrc`, keychain, cloud creds) without explicit user intent

## Allowlist guidance
Network:
- Allow only documented upstreams, per-domain, per-protocol.
- Prefer `web_fetch` style fetching (read-only) vs arbitrary requests.

Execution:
- Prefer pure functions / read-only transforms.
- If execution is necessary, require deterministic scripts with explicit inputs/outputs.

## Logging
Always record:
- source URL / commit hash
- gate report (JSON + MD)
- decision + rationale
- any rewrite diffs
