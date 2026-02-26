# 🔍 Agent Skill Trend Sweep — 2026-02-13 12:00 KST

## 📊 Market Overview

### skills.sh (Vercel) — The Dominant Open Directory
- **55,783 total installs** across ecosystem
- 20+ agents supported (Claude Code, Codex, Copilot, Cursor, Windsurf, Gemini, Kiro, Goose, Trae, AmpCode, etc.)
- Leaderboard format: All Time / Trending 24h / Hot

### skills.sh Trending 24h (Feb 13)
| # | Skill | 24h Installs | Publisher |
|---|-------|-------------|-----------|
| 1 | find-skills | 11.4K | vercel-labs |
| 2 | vercel-react-best-practices | 4.9K | vercel-labs |
| 3 | remotion-best-practices | 3.2K | remotion-dev |
| 4 | frontend-design | 2.9K | anthropics |
| 5 | web-design-guidelines | 2.8K | vercel-labs |
| 6 | content-strategy | 2.2K | coreyhaines31 |
| 7 | product-marketing-context | 2.2K | coreyhaines31 |
| 8 | agent-browser | 1.8K | vercel-labs |
| 9 | vercel-composition-patterns | 1.8K | vercel-labs |
| 10 | skill-creator | 1.4K | anthropics |

### skills.sh All-Time Top
| # | Skill | Total Installs |
|---|-------|---------------|
| 1 | find-skills | 203.3K |
| 2 | vercel-react-best-practices | 126.4K |
| 3 | web-design-guidelines | 94.8K |
| 4 | remotion-best-practices | 86.9K |
| 5 | frontend-design | 64.4K |

**Notable new entries:**
- `form-cro` (925 daily) — Form conversion rate optimization, coreyhaines31. Marketing skills suite dominates.
- `nodejs-backend-patterns` (890 daily) — wshobson. Backend patterns trending.
- `enhance-prompt` (817 daily) — google-labs-code/stitch-skills. Google's prompt engineering skill.
- `vite` (815 daily) — antfu/skills. Build tooling.
- `referral-program` (823 daily) — coreyhaines31. Viral marketing skill.

### LobeHub MCP Marketplace
Hot MCP servers (Feb 13):
| Server | Stars | GitHub Stars | Category |
|--------|-------|-------------|----------|
| Context7 (Upstash) | 3,212 | 35,324 | Docs — live library docs in prompt |
| Playwright | 4,169 | 22,487 | Browser automation |
| BlenderMCP | 820 | 13,973 | 3D modeling |
| Tavily Search | 2,197 | 434 | Web search + extraction |
| Firecrawl | 1,899 | 3,303 | Web scraping |
| AntV Charts | 1,457 | 3,058 | Chart generation |
| Grep.app | 202 | — | Code search across GitHub |
| Postgres MCP Pro | 436 | 477 | DB tuning + health checks |

### ClawHub — 500+ Skills, Security Nightmare Continues
- 341+ malicious skills confirmed (unchanged from prior sweep)
- **NEW:** Campaign shifted from embedded payloads → off-platform lures (evading VT scanning)
- Reddit r/AI_Agents post trending: "Best OpenClaw Skills" — lists GitHub, AgentMail, Linear, Playwright, Obsidian-Direct
- **Pricing:** No built-in payment. Monetization via SaaS API gating (free tier + paid API key) or consulting leads.

### VS Code Agent Ecosystem (Jan 2026 Update)
- **Copilot v1.109:** Parallel subagent execution, tool-restricted agents (`.github/agents/*.md`), Claude integration with extended thinking
- **Copilot Studio Extension:** GA (Jan 15) — pro-code agent development in VS Code
- **AI Toolkit:** Agent Framework integration for cost-efficient AI agent building
- **Skills system:** `chat.agentSkillsLocations` for shared team skill directories

### skill0 (atypica.ai) — Early-Stage Directory
- Alpha stage, community-driven skill submissions
- Skills vs MCP distinction becoming clear: Skills = internal expertise, MCP = external tools
- DeepLearning.AI launched official course: "Agent Skills with Anthropic"

### SkillsMP — Massive Scale
- 160,000+ agent skills indexed
- Cross-platform: Claude, Codex, ChatGPT
- Intelligent filtering by category, author, popularity
- Largest aggregator but quality control questionable

---

