#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

KST = ZoneInfo("Asia/Seoul") if ZoneInfo else None
WORKSPACE = Path("/Users/kjaylee/.openclaw/workspace")
DEFAULT_OUTPUT_ROOT = Path("/Volumes/workspace/ideas")
DEFAULT_STATE_ROOT = WORKSPACE / ".state" / "idea-factory-v2"
LOCAL_ARCHIVE_ROOT = WORKSPACE / "misskim-skills" / "intake-log"
SEARCH_FALLBACK = Path("/Volumes/workspace/scripts/search-fallback.sh")
TEMPLATE_REPO = "kjaylee/idea-factory-template"
DEFAULT_QUERIES = [
    "2026 local-first privacy mobile app trends",
    "receipt scanner app market trends 2026",
    "small business photo documentation app pain",
]

KEYWORD_TAGS: Dict[str, List[str]] = {
    "privacy": ["privacy", "private", "gdpr", "sensitive", "trust"],
    "local_first": ["local-first", "local first", "offline", "on-device", "on device", "ownership"],
    "camera": ["camera", "photo", "scan", "scanner", "capture", "image"],
    "mobile": ["mobile", "iphone", "ios", "android", "app store"],
    "subscription_fatigue": ["subscription fatigue", "lifetime", "one-time", "one time", "recurring fees"],
    "reseller": ["reseller", "seller", "ebay", "mercari", "listing", "collectors"],
    "landlord": ["landlord", "property", "turnover", "inspection", "evidence"],
    "warranty": ["receipt", "warranty", "serial", "invoice", "purchase proof"],
    "family": ["family", "kids", "school", "parents", "memory"],
    "pet": ["pet", "vet", "symptom", "medication"],
    "smallbiz": ["small business", "field service", "contractor", "before and after", "jobsite"],
}

