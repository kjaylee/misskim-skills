---
name: idea-factory-v2
description: Daily non-overlapping idea mining pipeline with first-class Red Team gating and artifact emission.
---

# Idea Factory v2

Use this pipeline when you need a scheduled batch of product ideas rather than a one-off brainstorm.

## Usage
```bash
python3 /Users/kjaylee/.openclaw/workspace/misskim-skills/skills/idea-factory-v2/scripts/idea_factory_v2.py --count 5 --output-root /Volumes/workspace/ideas --state-root /Users/kjaylee/.openclaw/workspace/.state/idea-factory-v2 --use-web-search
```

## Guarantees
- Red Team analysis is attached to every idea.
- Final batch enforces non-overlap across wedge / weakness / user job.
- Retry metadata is persisted in `state.json`.
- Repo creation is blocked unless the best idea clears threshold.
