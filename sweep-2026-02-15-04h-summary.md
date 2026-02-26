# 🔍 Agent Skill Trend Sweep — 2026-02-15 04:00 KST

## 🔴 CRITICAL — Security

### ClawHavoc Escalation Continues
- **386 malicious skills** now confirmed on ClawHub (up from 341 on Feb 9)
- New tactic: clean SKILL.md + **off-platform malware lures** to evade VirusTotal scanning
- OpenClaw + VirusTotal partnership live: all skills scanned via VT Code Insight
- Snyk ToxicSkills study: **36% of ClawHub skills contain prompt injection**, 1,467 malicious payloads
- Daily submissions jumped from <50 (mid-Jan) to **500+** (early Feb) — 10x in weeks
- Top attacker `hightower6eu` has 7,000+ downloads; C2 at 91.92.242.30 still operational
- **r/cybersecurity thread** from skill marketplace operator confirms: skills run with agent's full permissions (shell, filesystem, API keys, browser)
- **Action:** Zero-blind-install policy REINFORCED. All candidates → audit → rewrite pipeline.

## 🔴 CRITICAL — OpenAI Enters Skills Ecosystem

### OpenAI Responses API: Skills + Hosted Shell + Compaction (Feb 11)
- OpenAI now supports **Agent Skills standard** natively in Responses API
- **Hosted Shell Containers**: Debian 12 managed execution environment for agents
- **Server-side Compaction**: 5M+ token session memory management
- Skills can be sent inline as **base64-encoded zips** or pre-uploaded
- Simon Willison demonstrated: `gpt-5.2` + shell tool + inline skills = instant domain expertise
- **Impact:** Skills are now a cross-platform standard — OpenAI, Anthropic, Microsoft, 25+ platforms
- **Action:** Monitor. Our skills already compatible via Agent Skills Standard.

## 🟡 HIGH — Platform Updates

### VS Code 1.109 (Jan 2026 release — GA Feb 4)
- **Agent Skills GA** — enabled by default. `.github/agents/*.md` with `tools:` whitelist
- **Copilot Memory** — cross-session memory (preview). `github.copilot.chat.copilotMemory.enabled`
- **Parallel subagent execution** — multiple agents in concurrent sessions
- **Claude Agent SDK integration** — Anthropic's agent SDK directly in VS Code
- **MCP Apps support** — interactive UI visualizations rendered in chat
- **Terminal sandboxing** (experimental) — restricts file/network for agent commands
- **Copilot Studio extension GA** (Jan 15) — pro-code agent development
- **Action:** Study tool-restricted subagent pattern for workflow improvements.

### ClawHub Marketplace Scale
- **3,000+ published skills**, 800+ active developers, 15K+ daily installs
- VirusTotal scanning + verified badges system
- Despite security concerns, growth continues at breakneck pace
- **Action:** Continue publishing @kjaylee skills (30 published). Maintain audit discipline.

### Skills.sh Platform
- Open-source skills directory with leaderboards + 24h trending analytics
- Supports 18+ agent platforms (Claude Code, Codex, Cursor, Copilot, etc.)
- Free CLI: `npx skills` for discovery and installation
- **Action:** Monitor trending for intake candidates.

### SkillsMP — 160K+ Skills Directory
- Largest directory: indexes SKILL.md files from GitHub automatically
- Daily automated updates, category/author/popularity filtering
- Install: `npx skills add author/repo`
- **Action:** Use as discovery tool. All candidates still go through audit pipeline.

## 🟡 HIGH — MCP Market (LobeHub)

### Top MCP Servers by Stars (Feb 14 snapshot)
| Server | Stars | GitHub Stars | Category |
|--------|-------|-------------|----------|
| Context7 | 3,223 | 35,324 | Dev docs — live, version-specific library docs |
| Playwright | 4,195 | 22,487 | Browser automation |
| BlenderMCP | 820 | 13,973 | 3D modeling via natural language |
| AntV Charts | 1,462 | 3,058 | Chart/visualization generation |
| Firecrawl | 1,935 | 3,303 | Web scraping + structured extraction |
| Tavily | 2,223 | 434 | Advanced web search |
| Postgres MCP Pro | 439 | 477 | DB index tuning, health checks, safe SQL |
| Grep.app MCP | 207 | — | Code search across public GitHub repos |

