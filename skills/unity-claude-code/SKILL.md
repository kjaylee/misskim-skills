---
name: unity-claude-code
description: Prepare and execute Unity project work with Claude Code-style coding flows. Use when working on Unity repositories that need safe file discovery, `.meta` preservation, scene/prefab caution, asmdef-aware edits, validation checklists, or when handing Unity implementation tasks to Claude Code / ACP sessions.
---

# Unity Claude Code

Use this skill for Unity repositories where coding speed matters but asset integrity matters more.

## Workflow
1. Confirm the repo is actually a Unity project.
2. Run `scripts/unity-preflight.sh <repo-root>` before proposing edits.
3. Read only the needed reference file:
   - `references/project-discovery.md` for repo scan and change targeting
   - `references/safe-editing-rules.md` for Unity-specific guardrails
   - `references/claude-code-handoff.md` when preparing a Claude Code / ACP task
4. Keep edits scoped to the requested feature or bug.
5. Validate with concrete checks, not assumptions.

## Non-negotiables
- Preserve `.meta` files. Never mass-delete, regenerate, or rename them casually.
- Treat `*.unity`, `*.prefab`, `*.asset`, `*.mat`, and `ProjectSettings/*` as high-risk files.
- Prefer C# code changes over broad YAML edits when both can solve the task.
- Call out any scene/prefab edits explicitly in the report.
- If a task touches Addressables, asmdef boundaries, packages, or build settings, mention the impact area before implementation.

## Default execution pattern
### 1. Preflight
Run:
```bash
bash scripts/unity-preflight.sh /path/to/repo
```

### 2. Identify the narrowest safe target
Prioritize these folders in order:
- `Assets/**` for gameplay/runtime/editor code
- `Packages/manifest.json` for package dependencies
- `ProjectSettings/**` only when project configuration changes are required

### 3. Match the task type
- **Bugfix** → inspect stack path, assembly boundary, scene references, regression risk
- **Feature** → identify runtime entry points, serialized fields, authoring flow, validation path
- **Refactor** → map public APIs, scene bindings, serialized names, asmdef consumers
- **Review / Handoff** → create a Claude Code-ready task brief using `references/claude-code-handoff.md`

### 4. Verify concretely
Use whichever checks fit the repo:
- `bash -n` for helper scripts
- `node --check` / `node --test` for JS tooling around the Unity repo
- repo-specific build/test commands if available
- file diff inspection for `.meta` churn and scene/prefab YAML churn

## Reporting format
- **Changed**: exact files
- **Risk**: scene/prefab/meta/asmdef/package impact
- **Verify**: commands run and outcomes
- **Next**: one recommended follow-up

## Resources
- `references/project-discovery.md`
- `references/safe-editing-rules.md`
- `references/claude-code-handoff.md`
- `scripts/unity-preflight.sh`
