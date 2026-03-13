# app-store-review-intelligence

Fetch and analyze Apple App Store reviews deterministically — no LLM, no external dependencies, Python 3 stdlib only.

## Quick Start

```bash
# 1. Resolve app ID from URL, name, or direct ID
python3 scripts/resolve_app.py --url 'https://apps.apple.com/us/app/google/id284815942' --country us
python3 scripts/resolve_app.py --query 'Google Search' --country us
python3 scripts/resolve_app.py --id 284815942 --country us

# 2. Fetch reviews (1-10 pages per country, deduped)
python3 scripts/fetch_apple_reviews.py \
  --app-id 284815942 \
  --countries us,gb,ca \
  --pages 3 \
  --out /tmp/corpus.json

# Filter by rating
python3 scripts/fetch_apple_reviews.py --app-id 284815942 --min-rating 1 --max-rating 2 --out /tmp/low-corpus.json

# 3. Analyze (with optional competitor files)
python3 scripts/analyze_reviews.py \
  --input /tmp/corpus.json \
  --competitor tests/fixtures/competitor-a.json \
  --competitor tests/fixtures/competitor-b.json \
  --out-md /tmp/report.md \
  --out-json /tmp/report.json
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/resolve_app.py` | Resolve app to numeric ID via URL / ID / search query |
| `scripts/fetch_apple_reviews.py` | Fetch reviews from Apple RSS (up to 10 pages/country) |
| `scripts/analyze_reviews.py` | Deterministic analysis: complaints, praise, feature requests, version regressions, competitor whitespace |

## Output Sections (analyze_reviews.py)

- **Rating Distribution** — star counts and averages
- **Top Complaints** — keyword-matched complaint phrases ranked by frequency
- **Top Praise** — keyword-matched praise phrases ranked by frequency
- **Feature Requests** — pattern-detected user asks
- **Version Regressions** — versions where avg rating dropped > 0.5 stars
- **Top Complaint Bigrams** — verbatim two-word phrases from low-rated reviews
- **Competitor Whitespace** — where competitors outperform or lag vs. this app
- **Limitations** — explicit caveats on data coverage and method

## Known Limitations

- Apple RSS exposes only the **10 most recent pages** (~500 reviews) per country/app.
- Analysis is **keyword-based**, not semantic; sarcasm and nuance are missed.
- Fewer than 10 reviews triggers a **LOW CONFIDENCE** warning.
- Version regression detection requires reviews to include `im:version` metadata.
- Network failures exit with code 2; partial results are not written.

## Dependencies

- Python 3.6+
- No pip packages — stdlib only (`urllib`, `json`, `collections`, `re`, `argparse`, `unittest`)

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Corpus Format

Both `fetch_apple_reviews.py` output and the Apple RSS fixture are accepted by `analyze_reviews.py`.

```json
{
  "meta": { "app_id": "...", "total_reviews": 50 },
  "reviews": [
    { "id": "...", "rating": 4, "title": "...", "body": "...",
      "author": "...", "date": "YYYY-MM-DD", "version": "...", "country": "us" }
  ]
}
```

See `references/output-template.md` for the full report format.