## 🚨 Security Updates

1. **ClawHub campaign evolved:** Off-platform lures bypass VT scanning. Snyk study: 36% prompt injection rate unchanged.
2. **VSCode extension supply chain:** Fake Moltbot/OpenClaw extensions confirmed active. Typosquatting campaign.
3. **Anthropic DXT flagged:** Runs with full system privileges — critical RCE vector.
4. **CoSAI + Cisco CodeGuard:** Donated for zero-trust agent security (still under evaluation).

---

## 🎯 Actionable Items for misskim-skills

### ⭐ IMMEDIATE (This Week)

1. **Absorb `coreyhaines31/marketingskills` patterns**
   - 8 skills dominating marketing category (content-strategy, SEO audit, copywriting, pricing-strategy, launch-strategy, form-CRO, referral-program, social-content)
   - Combined 80K+ installs. Our `game-marketing` could absorb these patterns.
   - **Action:** Audit coreyhaines31 repo → extract reusable marketing prompts → enhance `game-marketing` skill.

2. **Study `obra/superpowers` suite**
   - brainstorming (17.9K), systematic-debugging (9.8K), writing-plans (8.5K), executing-plans (7.5K), TDD (8.2K), subagent-driven-development (6.3K), requesting-code-review (6.9K)
   - These are meta-skills that improve agent workflow quality. Directly relevant to our progressive disclosure / ralph-loop pattern.
   - **Action:** Audit → absorb best patterns into our AGENTS.md and subagent templates.

3. **Evaluate Context7 MCP for docs**
   - 35K GitHub stars, live library documentation in prompt. Could replace outdated docs problem.
   - **Action:** Test `npx -y @upstash/context7-mcp` on MiniPC → benchmark vs RAG search.

### ⭐ HIGH PRIORITY (This Sprint)

4. **VS Code `.github/agents/*.md` pattern study**
   - Tool-restricted subagents with parallel execution. Validates and extends our progressive disclosure.
   - `tools:` whitelist, `infer: false` for dangerous agents. Copy pattern for our specs/.
   
5. **Google `enhance-prompt` skill (817 daily trending)**
   - google-labs-code/stitch-skills. Prompt engineering best practices from Google.
   - **Action:** Audit → integrate into our skill-creation workflow.

6. **`form-cro` + `referral-program` patterns**
   - Conversion optimization and viral mechanics. Directly useful for game marketing.
   - **Action:** Fold into game-marketing skill update.

### 📋 MONITOR

7. **SkillsMP growth** — 160K+ skills. Watch for quality filtering features.
8. **Pricing models** — ClawHub considering SaaS-gated skills. Potential revenue for our skills.
9. **inference-sh gateway** — 150+ AI services in single CLI. Track maturity.
10. **BlenderMCP** (13.9K stars) — Evaluate vs our blender-pipeline skill.

---

## 💰 Pricing Landscape

- **skills.sh:** Free / open-source only. No paid tier.
- **ClawHub:** Free. Monetization via SaaS API gating or consulting leads. No built-in payments yet.
- **SkillsMP:** Free discovery. Premium filtering ($?). Details unclear.
- **MCP servers:** Mostly open-source. Some premium (Tavily, Firecrawl have paid API tiers).
- **Copilot Studio:** Part of Microsoft 365 Copilot license.
- **Trend:** Skills themselves are free; value capture happens via connected SaaS APIs or consulting.

---

## 📈 Key Trends

1. **Marketing skills exploding** — coreyhaines31 suite shows demand for AI-driven marketing automation. 8 skills, combined 80K+ installs.
2. **Meta-skills gaining traction** — obra/superpowers (brainstorming, planning, debugging) shows agents need process skills, not just tool skills.
3. **Subagent orchestration becoming standard** — VS Code, Claude Code, and OpenClaw all converging on parallel subagent execution with tool restrictions.
4. **Security remains critical** — Supply chain attacks on ClawHub AND VSCode marketplace. Zero-blind-install policy validated.
5. **Context7 (live docs)** is the breakout MCP server — 35K stars. Solves a real pain point.
6. **Skill ecosystems consolidating** — skills.sh (Vercel) emerging as the npm-for-skills standard. 55K+ installs tracked.

---

*Sweep completed: 2026-02-13 12:00 KST*
*Next sweep: 2026-02-13 16:00 KST*
