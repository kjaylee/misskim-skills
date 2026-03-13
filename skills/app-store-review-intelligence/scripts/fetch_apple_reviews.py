#!/usr/bin/env python3
"""Fetch Apple App Store reviews via RSS feed and write a unified JSON corpus."""

import argparse
import json
import sys
import time
import urllib.request

RSS_URL = "https://itunes.apple.com/rss/customerreviews/id={app_id}/sortBy=mostRecent/page={page}/json"
MAX_PAGES = 10  # Apple RSS only exposes pages 1-10


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AppReviewIntelligence/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # page doesn't exist
        print(f"ERROR: HTTP {e.code} fetching {url}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: network failure: {e}", file=sys.stderr)
        sys.exit(2)


def parse_entry(entry, country):
    def text(key):
        v = entry.get(key, {})
        if isinstance(v, dict):
            return v.get("label", "")
        return str(v) if v else ""

    rating_str = text("im:rating")
    try:
        rating = int(rating_str)
    except ValueError:
        rating = 0

    version_str = text("im:version")
    author = entry.get("author", {})
    author_name = author.get("name", {}).get("label", "") if isinstance(author, dict) else ""
    entry_id = text("id")
    updated = text("updated")

    return {
        "id": entry_id,
        "rating": rating,
        "title": text("title"),
        "body": text("content"),
        "author": author_name,
        "date": updated[:10] if updated else "",
        "version": version_str,
        "country": country,
    }


def fetch_country(app_id, country, pages, min_rating, max_rating):
    reviews = []
    seen_ids = set()
    for page in range(1, min(pages, MAX_PAGES) + 1):
        url = RSS_URL.format(app_id=app_id, page=page)
        data = fetch_json(url)
        if data is None:
            break
        feed = data.get("feed", {})
        entries = feed.get("entry", [])
        # First entry on page 1 is the app metadata, not a review
        if page == 1 and entries and "im:rating" not in entries[0]:
            entries = entries[1:]
        if not entries:
            break
        for entry in entries:
            parsed = parse_entry(entry, country)
            if parsed["id"] and parsed["id"] in seen_ids:
                continue
            seen_ids.add(parsed["id"])
            if min_rating is not None and parsed["rating"] < min_rating:
                continue
            if max_rating is not None and parsed["rating"] > max_rating:
                continue
            reviews.append(parsed)
        if page < pages:
            time.sleep(0.3)  # polite delay
    return reviews


def main():
    parser = argparse.ArgumentParser(description="Fetch Apple App Store reviews")
    parser.add_argument("--app-id", required=True, help="Numeric App Store app ID")
    parser.add_argument("--countries", default="us", help="Comma-separated country codes (default: us)")
    parser.add_argument("--pages", type=int, default=1, help=f"Pages per country, max {MAX_PAGES} (default: 1)")
    parser.add_argument("--min-rating", type=int, choices=range(1, 6), metavar="1-5", help="Minimum star rating to include")
    parser.add_argument("--max-rating", type=int, choices=range(1, 6), metavar="1-5", help="Maximum star rating to include")
    parser.add_argument("--out", required=True, help="Output JSON file path")
    args = parser.parse_args()

    if args.pages > MAX_PAGES:
        print(f"WARNING: Apple RSS only exposes pages 1-{MAX_PAGES}; capping at {MAX_PAGES}", file=sys.stderr)
        args.pages = MAX_PAGES

    countries = [c.strip().lower() for c in args.countries.split(",") if c.strip()]
    all_reviews = []
    seen_ids = set()

    for country in countries:
        reviews = fetch_country(args.app_id, country, args.pages, args.min_rating, args.max_rating)
        for r in reviews:
            key = f"{r['id']}_{country}"
            if key not in seen_ids:
                seen_ids.add(key)
                all_reviews.append(r)

    corpus = {
        "meta": {
            "app_id": args.app_id,
            "countries": countries,
            "pages_requested": args.pages,
            "total_reviews": len(all_reviews),
            "limitations": [
                "Apple RSS feed exposes only the 10 most recent pages (~500 reviews) per country.",
                "Reviews may be missing if Apple rate-limits or removes them.",
                "Ratings distribution may not reflect all-time totals.",
            ],
        },
        "reviews": all_reviews,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(all_reviews)} reviews to {args.out}", file=sys.stderr)
    if len(all_reviews) < 10:
        print("WARNING: corpus has fewer than 10 reviews; analysis confidence will be low.", file=sys.stderr)


if __name__ == "__main__":
    main()
