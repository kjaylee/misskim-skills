# Unity Bugfix Prompt

Fix the requested Unity bug with minimal collateral changes.

## Before coding
- run `bash scripts/unity-preflight.sh .`
- locate the failing assembly, scene, prefab, or system boundary
- identify whether the bug is code-only or serialized-data-coupled

## Guardrails
- do not rename serialized fields unless unavoidable
- do not broad-edit scenes/prefabs when a code fix can solve it
- call out any dependency on package or project settings changes

## Verify
- inspect diff for `.meta`, `.unity`, `.prefab`, `.asset`
- run any repo-native tests/build checks if available
- summarize regression risk

## Output
- root cause
- changed files
- risk
- verification evidence
