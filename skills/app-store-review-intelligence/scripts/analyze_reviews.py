#!/usr/bin/env python3
"""Deterministic App Store review analysis — no LLM required."""

import argparse
import collections
import json
import re
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Phrase dictionaries
# ---------------------------------------------------------------------------
COMPLAINT_PHRASES = [
    "crash", "crashes", "crashing", "freeze", "freezes", "frozen",
    "slow", "lag", "laggy", "battery drain", "battery", "bug", "bugs",
    "broken", "not working", "doesn't work", "error", "fix", "terrible",
    "awful", "horrible", "unusable", "waste", "disappointed", "frustrating",
]

PRAISE_PHRASES = [
    "love", "great", "excellent", "amazing", "fantastic", "wonderful",
    "best", "awesome", "perfect", "clean interface", "easy to use",
    "intuitive", "fast", "smooth", "reliable", "helpful", "beautiful",
]

FEATURE_REQUEST_SIGNALS = [
    r"\bplease add\b", r"\bwould love\b", r"\bwish it had\b", r"\bneeds?\b.*mode",
    r"\brequest\b", r"\bfeature request\b", r"\bwant\b.*feature",
    r"\badd\b.*support", r"\bsupport for\b", r"\bwould be great\b",
    r"\bmissing\b", r"\bno\b.*mode", r"\bneed[s]?\b.*feature",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(text):
    return text.lower()


def ngrams(words, n):
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]


def top_ngrams(texts, n=2, top_k=10):
    counter = collections.Counter()
    for text in texts:
        words = re.findall(r'\b[a-z]{3,}\b', normalize(text))
        counter.update(ngrams(words, n))
    return counter.most_common(top_k)


def phrase_hits(text, phrases):
    t = normalize(text)
    return [p for p in phrases if p in t]


def detect_feature_requests(text):
    t = normalize(text)
    hits = []
    for pattern in FEATURE_REQUEST_SIGNALS:
        m = re.search(pattern, t)
        if m:
            # Extract surrounding context (up to 60 chars)
            start = max(0, m.start() - 10)
            end = min(len(t), m.end() + 50)
            hits.append(t[start:end].strip())
    return hits


