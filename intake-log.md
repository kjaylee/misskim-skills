# misskim-skills intake log

## 2026-02-08 Agent skill trend sweep (20:00 KST)
Sources: SkillsMP (skillsmp.com), skills.sh (Vercel), LobeHub MCP Marketplace, ClawHub security reports, Molt Road analysis, VSCode Copilot Agent Mode, scriptbyai.com top-10 list, creative-tim skills.sh guide, GitHub trending, Snyk/Veracode/HackerNews security advisories.

### 🔥 Key Developments This Week

1. **skills.sh (Vercel) — NEW MAJOR PLAYER**: Vercel launched skills.sh, an open Agent Skills directory with `npx skills add` CLI. 20K+ installs in launch week. Top all-time: `find-skills`, `vercel-react-best-practices`, `web-design-guidelines`, `remotion-best-practices`, `frontend-design` (Anthropic), `vercel-composition-patterns`, `agent-browser`, `skill-creator` (Anthropic), `browser-use`. Pricing: Free/open-source. **Action: HIGH PRIORITY — audit vercel-labs/agent-skills repo for React/Next.js patterns to merge into our web-design-pro and ui-ux-pro-max.**

2. **inference.sh ecosystem — TRENDING**: Dominating 24h trending on skills.sh. Includes `inference-sh` (150+ AI apps via infsh CLI), `agentic-browser` (Playwright + inference.sh), `ai-podcast-creation`. **Action: Evaluate inference-sh as a multi-model gateway skill for misskim-skills.**

3. **LobeHub MCP Marketplace — TOP SERVERS (Feb 8)**: Context7 (35K stars, version-specific docs), Playwright Browser (22K stars), BlenderMCP (14K stars), 21st.dev Magic UI Builder (3.8K stars), Firecrawl (3.3K stars), AntV Charts (3K stars), Tavily web search (2.1K stars), grep.app code search (new featured), Postgres MCP Pro. **Action: Context7 + grep.app are directly useful for our dev workflow — evaluate as MCP server additions.**

4. **🚨 ClawHub SECURITY CRISIS**: 341+ malicious skills discovered (Snyk, 1Password, Veracode, The Register, HackerNews). 7,743 downloads on the most popular malicious package alone. Credential theft, reverse shells, crypto stealers. ClawHub maintainer admitted registry cannot be secured. **Action: ZERO skills from ClawHub without full manual audit. Reinforce our Research→Audit→Rewrite policy.**

5. **Molt Road — CONFIRMED ILLICIT MARKETPLACE**: Security researchers (InfoStealers, Vectra AI) confirm Molt Road is a black market for autonomous agents trading stolen credentials, weapon skills with reverse shells. **Action: DO NOT ENGAGE. Monitor for threat intelligence only.**

6. **Top 10 Skills List (scriptbyai.com, Feb 2026)**: Superpowers (planning-first dev), ui-ux-pro-max (design systems), agent-skills (Vercel/React), planning-with-files (Manus workflow), context-engineering, obsidian-skills, scientific-skills, marketingskills (CRO/copy), dev-browser, humanizer. **Action: We already have ui-ux-pro-max. Evaluate Superpowers' TDD/debugging workflows and planning-with-files' persistent markdown approach.**

7. **VSCode Copilot Agent Mode**: Now reads SKILL.md files natively. SkillsMP indexes Microsoft's own skills (9.3K stars, 1.6K forks). Skills work cross-platform: Claude Code, Cursor, Copilot, Gemini CLI, OpenCode. **Action: Ensure all misskim-skills have proper SKILL.md frontmatter for cross-platform compat.**

8. **OpenClaw hits 146K GitHub stars** (up from ~130K). Neovim agent "99" by ThePrimeagen gaining traction (2.8K stars). `claude-mem` automatic memory capture at 16.9K stars. **Action: Evaluate claude-mem patterns for our memory system improvement.**

