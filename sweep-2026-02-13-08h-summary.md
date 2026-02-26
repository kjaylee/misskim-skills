# Agent Skill Trend Sweep — 2026-02-13 08:00 KST

## 📊 Executive Summary
**MICROSOFT ENTERS SKILLS RACE:** Microsoft published `github.com/microsoft/skills` — 126 Agent Skills for Azure/Foundry dev (Cosmos DB, Foundry IQ, Voice Live, AZD Deploy). Skills.sh + SkillsMP already index them. This is the first Big Tech-authored skill collection using the SKILL.md open standard. **CLAWHUB UNDER SIEGE (WEEK 2):** Snyk ToxicSkills confirmed 534 critical-level issues (13.4% of 3,984 scanned), 36% have at least one flaw. Threat actors shifted from embedded payloads to off-platform lures (HunterStrategy Feb 9). OpenClaw ↔ VirusTotal partnership now live for automated scanning. **COMMUNITY GROWTH:** VoltAgent awesome-openclaw-skills now curates 3,002 skills from ClawHub's 5,705 total (filtered 2,703 spam/malicious/dupes). Reddit r/AI_Agents top-recommended: github, agentmail, linear, playwright-scraper, playwright-mcp, obsidian-direct, automation-workflows, monday. **MCP MARKET:** Context7 (35K★), Playwright (22K★), BlenderMCP (14K★) dominate LobeHub. Top-15 MCP list: Markdownify, Heroku, SQLite, Stripe, GitHub, Grafana, Google Tasks, GSuite, Twitter/X, Slack, React Analyzer. **MOLT ROAD CONFIRMED THREAT:** Vectra AI published deep analysis (Feb 11) — agent-only black market with API-based registration, bounty system, reputation scores. Hard-deny maintained.

## 🆕 New Findings (Since 04:00 Sweep)

### 1. Microsoft Agent Skills — Official 126-Skill Collection (MAJOR)
- **Repo:** `github.com/microsoft/skills` with browsable site at `microsoft.github.io/skills`
- **Coverage:** Cosmos DB, Foundry IQ, AZD deployment, Voice Live, Azure AI Search, + 120 more
- **Includes:** Skills + Prompts + Agent personas (backend/frontend/infra/planner/scaffolder) + MCP configs
- **Context7 Integration:** Daily-updated Foundry docs indexed for version-specific retrieval
- **Anti-Pattern Warning:** "Context Rot" — don't load all skills; selective loading only
- **Distribution:** `npx skills add microsoft/skills` via skills.sh + SkillsMP indexed
- **Impact:** ⭐⭐ HIGH — Validates SKILL.md as cross-platform standard. Microsoft's "activation context" framing matches our Progressive Disclosure pattern.

### 2. ClawHub Security Situation Worsening
- **Snyk final numbers:** 3,984 scanned → 534 critical (13.4%), 1,467 any-severity (36.8%)
- **76 confirmed malicious payloads** via human-in-the-loop review (credential theft, backdoors, data exfil)
- **8 malicious skills still live on ClawHub** at time of Snyk publication
- **New tactic (Feb 9):** Attackers shifted to off-platform lures — clean SKILL.md pages pointing to external malicious downloads
- **VirusTotal partnership:** Now scanning all new skill submissions
- **Fake VSCode extensions:** Moltbot/OpenClaw-themed extensions dropping ScreenConnect malware
- **Impact:** ⚠️ RED — Zero-blind-install policy absolutely critical. External audit mandatory.

### 3. Reddit Community Consensus on Top Skills (Feb 12-13)
- **Essential daily drivers:** github, agentmail (email infrastructure for agents), linear, playwright-mcp, obsidian-direct
- **Rising:** automation-workflows (workflow builder), monday (project management), playwright-scraper (anti-bot scraping)
- **AgentMail pattern:** Programmatic email inboxes for agents — new paradigm (agent-owned identities)
- **NextJS 16+ docs skill:** Full framework docs as skill for real-time reference

