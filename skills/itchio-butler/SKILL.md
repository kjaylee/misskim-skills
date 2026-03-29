---
name: itchio-butler
description: Publish and manage game builds on itch.io using the butler CLI. Use when deploying HTML5 games, desktop builds, or Android APKs to itch.io — including first-time auth, channel push, multi-platform releases, and integration with Godot/Unity export pipelines. Triggers: "deploy to itch.io", "publish game", "push to itch", "butler push", "itch.io release", "update itch build".
metadata:
  openclaw:
    emoji: "🎮"
    requires:
      bins: ["butler"]
      os: ["darwin", "linux", "win32"]
version: 1.0.0
---

# itch.io Butler Skill

Deploy game builds to itch.io with `butler` — the official itch.io CLI for fast, delta-compressed uploads.

## Prerequisites

```bash
# Check butler is installed
butler version
# Expected: "head, built on ..."

# If not installed (macOS):
brew install itchio/itchio/butler

# Or download directly:
# https://itchio.itch.io/butler
```

Butler credentials are stored at:
`~/Library/Application Support/itch/butler_creds` (macOS)
`~/.config/itch/butler_creds` (Linux)

## Authentication

### First-time login
```bash
butler login
# Opens browser → log in to itch.io → token saved automatically
```

### Verify auth
```bash
butler status user/game:channel 2>/dev/null || echo "Not authenticated or game not pushed yet"
```

### Custom credential path
```bash
butler -i /path/to/butler_creds push ./build user/game:channel
```

## Core Command: Push a Build

```bash
# Syntax
butler push <build_dir_or_zip> <user>/<game>:<channel>

# HTML5 game (folder)
butler push ./dist/web   kjaylee/my-game:html5

# Windows build
butler push ./dist/win   kjaylee/my-game:windows

# macOS .app (zip first for delta efficiency)
butler push ./dist/mac   kjaylee/my-game:mac

# Linux
butler push ./dist/linux kjaylee/my-game:linux

# Android APK
butler push ./dist/android/game.apk kjaylee/my-game:android
```

### Version tagging
```bash
# Tag a specific version
butler push ./dist/web kjaylee/my-game:html5 --userversion 1.2.0

# Use git tag as version
butler push ./dist/web kjaylee/my-game:html5 --userversion $(git describe --tags --abbrev=0)
```

### Ignore patterns (skip large dev files)
```bash
butler push ./dist/web kjaylee/my-game:html5 \
  --ignore "*.pdb" \
  --ignore ".git*" \
  --ignore "*.map"
```

## Channel Status

```bash
# Check what's live on a channel
butler status kjaylee/my-game:html5

# Output includes: version, size, build ID, upload date
```

## Full Multi-Channel Release Workflow

Use the provided script for consistent multi-platform releases:

```bash
bash {baseDir}/scripts/release.sh kjaylee/my-game ./dist 1.2.0
```

This pushes all present channel directories with version tag and reports status.

## Godot Export → itch.io Pipeline

```bash
# 1. Export HTML5 from Godot (headless, on MiniPC)
godot4 --headless --path ./MyGame --export-release "Web" ../dist/web/index.html

# 2. Push to itch.io
butler push ./dist/web kjaylee/my-game:html5 --userversion 1.0.0

# Or use the combined script:
bash {baseDir}/scripts/godot-to-itch.sh ./MyGame kjaylee/my-game 1.0.0
```

## Unity Export → itch.io Pipeline

```bash
# 1. Unity WebGL build (assumed already exported)
# Build output: ./Build/WebGL/

# 2. Push WebGL build
butler push ./Build/WebGL kjaylee/my-game:html5 --userversion 1.0.0

# Or use combined script:
bash {baseDir}/scripts/unity-to-itch.sh ./Build/WebGL kjaylee/my-game 1.0.0
```

## Validate Before Push

```bash
# Check build structure (HTML5 must have index.html)
butler validate ./dist/web

# Diff against live (shows what changed without pushing)
butler diff kjaylee/my-game:html5 ./dist/web
```

## Common Channel Names

| Platform   | Channel Name | Notes |
|------------|-------------|-------|
| HTML5/Web  | `html5`     | Must have `index.html` at root |
| Windows    | `windows`   | .exe or folder with .exe |
| macOS      | `mac`       | .app bundle (zip for delta) |
| Linux      | `linux`     | ELF binary or AppImage |
| Android    | `android`   | .apk file |
| Universal  | `universal` | Cross-platform (Godot) |

## Error Handling

### Auth errors
```bash
# Re-authenticate
butler logout && butler login
```

### "Game not found"
- Create the game on itch.io first: https://itch.io/game/new
- Set the URL slug — that's what goes in `user/game`

### "No index.html found" for HTML5
- Butler requires `index.html` at the root of the web build dir
- Godot exports `index.html` by default ✓

### Large builds slow
- Butler does delta compression — subsequent pushes are fast
- First push uploads everything; subsequent pushes only diffs

### Network timeout
```bash
# Increase timeout
butler --context-timeout=60 push ./dist/web kjaylee/my-game:html5
```

## Automation Pattern (CI/CD)

```bash
#!/bin/bash
# In GitHub Actions or local CI

VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "dev-$(date +%Y%m%d)")
GAME="kjaylee/my-game"
DIST="./dist"

# Push HTML5
if [ -d "$DIST/web" ]; then
  butler push "$DIST/web" "$GAME:html5" --userversion "$VERSION" --assume-yes
fi

# Push Windows
if [ -d "$DIST/win" ]; then
  butler push "$DIST/win" "$GAME:windows" --userversion "$VERSION" --assume-yes
fi

echo "✅ Released $GAME v$VERSION"
```

## Integration with Jay's Distribution Pipeline

Jay's priority stack: Telegram Mini App → **itch.io** → Google Play/App Store → Steam

itch.io is the fast, zero-friction distribution channel. Use this skill after:
1. `godot` skill builds + exports the game
2. `game-qa` validates the build
3. This skill publishes to itch.io (and optionally tags a GitHub release)

Next steps after itch.io: feed the same HTML5 build into a Telegram Mini App (`openclaw-tg-canvas` skill).
