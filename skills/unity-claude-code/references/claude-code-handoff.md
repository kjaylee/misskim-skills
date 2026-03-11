# Claude Code Handoff

Use this structure when handing a Unity task to Claude Code / ACP.

## Handoff template
```markdown
## Task
[one concrete requested outcome]

## Repo root
[path]

## Unity signals
- Assets/: [yes/no]
- Packages/manifest.json: [yes/no]
- ProjectSettings/: [yes/no]
- asmdef files involved: [list]

## Allowed changes
- [exact files or directories]

## Avoid
- bulk `.meta` churn
- unrelated scene/prefab rewrites
- package upgrades unless required

## Validation
- [exact commands]
- inspect diff for `.meta`, `.unity`, `.prefab`, `.asset`

## Report back
- changed files
- risks
- verification evidence
```

## Good Unity task shapes
- "Fix input routing in `Assets/Scripts/UI/InventoryPanel.cs` without touching unrelated prefabs."
- "Add a cooldown bar to the combat HUD and report any prefab edits separately."
- "Refactor save-system code across these 3 files only; preserve serialized names."

## Bad task shapes
- "Clean up the whole Unity project"
- "Refactor scenes if needed"
- "Upgrade packages if it helps"
