# Agent Skill Trend Sweep — 2026-02-12 12:00 KST

## 📊 Executive Summary
**SECURITY INTENSIFIES:** Snyk's ToxicSkills study finds prompt injection in 36% of sampled skills + 1,467 malicious payloads across ClawHub. Anthropic DXT flagged for critical RCE (runs with full system privileges). CoSAI + Cisco CodeGuard donated for zero-trust agent security. **NEW ENTRANTS:** Skillkit (package manager, PH launch), AGNXI (curated directory, 8K+ skills), Google Developer Knowledge API+MCP. **MAJOR:** Claude Code Agent Teams now in research preview (multi-agent coordination). 16 Claude agents built a C compiler (Ars Technica). SkillsMP now indexes 185K+ skills. Skills.sh ecosystem maturing as safe alternative to ClawHub.

## 🔴 Security Updates (Critical)

### Snyk ToxicSkills Study (Feb ~9)
- 36% of sampled skills contain prompt injection payloads
- 1,467 malicious payloads identified across ClawHub
- First coordinated malware campaign targeting Claude Code + OpenClaw users
- Source: snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub

### Anthropic DXT RCE Vulnerability (Feb 10)
- DXT (Desktop Extensions) runs with full system privileges
- CSO Online flagged as "critical RCE vulnerability"
- Anthropic response: "users explicitly configure and grant permissions"
- **Impact on us:** Validates our audit-first policy

### CoSAI Security Framework + Cisco CodeGuard (Feb 9)
- Cisco donated Project CodeGuard to CoSAI (open-source)
- Embeds security rules directly into AI coding workflows
- Zero-trust principles for MCP servers as critical infrastructure
- Source: dev.to AI Weekly Digest

### Adversa AI: 19 MCP Security Resources (Feb ~5)
- Confirmed RCE in Anthropic's Git MCP server
- Emerging attack vectors: tool poisoning, prompt injection via MCP
- CoSAI framework recommended for enterprise MCP deployments

### ClawHub Status (Feb 12)
- VirusTotal scanning live but VT admits "not a silver bullet"
- Snyk: 36% prompt injection rate persists despite scanning
- **Our policy remains: ZERO blind installs, audit → rewrite only**

## 🆕 New Platforms & Tools

### 1. **Skillkit** (NEW — PH Launch Feb 8-12)
- **What:** Universal skill package manager for AI coding agents
- **Features:** Auto-generate instructions (Primer), persist learnings (Memory), distribute across Mesh networks
- **Supports:** Claude, Cursor, Windsurf, Copilot + 28 more
- **CLI:** One-command install across all platforms
- **PH Rank:** #3 Day, 259 upvotes
- **Source:** producthunt.com/products/skillkit-2, agentskills.com
- **Relevance:** ⭐ HIGH — could replace our manual skill management
- **Action:** 🔍 EVALUATE — test CLI, compare with `npx skills add`

### 2. **AGNXI** (NEW)
- **What:** Curated directory of 8,000+ Agent Skills (manually selected vs mass-scraped)
- **Approach:** Human-curated from major companies, not auto-scraping GitHub
- **Features:** Search by functionality (not just name), quality filtering
- **Source:** agnxi.com, reddit.com/r/Trae_ai
- **Relevance:** 🟢 MEDIUM — useful for discovery, complementary to SkillsMP
- **Action:** 🟡 MONITOR — bookmark for research

### 3. **Google Developer Knowledge API + MCP Server** (Feb 4)
- **What:** Machine-readable gateway to all Google developer docs
- **Enables:** AI agents access current, accurate Google documentation programmatically
- **Setup:** `gcloud beta service mcp enable`
- **Source:** infoworld.com, winbuzzer.com
- **Relevance:** 🟢 MEDIUM — useful for GCP/Firebase work
- **Action:** 🔍 EVALUATE — could improve our GCP VM management accuracy

### 4. **Amazon Ads MCP Server** (Feb 2 — Open Beta)
- **What:** Natural-language campaign management across Amazon marketplaces
- **Features:** Create campaigns, optimize bids, pull reports via Claude/ChatGPT/Gemini
- **Source:** advertising.amazon.com, clearadsagency.com
- **Relevance:** 🟡 LOW — not in our current scope (no Amazon ads)
- **Action:** 🟡 MONITOR for future monetization options

### 5. **Miro MCP Server** (Feb 2)
- **What:** Visual collaboration → AI coding tools bridge
- **Built with:** Anthropic, AWS, GitHub, Google, Windsurf
- **Relevance:** 🟡 LOW — interesting for design workflows but not priority
- **Action:** 🟡 MONITOR only

