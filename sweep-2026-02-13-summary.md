# Agent Skill Trend Sweep — 2026-02-13 04:00 KST

## 📊 Executive Summary
**VS CODE 1.109 SKILLS GO MAINSTREAM:** Agent Skills are now enabled by default in VS Code 1.109 (Feb 4 stable release) — parallel subagent execution, fine-grained tool access control, and extension-contributed skills. This is the biggest adoption catalyst since skills.sh launch. **SKILLS.SH ECOSYSTEM EXPLODES:** SkillsMP now indexes 160K+ skills (up from 185K claimed earlier — confirmed via archive.is), skills.sh at 54K+ tracked installs with find-skills leading at 193K+. Vercel's inference-sh ecosystem dominates 24h trending. **OPENAI FRONTIER LAUNCHED:** Enterprise agent platform (Feb 5) — treats agents like employees with shared business context, connects silos. Not skill-based but signals enterprise appetite. **SECURITY REMAINS RED:** Snyk confirms 36% prompt injection rate on ClawHub (1,467 malicious payloads), MCP Git server RCE patched (3 CVEs), CoSAI framework published. **NEW NOTABLE:** Skillkit PH launch (universal package manager, 28+ agent support), Google Antigravity for multi-agent coordination.

## 🆕 New Findings (Since 2026-02-12 20:00 Sweep)

### 1. VS Code 1.109 — Skills as First-Class Feature (MAJOR)
- **Parallel Subagent Execution:** Multiple runSubagent calls now concurrent (was sequential)
- **Fine-Grained Tool Access:** `.github/agents/*.md` with `tools:` whitelist per subagent
- **Extension-Contributed Skills:** Extensions can now register and provide skills natively
- **Custom Skill Locations:** `chat.agentSkillsLocations` setting for shared team skills
- **Copilot Memory:** `github.copilot.chat.copilotMemory.enabled` for persistent context
- **Claude Agent Support:** Native Claude integration in VS Code Copilot
- **Impact:** ⭐⭐ CRITICAL — Skills are no longer opt-in. Every VS Code + Copilot user now has them.

### 2. Inference.sh Ecosystem (Trending #1 on skills.sh)
- **inference-sh:** Gateway skill for 150+ AI apps (LLMs, image, video, search, Twitter, 3D) via `infsh` CLI
- **agentic-browser:** Browser automation via Playwright + inference.sh (open, snapshot, interact, @e1 selectors)
- **ai-podcast-creation:** Turn scripts into podcast episodes with TTS + AI music
- **Impact:** Full-stack AI capabilities in a single skill ecosystem. Watch for maturity.

### 3. OpenAI Frontier Enterprise Platform (Feb 5)
- **What:** Enterprise agent management — build, deploy, manage agent fleets
- **Architecture:** Shared business context, connects internal apps, ticketing, data warehouses
- **Not skill-based:** Protocol-level integration, not SKILL.md compatible
- **Impact:** Signals enterprise spending on agent infrastructure. Not directly actionable for us.

### 4. Google Antigravity (Product Hunt Mention)
- Multi-agent coordination for code builds
- Product Hunt listed alongside Cursor and Claude Code
- **Action:** 🔍 Monitor — minimal details available yet

### 5. MCP Security Landscape (February 2026 Digest)
- **3 CVEs in Anthropic Git MCP Server:** CVE-2025-68145, -68143, -68144 (path bypass, unrestricted git_init, argument injection)
- **CoSAI White Paper:** 40+ MCP threats cataloged, framework for controls/mitigations
- **OAuth Resource Servers:** MCP servers now officially classified as OAuth Resource Servers
- **Securing MCP Guide:** mTLS, zero-trust patterns published (dasroot.net)
- **Impact:** Our zero-blind-install policy vindicated. MCP attack surface growing fast.

### 6. Malicious Skills Research Update
- **Snyk ToxicSkills:** 3,984 ClawHub skills scanned → 76 confirmed malicious (human-verified)
- **arXiv Paper:** "Malicious Agent Skills in the Wild" — 98K+ skills in community registries within 3 months of launch
- **ClawHavoc Campaign:** 341 skills, 9,000+ installations compromised
- **Fake VSCode Extensions:** Moltbot/OpenClaw developer tooling used to drop malware via VSCode Marketplace
- **Impact:** ⚠️ VSCode extension supply chain attacks now confirmed vector

