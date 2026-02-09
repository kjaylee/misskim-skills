# Agent Skill Trend Sweep — 2026-02-09 08:00 KST

## Marketplaces Surveyed
- ClawHub (clawhub.ai)
- SkillzWave Marketplace
- Agent37.com
- LobeHub MCP Marketplace (lobehub.com/mcp)
- VSCode Agent Skills (Copilot v1.109)
- claude-plugins.dev, mcpservers.org

---

## 🚨 #1 — ClawHub Security Crisis (CRITICAL)

**Status:** Ongoing, mitigation deployed

- **341 malicious skills** found by Koi Security across 2,857 audited skills (~12% infection rate)
- Campaign "ClawHavoc": Atomic Stealer (AMOS) delivered via fake "Prerequisites" install steps
- Targets: macOS (shell via glot.io → C2 at 91.92.242.30) and Windows (trojanized ZIP)
- Categories exploited: crypto wallets, YouTube tools, Google Workspace, auto-updaters, typosquats
- Additional: reverse shells (polymarket skills), credential exfil to webhook.site
- Coverage: The Verge, The Register, HackerNews, Cisco, Bitdefender, Snyk, Noma Security
- **Response (2026-02-08):** OpenClaw partnered with VirusTotal — all skills now scanned via Code Insight. Daily re-scans. Flagging/blocking system live.
- **Our policy remains:** REJECT all ClawHub skills. Audit → Rewrite into misskim-skills. No exceptions.

---

## 🔥 #2 — Top Trending Skills (Cross-Platform)

### From ScriptByAI "10 Best Agent Skills 2026":
1. **Superpowers** (obra/superpowers) — Planning-first dev workflow, TDD, debugging. ⭐ Most popular.
2. **ui-ux-pro-max** — Design system generator. ✅ We already have this.
3. **Vercel agent-skills** — React/Next.js optimization, a11y audits, Vercel deploy.
4. **planning-with-files** — Persistent task tracking via markdown files ("Manus" workflow).
5. **context-engineering** — Building custom agent systems.
6. **obsidian-skills** — Obsidian vault integration. ✅ We have obsidian skill.
7. **claude-scientific-skills** — Scientific computing workflows.
8. **marketingskills** — CRO and copywriting.
9. **dev-browser** — Visual browser testing.
10. **humanizer** — Remove AI writing patterns.

### Emerging on LobeHub MCP:
- **Context7 MCP** — Version-specific documentation injection. Featured, Feb 7.
- **Financial Analyst MCP** — Stocks analysis. 43 installs in 3 days.
- **Lightning Faucet** — Bitcoin Lightning Network send/receive via MCP.
- **Basecamp/ClickUp/Housecall Pro MCP** — Project management integrations (2026 complete versions).

---

## 🆕 #3 — VSCode Copilot v1.109 (Jan 2026 Release)

Major agent upgrades:
- **Skills now first-class** — Enabled by default for all users (was experimental in v1.108)
- **Parallel subagent execution** — Multiple subagents run concurrently
- **Fine-grained tool access** — Restrict tools per subagent (read-only agents, etc.)
- **Custom skill locations** — `chat.agentSkillsLocations` setting for shared team skills
- **Extension-contributed skills** — Extensions can bundle skills
- **Claude integration** — Anthropic Claude supported as agent backend in VS Code
- **Implication:** Agent Skills are becoming the universal standard. 25+ platforms support them now.

---

## 💰 #4 — Monetization Landscape

### Agent37.com
- **Paid skill marketplace** — Upload skill, set price, get shareable link
- Focus: Non-technical users who can't use Claude Code/Codex directly
- Creating a "digital economy" around skills
- **Opportunity:** If we build quality skills, Agent37 is a monetization channel

### SkillzWave Marketplace
- Cross-platform skill distribution (Claude Code, Codex, Gemini, Cursor, GitHub Copilot)
- Open source `skilz` CLI as universal installer
- Network effects from 25+ platform support

### Claude-plugins.dev
- Community recommended as "most helpful" catalog besides official (Reddit r/ClaudeAI)

---

## 📊 #5 — Industry Trends

1. **Skills vs MCP convergence** — Skills = internal expertise, MCP = external tools. dbt released agent skills that complement their MCP server. Pattern: skill instructs HOW, MCP provides WHAT.
2. **Security as differentiator** — Post-ClawHub crisis, audited/verified skills are premium. Our "audit → rewrite" policy is now a competitive advantage.
3. **Meta-MCP pattern** growing — Single orchestrator managing multiple MCP servers (Roundtable, Magg). Reduces tool bloat.
4. **Sandboxed execution** — Container-based isolation (Dagger container-use, Piston) becoming standard for agent safety.
5. **Moltbook social network** — AI agents interacting autonomously on Reddit-style platform. Security concerns rising.

---

## ✅ Actionable Items

### Immediate (This Week)
1. ✅ **INTAKE.md updated** with ClawHub/VirusTotal developments
2. 🔲 **Audit `Superpowers`** (obra/superpowers) — Most popular skill globally. Evaluate if planning-first workflow complements ralph-loop or should be absorbed
3. 🔲 **Audit `planning-with-files`** — Persistent markdown task tracking. Could enhance our subagent workflows
4. 🔲 **Audit `humanizer`** — AI writing pattern removal. Useful for blog/marketing content

### Short-Term (This Month)
5. 🔲 **Evaluate Agent37 monetization** — Test uploading a skill to agent37.com for paid distribution
6. 🔲 **Context7 MCP evaluation** — Version-specific docs injection could improve coding accuracy
7. 🔲 **Marketing skills audit** — CRO/copywriting skill for game-marketing pipeline

### Strategic
8. 🔲 **Publish misskim-skills to SkillzWave** — Cross-platform distribution via `skilz` CLI
9. 🔲 **Security badge program** — Differentiate misskim-skills as "audited & verified" in marketplaces
10. 🔲 **VSCode skill compatibility** — Ensure misskim-skills work in VS Code Copilot (shared format)

---

## ❌ Rejected This Sweep
- All ClawHub unverified skills (security policy)
- Unity3D MCP (stack directive)
- Heavy JS/TS-only MCP servers without Rust path