## 🧠 Major Technical Developments

### Claude Code Agent Teams (Research Preview, Feb 2026)
- **What:** Lead AI spawns teammate agents, each with own context window, message-passing coordination
- **Enable:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings
- **Validation:** 16 Claude instances built a C compiler (Ars Technica, Carlini research)
- **Architecture:** Docker containers per agent, shared Git repo, task lock files
- **Relevance:** ⭐⭐ CRITICAL — directly validates our ralph-loop multi-agent pattern
- **Action:** ⭐ HIGH — study architecture, compare with our subagent delegation model

### SkillsMP Scale: 185,359 Skills
- Grew from 96K → 185K in ~3 weeks
- Supports "Run in Manus" integration
- AI semantic search + category browsing + popularity sorting
- Source: archive.is/Hf3ed

### Agent Skills Standard Maturity
- Anthropic + OpenAI + Vercel + 25+ platforms unified on SKILL.md
- `npx skills add` supports 16 different agent config paths
- skills.sh = primary distribution hub (Vercel)
- MCP = enterprise deterministic execution (coexists, not competing)

## 📈 Skills.sh Leaderboard (Feb 12 Estimate)

### All-Time Top (stable):
1. find-skills (vercel-labs) — meta-discovery
2. vercel-react-best-practices — React/Next.js
3. web-design-guidelines — UI compliance
4. remotion-best-practices — video production
5. frontend-design (Anthropic) — aesthetic codification
6. agent-browser — browser automation
7. skill-creator (Anthropic) — skill authoring
8. browser-use — persistent Chromium

### Trending Signals (Feb 7-12):
- **inference-sh** — 150+ AI apps gateway (continued growth)
- **media generation cluster:** podcast, social video, product photography, voice cloning
- **orchestration tools:** ai-automation-workflows, planning-with-files
- **Superpowers** — planning-first TDD workflow (top 10 recommended)
- **humanizer** — remove AI writing patterns
- **marketingskills** — CRO/copywriting/psychology

## 🎯 Actionable Items (Feb 12)

| # | Priority | Action | Status |
|---|----------|--------|--------|
| 1 | ⭐ CRITICAL | Study Claude Code Agent Teams architecture — compare with ralph-loop | **NEW** |
| 2 | ⭐ HIGH | Evaluate Skillkit CLI (`agentskills.com`) — potential workflow improvement | **NEW** |
| 3 | ⭐ HIGH | Evaluate Google Dev Knowledge MCP for GCP/Firebase accuracy | **NEW** |
| 4 | ⭐ HIGH | Review CoSAI + Cisco CodeGuard for our security-scan integration | **NEW** |
| 5 | ⭐ HIGH | Evaluate inference-sh for game trailer audio/podcasts | CARRY |
| 6 | ⭐ HIGH | Study Anthropic frontend-design for game UI patterns | CARRY |
| 7 | ⭐ HIGH | Study Anthropic skill-creator best practices | CARRY |
| 8 | 🟢 MEDIUM | Absorb Superpowers TDD workflow patterns into ralph-loop | CARRY |
| 9 | 🟢 MEDIUM | Absorb marketingskills (SEO, copy, psychology, pricing) | CARRY |
| 10 | 🟢 MEDIUM | Absorb humanizer patterns for game descriptions | CARRY |
| 11 | 🟡 LOW | Monitor AGNXI curation approach for discovery | **NEW** |
| 12 | 🟡 LOW | Monitor Amazon Ads MCP for future monetization | **NEW** |

## 💰 Pricing Landscape

| Platform | Model | Scale | Security |
|----------|-------|-------|----------|
| **skills.sh** | FREE (open) | 48K+ installs | Versioned ✅ |
| **SkillsMP** | FREE (directory) | 185K indexed | No audit ⚠️ |
| **ClawHub** | FREE (registry) | 5K+ skills | VT scanning, still risky ⚠️ |
| **AGNXI** | FREE (curated) | 8K+ skills | Human-curated ✅ |
| **Skillkit** | FREE (open-source) | New launch | Audit needed 🔍 |

## 🔮 Trend Forecast
1. **Multi-agent coordination** is exploding — Claude Agent Teams, OpenCode port, Docker-per-agent pattern
2. **Media generation skills** (video/audio/image) becoming the next frontier after code skills plateau
3. **Security frameworks** (CoSAI, CodeGuard) becoming mandatory for enterprise agent deployments
4. **Skill package managers** (skills.sh, Skillkit) consolidating — expect npm-like ecosystem by Q2
5. **MCP enterprise adoption** accelerating — Amazon, Google, Miro, HubSpot, Salesforce all launching servers