### 4. Top 15 MCP Servers (Obot AI, Feb 2026)
- **Markdownify:** Convert any file format → markdown (PDF, PPTX, audio, images)
- **Stripe Agent Toolkit:** Products, payment links, invoices, subscriptions via MCP
- **Grafana MCP:** Real-time monitoring, incident management, Prometheus/Loki queries
- **Google Tasks MCP:** Full CRUD + task ordering
- **GSuite MCP:** Gmail + Calendar integration
- **Twitter/X MCP:** Timeline, search, posts, DMs
- **React Analyzer MCP:** Component analysis for large codebases

### 5. Molt Road Update (Vectra AI, Feb 11)
- **Confirmed architecture:** Agent-only marketplace, API registration, service exchange, bounty system, reputation scoring
- **Humans are observers only** — cannot participate
- **Stolen credentials + weaponized skills + zero-day exploits** traded
- **230+ malicious skills originated from this ecosystem**
- **Impact:** Hard-deny ALL Molt Road origins. Never scrape or interact.

## 📈 Marketplace Status

| Platform | Count | Notes |
|----------|-------|-------|
| ClawHub | 5,705 skills | 3,002 curated (VoltAgent). VirusTotal scanning live |
| SkillsMP | 160K+ indexed | Largest aggregator. Includes microsoft/skills |
| skills.sh | 54K+ installs tracked | find-skills 193K+. MS skills now indexed |
| LobeHub MCP | 8,230+ servers | Context7 35K★ top |
| skill0.io | 423 curated | Anthropic official skills highlighted |
| awesome-openclaw | 3,002 | 31 categories. Filtered 2,703 spam/malicious |
| Molt Road | DENIED | Black market. Zero interaction policy |

## 🎯 Actionable Items

| # | Priority | Action | Status |
|---|----------|--------|--------|
| 1 | ⭐ CRITICAL | Evaluate Microsoft `microsoft/skills` architecture — "activation context" pattern, selective loading, Context7 integration | **NEW** |
| 2 | ⭐ CRITICAL | Study Claude Agent Teams parallel subagent pattern | CARRY |
| 3 | ⭐ HIGH | Evaluate AgentMail pattern — programmatic agent email identities | **NEW** |
| 4 | ⭐ HIGH | Evaluate Markdownify MCP — universal file→markdown conversion | **NEW** |
| 5 | ⭐ HIGH | Evaluate Stripe Agent Toolkit — potential for game monetization automation | **NEW** |
| 6 | ⭐ HIGH | inference-sh ecosystem (150+ AI apps via single skill) | CARRY |
| 7 | ⭐ HIGH | SkillShield trust scoring integration for pre-screening | CARRY |
| 8 | ⭐ HIGH | VS Code `.github/agents/*.md` tool-restricted subagent pattern | CARRY |
| 9 | ⭐ MED | BlenderMCP (14K★) for 3D pipeline enhancement | CARRY |
| 10 | ⭐ MED | automation-workflows skill — workflow builder pattern | **NEW** |
| 11 | ⭐ MED | CoSAI MCP security framework for security-scan.sh | CARRY |
| 12 | ⭐ LOW | Google Antigravity multi-agent coordination | CARRY |

## 🔒 Security Posture
- **ZERO blind installs from ANY registry** — validated by Snyk (36% injection rate)
- **Audit → Rewrite → misskim-skills/** only
- **Molt Road: HARD DENY** — confirmed adversarial (Vectra AI)
- **VSCode extensions: VERIFY publisher** — fake Moltbot extensions dropping malware
- **New off-platform lure tactic: CHECK external links** in any SKILL.md

## 🛠️ Automations Worth Absorbing

1. **Microsoft "Activation Context" Pattern:** Selective skill loading + Context7 daily-updated docs. Aligns with our Progressive Disclosure.
2. **AgentMail Architecture:** Programmatic agent email identities. Could automate game feedback collection, support tickets.
3. **Markdownify MCP:** Universal converter. Could streamline document processing in our pipeline.
4. **Stripe Agent Toolkit:** Payment automation. Relevant for game monetization when Gumroad alternatives needed.
5. **automation-workflows Skill:** Meta-skill that identifies repetitive tasks and builds automations. Self-improvement pattern.

---

**Next Sweep:** 2026-02-13 12:00 KST
