#!/usr/bin/env bash
# release.sh — Push all channel builds to itch.io
# Usage: bash release.sh <user/game> <dist_dir> [version]
# Example: bash release.sh kjaylee/my-game ./dist 1.2.0

set -euo pipefail

GAME="${1:?Usage: release.sh <user/game> <dist_dir> [version]}"
DIST="${2:?Usage: release.sh <user/game> <dist_dir> [version]}"
VERSION="${3:-$(git describe --tags --abbrev=0 2>/dev/null || echo "dev-$(date +%Y%m%d-%H%M)")}"

BUTLER="${BUTLER_PATH:-butler}"

# Verify butler is available
if ! command -v "$BUTLER" &>/dev/null; then
  echo "❌ butler not found. Install: brew install itchio/itchio/butler"
  exit 1
fi

# Verify auth
if ! "$BUTLER" status "$GAME:html5" &>/dev/null 2>&1; then
  echo "⚠️  Butler not authenticated or game channel not yet created."
  echo "   Run: butler login"
  echo "   Then create game at: https://itch.io/game/new"
fi

echo "🚀 Releasing $GAME @ v$VERSION"
echo "   Source: $DIST"
echo ""

PUSHED=0

# Channel map: directory → itch.io channel name
declare -A CHANNELS=(
  ["web"]="html5"
  ["html5"]="html5"
  ["win"]="windows"
  ["windows"]="windows"
  ["mac"]="mac"
  ["macos"]="mac"
  ["linux"]="linux"
  ["android"]="android"
  ["universal"]="universal"
)

for dir_name in "${!CHANNELS[@]}"; do
  dir_path="$DIST/$dir_name"
  channel="${CHANNELS[$dir_name]}"
  
  if [ -d "$dir_path" ] || [ -f "$dir_path" ]; then
    echo "📦 Pushing $dir_name → $GAME:$channel (v$VERSION)..."
    "$BUTLER" push "$dir_path" "$GAME:$channel" \
      --userversion "$VERSION" \
      --assume-yes \
      --ignore ".git*" \
      --ignore "*.map" \
      --ignore "*.pdb"
    echo "   ✅ $channel pushed"
    PUSHED=$((PUSHED + 1))
  fi
done

if [ "$PUSHED" -eq 0 ]; then
  echo "⚠️  No build directories found in: $DIST"
  echo "   Expected subdirs: web/, html5/, win/, windows/, mac/, linux/, android/"
  exit 1
fi

echo ""
echo "✅ Released $PUSHED channel(s) for $GAME @ v$VERSION"
echo "   View: https://$(echo "$GAME" | cut -d/ -f1).itch.io/$(echo "$GAME" | cut -d/ -f2)"