### Pricing Snapshot
| Platform | Model | Price |
|----------|-------|-------|
| skills.sh | Open directory + npx CLI | Free |
| SkillsMP | Browsable catalog (66K-87K skills) | Free browse, compute cost only |
| SkillHub | Curated + graded (15K skills) | Free tier / Pro $9.99/mo / Agent $19-199/mo |
| LobeHub MCP | Open-source MCP servers | Free (MIT) |
| ClawHub | Marketplace (COMPROMISED) | Free but HIGH RISK |

### Actionable Items (Priority Order)
1. **P1**: Audit `vercel-labs/agent-skills` for React/Next.js/web-design patterns → merge into our skills
2. **P1**: Add SKILL.md cross-platform frontmatter to all misskim-skills
3. **P2**: Evaluate inference.sh as multi-model gateway
4. **P2**: Evaluate Context7 + grep.app MCP servers for dev workflow
5. **P2**: Study Superpowers' TDD workflow + planning-with-files' persistent markdown pattern
6. **P3**: claude-mem memory patterns → improve our memory system
7. **P3**: Remotion best-practices skill → useful for video-pro skill
8. **SECURITY**: Zero ClawHub installs without manual audit. Update security policy docs.

---

## 2026-02-05 Agent skill trend sweep
Sources: SmartScope SkillsMP guide (Feb 2026), CherryHQ MCP Market README, SkillHub rankings page, ClawNews Molt Road skill post, formulahendry VS Code Agent Skills extension README.

- **SkillsMP** now counts 66,541 SDLC-aligned skills and highlights the planning/design stack (`architecture`, `adr`, `project-planner`, `roadmap-generator`), implementation/QA (`code-reviewer`, `repo-rag`, `requesting-code-review`, `test-master`, `test-generation`, `writing-go-tests/py-tests`), security (`secure-code-guardian`, `vulnerability-scanning`, `security-reporter`), deployment (`iac-terraform`, `terraform-docs`) and ops (`cost-optimization`, `database-optimizer`). Pricing: the marketplace itself is free to browse; executing a skill costs whatever Claude/Codex/ChatGPT plan is running it. Action: package a planning/ADR stack, extend our QA/testing skill set with the test-master/test-generation/test-driven patterns, add Terraform doc guards and ops-health monitors to `misskim-skills`.
- **MCP Market** is a pnpm monorepo of `@mcpmarket/*` MCP servers with TypeScript typings, consistent protocol definitions, and a CLI-driven `@mcpmarket/auto-install` that discovers servers via natural-language `add-source` commands. Pricing: MIT-licensed packages install freely via pnpm; the only cost is running the MCP infrastructure. Action: hook our curated MCP servers into the `auto-install` pipeline, add a `mcpmarket-watch` skill that polls npm tags/registry for upstream updates, and stage connectors (agents-md, mcporter, data connectors) to auto-sync alongside the pipeline.
- **SkillHub** ranks 15,000+ curated skills with LLM evaluations. The S/A leaders include `gh-ticket`, `systematic-debugging`, `breaking-change-detector`, `condition-based-waiting`, `repairing-geometry-issues`, `pci-compliance`, `secrets-management`, `accessibility-design`, `qa-refactoring`, `biopython`, `data-modeling`, `mermaidjs-v11`, `AgentDB Performance Optimization`, `rdkit`, `software-localisation`, `scanpy`, `ffuf`, `plotly`, `qa-resilience`, `claude-cli`, `wordpress-plugin-core`, `error-tracking`, `az`, `1k-date-formatting`, `hallucination-detector`, `building-nextjs-apps`, `6_stripe-integration`, and `test-driven-development`. Pricing: the landing page touts a free weekly digest/premium stack preview (“Weekly digest. No spam. Free forever”) but specific Pro/Agent tiers are gated behind the account. Action: absorb the debugging/security flows, QA resilience/condition-based waiting, and compliance/anomaly-detection patterns into our QA/security stack, and capture SkillHub’s ranked signals in a weekly digest for inspiration.
- **Molt Road** provides an autonomous marketplace API (POST `/register` to secure an API key + 100 credits, GET/POST `/listings`, POST `/orders`, POST `/bounties`, POST `/orders/:id/deliver`) backed by escrow, ratings, badges, a bounty board, and listing comments. Pricing: register to get 100 starter credits; additional credit pricing is not published yet. Action: build a `moltroad-watch` skill that polls `/listings` for escrowed/high-trust opportunities, filters by keyword/price/ratings, and escalates high-value bounties/orders into our automation queue.
- **VS Code Agent Skills extension** (formulahendry) is a free marketplace that lets you browse multiple GitHub repos, search, one-click install, and manage skills in `.github/skills` or `.claude/skills`, with GitHub-token-backed metadata caching (default TTL 3600s) and workspace sync. Pricing: free on the VS Code Marketplace. Action: mirror its metadata+caching approach by auto-publishing bundle metadata to `.github/skills`, exposing our own `agentSkills.skillRepositories` mirror in repo manifests, and emitting update alerts when new bundles arrive.

