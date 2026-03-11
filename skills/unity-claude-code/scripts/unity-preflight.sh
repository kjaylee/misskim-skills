#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

if [ ! -d "$ROOT" ]; then
  echo "ERROR: repo root not found: $ROOT" >&2
  exit 1
fi

cd "$ROOT"

echo "[unity-preflight] root=$(pwd)"

has_assets=no
has_packages=no
has_projectsettings=no
[ -d Assets ] && has_assets=yes
[ -f Packages/manifest.json ] && has_packages=yes
[ -d ProjectSettings ] && has_projectsettings=yes

echo "assets=$has_assets"
echo "packages_manifest=$has_packages"
echo "projectsettings=$has_projectsettings"

if [ "$has_assets" = no ] || [ "$has_packages" = no ]; then
  echo "WARN: this does not look like a standard Unity repo" >&2
fi

scene_count=$(find Assets -type f -name '*.unity' 2>/dev/null | wc -l | tr -d ' ')
prefab_count=$(find Assets -type f -name '*.prefab' 2>/dev/null | wc -l | tr -d ' ')
asset_count=$(find Assets -type f -name '*.asset' 2>/dev/null | wc -l | tr -d ' ')
asmdef_count=$(find Assets Packages -type f -name '*.asmdef' 2>/dev/null | wc -l | tr -d ' ')
editor_dir_count=$(find Assets -type d -name Editor 2>/dev/null | wc -l | tr -d ' ')

echo "scenes=$scene_count"
echo "prefabs=$prefab_count"
echo "assets=$asset_count"
echo "asmdefs=$asmdef_count"
echo "editor_dirs=$editor_dir_count"

echo "top_level_scripts="
find Assets -type f -name '*.cs' 2>/dev/null | sed 's#^./##' | sort | head -20

echo "high_risk_files="
{
  find Packages -maxdepth 1 -type f -name 'manifest.json' 2>/dev/null
  find ProjectSettings -maxdepth 1 -type f 2>/dev/null | sort | head -10
} | sed 's#^./##'