### New Notable MCP Servers
- **Amazon Ads MCP** (Feb 2, beta) — natural language ad campaign management
- **Finance/Stock Research MCP** — quotes, technicals, analyst ratings, sentiment
- **LeetCode MCP** — problem search, daily challenges, submissions tracking
- **LinkedIn via BrightData MCP** — LinkedIn data extraction

### MCP Apps Standard (GA Jan 26)
- Tools return **interactive UI** (dashboards, forms) in-conversation via `ui://` resources
- Sandboxed iframes, pre-declared templates, auditable JSON-RPC
- Partners: OpenAI + Anthropic co-created the standard
- **Action:** Evaluate for game analytics dashboards.

## 🟢 Trends & Patterns

### Market Consolidation
- Agent Skills Standard now supported by **25+ platforms** (universal standard achieved)
- Three marketplace tiers emerging:
  1. **Free/Open:** ClawHub, skills.sh, SkillsMP (community-driven)
  2. **Curated/Freemium:** SkillHub (Pro stacks), skill0/Atypica
  3. **Enterprise/Paid:** SkillzWave ($299-399/mo domain packages), Airia MCP Apps
- DeepLearning.AI launched **"Agent Skills with Anthropic"** course — mainstream education signal

### Security as Differentiator
- VirusTotal scanning becoming table stakes for skill marketplaces
- Snyk 36% prompt injection rate is industry wake-up call
- CoSAI + Cisco CodeGuard donated for zero-trust agent security
- Sandboxed execution (Piston, container-use, VS Code terminal sandbox) gaining momentum

### Platform Strategy Shift
- OpenAI: Hosted shells + server-side compaction = long-running autonomous workers
- Anthropic: Expertise marketplace + ClawHub ecosystem
- Microsoft: VS Code as "home for multi-agent development"
- All converging on: Skills + MCP + Sandboxed Execution

## 📋 New Intake Items

### 31. **OpenAI Inline Skills API Pattern**
- Base64-encoded zip skills in Responses API
- **Relevance:** Cross-platform skill portability validation
- **Action:** Ensure misskim-skills are zip-compatible for OpenAI deployment

### 32. **Grep.app MCP Server**
- Code search across public GitHub repos via MCP
- **Relevance:** Could enhance code research workflows
- **Action:** 🔍 Evaluate for MiniPC integration

### 33. **Amazon Ads MCP** (Beta)
- Natural language ad campaign management
- **Relevance:** Low (no Amazon ads currently), but validates enterprise MCP adoption
- **Action:** Monitor only

### 34. **DeepLearning.AI Skills Course**
- Official Anthropic partnership course on building Agent Skills
- **Relevance:** Educational resource for skill quality improvement
- **Action:** 🔍 Review curriculum for best practice patterns

---

## 📊 Actionable Summary

| Priority | Action | Status |
|----------|--------|--------|
| 🔴 CRITICAL | Maintain zero-blind-install. ClawHavoc at 386 skills, off-platform lure tactics | ONGOING |
| 🔴 CRITICAL | Monitor OpenAI Skills API adoption — our skills already compatible | NEW |
| ⭐ HIGH | Study VS Code 1.109 parallel subagent + tool-restricted pattern | CARRY-OVER |
| ⭐ HIGH | Evaluate Context7 MCP (35K stars, live docs) on MiniPC | CARRY-OVER |
| ⭐ HIGH | Audit coreyhaines31/marketingskills → enhance game-marketing | CARRY-OVER |
| ⭐ HIGH | Audit obra/superpowers → absorb meta-skill patterns | CARRY-OVER |
| ⭐ HIGH | Ensure misskim-skills are zip-portable for OpenAI Responses API | NEW |
| 🟡 MED | Evaluate Grep.app MCP for code research | NEW |
| 🟡 MED | Review DeepLearning.AI Skills course for best practices | NEW |
| 🟡 MED | Monitor SkillzWave premium pricing model | CARRY-OVER |

**Status:** Ecosystem maturing fast. Skills standard now universal (25+ platforms). Security remains #1 concern. OpenAI's entry validates the entire Skills paradigm.

---
*Sweep completed: 2026-02-15 04:00 KST*