## 2026-02-05 Agent skill trend sweep (update)
Sources: SmartScope SkillsMP guide (Feb 2026), Medium “SkillsMP: This 87,427+ Claude Code Skills Directory Just Exploded” (Jan 2026), SkillHub home/pricing/rankings, Brave search snippets for MCP Market’s Agent Builder & Codex Skill Builder, ClawNews Molt Road post, Visual Studio Marketplace Agent Skills extension page.

- **SkillsMP** now hosts 66,541 (SmartScope) and growing toward 87,000+ skills (Medium) across Claude/Codex/ChatGPT; the SDLC guide spotlights plan/design automations (`architecture`, `adr`, `project-planner`, `roadmap-generator`), implementation/testing (`code-reviewer`, `repo-rag`, `test-master`, `test-generation`, `writing-go-tests`, `writing-py-tests`), safety/security (`secure-code-guardian`, `vulnerability-scanning`, `security-reporter`), deployment (`iac-terraform`, `terraform-docs`), and ops (`cost-optimization`, `database-optimizer`). The catalog is open SKILL.md plus GitHub-sourced, so browsing is free and the only spend is the host Claude/Codex compute. Action: assemble these plan/test/ops stacks, queue test-generation/test-master and Terraform doc guards into `misskim-skills`, and add a watcher that surfaces category/popularity signals to keep updates synchronized.

- **MCP Market** is pushing meta utilities: Agent Builder carves focused sub-agents for repeated roles (code review, debugging, data analysis) to prevent context pollution, while Codex Skill Builder automates SKILL.md creation/maintenance (goals, triggers, tool permissions) so new skills stay structured. The packages themselves are MIT/PNPM free modules—the only cost is the MCP runtime we already host. Action: add a `skill-builder` automation that scaffolds new SKILL.md bundles and mirror the Agent Builder pattern inside our QA workflow so each `misskim-skills` skill ships with a curated trigger/permission blueprint.

- **SkillHub** grades 15k+ skills; S-rank/high-rated ones recently surfaced include `file-search`, `systematic-debugging`, `doc-coauthoring`, `doc-review`, `frontend-design`, `backend-models-standards`, `skill-builder`, and premium Skill Stacks such as the Solopreneur Toolkit (15 credits) and the AI Video Ad Generator (11 skills, 50 credits). Pricing: Pro is US$9.99/month (50 queries/day, priority search, early features) plus credit packs, while managed Agent plans range from $19/mo (Starter) to $199/mo (Team). Automation features include CLI/search commands (`npx @skill-hub/cli install frontend-design`, `search "react"`), AI-powered search assistant with daily quota that can be extended via API keys/credits, weekly S-rank alerts/digest, and premium Skill Stacks unlocked via credits. Action: absorb SkillHub’s debugging/security flows (systematic-debugging, breaking-change-detector, QA resilience, condition-based waiting, compliance/security skills) into our test/security catalog, and mimic the weekly digest/alert model when tagging new S/A skills for `misskim-skills`.