## 📈 Marketplace Leaderboard

### skills.sh (Vercel) — All-Time Top
| Rank | Skill | Installs | Category |
|------|-------|----------|----------|
| 1 | find-skills (vercel-labs) | 193K+ | Meta/Discovery |
| 2 | vercel-react-best-practices | 20K+ | React/Next.js |
| 3 | web-design-guidelines | — | UI/UX |
| 4 | remotion-best-practices | — | Video |
| 5 | frontend-design (anthropics) | — | Design |
| 6 | agent-browser (vercel-labs) | — | Browser |
| 7 | skill-creator (anthropics) | — | Meta |
| 8 | browser-use | — | Browser |

### skills.sh — 24h Trending
| Rank | Skill | Category |
|------|-------|----------|
| 1 | inference-sh | AI Gateway |
| 2 | agentic-browser | Browser Automation |
| 3 | ai-podcast-creation | Media |

### SkillsMP
- **160,000+ skills indexed** (largest directory)
- Top: microsoft/vscode-copilot-chat (9,413 stars, 1,628 forks)

### LobeHub MCP Marketplace
| Rank | Server | Stars |
|------|--------|-------|
| 1 | Context7 (version-specific docs) | 35,324 |
| 2 | Playwright (browser automation) | 22,487 |
| 3 | BlenderMCP (3D modeling) | 13,973 |
| 4 | Firecrawl (web scraping) | 3,303 |
| 5 | AntV Charts (chart generation) | 3,058 |
| 6 | Tavily Search | 434 |
| 7 | Postgres MCP Pro | 477 |

### Pricing
- All major skill directories: **FREE** (open source)
- No paid marketplace has gained traction
- Skillkit: Free CLI, unknown monetization plan
- OpenAI Frontier: Enterprise pricing (undisclosed)

## 🎯 Actionable Items

| # | Priority | Action | Status |
|---|----------|--------|--------|
| 1 | ⭐ CRITICAL | Study Claude Code Agent Teams — parallel subagent pattern now validated in VS Code 1.109 too | ESCALATED |
| 2 | ⭐ CRITICAL | Audit VSCode extension supply chain — fake OpenClaw/Moltbot extensions dropping malware | **NEW** |
| 3 | ⭐ HIGH | Evaluate inference-sh ecosystem (150+ AI apps via single skill) | **NEW** |
| 4 | ⭐ HIGH | Consider SkillShield integration for pre-screening (0-100 trust scoring) | CARRY |
| 5 | ⭐ HIGH | Evaluate Skillkit CLI (28+ agents, Primer/Memory/Mesh features) | CARRY |
| 6 | ⭐ HIGH | Study VS Code `.github/agents/*.md` tool-restricted subagent pattern | **NEW** |
| 7 | ⭐ MED | Monitor Google Antigravity multi-agent coordination | **NEW** |
| 8 | ⭐ MED | Review CoSAI MCP security framework (40+ threats) for security-scan.sh | CARRY |
| 9 | ⭐ MED | Evaluate BlenderMCP (13.9K stars) for 3D pipeline enhancement | **NEW** |
| 10 | ⭐ LOW | Track OpenAI Frontier for enterprise patterns (not directly usable) | **NEW** |

## 🛠️ Automations Worth Absorbing

1. **inference-sh Gateway Pattern:** Single CLI wrapping 150+ AI services. Could simplify our multi-model access.
2. **VS Code Parallel Subagents:** Fine-grained tool access + concurrent execution. Validate against our ralph-loop.
3. **SkillShield Auto-Scoring:** 4-layer analysis pipeline. Automate pre-screening before manual audit.
4. **Context7 MCP Pattern:** Version-specific docs injection into prompts. Could improve our GCP/Godot work accuracy.
5. **BlenderMCP:** Claude ↔ Blender 3D integration. Relevant for game asset pipeline.

---

**Next Sweep:** 2026-02-13 08:00 KST
