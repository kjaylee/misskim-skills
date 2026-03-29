#!/usr/bin/env bash
# godot-to-itch.sh — Export Godot project and push HTML5 to itch.io
# Usage: bash godot-to-itch.sh <godot_project_dir> <user/game> [version] [channel]
# Example: bash godot-to-itch.sh ./MyGame kjaylee/my-game 1.0.0 html5

set -euo pipefail

PROJECT="${1:?Usage: godot-to-itch.sh <godot_project_dir> <user/game> [version] [channel]}"
GAME="${2:?Usage: godot-to-itch.sh <godot_project_dir> <user/game> [version] [channel]}"
VERSION="${3:-$(git -C "$PROJECT" describe --tags --abbrev=0 2>/dev/null || echo "dev-$(date +%Y%m%d-%H%M)")}"
CHANNEL="${4:-html5}"

BUTLER="${BUTLER_PATH:-butler}"
GODOT="${GODOT_PATH:-godot4}"
EXPORT_DIR="$(mktemp -d)/web"

echo "🎮 Godot → itch.io Pipeline"
echo "   Project: $PROJECT"
echo "   Game:    $GAME"
echo "   Version: $VERSION"
echo "   Channel: $CHANNEL"
echo ""

# 1. Verify tools
for cmd in "$GODOT" "$BUTLER"; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "❌ $cmd not found"
    exit 1
  fi
done

# 2. Ensure export output directory exists
mkdir -p "$EXPORT_DIR"

# 3. Export HTML5 from Godot
echo "📦 Exporting HTML5..."
"$GODOT" --headless --path "$PROJECT" \
  --export-release "Web" "$EXPORT_DIR/index.html"

# 4. Validate export
if [ ! -f "$EXPORT_DIR/index.html" ]; then
  echo "❌ Export failed — index.html not found in $EXPORT_DIR"
  echo "   Make sure you have a 'Web' export preset in export_presets.cfg"
  exit 1
fi

echo "   ✅ Export complete: $EXPORT_DIR"
echo ""

# 5. Push to itch.io
echo "🚀 Pushing to itch.io..."
"$BUTLER" push "$EXPORT_DIR" "$GAME:$CHANNEL" \
  --userversion "$VERSION" \
  --assume-yes

# 6. Clean up temp dir
rm -rf "$(dirname "$EXPORT_DIR")"

echo ""
echo "✅ Done! $GAME:$CHANNEL @ v$VERSION"
echo "   Play: https://$(echo "$GAME" | cut -d/ -f1).itch.io/$(echo "$GAME" | cut -d/ -f2)"