- **Molt Road** presents an autonomous marketplace API (POST `/register` returns API key + 100 credits, `/listings`, `/orders`, `/bounties`, `/orders/:id/deliver`) with escrow, rating/badge trust signals, bounty boards, and listing comments. Additional credits (beyond the starter 100) are not yet public. Action: craft a `moltroad-watch` skill that polls listings, filters by escrowed/high-rated opportunities, and escalates high-tier bounties/orders into our automation queue so agents can respond immediately.

- **VS Code Agent Skills extension** (formulahendry) is a free marketplace UI with search, one-click install, skill details (SKILL.md docs), configurable GitHub skill repositories, install locations (`.github/skills` vs `.claude/skills`), GitHub token support, and metadata caching (default TTL 3600s). Action: replicate its metadata/caching blueprint, publish curated bundle metadata to `.github/skills`, expose our own `agentSkills.skillRepositories` mirror, and emit repo-level alerts when bundles are updated so downstream installs stay fresh.

## 2026-02-04 Agent skill trend sweep
Sources: SmartScope SkillsMP guide, awesome-openclaw-skills README, SkillHub rankings, ClawNews Molt Road page, VS Code "Agent Skills" extension doc.

- **SkillsMP** now catalogs ~145,000+ skills (up from 66k) for Claude/Codex/ChatGPT, and the new SmartScope SDLC guide highlights turnkey prompt templates such as `architecture`, `project-planner`, `adr`, `roadmap-generator`, `code-reviewer`, `repo-rag`, `test-master`, `test-generation`, `secure-code-guardian`, and `iac-terraform`. Action: package a planning/ADR skill that bundles those templates and expand our QA set with the `test-master`/`test-generation` automations plus Terraform documentation checks.
- **Vercel Agent Skills** (`vercel-labs/agent-skills`) and the `skills` NPM package are trending as the "official" web dev standard. Action: Audit Vercel's collection for Next.js/React best practices to merge into `ui-ux-pro-max`.
- **MCP Market / awesome-openclaw-skills** (used as its discovery source) lists dozens of MCP-focused skills: `mcp-builder`, `mcporter`, `mcp-registry-manager`, `scrappa`, `openai-docs-skill`, `skill-scanner`, `penfield` memory tooling, and connectors for Guru, ClickUp, Snowflake, Microsoft Ads, Swiggy, etc. Action: create a `skill-scanner` guard, an MCP-registry watcher, and a mcporter-style helper that keeps our curated MCP servers in sync.
- **SkillHub** trending S/A skills include `file-search`, `context-optimization`, `frontend-design`, `systematic-debugging`, `doc-coauthoring`, `docs-review`, `xlsx`, `backend-models-standards`, `skill-builder`, `mcp-builder`, `memory-systems`, and `skill-creator`. Pro membership is $9.99/mo and Agent plans start at $19/mo (Starter) up to $199/mo (Team). Action: absorb the systematic-debugging/docs-review flows into our debugging/test stack and capture a weekly digest of SkillHub S-rank signals for inspiration.
- **Molt Road** (ClawNews) publishes a marketplace API (POST /register with 100 credits, GET/POST /listings, POST /orders, POST /bounties, POST /orders/:id/deliver) backed by escrow, ratings, badges, bounty board, and listing comments. Action: build a `moltroad-watch` skill that polls `GET /listings`, filters by keywords/escrow status, and fires alerts for high-value items so our agents can respond automatically.
- **VS Code Agent Skills extension** (formulahendry) is a free marketplace UI with search/install, GitHub-token-backed caching, configurable skill repositories, selectable install location (.github/skills vs .claude/skills), and background sync. Action: mirror its metadata/caching approach when publishing bundles so our `misskim-skills` repo can drive auto-install scripts + update notifications.

## 2026-02-04 Agent skill trend sweep (follow-up)
Sources: SmartScope SkillsMP guide (Jan 2026 figures), SkillHub home/pricing/rankings, CherryHQ MCP Market README, ClawNews Molt Road update, VS Code Agent Skills README.

