# Skill Trend Sweep — 2026-02-14 12:00 KST

## 🆕 New Signals Since 08:00 Sweep

### 1. Microsoft Agent Skills — Major Ecosystem Play (Feb 11, new detail)
Microsoft released `github.com/microsoft/skills` — **126 modular skills** for Azure & Foundry development.
- Skills include: Cosmos DB, Foundry IQ, AZD Deployment, Voice Live, etc.
- Ships with pre-configured MCP servers (GitHub, Playwright, Microsoft Docs, Context7)
- Context7 integration with daily-updated Foundry documentation via GitHub Actions
- Browse at `microsoft.github.io/skills`, installable via `npx skills add microsoft/skills`
- Anti-pattern advice: "Context Rot" — loading all skills at once dilutes quality. Matches our Progressive Disclosure approach.
**Impact:** Microsoft validates the skills + MCP + AGENTS.md 3-layer model. Their "Context Rot" warning = our Antigravity pattern. Enterprise legitimacy boost for the entire skill ecosystem.

### 2. SkillsMP Scale Update — 66,541+ Skills (Jan 2026 confirmed)
SkillsMP now confirmed at 66,541+ skills with real-time GitHub-sourced updates.
- Breakdown: Tools (22,813), Development (19,563), Data & AI (13,091), Business (11,814), DevOps (11,013), Testing/Security (8,126), Documentation (5,704)
- Agent Skills open standard (agentskills.io) now backed by Anthropic, OpenAI, Microsoft, GitHub Copilot
- `skills.sh` CLI emerging as cross-platform installer (`npx skills add <org>/<repo>`)
**Impact:** The SKILL.md format is now the undisputed standard. Our skills are natively compatible.

### 3. VSCode Agent Skills Extension (formulahendry)
Extension provides marketplace UI inside VS Code:
- Browse skills from multiple GitHub repos (anthropics/skills, openai/skills, pytorch/pytorch)
- One-click install to `.github/skills/` or `.claude/skills/`
- Configurable custom repo sources, GitHub token support for rate limits
- Skills follow agentskills.io specification
**Impact:** IDE-native skill discovery is mainstream. Our misskim-skills repo could be added as a custom source.

### 4. Agent Skills Open Standard — Full Convergence
The Agent Skills spec (agentskills.io) is now the universal standard:
- **Anthropic:** Claude Code (originator)
- **OpenAI:** Codex CLI + ChatGPT agent extension
- **Microsoft:** GitHub Copilot (VS Code, CLI, coding agent)
- **Cursor:** Same SKILL.md standard
- Format: YAML frontmatter (name, description) + markdown body + optional scripts/resources
- Locations: `.github/skills/`, `.claude/skills/`, `.agents/skills/`, `~/.copilot/skills/`
**Impact:** Write once, run everywhere. Our ClawHub skills are automatically compatible with all major platforms.

### 5. Molt Road — Confirmed Adversarial (Vectra Analysis)
Vectra AI published deep analysis (Feb 10):
- Agent-only marketplace: autonomous systems register via API, exchange services, complete bounties
- Initially named "Open Road" ("Silk Road but for agents")
- Archive showed categories: substances, contraband, weapons, documents, jailbreak prompts
- Now sanitized surface but underlying mechanics unchanged
- On-chain escrow (USDC on Base) + MOLTROAD tokens
**Status:** HARD-DENY confirmed. No interaction, observation only for threat intelligence.

### 6. MCP Market — Trending Categories
MCP Market (mcpmarket.com) trending servers include:
- **Godot MCP:** Launch editor, run projects, capture debug output — *directly relevant to our stack*
- **Ghidra MCP:** Reverse engineering via LLM
- **Excel MCP:** File manipulation without MS Office
- **Unity MCP:** Automate workflows + control editor
- **Trending topics aggregator:** 35+ platforms, AI-powered analysis
- Top 2026 MCP servers: HubSpot, Salesforce, Ahrefs, GitHub, Jira, Docker Hub, Skyvia, Vectara, Slack, Notion, Google Workspace, K2view

