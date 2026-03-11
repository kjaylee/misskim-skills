#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not a git repository" >&2
  exit 1
fi

echo "[unity-change-summary] repo=$(pwd)"

echo "changed_files="
git diff --name-only -- . ':(exclude)Library' ':(exclude)Temp' ':(exclude)Logs' ':(exclude)obj'

echo "\nmeta_changes="
git diff --name-only -- '*.meta' || true

echo "\nscene_prefab_asset_changes="
git diff --name-only -- '*.unity' '*.prefab' '*.asset' '*.mat' || true

echo "\npackage_settings_changes="
git diff --name-only -- Packages/manifest.json ProjectSettings || true