BLUEPRINTS = [
    {
        "slug": "listlens",
        "title": "ListLens",
        "tagline": "Local-first camera workflow that turns item photos into listing-ready inventory records.",
        "target_user": "solo resellers, collectors, side-hustle flippers",
        "user_job": "catalog items fast and prepare marketplace listings without spreadsheet cleanup",
        "wedge": "single-session structured capture from photo → condition → price → export",
        "wedge_class": "structured_capture",
        "incumbents": ["Sortly", "Airtable templates", "generic scanner apps"],
        "incumbent_weakness": "cloud/team-first inventory tools are bloated for one-person sellers and generic scanner apps stop before listing-ready structure",
        "weakness_class": "cloud_pos_bloat",
        "job_class": "list_items",
        "why_now": "privacy-first + on-device AI + resale-side-hustle growth make faster listing prep valuable now",
        "monetization": "free capture, paid CSV/export bundles, lifetime pro unlock",
        "distribution": "YouTube reseller channels, eBay/Facebook seller groups, flipping newsletters",
        "product_sketch": "capture photos, auto-group fronts/backs, extract brand/model/serial when visible, save condition template, export listing packet",
        "version_72h": [
            "camera capture + batch session",
            "condition template presets",
            "manual price + cost fields",
            "CSV / markdown export",
            "simple item history",
        ],
        "trend_tags": ["privacy", "local_first", "camera", "mobile", "reseller", "subscription_fatigue"],
        "master_fit": "camera-heavy iOS utility with recurring usage and clean App Store framing",
        "retention_hint": "daily/weekly repeated listing workflow",
        "ai_cost_destroy": "on-device extraction reduces manual cataloging time instead of adding a chat wrapper",
    },
    {
        "slug": "proofkit",
        "title": "ProofKit",
        "tagline": "A photo-evidence timeline for landlords, cleaners, and field operators.",
        "target_user": "small landlords, cleaners, field-service owners",
        "user_job": "prove property or jobsite condition before and after work",
        "wedge": "tamper-resistant chronological photo packet with room/job labels and exportable proof bundle",
        "wedge_class": "evidence_timeline",
        "incumbents": ["camera roll", "Google Drive folders", "property inspection suites"],
        "incumbent_weakness": "camera rolls are chaotic and full inspection suites are expensive and team-oriented",
        "weakness_class": "camera_roll_chaos",
        "job_class": "document_condition",
        "why_now": "small operators need proof without paying enterprise inspection software or trusting cloud folders",
        "monetization": "subscription for multi-property packs, one-time single-owner pro tier",
        "distribution": "landlord communities, cleaning-business creators, property manager newsletters",
        "product_sketch": "capture room-tagged photos, lock timestamps, add checklist notes, export shareable PDF evidence packet",
        "version_72h": [
            "timestamped session capture",
            "room/job labels",
            "before/after pairing",
            "PDF evidence export",
            "local archive search",
        ],
        "trend_tags": ["privacy", "local_first", "camera", "smallbiz", "landlord"],
        "master_fit": "camera proof workflow with professional utility positioning",
        "retention_hint": "reused every turnover or service visit",
        "ai_cost_destroy": "AI helps auto-label spaces and reduce admin packaging time",
    },
    {
        "slug": "serialnest",
        "title": "SerialNest",
        "tagline": "On-device home warranty vault for receipts, serial numbers, and proof-of-purchase.",
        "target_user": "homeowners, parents managing appliances and gadgets",
        "user_job": "find purchase proof and serial info immediately when something breaks",
        "wedge": "receipt + box + serial + warranty end date captured in one flow",
        "wedge_class": "warranty_vault",
        "incumbents": ["generic document scanners", "notes apps", "email search"],
        "incumbent_weakness": "scanner apps over-serve business scanning and notes apps do not maintain warranty-specific structure",
        "weakness_class": "scanner_bloat",
        "job_class": "prove_warranty",
        "why_now": "subscription fatigue and privacy concern make simple local ownership tools more appealing than cloud document lockers",
        "monetization": "one-time unlock for unlimited items + reminder exports",
        "distribution": "home organization creators, deal newsletters, parenting communities",
        "product_sketch": "snap receipt and serial, assign room/product type, show warranty expiry timeline, surface claim packet instantly",
        "version_72h": [
            "receipt + serial capture",
            "manual warranty expiry",
            "room / category tags",
            "claim packet export",
            "expiry reminders file",
        ],
        "trend_tags": ["privacy", "local_first", "camera", "warranty", "subscription_fatigue"],
        "master_fit": "simple consumer utility with one-time purchase upside",
        "retention_hint": "episodic but high-value recall utility",
        "ai_cost_destroy": "AI extracts structured fields locally instead of requiring manual filing",
    },
    {
        "slug": "artshelf",
        "title": "ArtShelf",
        "tagline": "A parent-first archive for kid artwork, worksheets, and school memories.",
        "target_user": "parents with elementary-age children",
        "user_job": "keep the meaningful school papers without drowning in camera-roll clutter",
        "wedge": "capture, date, child-tag, and curate school artifacts into tidy seasonal memory books",
        "wedge_class": "memory_curation",
        "incumbents": ["camera roll", "generic family photo apps", "cloud storage folders"],
        "incumbent_weakness": "general photo tools do not treat paper artifacts as curated memories with low-friction organization",
        "weakness_class": "gallery_noise",
        "job_class": "preserve_school_work",
        "why_now": "parents already scan kids' work but existing tools collapse it into generic photo clutter",
        "monetization": "free monthly cap, paid seasonal book export / unlimited archive",
        "distribution": "mom creators, school-parent groups, printable memory communities",
        "product_sketch": "capture page, crop cleanly, tag child and grade, auto-group into timeline collections, export annual keepsake PDF",
        "version_72h": [
            "camera import + crop",
            "child / grade tagging",
            "timeline collections",
            "PDF memory book export",
            "favorites / purge queue",
        ],
        "trend_tags": ["camera", "family", "mobile", "subscription_fatigue"],
        "master_fit": "camera utility with emotional retention and printable upsell",
        "retention_hint": "weekly capture during school term",
        "ai_cost_destroy": "basic OCR/date grouping reduces manual album maintenance",
    },
    {
        "slug": "vetledger",
        "title": "VetLedger",
        "tagline": "A symptom and medication photo timeline you can bring into the vet room.",
        "target_user": "pet owners tracking recurring symptoms",
        "user_job": "show vets a clean timeline of symptoms, meds, food, and visible changes",
        "wedge": "photo-first symptom log built for handoff, not journaling",
        "wedge_class": "symptom_timeline",
        "incumbents": ["notes apps", "chat threads", "pet health apps"],
        "incumbent_weakness": "general notes fragment evidence and pet apps often overreach into heavy record systems",
        "weakness_class": "note_fragmentation",
        "job_class": "prep_vet_visit",
        "why_now": "pet owners already gather photos and medication notes ad hoc; a focused timeline reduces stress during expensive visits",
        "monetization": "subscription for multi-pet history + export packets",
        "distribution": "pet creator communities, breed groups, vet-adjacent content",
        "product_sketch": "log symptom photo/video note, meds, stool/appetite tags, and export a visit summary packet",
        "version_72h": [
            "photo timeline",
            "medication/event tags",
            "single-pet profile",
            "summary export",
            "visit mode view",
        ],
        "trend_tags": ["camera", "mobile", "pet", "privacy"],
        "master_fit": "camera + timeline workflow with real emotional urgency",
        "retention_hint": "reused during symptom flare-ups and treatment periods",
        "ai_cost_destroy": "AI summarizes repetitive logs into a compact visit handoff",
    },
    {
        "slug": "tooltrace",
        "title": "ToolTrace",
        "tagline": "Camera-first maintenance and ownership logs for contractors with too many tools.",
        "target_user": "solo contractors and tradespeople",
        "user_job": "track tool condition, purchase info, and service history without spreadsheets",
        "wedge": "snap tool, log service, attach receipt, and keep a portable ownership ledger",
        "wedge_class": "maintenance_ledger",
        "incumbents": ["spreadsheets", "asset management suites", "photo folders"],
        "incumbent_weakness": "asset suites are overbuilt for fleets and spreadsheets are abandoned in the field",
        "weakness_class": "spreadsheet_friction",
        "job_class": "track_tool_ownership",
        "why_now": "solo operators want cheap proof and maintenance memory without SaaS admin overhead",
        "monetization": "one-time pro + optional backup pack",
        "distribution": "trade YouTube, contractor forums, tool deal communities",
        "product_sketch": "capture tool photos, serials, receipts, maintenance events, and export proof for insurance or resale",
        "version_72h": [
            "tool profile capture",
            "service event log",
            "serial / receipt attachment",
            "ownership export",
            "maintenance due list",
        ],
        "trend_tags": ["camera", "smallbiz", "warranty", "privacy", "local_first"],
        "master_fit": "clear utility with pragmatic B2C/B2B edge",
        "retention_hint": "monthly maintenance and occasional proof needs",
        "ai_cost_destroy": "structured extraction removes spreadsheet entry burden",
    },
]

