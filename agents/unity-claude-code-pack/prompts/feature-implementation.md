# Unity Feature Implementation Prompt

Implement the requested Unity feature with the narrowest safe change set.

## Before coding
- run `bash scripts/unity-preflight.sh .`
- identify the target assembly and the scene/prefab impact
- list the exact files you expect to touch

## Guardrails
- preserve `.meta` files
- prefer C# over large YAML edits
- avoid package changes unless required
- report prefab/scene edits separately

## Verify
Use the repo's concrete checks when available. At minimum:
- inspect diff for `.meta`, `.unity`, `.prefab`, `.asset`
- verify no unrelated folders changed

## Output
- changed files
- why each file changed
- risks
- verification evidence
