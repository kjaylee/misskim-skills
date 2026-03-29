#!/usr/bin/env bash
# unity-to-itch.sh — Push Unity WebGL (or other) build to itch.io
# Usage: bash unity-to-itch.sh <build_dir> <user/game> [version] [channel]
# Example: bash unity-to-itch.sh ./Build/WebGL kjaylee/my-game 1.0.0 html5

set -euo pipefail

BUILD_DIR="${1:?Usage: unity-to-itch.sh <build_dir> <user/game> [version] [channel]}"
GAME="${2:?Usage: unity-to-itch.sh <build_dir> <user/game> [version] [channel]}"
VERSION="${3:-dev-$(date +%Y%m%d-%H%M)}"
CHANNEL="${4:-html5}"

BUTLER="${BUTLER_PATH:-butler}"

echo "🎮 Unity → itch.io Pipeline"
echo "   Build: $BUILD_DIR"
echo "   Game:  $GAME"
echo "   v$VERSION → $CHANNEL"
echo ""

# Verify butler
if ! command -v "$BUTLER" &>/dev/null; then
  echo "❌ butler not found. Install: brew install itchio/itchio/butler"
  exit 1
fi

# Validate build dir
if [ ! -d "$BUILD_DIR" ]; then
  echo "❌ Build directory not found: $BUILD_DIR"
  exit 1
fi

# For HTML5/WebGL: check for index.html
if [[ "$CHANNEL" == "html5" ]]; then
  if [ ! -f "$BUILD_DIR/index.html" ]; then
    echo "⚠️  No index.html in $BUILD_DIR — Unity WebGL builds may place it here:"
    find "$BUILD_DIR" -name "index.html" -maxdepth 3 2>/dev/null || echo "   Not found"
    echo "   Trying to push anyway..."
  fi
fi

# Validate
"$BUTLER" validate "$BUILD_DIR" 2>/dev/null || true

# Push
echo "🚀 Pushing $BUILD_DIR → $GAME:$CHANNEL..."
"$BUTLER" push "$BUILD_DIR" "$GAME:$CHANNEL" \
  --userversion "$VERSION" \
  --assume-yes \
  --ignore ".git*" \
  --ignore "*.pdb" \
  --ignore "*.map"

echo ""
echo "✅ Done! $GAME:$CHANNEL @ v$VERSION"
echo "   Play: https://$(echo "$GAME" | cut -d/ -f1).itch.io/$(echo "$GAME" | cut -d/ -f2)"