- **SkillsMP** now lists 66,541 skills across Claude/Codex/ChatGPT with breakdowns (Tools 22,813, Development 19,563, Data & AI 13,091, Business 11,814, DevOps 11,013, Testing & Security 8,126, Documentation 5,704). Signature automations: planning (architecture, adr, project-planner, roadmap-generator), implementation (code-reviewer, repo-rag, requesting-code-review), testing (test-master, test-generation, writing-go-tests/py-tests), security (secure-code-guardian, vulnerability-scanning, security-reporter), deployment (iac-terraform, terraform-docs), ops (cost-optimization, database-optimizer). Action: repackage a planning/ADR stack + QA suite (test-master/test-generation) and add Terraform infra checks + ops health checkers to `misskim-skills`.
- **SkillHub** curates 15,000+ skills graded on Practicality, Clarity, Automation, Quality, and Impact. S-rank (≥9.0) leaders include `gh-ticket`, `systematic-debugging`, `breaking-change-detector`, `condition-based-waiting`, `repairing-geometry-issues`, `pci-compliance`, `secrets-management`, `accessibility-design`, `qa-refactoring`, `biopython`, `data-modeling`, `mermaidjs-v11`, `AgentDB Performance Optimization`, `rdkit`, `software-localisation`, `scanpy`, `ffuf`, and `plotly`. Pro plan is $9.99/month (50 queries/day + priority search), credits from $4.99/50; agent hosting tiers run $19/$49/$99/$199. Action: surface SkillHub S/A winners in a weekly digest, absorb debugging/security flows (systematic-debugging, breaking-change-detector, secrets mgmt, accessibility design) and integrate `qa-refactoring`/`condition-based-waiting` style guardrails into our QA/testing pipeline.
- **MCP Market** (CherryHQ repo) is now a pnpm-organized monorepo of `@mcpmarket/*` servers with TypeScript typings, CLI auto-installation, and consistent MCP protocol definitions. Highlight: `@mcpmarket/auto-install` discovers MCP servers via natural language `add-source` commands. Action: plug our curated MCP servers into that auto-install pipeline, create a `mcpmarket-watch` skill that checks npm tags/registry, and add watchers for connectors we rely on (agents-md, mcporter, data connectors).
- **Molt Road** exposes an autonomous marketplace API (register → 100 credits, listings, escrow orders, bounties, deliver endpoint) plus trust features (escrow, ratings, badges, bounty board, listing comments). Action: build a `moltroad-watch` skill that polls `GET /listings`, filters by escrow status/trust score, and escalates high-value bounties to our automation queue.
- **VS Code Agent Skills extension** offers a marketplace UI with repo-configurable sources, one-click install, GitHub token-backed caching, install location toggle (`.github/skills` vs `.claude/skills`), and in-memory metadata caching with a customizable timeout. Action: emulate its metadata+cache syncing for `misskim-skills` (auto-publishing metadata to `.github/skills`, expose `agentSkills.skillRepositories` mirror, and emit update alerts when new bundles appear).

---

## 2026-02-09 00:00 KST — Agent Skill Trend Sweep

### 🔥 HEADLINE: OpenClaw × VirusTotal Partnership (Feb 8)

**The biggest story this cycle.** After the 341 malicious skills scandal, OpenClaw partnered with Google's VirusTotal for automated ClawHub scanning:
- All published skills now undergo SHA-256 hashing → VirusTotal lookup → Gemini-powered Code Insight analysis
- Malicious → instant block. Suspicious → warning label. Benign → auto-approved
- **Daily re-scans** of all active skills (detects time-bomb mutations)
- Coverage: The Register, HackerNews, The Verge, The Decoder, CyberSecurityNews

**Assessment:** Positive step, but NOT a silver bullet. SKILL.md prompt injection attacks are fundamentally harder to detect than binary malware. Our policy stands: **Research → Audit → Rewrite → misskim-skills. No blind installs.**

### 🆕 New Tools & Skills Discovered

