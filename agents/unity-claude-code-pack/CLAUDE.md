# Unity Claude Code Pack

Use this pack when working inside a Unity repository with Claude Code.

## First move
Run:
```bash
bash scripts/unity-preflight.sh .
```

## Priorities
1. Preserve `.meta` files.
2. Prefer narrow C# edits over broad scene/prefab YAML churn.
3. Call out any change to `*.unity`, `*.prefab`, `*.asset`, `Packages/manifest.json`, or `ProjectSettings/*`.
4. Respect asmdef boundaries.
5. Report exact validation commands and changed files.

## Repo scan order
- `Assets/`
- `Packages/manifest.json`
- `Assets/**/*.asmdef` and `Packages/**/*.asmdef`
- `ProjectSettings/` only if needed

## Hard rules
- Do not mass-rename folders.
- Do not delete or regenerate `.meta` files casually.
- Do not do formatting-only rewrites of scene/prefab YAML.
- Do not upgrade packages unless the task explicitly requires it.

## Task modes
Choose one prompt from `prompts/` before major work:
- `prompts/project-audit.md`
- `prompts/feature-implementation.md`
- `prompts/bugfix.md`

## Report format
- Changed
- Risk
- Verify
- Next
