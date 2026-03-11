# Project Discovery

## Goal
Find the smallest safe edit surface in a Unity repository before touching files.

## Check in this order
1. `Assets/` — scripts, prefabs, scenes, ScriptableObjects, editor tools
2. `Packages/manifest.json` — package dependencies
3. `Packages/*.asmdef` and `Assets/**/*.asmdef` — assembly boundaries
4. `ProjectSettings/` — only if the task truly requires project-level config changes

## Unity-specific scan questions
- Which scene or prefab instantiates this behavior?
- Does the code sit in a runtime assembly or an editor-only assembly?
- Are there serialized field names that must stay stable?
- Is there any `.meta` file coupled to a rename or move?
- Does the request really require scene YAML edits, or can the same outcome be achieved in C#?

## High-signal files
- `Assets/**/Scripts/**/*.cs`
- `Assets/**/*.asmdef`
- `Packages/manifest.json`
- `ProjectSettings/ProjectSettings.asset`
- `Assets/**/*.unity`
- `Assets/**/*.prefab`

## Report before large edits
If more than 8 files or any scene/prefab/package file will change, summarize:
- target area
- reason
- validation path
