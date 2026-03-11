# Safe Editing Rules

## Protect asset integrity
- Never bulk-delete `.meta` files.
- Never rename folders with many serialized references unless the task explicitly requires it.
- Avoid formatting-only rewrites of scene/prefab YAML.

## Prefer code over YAML churn
When possible:
- add a component script instead of hand-editing many prefab fields
- expose serialized fields instead of renaming existing serialized members
- isolate new behavior behind one MonoBehaviour or ScriptableObject

## Be careful with
- `*.unity`
- `*.prefab`
- `*.asset`
- `*.mat`
- `ProjectSettings/*`
- `Packages/manifest.json`

## asmdef rules
Before moving or adding scripts:
- confirm the target assembly
- check test assemblies separately
- avoid introducing cyclic references

## Editor/runtime split
- `Assets/**/Editor/**` should stay editor-only
- runtime code should not depend on `UnityEditor`
- tooling scripts should not leak into player builds

## Minimum post-edit review
After edits, explicitly check:
- `.meta` file churn
- unexpected scene/prefab changes
- public API or serialized field renames
