#!/usr/bin/env bash
# status.sh — Check live build status for all channels of a game
# Usage: bash status.sh <user/game>
# Example: bash status.sh kjaylee/my-game

set -euo pipefail

GAME="${1:?Usage: status.sh <user/game>}"
BUTLER="${BUTLER_PATH:-butler}"

CHANNELS=("html5" "windows" "mac" "linux" "android" "universal")

echo "📊 itch.io Status: $GAME"
echo "───────────────────────────────────"

FOUND=0
for channel in "${CHANNELS[@]}"; do
  output=$("$BUTLER" status "$GAME:$channel" 2>&1) && rc=0 || rc=$?
  if echo "$output" | grep -q "Upload\|version\|Build"; then
    echo "🟢 $channel"
    echo "$output" | grep -E "version|size|Upload|Build" | sed 's/^/   /'
    FOUND=$((FOUND + 1))
  fi
done

if [ "$FOUND" -eq 0 ]; then
  echo "⚠️  No live builds found for $GAME"
  echo "   Push first: butler push ./dist/web $GAME:html5"
fi

echo ""
echo "🔗 https://$(echo "$GAME" | cut -d/ -f1).itch.io/$(echo "$GAME" | cut -d/ -f2)"