STOPWORDS = {
    "the", "and", "for", "with", "into", "from", "that", "this", "your", "without", "their", "they", "them",
    "local", "first", "camera", "mobile", "app", "photo", "utility", "user", "users", "data", "tool", "tools",
    "built", "make", "more", "less", "than", "into", "using", "used", "when", "what", "where", "will", "does",
}


@dataclass
class Idea:
    slug: str
    title: str
    tagline: str
    target_user: str
    user_job: str
    wedge: str
    wedge_class: str
    incumbent_weakness: str
    weakness_class: str
    job_class: str
    why_now: str
    monetization: str
    distribution: str
    product_sketch: str
    version_72h: List[str]
    incumbents: List[str]
    master_fit: str
    retention_hint: str
    ai_cost_destroy: str
    trend_tags: List[str]
    signal_score: float
    doctrine_score: int
    wedge_score: int
    distribution_score: int
    monetization_score: int
    master_fit_score: int
    durability_score: int
    subtotal: int
    overall_score: int
    red_team: Dict[str, object]
    overlap_key: str


def now_kst() -> datetime:
    return datetime.now(KST) if KST else datetime.now()


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return text or "idea"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def load_local_archive() -> Tuple[List[Dict[str, object]], Dict[str, int]]:
    texts: List[str] = []
    source_meta: List[Dict[str, object]] = []
    if not LOCAL_ARCHIVE_ROOT.exists():
        return source_meta, {}
    paths = sorted(LOCAL_ARCHIVE_ROOT.glob("*trend*.*"))[-30:]
    for path in paths:
        if path.suffix.lower() == ".json":
            raw = read_text(path)
            texts.append(raw)
        else:
            texts.append(read_text(path))
        source_meta.append({"path": str(path), "kind": path.suffix.lower().lstrip(".")})
    signal_counts = count_tags("\n".join(texts))
    return source_meta, signal_counts


def count_tags(text: str, weight: int = 1) -> Dict[str, int]:
    lower = text.lower()
    counts: Dict[str, int] = {k: 0 for k in KEYWORD_TAGS}
    for tag, words in KEYWORD_TAGS.items():
        total = 0
        for word in words:
            total += lower.count(word.lower())
        counts[tag] = total * weight
    return counts


def merge_counts(*items: Dict[str, int]) -> Dict[str, int]:
    merged: Dict[str, int] = {k: 0 for k in KEYWORD_TAGS}
    for item in items:
        for k in merged:
            merged[k] += int(item.get(k, 0))
    return merged