### 7. skills.sh — New Universal Installer
`skills.sh` emerging as the CLI for cross-platform skill installation:
- `npx skills add microsoft/skills` — installs from any GitHub repo
- Pairs with SkillsMP discovery
- Potential competitor/complement to `clawdhub` CLI
**Watch:** Could become the `npm` of agent skills.

## 📊 Ecosystem Totals (Feb 14 12:00)
| Platform | Count | Trend | Notes |
|----------|-------|-------|-------|
| SkillsMP | 66,541+ | ↑ rapid | Largest, GitHub-sourced |
| SkillzWave | 42,645+ | ↑ steady | Premium tiers $299-399/mo |
| ClawHub | 5,705+ | ↑ (security crisis) | 341 malicious skills found |
| LobeHub MCP | 8,230+ | ↑ daily | MCP server registry |
| Microsoft Skills | 126 | NEW | Azure/Foundry specific |
| VSCode Extension | active | NEW | IDE-native marketplace |
| Smithery MCP | 938+ | ↑ | Curated repos |
| SkillHub | 7,000+ | ↑ | Mixed quality |
| Molt Road | ~dozens agents | ⚠️ | Adversarial, HARD-DENY |

## 🎯 Actionable Items

### 🔴 HIGH Priority
1. **Godot MCP server** — Native Godot editor control via MCP. Directly relevant to our game dev pipeline. Evaluate for MiniPC integration.
2. **Context7 integration** — Microsoft uses it for daily-updated docs. We should adopt for our Godot/Rust docs grounding.
3. **skills.sh compatibility** — Ensure our published skills work with `npx skills add`. Potential wider distribution channel beyond ClawHub.
4. **AgentMail skill** — Agent email inboxes trending hard. Useful for automated verification flows.

### 🟡 MEDIUM Priority
5. **Publish misskim-skills as VSCode source** — The Agent Skills extension supports custom repo sources. Add our repo = instant IDE discovery.
6. **Microsoft skills audit** — 126 skills for Azure. Cherry-pick patterns (Cosmos DB, Context7 integration) worth absorbing.
7. **Automation-workflows pattern** — Trigger/action workflow builder. High community demand. Could complement our cron/heartbeat system.
8. **Stripe MCP wrapper** — Payment integration still high demand signal.

### 🟢 LOW Priority
9. **Monitor skills.sh** as potential npm-of-skills. Track adoption vs clawdhub CLI.
10. **Track Codex Apps SDK** for third-party marketplace opportunity.
11. **SkillzWave premium bundles** — $299-399/mo for curated domain packs. Potential monetization for our game dev skills.

### 🔒 Security Standing
- **ClawHub:** 🔴 RED — 341 malicious skills, 9K compromised installs. Zero blind install.
- **Molt Road:** ⛔ HARD-DENY — Confirmed adversarial agent marketplace.
- **SkillzWave:** 🟡 YELLOW — AI-evaluated quality, less battle-tested.
- **SkillsMP:** 🟢 GREEN — GitHub-sourced, community-vetted, open standard.
- **Microsoft Skills:** 🟢 GREEN — Corporate-backed, open source.
- **Policy:** Audit → Rewrite → misskim-skills/. No exceptions.

## Sources Checked
- SkillsMP (smartscope.blog guide, aitoolnet listing)
- MCP Market (mcpmarket.com — Vercel-protected, search results only)
- VSCode Agent Skills Extension (marketplace.visualstudio.com)
- Agent Skills specification (agentskills.io, github.com/agentskills/agentskills)
- Microsoft Agent Skills (devblogs.microsoft.com, github.com/microsoft/skills)
- Molt Road (vectra.ai analysis, moltroad.com, X/moltroad)
- Builder.io Best MCP Servers 2026 guide
- Reddit r/AI_Agents ClawHub skills thread
- Visual Studio Magazine: VSCode 1.108 Agent Skills, Top Agentic AI Tools
- OpenAI Codex developer docs (developers.openai.com/codex/skills)