def load_corpus(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(2)

    # Support both formats: corpus with .reviews list, or Apple RSS fixture
    if "reviews" in data:
        return data["reviews"], data.get("meta", {})
    # Apple RSS format
    feed = data.get("feed", {})
    entries = feed.get("entry", [])
    if entries and "im:rating" not in entries[0]:
        entries = entries[1:]
    reviews = []
    for e in entries:
        def text(key):
            v = e.get(key, {})
            return v.get("label", "") if isinstance(v, dict) else str(v)
        try:
            rating = int(text("im:rating"))
        except ValueError:
            rating = 0
        author = e.get("author", {})
        author_name = author.get("name", {}).get("label", "") if isinstance(author, dict) else ""
        reviews.append({
            "id": text("id"),
            "rating": rating,
            "title": text("title"),
            "body": text("content"),
            "author": author_name,
            "date": text("updated")[:10],
            "version": text("im:version"),
        })
    return reviews, {}


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(reviews, competitor_data):
    n = len(reviews)
    low_confidence = n < 10

    # Rating distribution
    rating_dist = collections.Counter(r["rating"] for r in reviews)
    avg_rating = sum(r["rating"] for r in reviews) / n if n else 0

    # Complaint clusters
    complaint_counter = collections.Counter()
    for r in reviews:
        full = f"{r.get('title','')} {r.get('body','')}"
        for hit in phrase_hits(full, COMPLAINT_PHRASES):
            complaint_counter[hit] += 1

    # Praise clusters
    praise_counter = collections.Counter()
    for r in reviews:
        full = f"{r.get('title','')} {r.get('body','')}"
        for hit in phrase_hits(full, PRAISE_PHRASES):
            praise_counter[hit] += 1

    # Feature requests
    feature_requests = collections.Counter()
    for r in reviews:
        full = f"{r.get('title','')} {r.get('body','')}"
        for snippet in detect_feature_requests(full):
            feature_requests[snippet] += 1

    # Version regressions: compare avg rating by version
    version_ratings = collections.defaultdict(list)
    for r in reviews:
        v = r.get("version") or "unknown"
        if r["rating"] > 0:
            version_ratings[v].append(r["rating"])
    version_avg = {
        v: sum(rs)/len(rs) for v, rs in version_ratings.items() if rs
    }
    sorted_versions = sorted(version_avg.keys())
    regressions = []
    for i in range(1, len(sorted_versions)):
        prev, curr = sorted_versions[i-1], sorted_versions[i]
        delta = version_avg[curr] - version_avg[prev]
        if delta < -0.5:
            regressions.append({
                "from_version": prev, "to_version": curr,
                "avg_before": round(version_avg[prev], 2),
                "avg_after": round(version_avg[curr], 2),
                "delta": round(delta, 2),
            })

    # Verbatim copy: top 5 most common bigrams from 1-star reviews
    low_reviews = [r for r in reviews if r["rating"] <= 2]
    low_texts = [f"{r.get('title','')} {r.get('body','')}" for r in low_reviews]
    top_complaints_ngram = top_ngrams(low_texts, n=2, top_k=5)

    # Competitor whitespace analysis
    competitor_strengths = []
    competitor_gaps = []
    for comp_name, comp_reviews in competitor_data.items():
        comp_praise = collections.Counter()
        comp_complaints = collections.Counter()
        for r in comp_reviews:
            full = f"{r.get('title','')} {r.get('body','')}"
            for hit in phrase_hits(full, PRAISE_PHRASES):
                comp_praise[hit] += 1
            for hit in phrase_hits(full, COMPLAINT_PHRASES):
                comp_complaints[hit] += 1
        # Strengths: competitor praised for things our users complain about
        for phrase, count in comp_praise.most_common(5):
            if complaint_counter.get(phrase, 0) > 0:
                competitor_strengths.append({"competitor": comp_name, "phrase": phrase, "competitor_praise": count})
        # Gaps: competitor complained about things our users praise
        for phrase, count in comp_complaints.most_common(5):
            if praise_counter.get(phrase, 0) > 0:
                competitor_gaps.append({"competitor": comp_name, "phrase": phrase, "competitor_complaint": count})

    # Copy extraction: screenshot headlines and ASO phrases from top praise
    copy_candidates = []
    # From praise: top phrases as headline seeds
    for phrase, count in praise_counter.most_common(5):
        copy_candidates.append({"type": "headline", "phrase": phrase, "source": "praise", "frequency": count})
    # From high-rated reviews: extract short punchy quotes
    high_reviews = [r for r in reviews if r["rating"] >= 4]
    for r in high_reviews[:5]:
        title = r.get("title", "").strip()
        if title and len(title) <= 60:
            copy_candidates.append({"type": "quote", "phrase": title, "source": "review_title", "rating": r["rating"]})

    return {
        "corpus_summary": {
            "total_reviews": n,
            "average_rating": round(avg_rating, 2),
            "low_confidence": low_confidence,
            "rating_distribution": {str(k): v for k, v in sorted(rating_dist.items())},
        },
        "complaint_clusters": [{"phrase": p, "count": c} for p, c in complaint_counter.most_common(10)],
        "praise_clusters": [{"phrase": p, "count": c} for p, c in praise_counter.most_common(10)],
        "feature_requests": [{"snippet": s, "count": c} for s, c in feature_requests.most_common(10)],
        "copy_extraction": copy_candidates,
        "version_regressions": regressions,
        "top_complaint_bigrams": [{"bigram": b, "count": c} for b, c in top_complaints_ngram],
        "competitor_whitespace": {
            "competitor_strengths_vs_our_weaknesses": competitor_strengths,
            "competitor_gaps_vs_our_strengths": competitor_gaps,
        },
        "limitations": [
            "Analysis uses keyword matching, not semantic NLP; nuanced sentiment may be missed.",
            "Apple RSS caps at 10 pages (~500 reviews); long-tail sentiment not captured.",
            "Version regression requires reviews to carry version metadata.",
            "Competitor analysis is surface-level phrase overlap, not causal.",
        ] + (["LOW CONFIDENCE: fewer than 10 reviews in corpus."] if low_confidence else []),
    }


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_md(result, app_id):
    lines = []
    s = result["corpus_summary"]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines.append(f"# App Store Review Intelligence Report")
    lines.append(f"\n**App ID:** {app_id}  \n**Generated:** {ts}  \n**Total Reviews:** {s['total_reviews']}  \n**Average Rating:** {s['average_rating']} ★")

    if s["low_confidence"]:
        lines.append("\n> ⚠️ **LOW CONFIDENCE:** Corpus has fewer than 10 reviews. Results may not be statistically meaningful.")

    lines.append("\n## Corpus summary\n")
    for star, count in sorted(s["rating_distribution"].items()):
        bar = "█" * count
        lines.append(f"  {star}★ {bar} ({count})")

    lines.append("\n## Top complaint clusters\n")
    for item in result["complaint_clusters"]:
        lines.append(f"- `{item['phrase']}` — {item['count']} mentions")

    lines.append("\n## Top praise clusters\n")
    for item in result["praise_clusters"]:
        lines.append(f"- `{item['phrase']}` — {item['count']} mentions")

    lines.append("\n## Feature requests / missing expectations\n")
    if result["feature_requests"]:
        for item in result["feature_requests"]:
            lines.append(f"- \"{item['snippet']}\" ({item['count']}×)")
    else:
        lines.append("- None detected.")

    lines.append("\n## Version Regressions\n")
    if result["version_regressions"]:
        for reg in result["version_regressions"]:
            lines.append(f"- **{reg['from_version']} → {reg['to_version']}**: avg rating {reg['avg_before']} → {reg['avg_after']} (Δ {reg['delta']})")
    else:
        lines.append("- No significant regressions detected.")

    lines.append("\n## Copy Extraction\n")
    if result.get("copy_extraction"):
        for item in result["copy_extraction"]:
            if item["type"] == "headline":
                lines.append(f"- **Headline seed:** \"{item['phrase']}\" (from {item['source']}, {item['frequency']}×)")
            elif item["type"] == "quote":
                lines.append(f"- **User quote:** \"{item['phrase']}\" ({item['rating']}★)")
    else:
        lines.append("- No copy candidates extracted.")

    lines.append("\n## Top Complaint Phrases (Bigrams)\n")
    for item in result["top_complaint_bigrams"]:
        lines.append(f"- `{item['bigram']}` ({item['count']}×)")

    cw = result["competitor_whitespace"]
    lines.append("\n## Competitor Whitespace\n")
    lines.append("### Where competitors outperform us\n")
    if cw["competitor_strengths_vs_our_weaknesses"]:
        for item in cw["competitor_strengths_vs_our_weaknesses"]:
            lines.append(f"- **{item['competitor']}** praised for `{item['phrase']}` ({item['competitor_praise']}×) — we have complaints here")
    else:
        lines.append("- No clear competitor advantages found.")
    lines.append("\n### Where competitors lag behind us\n")
    if cw["competitor_gaps_vs_our_strengths"]:
        for item in cw["competitor_gaps_vs_our_strengths"]:
            lines.append(f"- **{item['competitor']}** complained about `{item['phrase']}` ({item['competitor_complaint']}×) — we excel here")
    else:
        lines.append("- No clear competitor gaps found.")

    lines.append("\n## Limitations\n")
    for lim in result["limitations"]:
        lines.append(f"- {lim}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Analyze App Store reviews (deterministic, no LLM)")
    parser.add_argument("--input", required=True, help="Primary corpus JSON file")
    parser.add_argument("--competitor", action="append", default=[], metavar="FILE",
                        help="Competitor corpus JSON file (repeatable)")
    parser.add_argument("--out-md", required=True, help="Output Markdown report path")
    parser.add_argument("--out-json", required=True, help="Output JSON analysis path")
    args = parser.parse_args()

    reviews, meta = load_corpus(args.input)
    app_id = meta.get("app_id", "unknown")

    competitor_data = {}
    for comp_path in args.competitor:
        comp_reviews, comp_meta = load_corpus(comp_path)
        name = comp_meta.get("app_name") or comp_path
        competitor_data[name] = comp_reviews

    result = analyze(reviews, competitor_data)

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    md = render_md(result, app_id)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Analysis complete: {result['corpus_summary']['total_reviews']} reviews processed.", file=sys.stderr)
    print(f"  MD  → {args.out_md}", file=sys.stderr)
    print(f"  JSON → {args.out_json}", file=sys.stderr)


if __name__ == "__main__":
    main()