def run_search_fallback(query: str) -> List[Dict[str, str]]:
    if not SEARCH_FALLBACK.exists():
        return []
    try:
        result = subprocess.run(
            [str(SEARCH_FALLBACK), query, "8"],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        if isinstance(data, list):
            cleaned = []
            for row in data[:8]:
                cleaned.append(
                    {
                        "title": str(row.get("title", "")),
                        "url": str(row.get("url", "")),
                        "snippet": str(row.get("snippet", "")),
                    }
                )
            return cleaned
    except Exception:
        return []
    return []


def collect_web_signals(enabled: bool) -> Tuple[List[Dict[str, object]], Dict[str, int]]:
    if not enabled:
        return [], {k: 0 for k in KEYWORD_TAGS}
    all_rows: List[Dict[str, object]] = []
    combined = {k: 0 for k in KEYWORD_TAGS}
    for query in DEFAULT_QUERIES:
        rows = run_search_fallback(query)
        blob = "\n".join(f"{r['title']}\n{r['snippet']}" for r in rows)
        counts = count_tags(blob, weight=1)
        combined = merge_counts(combined, counts)
        all_rows.append({"query": query, "results": rows})
    return all_rows, combined


def normalized_tokens(text: str) -> set:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def trend_boost(blueprint: Dict[str, object], counts: Dict[str, int]) -> float:
    tags = blueprint.get("trend_tags", [])
    if not isinstance(tags, list):
        return 0.0
    total = sum(counts.get(tag, 0) for tag in tags)
    return min(12.0, total / 4.0)


def build_red_team(blueprint: Dict[str, object]) -> Dict[str, object]:
    risks: List[str] = []
    mitigations: List[str] = []
    penalty = 0

    weak = str(blueprint.get("weakness_class", ""))
    job = str(blueprint.get("job_class", ""))
    monetization = str(blueprint.get("monetization", "")).lower()
    distribution = str(blueprint.get("distribution", "")).lower()
    wedge = str(blueprint.get("wedge", "")).lower()
    retention = str(blueprint.get("retention_hint", "")).lower()
    tags = set(blueprint.get("trend_tags", []))

    if "chat" in wedge or "assistant" in wedge:
        risks.append("AI wrapper risk: the product could collapse into a generic assistant instead of a capture-to-outcome tool.")
        mitigations.append("Keep the hero flow camera-first and outcome-first; AI stays invisible and subordinate.")
        penalty += 10
    else:
        risks.append("Acquisition risk: niche users may still tolerate ugly incumbent workflows longer than expected.")
        mitigations.append("Lead with a single measurable time-saved claim rather than generic AI convenience.")
        penalty += 3

    if any(x in distribution for x in ["groups", "youtube", "newsletters", "forums", "communities"]):
        risks.append("Channel risk: creator/community distribution is testable but noisy, and CAC may spike if the pain is not urgent enough.")
        mitigations.append("Test one community/channel at a time and demand evidence of organic saves/shares before paid growth.")
        penalty += 3
    else:
        risks.append("Acquisition risk: first-100-user path is too vague.")
        mitigations.append("Constrain launch to one creator cluster or one repeated search-driven use case.")
        penalty += 8

    if any(x in retention for x in ["daily", "weekly", "reused", "monthly"]):
        risks.append("Retention risk: even recurring workflows can decay if setup or export friction is only marginally better than Notes + camera roll.")
        mitigations.append("Benchmark the full capture-to-export loop against the incumbent hack and require a decisive speed advantage.")
        penalty += 3
    else:
        risks.append("Retention risk: usage may be episodic and too weak for sustained revenue.")
        mitigations.append("Bias monetization toward lifetime unlocks or high-value export moments rather than forced subscription.")
        penalty += 7

    if weak in {"scanner_bloat", "gallery_noise", "note_fragmentation"}:
        risks.append("Fast-follow risk: incumbents could imitate this with one focused feature or onboarding template.")
        mitigations.append("Defend with sharper positioning, faster capture UX, and a better export packet than general-purpose apps can justify building.")
        penalty += 6
    else:
        risks.append("Incumbent response risk: a motivated incumbent could still undercut the wedge if distribution stays weak.")
        mitigations.append("Win on narrow speed, better defaults, and a stronger use-case story before broader expansion.")
        penalty += 4

    if job in {"preserve_school_work", "prep_vet_visit"}:
        risks.append("Payment risk: emotional utility may produce gratitude but not strong willingness to pay.")
        mitigations.append("Treat premium export and convenience as the paid event; validate before deepening scope.")
        penalty += 5

    if "subscription" in monetization and job in {"prove_warranty", "track_tool_ownership"}:
        risks.append("Pricing risk: subscription may feel heavier than the job frequency warrants.")
        mitigations.append("Put lifetime or one-time ownership in front; reserve subscription for power-user backup/history only.")
        penalty += 5

    if "camera" not in tags or not ({"mobile", "local_first"} & tags):
        risks.append("Focus risk: weak alignment with camera/mobile/local-first strengths could dilute execution quality.")
        mitigations.append("Reject or shrink anything that cannot ship as a tight camera-centric iOS utility quickly.")
        penalty += 8

    if penalty >= 26:
        verdict = "reject"
    elif penalty >= 15:
        verdict = "shrink"
    else:
        verdict = "go"

    return {
        "reject_risks": risks,
        "mitigations": mitigations,
        "penalty": penalty,
        "verdict": verdict,
    }


def score_blueprint(blueprint: Dict[str, object], counts: Dict[str, int]) -> Idea:
    boost = trend_boost(blueprint, counts)
    red_team = build_red_team(blueprint)

    doctrine = 24
    if "local_first" in blueprint["trend_tags"]:
        doctrine += 3
    if "privacy" in blueprint["trend_tags"]:
        doctrine += 2
    if blueprint["wedge_class"] in {"structured_capture", "evidence_timeline", "warranty_vault"}:
        doctrine += 2
    doctrine = min(30, doctrine)

    wedge_score = 15
    if len(str(blueprint["user_job"])) < 100:
        wedge_score += 5
    if blueprint["weakness_class"] in {"cloud_pos_bloat", "camera_roll_chaos", "spreadsheet_friction"}:
        wedge_score += 3
    wedge_score = min(22, wedge_score)

    distribution_score = 10
    if any(ch in str(blueprint["distribution"]).lower() for ch in ["youtube", "groups", "forums", "newsletters"]):
        distribution_score += 6
    distribution_score = min(16, distribution_score)

    monetization_score = 9
    monetization_lower = str(blueprint["monetization"]).lower()
    if "lifetime" in monetization_lower or "one-time" in monetization_lower or "one-time" in monetization_lower:
        monetization_score += 5
    if "free" in monetization_lower:
        monetization_score += 1
    monetization_score = min(15, monetization_score)

    master_fit_score = 10
    if "camera" in blueprint["trend_tags"]:
        master_fit_score += 4
    if "mobile" in blueprint["trend_tags"]:
        master_fit_score += 1
    if "local_first" in blueprint["trend_tags"]:
        master_fit_score += 2
    master_fit_score = min(16, master_fit_score)

    durability_score = 7
    if blueprint["job_class"] in {"list_items", "document_condition", "track_tool_ownership"}:
        durability_score += 4
    if blueprint["wedge_class"] in {"structured_capture", "evidence_timeline", "maintenance_ledger"}:
        durability_score += 3
    durability_score = min(14, durability_score)

    subtotal = doctrine + wedge_score + distribution_score + monetization_score + master_fit_score + durability_score + round(boost)
    overall = max(0, min(100, round(subtotal * 0.78) - int(red_team["penalty"])))

    overlap_key = f"{blueprint['wedge_class']}|{blueprint['weakness_class']}|{blueprint['job_class']}"

    return Idea(
        slug=str(blueprint["slug"]),
        title=str(blueprint["title"]),
        tagline=str(blueprint["tagline"]),
        target_user=str(blueprint["target_user"]),
        user_job=str(blueprint["user_job"]),
        wedge=str(blueprint["wedge"]),
        wedge_class=str(blueprint["wedge_class"]),
        incumbent_weakness=str(blueprint["incumbent_weakness"]),
        weakness_class=str(blueprint["weakness_class"]),
        job_class=str(blueprint["job_class"]),
        why_now=str(blueprint["why_now"]),
        monetization=str(blueprint["monetization"]),
        distribution=str(blueprint["distribution"]),
        product_sketch=str(blueprint["product_sketch"]),
        version_72h=list(blueprint["version_72h"]),
        incumbents=list(blueprint["incumbents"]),
        master_fit=str(blueprint["master_fit"]),
        retention_hint=str(blueprint["retention_hint"]),
        ai_cost_destroy=str(blueprint["ai_cost_destroy"]),
        trend_tags=list(blueprint["trend_tags"]),
        signal_score=round(boost, 2),
        doctrine_score=doctrine,
        wedge_score=wedge_score,
        distribution_score=distribution_score,
        monetization_score=monetization_score,
        master_fit_score=master_fit_score,
        durability_score=durability_score,
        subtotal=subtotal,
        overall_score=overall,
        red_team=red_team,
        overlap_key=overlap_key,
    )


def ideas_overlap(a: Idea, b: Idea) -> Tuple[bool, Dict[str, object]]:
    shared_axes = 0
    if a.wedge_class == b.wedge_class:
        shared_axes += 1
    if a.weakness_class == b.weakness_class:
        shared_axes += 1
    if a.job_class == b.job_class:
        shared_axes += 1

    token_a = normalized_tokens(" ".join([a.title, a.tagline, a.user_job, a.wedge, a.incumbent_weakness]))
    token_b = normalized_tokens(" ".join([b.title, b.tagline, b.user_job, b.wedge, b.incumbent_weakness]))
    similarity = jaccard(token_a, token_b)
    overlap = shared_axes >= 2 or similarity >= 0.55 or (shared_axes >= 1 and similarity >= 0.42)
    return overlap, {"shared_axes": shared_axes, "keyword_jaccard": round(similarity, 3)}


def suppress_overlap(scored: List[Idea], desired_count: int) -> Tuple[List[Idea], List[Dict[str, object]]]:
    kept: List[Idea] = []
    suppressed: List[Dict[str, object]] = []
    for idea in sorted(scored, key=lambda x: (-x.overall_score, -x.signal_score, x.title)):
        blocked = None
        for existing in kept:
            overlap, meta = ideas_overlap(idea, existing)
            if overlap:
                blocked = {"dropped": idea.title, "kept": existing.title, **meta}
                break
        if blocked:
            suppressed.append(blocked)
            continue
        kept.append(idea)
        if len(kept) >= desired_count:
            continue
    return kept[:desired_count], suppressed


def render_batch_md(run_id: str, ideas: List[Idea], suppressed: List[Dict[str, object]], counts: Dict[str, int], state: Dict[str, object]) -> str:
    top_signals = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    signal_text = ", ".join(f"{k}:{v}" for k, v in top_signals if v > 0) or "no-strong-signal"
    lines = [
        f"# Idea Factory v2 — Daily Batch ({run_id})",
        "",
        f"- Quality pass: **{state['quality_pass']}**",
        f"- Status: **{state['status']}**",
        f"- Count: **{len(ideas)}**",
        f"- Overlap suppression rule: **drop if shared axes >=2, or keyword Jaccard >=0.55, or shared axes >=1 plus Jaccard >=0.42**",
        f"- Top signals: {signal_text}",
        "",
    ]
    for idx, idea in enumerate(ideas, 1):
        lines.extend([
            f"## {idx}. {idea.title} — {idea.overall_score}",
            "",
            f"**Tagline:** {idea.tagline}",
            f"**Target user:** {idea.target_user}",
            f"**User job:** {idea.user_job}",
            f"**Wedge:** {idea.wedge}",
            f"**Incumbent weakness:** {idea.incumbent_weakness}",
            f"**Why now:** {idea.why_now}",
            f"**Monetization:** {idea.monetization}",
            f"**Distribution:** {idea.distribution}",
            f"**72h version:** {', '.join(idea.version_72h)}",
            f"**Axes:** wedge=`{idea.wedge_class}` / weakness=`{idea.weakness_class}` / job=`{idea.job_class}`",
            "",
            "### Red Team",
            f"- Verdict: **{idea.red_team['verdict']}**",
            f"- Penalty: **{idea.red_team['penalty']}**",
            "- Reject risks:",
        ])
        for risk in idea.red_team["reject_risks"]:
            lines.append(f"  - {risk}")
        lines.append("- Mitigations:")
        for mitigation in idea.red_team["mitigations"]:
            lines.append(f"  - {mitigation}")
        lines.append("")
    if suppressed:
        lines.extend(["## Suppressed overlaps", ""])
        for row in suppressed:
            lines.append(f"- dropped `{row['dropped']}` in favor of `{row['kept']}` (shared_axes={row['shared_axes']}, jaccard={row['keyword_jaccard']})")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_best_idea_md(idea: Idea, repo_url: str | None = None) -> str:
    lines = [
        f"# {idea.title}",
        "",
        f"**Score:** {idea.overall_score}",
        f"**Tagline:** {idea.tagline}",
        "",
        "## Thesis",
        f"{idea.title} helps {idea.target_user} {idea.user_job}.",
        "",
        "## Wedge",
        idea.wedge,
        "",
        "## Incumbent weakness",
        idea.incumbent_weakness,
        "",
        "## Why now",
        idea.why_now,
        "",
        "## Monetization",
        idea.monetization,
        "",
        "## Distribution",
        idea.distribution,
        "",
        "## 72h Product Version",
    ]
    for item in idea.version_72h:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Red Team",
        f"- Verdict: {idea.red_team['verdict']}",
        f"- Penalty: {idea.red_team['penalty']}",
        "- Reject risks:",
    ])
    for risk in idea.red_team["reject_risks"]:
        lines.append(f"  - {risk}")
    lines.append("- Mitigations:")
    for mitigation in idea.red_team["mitigations"]:
        lines.append(f"  - {mitigation}")
    if repo_url:
        lines.extend(["", f"## Repo\n- {repo_url}"])
    return "\n".join(lines).strip() + "\n"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def repo_exists(name: str) -> bool:
    result = subprocess.run(["gh", "repo", "view", f"kjaylee/{name}"], capture_output=True, text=True)
    return result.returncode == 0


