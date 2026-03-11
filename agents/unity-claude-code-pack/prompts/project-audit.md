# Unity Project Audit Prompt

Audit this Unity project before implementation.

## Goals
- identify runtime/editor assembly layout
- identify risky scene/prefab/package areas
- find smallest safe edit surface for the requested work

## Deliver
- likely entry files
- asmdef boundaries
- scene/prefab risk areas
- required verification commands
- one recommended implementation path

## Guardrails
- no edits yet unless explicitly requested
- call out `.meta` churn risk
- call out serialized field rename risk
