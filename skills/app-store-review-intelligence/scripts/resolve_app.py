#!/usr/bin/env python3
"""Resolve an App Store app to its numeric ID via URL, direct ID, or search query."""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

LOOKUP_URL = "https://itunes.apple.com/lookup"
SEARCH_URL = "https://itunes.apple.com/search"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AppReviewIntelligence/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except Exception as e:
        print(f"ERROR: network request failed: {e}", file=sys.stderr)
        sys.exit(2)


def resolve_from_url(app_url, country):
    # Extract numeric ID from URL like /id284815942
    m = re.search(r'/id(\d+)', app_url)
    if m:
        return resolve_from_id(m.group(1), country)
    print("ERROR: could not parse app ID from URL", file=sys.stderr)
    sys.exit(1)


def resolve_from_id(app_id, country):
    params = urllib.parse.urlencode({"id": app_id, "country": country})
    data = fetch_json(f"{LOOKUP_URL}?{params}")
    results = data.get("results", [])
    if not results:
        print(f"ERROR: no app found for id={app_id}", file=sys.stderr)
        sys.exit(1)
    return results[0]


def resolve_from_query(query, country):
    params = urllib.parse.urlencode({"term": query, "country": country, "entity": "software", "limit": 5})
    data = fetch_json(f"{SEARCH_URL}?{params}")
    results = data.get("results", [])
    if not results:
        print(f"ERROR: no results for query={query!r}", file=sys.stderr)
        sys.exit(1)
    return results[0]


def main():
    parser = argparse.ArgumentParser(description="Resolve App Store app to numeric ID")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="App Store URL (e.g. https://apps.apple.com/us/app/name/id123)")
    group.add_argument("--id", dest="app_id", help="Numeric app ID")
    group.add_argument("--query", help="Search query string")
    parser.add_argument("--country", default="us", help="Two-letter country code (default: us)")
    args = parser.parse_args()

    if args.url:
        result = resolve_from_url(args.url, args.country)
    elif args.app_id:
        result = resolve_from_id(args.app_id, args.country)
    else:
        result = resolve_from_query(args.query, args.country)

    out = {
        "app_id": result.get("trackId"),
        "name": result.get("trackName"),
        "bundle_id": result.get("bundleId"),
        "developer": result.get("artistName"),
        "country": args.country,
        "store_url": result.get("trackViewUrl"),
        "version": result.get("version"),
        "rating": result.get("averageUserRating"),
        "rating_count": result.get("userRatingCount"),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
