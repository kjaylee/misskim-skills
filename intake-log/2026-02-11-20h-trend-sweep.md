# Agent Skill Trend Sweep — 2026-02-11 20:00 KST

## Survey Scope
- SkillsMP
- MCP Market
- SkillHub
- Molt Road
- VSCode Agent Skills extension (`formulahendry.agent-skills`)

## Executive Summary
- **SkillsMP scale up:** live counter now shows **185,359 skills** (top 5,000 browsable in UI), with strongest categories in Tools/Development/Data-AI.
- **MCP Market growth:** **20,805 servers** indexed (updated 2h ago), with strong leaderboard concentration around automation/dev infra servers.
- **SkillHub is now clearly freemium+SaaS:** explicit pricing page live (Free, Pro, Credit Packs, Agent Plans).
- **Molt Road still high-risk signal:** currently framed as a “game” with credits, but active autonomous market mechanics remain visible (listings, pricing, dealer reputation labels).
- **VSCode extension channel is real and usable:** Agent Skills extension is live, free, and installable with custom multi-repo sources + one-click install workflows.

---

## 1) SkillsMP — Popular Skills + Signals
### Observed metrics
- Total skills shown: **185,359**
- Browse cap: **Top 5,000** skills
- Category volume highlights:
  - Tools: **62,061**
  - Development: **50,942**
  - Data & AI: **36,828**
  - Business: **33,835**
  - DevOps: **27,920**

### Popular skills visible on homepage (sorted by stars)
- `flow.md` / `fix.md` / `extract-errors.md` / `test.md` / `feature-flags.md` from `facebook/react` — each around **242.9k**
- OpenClaw skills like `gemini`, `github`, `nano-pdf`, `blucli` — around **182.5k**

### Pricing
- No paid pricing tier exposed on public pages.
- Positioning remains: community discovery/aggregation project.

---

## 2) MCP Market — Popular Servers + Skills
### Observed metrics
- **20,805 servers**, “updated 2 hours ago”

### Popular MCP servers (homepage “인기 MCP 서버”)
- Superpowers — **49,315**
- TrendRadar — **46,053**
- Context7 — **45,352**
- MindsDB — **38,438**
- Playwright — **26,966**
- GitHub — **26,816**

### Popular Agent Skills (MCP Market skills section)
- React Code Fix & Linter — **242,682**
- n8n Pull Request Creator — **170,914**
- Interactive Book Translator — **144,375**
- Prompt Finder & Enhancer — **144,375**
- Skill Finder & Installer — **144,375**

### Pricing
- No direct platform subscription page (pricing URL returns 404).
- Sponsored placements are active (e.g., Bright Data, Scout Monitoring), suggesting ad-based monetization.

---

## 3) SkillHub — Popular Skills + Full Pricing Unlocked
### Observed metrics
- Homepage headline: **21.3K skills**, **3.7M stars**
- Semantic CLI flows promoted:
  - `npx @skill-hub/cli install frontend-design`
  - `npx @skill-hub/cli search "react"`

### Trending Today (homepage)
- camsnap (+180,250)
- wacli (+180,193)
- trello (+177,098)
- video-frames (+174,365)
- slack (+168,423)

### Hot Skills panel
- `frontend-design` (anthropics) — **66.0k**
- `systematic-debugging` (obra) — **49.4k**
- `docs-review` (metabase) — **45.9k**

### Pricing (new actionable clarity)
- **Free:** 2 queries/day
- **Pro:** $9.99/mo (50 AI queries/day)
- **Credit packs:**
  - 50 credits: $4.99
  - 200 credits: $14.99
  - 500 credits: $29.99
- **Agent Plans:**
  - Starter: $19/mo (BYOK, web, up to 3 skills)
  - Pro: $49/mo (BYOK, all channels, unlimited skills)
  - Managed: $99/mo ($50 AI credits included)
  - Team: $199/mo (5 instances + team features)

---

## 4) Molt Road — Current State
### Live state observed
- Market page active with **41 listings**
- Live counters: **5 agents online**, **35 humans watching**
- Listings include exploit/forgery/intel/service items priced in **credits (cr)**
  - Examples: SQL Injection Tool (43–65 cr), Deepfake Engine (741 cr), Ransomware Builder (767 cr), Witness Relocation (4500 cr)
- Footer still states: **“A game. Nothing is real. Everything is permitted.”**

### Security interpretation
- Even with “game” framing, market mechanics (listing, pricing, reputation tags, trade activity) are directly reusable trust/incentive patterns.
- Keep **hard block / no integration** posture.

---

## 5) VSCode Agent Skills Extension
### Extension snapshot
- Marketplace item: `formulahendry.agent-skills`
- Installs: **1,569**
- Rating: **5.0 (1 review)**
- Price: **Free**

### Practical automation features
- Multi-repo skill indexing from GitHub
- One-click install/uninstall into workspace
- Configurable install targets (`.github/skills`, `.claude/skills`)
- Optional GitHub token for higher API limits
- Sync/refresh workflows and cache controls

### Strategic relevance
- Strong bridge from registry-style discovery to local operational use.
- Aligns with Copilot’s official Agent Skills rollout and open standard portability.

---

## Automation Absorption Candidates for `misskim-skills`
### High priority
1. **Build `skill-intake-sync` automation**
   - Mirror VSCode extension behavior: multi-repo fetch, cache TTL, parallel metadata sync.
2. **Build `skill-triage-score` pipeline**
   - Add repeatable scoring dimensions (Practicality/Clarity/Automation/Quality/Impact) + security gate.
3. **Add `skillhub-cli-bridge` helper skill**
   - Wrap semantic search + install commands into safe audited workflow (search → audit checklist → stage).

### Medium priority
4. **Absorb workflow patterns from top practical skills**
   - `systematic-debugging`, `frontend-design`, `file-search`, `docs-review` into internal templates/checklists.
5. **Add popularity anomaly detection**
   - Flag large overnight jumps or duplicated score patterns before trusting trend data.

### Security action (carry)
6. **Continue absolute avoid list for Molt Road ingestion paths**
   - No source import, no automation hook, no credential interaction.

---

## Pricing Snapshot (this sweep)
| Platform | Pricing model | Notes |
|---|---|---|
| SkillsMP | Public/free discovery (no paid tier shown) | Aggregator model |
| MCP Market | No user pricing page; sponsored listings visible | Likely directory + ad model |
| SkillHub | Freemium + subscription + credits + agent plans | Most mature monetization among surveyed |
| Molt Road | Credit-based in-world pricing (`cr`) | Not acceptable source; security risk context |
| VSCode Agent Skills ext | Free extension | Distribution channel, not marketplace monetization |

---

## Recommended Immediate Next Steps
1. Ship `skill-intake-sync` spec + MVP this week.
2. Add `skill-triage-score` check as mandatory intake gate.
3. Audit/absorb 4 high-signal skills (`systematic-debugging`, `frontend-design`, `file-search`, `docs-review`) into internal skill templates.
4. Keep Molt Road on denylist with explicit rationale in security docs.

---
*Completed: 2026-02-11 20:00 KST*