#!/usr/bin/env python3
"""Unit tests for the app-store-review-intelligence pipeline."""

import json
import os
import sys
import tempfile
import unittest

# Make scripts importable
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPTS_DIR))

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fixture_path(name):
    return os.path.join(FIXTURES_DIR, name)


def load_fixture(name):
    with open(fixture_path(name), encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Fixture validation tests
# ---------------------------------------------------------------------------

class TestAppleFixture(unittest.TestCase):
    def setUp(self):
        self.data = load_fixture("apple-reviews-284815942-us-p1.json")

    def test_fixture_has_feed(self):
        self.assertIn("feed", self.data)

    def test_feed_has_entries(self):
        entries = self.data["feed"].get("entry", [])
        self.assertGreater(len(entries), 0, "Fixture must contain at least one entry")

    def test_entries_have_rating(self):
        entries = self.data["feed"].get("entry", [])
        # Skip first entry if it's app metadata (no im:rating)
        review_entries = [e for e in entries if "im:rating" in e]
        self.assertGreater(len(review_entries), 0, "Must have review entries with im:rating")
        for entry in review_entries[:5]:
            rating_label = entry["im:rating"].get("label", "")
            self.assertRegex(rating_label, r"^[1-5]$", "Rating must be 1-5")

    def test_entries_have_content(self):
        entries = self.data["feed"].get("entry", [])
        review_entries = [e for e in entries if "content" in e]
        self.assertGreater(len(review_entries), 0, "Reviews must have content field")


class TestSyntheticCorpus(unittest.TestCase):
    def setUp(self):
        self.data = load_fixture("synthetic-mixed-corpus.json")

    def test_has_reviews_key(self):
        self.assertIn("reviews", self.data)

    def test_review_count(self):
        self.assertEqual(len(self.data["reviews"]), 15)

    def test_mixed_ratings(self):
        ratings = {r["rating"] for r in self.data["reviews"]}
        self.assertEqual(ratings, {1, 2, 3, 4, 5}, "Must have all ratings 1-5")

    def test_multiple_versions(self):
        versions = {r["version"] for r in self.data["reviews"]}
        self.assertGreaterEqual(len(versions), 2, "Must have at least 2 distinct versions")

    def test_required_fields(self):
        required = {"id", "rating", "title", "body", "author", "date", "version"}
        for r in self.data["reviews"]:
            for field in required:
                self.assertIn(field, r, f"Review missing field: {field}")

    def test_ratings_in_range(self):
        for r in self.data["reviews"]:
            self.assertIn(r["rating"], range(1, 6))


class TestCompetitorFixtures(unittest.TestCase):
    def _validate_fixture(self, name):
        data = load_fixture(name)
        self.assertIn("reviews", data)
        self.assertGreater(len(data["reviews"]), 0)
        for r in data["reviews"]:
            self.assertIn("rating", r)
            self.assertIn("body", r)

    def test_competitor_a(self):
        self._validate_fixture("competitor-a.json")

    def test_competitor_b(self):
        self._validate_fixture("competitor-b.json")

    def test_competitor_a_has_meta(self):
        data = load_fixture("competitor-a.json")
        self.assertIn("meta", data)
        self.assertIn("app_name", data["meta"])

    def test_competitor_b_has_meta(self):
        data = load_fixture("competitor-b.json")
        self.assertIn("meta", data)


# ---------------------------------------------------------------------------
# analyze_reviews module tests
# ---------------------------------------------------------------------------

import analyze_reviews as ar


class TestNgramHelper(unittest.TestCase):
    def test_bigrams(self):
        words = ["app", "crashes", "constantly"]
        result = ar.ngrams(words, 2)
        self.assertEqual(result, ["app crashes", "crashes constantly"])

    def test_unigrams(self):
        words = ["hello", "world"]
        result = ar.ngrams(words, 1)
        self.assertEqual(result, ["hello", "world"])

    def test_empty(self):
        self.assertEqual(ar.ngrams([], 2), [])


class TestPhraseHits(unittest.TestCase):
    def test_detects_crash(self):
        hits = ar.phrase_hits("The app crashes every day", ar.COMPLAINT_PHRASES)
        self.assertIn("crash", hits)

    def test_detects_praise(self):
        hits = ar.phrase_hits("I love the clean interface", ar.PRAISE_PHRASES)
        self.assertIn("love", hits)
        self.assertIn("clean interface", hits)

    def test_case_insensitive(self):
        hits = ar.phrase_hits("APP CRASHES DAILY", ar.COMPLAINT_PHRASES)
        self.assertIn("crash", hits)


class TestFeatureRequestDetection(unittest.TestCase):
    def test_please_add(self):
        hits = ar.detect_feature_requests("Please add dark mode to the app")
        self.assertTrue(len(hits) > 0)

    def test_would_love(self):
        hits = ar.detect_feature_requests("I would love offline mode")
        self.assertTrue(len(hits) > 0)

    def test_no_request(self):
        hits = ar.detect_feature_requests("Great app, works perfectly")
        self.assertEqual(hits, [])


class TestAnalyzeWithSyntheticCorpus(unittest.TestCase):
    def setUp(self):
        data = load_fixture("synthetic-mixed-corpus.json")
        self.reviews = data["reviews"]
        self.result = ar.analyze(self.reviews, {})

    def test_summary_keys(self):
        s = self.result["corpus_summary"]
        for key in ["total_reviews", "average_rating", "low_confidence", "rating_distribution"]:
            self.assertIn(key, s)

    def test_total_reviews(self):
        self.assertEqual(self.result["corpus_summary"]["total_reviews"], 15)

    def test_not_low_confidence(self):
        # 15 reviews >= 10, so low_confidence must be False
        self.assertFalse(self.result["corpus_summary"]["low_confidence"])

    def test_detects_crash_complaints(self):
        phrases = [c["phrase"] for c in self.result["complaint_clusters"]]
        self.assertTrue(any("crash" in p for p in phrases), f"Expected 'crash' in complaints: {phrases}")

    def test_detects_version_regression(self):
        # 2.0.5 avg should be higher than 2.1.0 (which has 1-star reviews)
        regs = self.result["version_regressions"]
        self.assertGreater(len(regs), 0, "Expected version regression 2.0.5 → 2.1.0")

    def test_detects_feature_requests(self):
        # "Please add dark mode", "offline mode", "widget support" in synthetic data
        self.assertGreater(len(self.result["feature_requests"]), 0)

    def test_result_has_limitations(self):
        self.assertGreater(len(self.result["limitations"]), 0)


class TestLowConfidenceWarning(unittest.TestCase):
    def test_low_confidence_flag(self):
        reviews = [{"id": f"r{i}", "rating": 4, "title": "ok", "body": "fine", "version": "1.0"} for i in range(5)]
        result = ar.analyze(reviews, {})
        self.assertTrue(result["corpus_summary"]["low_confidence"])
        lims = result["limitations"]
        self.assertTrue(any("LOW CONFIDENCE" in l for l in lims))


class TestAnalyzeWithCompetitors(unittest.TestCase):
    def test_competitor_whitespace(self):
        our_reviews = load_fixture("synthetic-mixed-corpus.json")["reviews"]
        comp_a = load_fixture("competitor-a.json")["reviews"]
        comp_b = load_fixture("competitor-b.json")["reviews"]
        result = ar.analyze(our_reviews, {"Alpha": comp_a, "Beta": comp_b})
        cw = result["competitor_whitespace"]
        self.assertIn("competitor_strengths_vs_our_weaknesses", cw)
        self.assertIn("competitor_gaps_vs_our_strengths", cw)


class TestLoadCorpus(unittest.TestCase):
    def test_load_synthetic(self):
        reviews, meta = ar.load_corpus(fixture_path("synthetic-mixed-corpus.json"))
        self.assertEqual(len(reviews), 15)
        self.assertIn("app_id", meta)

    def test_load_apple_rss_fixture(self):
        reviews, meta = ar.load_corpus(fixture_path("apple-reviews-284815942-us-p1.json"))
        self.assertGreater(len(reviews), 0)

    def test_load_missing_file_exits(self):
        with self.assertRaises(SystemExit) as ctx:
            ar.load_corpus("/nonexistent/path.json")
        self.assertEqual(ctx.exception.code, 2)


class TestRenderMarkdown(unittest.TestCase):
    def test_md_has_required_sections(self):
        data = load_fixture("synthetic-mixed-corpus.json")
        result = ar.analyze(data["reviews"], {})
        md = ar.render_md(result, "999999999")
        required_sections = [
            "# App Store Review Intelligence Report",
            "## Corpus summary",
            "## Top complaint clusters",
            "## Top praise clusters",
            "## Feature requests / missing expectations",
            "## Copy Extraction",
            "## Version Regressions",
            "## Top Complaint Phrases",
            "## Competitor Whitespace",
            "## Limitations",
        ]
        for section in required_sections:
            self.assertIn(section, md, f"Missing section: {section}")


class TestEndToEnd(unittest.TestCase):
    """Integration test: write corpus to temp file, run analyze, check outputs."""

    def test_full_pipeline(self):
        data = load_fixture("synthetic-mixed-corpus.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            corpus_path = os.path.join(tmpdir, "corpus.json")
            md_path = os.path.join(tmpdir, "report.md")
            json_path = os.path.join(tmpdir, "report.json")

            with open(corpus_path, "w") as f:
                json.dump(data, f)

            # Patch sys.argv and call main
            sys.argv = [
                "analyze_reviews.py",
                "--input", corpus_path,
                "--competitor", fixture_path("competitor-a.json"),
                "--competitor", fixture_path("competitor-b.json"),
                "--out-md", md_path,
                "--out-json", json_path,
            ]
            ar.main()

            self.assertTrue(os.path.exists(md_path))
            self.assertTrue(os.path.exists(json_path))

            with open(json_path) as f:
                result = json.load(f)
            self.assertIn("corpus_summary", result)
            self.assertIn("complaint_clusters", result)

            with open(md_path) as f:
                md = f.read()
            self.assertIn("## Top complaint clusters", md)


if __name__ == "__main__":
    unittest.main()
