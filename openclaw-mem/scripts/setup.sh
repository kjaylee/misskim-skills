#!/bin/bash
set -e
echo "📦 Installing openclaw-mem..."
pip3 install openclaw-mem
echo "🧠 Initializing workspace..."
openclaw-mem init
echo "✅ Done! Run 'openclaw-mem search \"query\"' to get started."
