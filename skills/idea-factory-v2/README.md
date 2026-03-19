# idea-factory-v2

Cron-friendly idea mining pipeline for Miss Kim's Idea Factory doctrine.

## What it does
- mines local trend/archive sources
- optionally enriches with fallback web search
- generates a daily batch of app ideas
- applies first-class Red Team rejection analysis per idea
- suppresses near-duplicate ideas across wedge / weakness / user-job axes
- writes markdown + JSON artifacts to `/Volumes/workspace/ideas`
- can create a private GitHub repo from `kjaylee/idea-factory-template` for a passing idea

## CLI
```bash
python3 skills/idea-factory-v2/scripts/idea_factory_v2.py \
  --count 5 \
  --output-root /Volumes/workspace/ideas \
  --state-root /Users/kjaylee/.openclaw/workspace/.state/idea-factory-v2 \
  --use-web-search
```

Repo creation test:
```bash
python3 skills/idea-factory-v2/scripts/idea_factory_v2.py \
  --count 5 \
  --output-root /Volumes/workspace/ideas \
  --state-root /Users/kjaylee/.openclaw/workspace/.state/idea-factory-v2 \
  --use-web-search \
  --create-repo \
  --repo-threshold 80
```

## Overlap-prevention rule
Drop the lower-scoring idea if:
- it shares at least 2 of 3 axes (`wedge_class`, `weakness_class`, `job_class`), or
- keyword Jaccard similarity is >= 0.55, or
- it shares at least 1 axis and keyword Jaccard is >= 0.42.
