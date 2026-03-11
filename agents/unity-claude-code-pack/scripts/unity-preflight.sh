#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

echo "[unity-preflight] root=$(pwd)"
[ -d Assets ] && echo "assets=yes" || echo "assets=no"
[ -f Packages/manifest.json ] && echo "packages_manifest=yes" || echo "packages_manifest=no"
[ -d ProjectSettings ] && echo "projectsettings=yes" || echo "projectsettings=no"

echo "asmdefs=$(find Assets Packages -type f -name '*.asmdef' 2>/dev/null | wc -l | tr -d ' ')"
echo "scenes=$(find Assets -type f -name '*.unity' 2>/dev/null | wc -l | tr -d ' ')"
echo "prefabs=$(find Assets -type f -name '*.prefab' 2>/dev/null | wc -l | tr -d ' ')"

echo "sample_scripts="
find Assets -type f -name '*.cs' 2>/dev/null | sed 's#^./##' | sort | head -20