def unique_repo_name(base: str) -> str:
    name = slugify(base)
    if not repo_exists(name):
        return name
    suffix = now_kst().strftime("%Y%m%d")
    alt = f"{name}-{suffix}"
    idx = 2
    while repo_exists(alt):
        alt = f"{name}-{suffix}-{idx}"
        idx += 1
    return alt


def write_repo_docs(repo_dir: Path, idea: Idea) -> None:
    files = {
        "AGENTS.md": f"# AGENTS\n\nBuild `{idea.title}` as a narrow, camera-first, privacy-respecting product.\n\n- Target user: {idea.target_user}\n- Core job: {idea.user_job}\n- Wedge: {idea.wedge}\n- Non-goal: generic AI assistant behavior\n- Success metric: users can finish the core capture-to-export loop in under 60 seconds\n",
        "THESIS.md": f"# THESIS\n\n## Product\n{idea.title} — {idea.tagline}\n\n## User\n{idea.target_user}\n\n## User job\n{idea.user_job}\n\n## Why now\n{idea.why_now}\n\n## Incumbent weakness\n{idea.incumbent_weakness}\n\n## Monetization\n{idea.monetization}\n",
        "PLANS.md": "# PLANS\n\n## 72h Product Version\n" + "\n".join(f"- {item}" for item in idea.version_72h) + f"\n\n🔴 Red Team:\n- [공격 1]: {idea.red_team['reject_risks'][0]}\n- [공격 2]: {idea.red_team['reject_risks'][1] if len(idea.red_team['reject_risks']) > 1 else 'Retention/distribution still need proof.'}\n- [방어/완화]: {' '.join(str(x) for x in idea.red_team['mitigations'][:2])}\n- [합의]: {'🟢극복' if idea.red_team['verdict']=='go' else '🟡위험수용'}\n",
        "UI.md": f"# UI\n\n## Product promise\nThe app must feel faster than using camera roll + notes + folders.\n\n## Core screens\n- Capture session\n- Structured detail edit\n- Timeline or archive\n- Export / share packet\n\n## Tone\nProfessional, calm, no gimmick AI chrome. The outcome matters more than the model.\n",
        "REDTEAM.md": "# REDTEAM\n\n## Reject risks\n" + "\n".join(f"- {item}" for item in idea.red_team["reject_risks"]) + "\n\n## Mitigations\n" + "\n".join(f"- {item}" for item in idea.red_team["mitigations"]) + f"\n\n## Verdict\n- {idea.red_team['verdict']}\n",
        "DISTRIBUTION.md": f"# DISTRIBUTION\n\n## First 100 users\n{idea.distribution}\n\n## Positioning\n- Camera-first\n- Local-first where possible\n- Narrow workflow wedge\n\n## Monetization fit\n{idea.monetization}\n",
        "README.md": f"# {idea.title}\n\n{idea.tagline}\n\n- Target user: {idea.target_user}\n- User job: {idea.user_job}\n- Wedge: {idea.wedge}\n- Incumbent weakness: {idea.incumbent_weakness}\n",
    }
    for name, content in files.items():
        (repo_dir / name).write_text(content, encoding="utf-8")