#### 1. **skillc** (govctl-org/skillc) — Agent Skills Development Kit
- CLI: `skc init` → `skc lint` → `skc build` → `skc stats` → publish
- Validates SKILL.md structure, links, quality
- Tracks how agents actually use skills (usage stats)
- Written in Rust 🟢 (aligns with our stack)
- **License:** Open-source
- **Action:** ⭐ EVALUATE — Use for skill authoring QA in misskim-skills

#### 2. **Skillradar** — Semantic Agent Skill Discovery
- Indexes 2,500+ skills with semantic search
- Agent-native mode: natural-language → structured search → ranked candidates
- Web UI + CLI integration
- **License:** Open-source
- **Action:** 🟢 TEST — Useful for discovering niche skills by task description

#### 3. **Top 10 MCP Servers for AI Builders (AnalyticsVidhya, Feb 5)**
New entrants vs. prior surveys:
- **Figma MCP** (official) — Design file → code. Read frames, components, design tokens
  - **Action:** ⭐ HIGH — Game UI mockup → code pipeline
- **Stripe MCP** (official) — Revenue, billing, subscription management
  - **Action:** 🟡 MONITOR — Useful when monetization scales
- **Vercel MCP** (official) — Deployment inspection, build logs, debugging
  - **Action:** 🟢 TEST — If we deploy anything to Vercel
- **Notion MCP** — Real-time doc automation
  - **Action:** 🟡 MONITOR — Depends on Notion adoption

#### 4. **Context7 Free Tier Slashed by 92%**
- Was generous free tier, now heavily rate-limited
- Still useful but paid plan may be needed for heavy use
- **Action:** 🟡 REASSESS — Check if free tier sufficient for our coding workflow

#### 5. **25+ Agent Skill Registries Index (Medium, Feb 5)**
Confirms ecosystem consolidation:
- Skills = internal expertise (SKILL.md packages)
- MCP = external services/tools
- Trend: Both converging into unified "agent capability" model

### 📊 Market Metrics Update

| Metric | Last Sweep (Feb 8) | Current (Feb 9) | Delta |
|--------|-------------------|------------------|-------|
| SkillsMP total skills | 87K+ | 87K+ (stable) | — |
| LobeHub MCP featured | 9 servers | 9 servers | — |
| ClawHub security | 341 malicious | VirusTotal scanning live | ⬆️ |
| skills.sh (Vercel) | 20K installs | Growing | ⬆️ |
| skillc (new) | — | Launched | 🆕 |
| Skillradar (new) | — | 2.5K indexed | 🆕 |
| VSCode 1.109 | Agent Skills GA | Stable | — |

### 🎯 Actionable Items (Feb 9 Delta)

| # | Priority | Action | Status |
|---|----------|--------|--------|
| 1 | ⭐ CRITICAL | Monitor VirusTotal scanning effectiveness on ClawHub | NEW |
| 2 | ⭐ HIGH | Evaluate skillc (Rust CLI) for misskim-skills QA | NEW |
| 3 | ⭐ HIGH | Test Figma MCP for game UI design → code | NEW |
| 4 | 🟢 MEDIUM | Test Skillradar for skill discovery | NEW |
| 5 | 🟡 MONITOR | Context7 pricing changes (92% free tier cut) | NEW |
| 6 | ⭐ CARRY | Audit all misskim-skills for credential exposure | ONGOING |
| 7 | ⭐ CARRY | Install Brave Search MCP + DocFork MCP | PENDING |
| 8 | ⭐ CARRY | Ensure SKILL.md cross-platform compat | PENDING |

### 🔒 Security Landscape
- ClawHub → VirusTotal scanning: Auto-block malicious, warn suspicious, re-scan daily
- Atomic Stealer (AMOS) campaign via typosquatted skills: **ACTIVE** (targets Mac users)
- Gen Agent Trust Hub: Free pre-scan tool available
- arXiv study: 26.1% of skills have vulnerabilities (unchanged)
- **Our policy reinforced:** No blind installs. Ever.

---

*Sweep completed: 2026-02-09 00:00 KST*
*Next sweep: 2026-02-10 00:00 KST (daily) / Full monthly: 2026-03-09*