def create_private_repo_from_template(idea: Idea) -> str:
    repo_name = unique_repo_name(idea.slug)
    temp_dir = Path(tempfile.mkdtemp(prefix="idea-factory-repo-"))
    try:
        subprocess.run(
            ["gh", "repo", "create", f"kjaylee/{repo_name}", "--private", "--template", TEMPLATE_REPO, "--clone"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        repo_dir = temp_dir / repo_name
        write_repo_docs(repo_dir, idea)
        subprocess.run(["git", "config", "user.name", "Miss Kim"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "misskim@local.invalid"], cwd=repo_dir, check=True)
        subprocess.run(["git", "add", "AGENTS.md", "THESIS.md", "PLANS.md", "UI.md", "REDTEAM.md", "DISTRIBUTION.md", "README.md"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", f"Seed docs for {idea.title}"], cwd=repo_dir, check=True, capture_output=True, text=True)
        subprocess.run(["git", "push", "origin", "HEAD"], cwd=repo_dir, check=True, capture_output=True, text=True)
        result = subprocess.run(["gh", "repo", "view", f"kjaylee/{repo_name}", "--json", "url", "-q", ".url"], cwd=repo_dir, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def persist_outputs(run_dir: Path, state_dir: Path, batch: Dict[str, object], batch_md: str, best_md: str) -> None:
    ensure_dir(run_dir)
    ensure_dir(state_dir)
    (run_dir / "batch.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "batch.md").write_text(batch_md, encoding="utf-8")
    (run_dir / "best-idea.md").write_text(best_md, encoding="utf-8")
    (run_dir / "state.json").write_text(json.dumps(batch["state"], ensure_ascii=False, indent=2), encoding="utf-8")
    (state_dir / "state.json").write_text(json.dumps(batch["state"], ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Idea Factory v2")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--use-web-search", action="store_true")
    parser.add_argument("--create-repo", action="store_true")
    parser.add_argument("--repo-threshold", type=int, default=80)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    now = now_kst()
    run_id = now.strftime("%Y%m%d-%H%M%S")
    day_dir = now.strftime("%Y-%m-%d")
    output_root = Path(args.output_root)
    run_dir = output_root / day_dir / "idea-factory-v2" / run_id
    state_dir = Path(args.state_root) / run_id

    local_sources, local_counts = load_local_archive()
    web_sources, web_counts = collect_web_signals(args.use_web_search)
    counts = merge_counts(local_counts, web_counts)

    scored = [score_blueprint(bp, counts) for bp in BLUEPRINTS]
    final_ideas, suppressed = suppress_overlap(scored, desired_count=args.count)
    overlap_violations = []
    for i, idea_a in enumerate(final_ideas):
        for idea_b in final_ideas[i + 1 :]:
            overlap, meta = ideas_overlap(idea_a, idea_b)
            if overlap:
                overlap_violations.append({"a": idea_a.title, "b": idea_b.title, **meta})

    scores = sorted(idea.overall_score for idea in final_ideas)
    median_score = scores[len(scores) // 2] if scores else 0
    max_score = max(scores) if scores else 0
    min_score = min(scores) if scores else 0
    quality_pass = (
        len(final_ideas) >= args.count
        and not overlap_violations
        and median_score >= 70
        and max_score >= args.repo_threshold
        and min_score >= 50
    )
    status = "success" if quality_pass else "needs_retry"
    best_idea = final_ideas[0] if final_ideas else None
    repo_url = None

    state = {
        "run_id": run_id,
        "generated_at_kst": now.isoformat(),
        "status": status,
        "quality_pass": quality_pass,
        "retry_count": 0 if quality_pass else 1,
        "next_recommended_retry_reason": None if quality_pass else "Need at least 5 non-overlapping ideas with score >= 70.",
        "overlap_rule": "drop if shared axes >=2, or keyword Jaccard >=0.55, or shared axes >=1 plus Jaccard >=0.42",
        "count_requested": args.count,
        "count_final": len(final_ideas),
        "repo_threshold": args.repo_threshold,
        "median_score": median_score,
        "max_score": max_score,
        "min_score": min_score,
        "overlap_violations": overlap_violations,
    }

    if args.create_repo and not args.dry_run and best_idea and quality_pass and best_idea.overall_score >= args.repo_threshold and best_idea.red_team["verdict"] != "reject":
        repo_url = create_private_repo_from_template(best_idea)
        state["repo_created"] = True
        state["repo_url"] = repo_url
    else:
        state["repo_created"] = False

    batch = {
        "run_id": run_id,
        "artifact_root": str(run_dir),
        "sources": {
            "local_archive": local_sources,
            "web_search": web_sources,
        },
        "signal_counts": counts,
        "ideas": [asdict(idea) for idea in final_ideas],
        "suppressed_overlaps": suppressed,
        "state": state,
    }

    batch_md = render_batch_md(run_id, final_ideas, suppressed, counts, state)
    best_md = render_best_idea_md(best_idea, repo_url) if best_idea else "# No idea generated\n"
    persist_outputs(run_dir, state_dir, batch, batch_md, best_md)

    summary = {
        "run_id": run_id,
        "artifact_root": str(run_dir),
        "quality_pass": quality_pass,
        "repo_url": repo_url,
        "best_idea": asdict(best_idea) if best_idea else None,
        "count": len(final_ideas),
        "overlap_rule": state["overlap_rule"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if quality_pass else 2


if __name__ == "__main__":
    sys.exit(main())
