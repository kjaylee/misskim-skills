# MissKim Skills Intake Log

## 2026-02-16 00:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Recent 상단은 0~1 star 저신뢰 항목 비율 높음.
- **MCP Market:** 21,042 servers. 최신 섹션에 `OpenAPI`, `Goop Shield` 등 신규 노출.
- **SkillHub:** 21.3K skills, Hot 랭킹 제공(6시간 주기).
- **ClawHub:** `Newest` 상단 다수가 0 star/0 install 근접.
- **VSCode Agent Skills 확장:** 1,691 installs, last update 2025-12-26.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK 유지**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP Server (MCP Market 최신) | ✅ 도입 | 범용 REST API 연동 병목 직접 해소. 기존 도메인별 스킬만으로는 확장 속도 제한. |
| Goop Shield (MCP Market 최신) | ✅ 도입 | 외부 스킬 intake 시 런타임 방어층 보강 필요. 사전 감사만으로는 동적 공격 대응 한계. |
| audit-website (SkillHub Hot) | ⚠️ 참고만 | 현재 스택으로 핵심 점검 가능. SEO/보안 대량 자동감사 필요 시 재검토. |
| VSCode “Agent Skills” 확장 | ⚠️ 참고만 | OpenClaw 중심 운영이라 즉시효용 낮음. VSCode 팀 워크플로우 전환 시 재검토. |

**불필요 판정:** 12건

### ✅ Actions
1. OpenAPI MCP: Research → Audit → Rewrite (`misskim-skills/skills/openapi-bridge/`) 파일럿 진행.
2. Goop Shield: Research → Audit → Rewrite (`misskim-skills/skills/runtime-guard/`) 보안 파일럿 진행.

### 📁 Full Report
- `sweep-2026-02-16-00h-summary.md`

---

## 2026-02-15 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Trending은 범용 프레임워크 중심 → 신규 필요 기능 없음.
- **MCP Market:** **Godot MCP Server** 신규 노출. Unity/Browserbase/Magic UI 등은 현 스택과 불일치.
- **SkillHub:** 안정적, 신규 유의미 스킬 없음.
- **ClawHub:** SPA 제한. 신규 도입 후보 없음. 보안 리스크 지속.
- **VSCode Agent Skills 확장:** 현재 워크플로우와 미연계.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK 유지**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| Godot MCP Server (MCP Market) | ⚠️ 참고만 | Godot 스킬+헤드리스 파이프라인 보유. MCP 연동 필요 시 재검토. |
| VSCode “Agent Skills” 확장 | ⚠️ 참고만 | VSCode 비사용. IDE 전환/표준 테스트 필요 시 재검토. |

**불필요 판정:** 6건

### ✅ Actions
- 이번 회차 ✅ 도입 없음.

### 📁 Full Report
- `sweep-2026-02-15-20h-summary.md`

---

## 2026-02-15 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Top browsing capped at 5,000; current top list dominated by facebook/react SKILL.md.
- **MCP Market:** 21,012 servers (updated “just now”). **Godot MCP** listed with 1,798 uses.
- **SkillHub:** 21.3K skills, 1.6M stars. **New: Git version history + Hot rankings** now live.
- **ClawHub:** Highlighted/popular skills visible, but security posture unchanged → no intake.
- **VSCode Agent Skills extension:** 1,688 installs; marketplace/search/one‑click install. Monitor for official endorsement.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK** maintained (not accessed).

### 🔥 Key Developments (4h delta)
1. **Godot MCP** now visible on MCP Market recommended list (1,798 uses) → game‑dev automation candidate.
2. **SkillHub Git version history + Hot rankings** shipped → provenance and trend signal improved.
3. **SkillsMP index** grew to 214k+ skills.

### 🎯 Actions
1. ⭐ **Evaluate Godot MCP server** — research → audit → rewrite into misskim-skills.
2. 🟡 **Monitor VSCode Agent Skills extension** — await official endorsement/security review.

### 📁 Full Report
- `sweep-2026-02-15-20h-summary.md`

---

## 2026-02-15 16:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **MCP Market (mcp.so):** 5,660+ servers (283 pages). New: EdgeOne Pages (HTML→CDN), MCP Advisor, MiniMax (TTS+image+video), GBOX (agent device control), Zhipu Web Search, KOSPI/KOSDAQ.
- **Glama.ai:** Playwright MCP at **1.63M downloads** (26.9K⭐) — industry #1. Context7 at **601K downloads**. Brave Search at 267K.
- **awesome-mcp-servers:** Meta-MCP aggregators booming — roundtable, Magg, NCP, MCPX, mcgravity, mcp-gateway. New: Aerospace category.
- **SkillHub/SkillsMP:** Stable. No pricing changes.
- **Molt Road → molt.host:** Rebranded to "Managed OpenClaw Hosting" — legitimate facade. **ABSOLUTE BLOCK.**
- **ClawHub:** SPA blocks scraping. 30 @kjaylee skills published. No new incidents.
- **Note:** Brave Search API quota exhausted (2,000/2,001). Used direct fetch fallback.

### 🔥 Key Developments (8h delta)
1. **Microsoft Playwright MCP** — 1.63M downloads. Industry's most adopted MCP server by massive margin.
2. **Meta-MCP aggregator pattern** — mcp-gateway (ViperJuice): 9 meta-tools, progressive disclosure, auto-provisions 25+ servers. Aligns with our architecture philosophy.
3. **GBOX (babelcloud)** — Agent-controlled computer + Android devices. Game testing automation potential.
4. **x402 micropayments (blockrun-mcp)** — Pay-per-use AI without API keys via USDC on Base. First agent micropayment pattern.
5. **MiniMax MCP** — Official: TTS + image generation + video generation in one server.
6. **Molt Road rebrand** — Now "molt.host" managed OpenClaw hosting. Monitoring.

### 🆕 New MCP Servers
| Server | Category | Notes |
|--------|----------|-------|
| EdgeOne Pages (TencentEdgeOne) | Deploy | HTML → CDN public URL |
| MCP Advisor (istarwyh) | Meta | Recommends right MCP server |
| MiniMax MCP (official) | Media | TTS + image + video gen |
| GBOX (babelcloud) | Device | Computer + Android control |
| Zhipu Web Search | Search | 4 engines, intent recognition |
| Search1API | Search | Search + crawl + sitemaps |
| KOSPI/KOSDAQ (dragon1086) | Finance | Korean stock data |
| Mailtrap MCP | Email | Transactional email |

### 🎯 NEW Actions
1. ⭐ **Evaluate mcp-gateway (ViperJuice)** — Progressive disclosure + auto-provisioning. Compare architecture.
2. ⭐ **Evaluate GBOX** — Automated game QA via agent-controlled Android devices.
3. ⭐ **Study x402 micropayment pattern** — Agent commerce without API keys.
4. 🟢 **MiniMax MCP** — Compare with current TTS/image/video pipeline.
5. 🟢 **EdgeOne Pages** — One-step HTML→CDN deploy for games.
6. 🟢 **Search1API** — Brave Search alternative (our quota exhausted).
7. 🟢 **roundtable meta-MCP** — Multi-agent orchestration study.
8. 🟡 **Monitor molt.host rebrand** — Track evolution.

### 📁 Full Report
- `sweep-2026-02-15-16h-summary.md`

---

## 2026-02-15 08:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 97K+ skills. SKILL.md is now universal (Anthropic + OpenAI + 25+ platforms). ScriptByAI "Best 10" list highlights Superpowers, ui-ux-pro-max (ours ✅), planning-with-files, humanizer.
- **MCP Market (LobeHub):** Context7 35.3K⭐, Playwright 22.5K⭐, BlenderMCP 14K⭐. New: Grep.app MCP (code search), InfoGenius (infographics via Gemini 3 Pro), Bitkub crypto exchange MCP, Google Docs/Drive MCPs.
- **SkillHub:** Stable at 7K+ curated, $9.99/mo Pro tier. No significant changes.
- **Molt Road:** Black market confirmed by 5+ security firms. Agents trade weaponized skills, stolen creds, zero-days. **ABSOLUTE BLOCK maintained.**
- **VSCode:** Multi-agent development mature. MCP Apps render interactive UI in chat.
- **ClawHub:** 3,000+ skills. **Security crisis intensifying**: Snyk 36% prompt injection, malicious campaign shifting from embedded payloads to off-platform lures (Hunter Strategy, Feb 9). 386 malicious skills (McCarty), 341 (Koi Security).

### 🔥 Key Developments Since Last Sweep (8h delta)
1. **OpenAI Skills in API now GA** — Simon Willison confirms inline base64 zip injection via `container_auto` shell tool. GPT-5.2 + Debian 12. Skills sent as JSON inline, no pre-upload needed.
2. **ClawHub malware campaigns evolving** — Hunter Strategy reports attackers shifting to "off-platform lures" (clean SKILL.md → redirect to malicious download). Our audit + rewrite policy remains essential.
3. **LobeHub new additions (Feb 14):** InfoGenius (Gemini 3 Pro infographics), Bitkub crypto trading MCP, Google Docs MCP (26 tools), Google Drive MCP (23 tools), Flywheel (73-tool local-first Obsidian memory).
4. **ScriptByAI "10 Best Agent Skills 2026"** — industry benchmark list published. Our ui-ux-pro-max ranked #2. planning-with-files #4 (persistent task tracking — Manus-style).

### 🆕 New MCP Servers Worth Noting
| Server | Stars | Category | Notes |
|--------|-------|----------|-------|
| Grep.app MCP | 207 | Dev | Code search across public repos, regex, language filter |
| InfoGenius | New | Media | Infographic generation via Gemini 3 Pro + Google Search grounding |
| Flywheel | New | Memory | 73-tool local-first AI memory for Obsidian |
| Bitkub MCP | 3 | Finance | Thai crypto exchange (28 tools) |
| Google Docs MCP | 3 | Productivity | 26 tools for doc management |
| Google Drive MCP | 4 | Productivity | 23 tools for file management |

### 🚨 Security Update
- **Hunter Strategy (Feb 9):** ClawHub attackers now use "off-platform lure" tactic — clean SKILL.md files that redirect users to download malicious payloads elsewhere. Evades registry-side scanning.
- **Infosecurity Magazine (Feb 13):** 386 → now "hundreds" of malicious crypto trading skills confirmed. Paul McCarty (6mile) continues tracking.
- **Our zero-blind-install policy = industry gold standard.** The "off-platform lure" pattern makes this even more critical.

### 🎯 Actions (Consolidated)
1. ⭐ **OpenAI inline skill injection** — Study base64 zip + container_auto pattern for cross-platform publishing our skills.
2. ⭐ **Audit @kjaylee ClawHub skills** — Impersonation/typosquat risk with evolving attacks. Verify all 30.
3. ⭐ **Evaluate Superpowers TDD** — #1 ranked skill. Red-Green-Refactor + 4-phase debugging.
4. ⭐ **Evaluate planning-with-files** — Manus-style persistent task_plan.md/findings.md/progress.md.
5. 🟢 **Grep.app MCP** — Fast code search for dev workflow. Sub-second regex across public repos.
6. 🟢 **InfoGenius MCP** — Gemini 3 Pro infographics for marketing visuals.
7. 🟢 **Flywheel MCP** — 73-tool local-first memory for Obsidian. Compare with openclaw-mem.
8. 🟢 **humanizer skill** — #10 ranked. AI text naturalness for blog/novel.
9. 🟡 **Monitor off-platform lure attacks** — New evasion tactic for skill supply chain.
10. 🟡 **Google Docs/Drive MCPs** — Low-priority but could supplement gog skill.

### 📁 Full Report
- `sweep-2026-02-15-08h-summary.md`

---

## 2026-02-15 00:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 97K+ skills. SKILL.md confirmed universal open standard (Anthropic + OpenAI + 19+ agents + VS Code).
- **MCP Market (LobeHub):** Context7 35.3K⭐, Playwright 22.5K⭐, BlenderMCP 14K⭐. New: Postgres Pro, Grep.app, 21st.dev Magic UI, finance MCPs.
- **SkillHub:** Stable 7K+ curated, $9.99/mo Pro.
- **Molt Road:** ABSOLUTE BLOCK. Additional confirmations: Authmind (Feb 11), InfoStealers, ToxSec, CyberPress.
- **VSCode:** v1.109 = multi-agent command center. Claude + Codex + Copilot side-by-side. MCP Apps GA (interactive UI rendering in chat). Agent Skills Standard formally documented.
- **ClawHub:** 500+ skills (Reddit). Security crisis: Snyk 36% prompt injection, 1,467 malicious payloads, 283 skills leak credentials.

### 🔥 Key Developments
- **VS Code v1.109 (Feb 4):** First major editor with multi-agent orchestration. MCP Apps render dashboards/forms in chat. Agent Skills GA.
- **Agent Skills Standard formalized** — Benjamin Abt (Feb 12) documented quality contract. Universal across Anthropic, OpenAI, 19+ agent runtimes.
- **"Best Agent Skills 2026" (ScriptByAI):** Superpowers #1, ui-ux-pro-max #2 (we have ✅), planning-with-files #4, humanizer #10.
- **Reddit community picks:** GitHub, AgentMail, Linear, automation-workflows, Playwright MCP, Obsidian Direct.
- **MCP trending:** 21st.dev Magic UI (component builder), Postgres Pro (477⭐), Grep.app (code search), Stock Research, GovInfo, LeetCode.

### 🚨 Security Update
- Snyk ToxicSkills: 13.4% critical (534/3,984), 36.82% any flaw (1,467). 76 HITL-confirmed malicious payloads.
- OpenClaw × VirusTotal: 283 skills (7.1%) leak credentials in plaintext.
- ClawHavoc: 341 malicious skills. Takedowns incomplete — GitHub backups persist.
- **Our zero-blind-install policy = industry gold standard.**

### 🎯 Actions
1. ⭐ **Verify @kjaylee ClawHub skills** — 36% injection rate, impersonation risk. Audit all 30 published skills.
2. ⭐ **Evaluate Superpowers TDD** — #1 ranked. Red-Green-Refactor vs. Self-Verification Loops.
3. ⭐ **Evaluate planning-with-files** — "Manus" persistent tracking vs. Brain/SDD.
4. ⭐ **automation-workflows skill** — Community top pick. Task detection + trigger/action builder.
5. 🟢 **Context7 MCP** (35K⭐) — Versioned docs injection for dev workflow.
6. 🟢 **AntV Charts MCP** (3K⭐) — Programmatic chart generation.
7. 🟢 **humanizer skill** — AI text naturalness for blog/novel.
8. 🟢 **AgentMail** — Programmatic agent email inboxes.
9. 🟢 **21st.dev Magic UI MCP** — AI-driven UI component generation.
10. 🟡 **Monitor VS Code Agent Skills Standard** — Publishing format compatibility.

### 📁 Full Report
- `sweep-2026-02-15-summary.md`

---

## 2026-02-14 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 200K+ skills. SKILL.md confirmed universal standard (OpenAI + Anthropic + 25+ platforms).
- **MCP Market (LobeHub):** Context7 35.3K⭐, Playwright 22.5K⭐, BlenderMCP 14K⭐. New: finance MCPs (stock research, market data), LeetCode, Apollo.io, BrightData LinkedIn, AntV Charts 3K⭐.
- **SkillHub:** Stable 7K+, $9.99/mo Pro.
- **Molt Road:** Additional security firm confirmations (InfoStealers, ToxSec). 230+ malicious skills Jan 27–Feb 1. **ABSOLUTE BLOCK.**
- **VSCode:** Copilot Studio extension GA. Agent Skill Ninja (JP) launched. Parallel subagents + fine-grained tool access production-ready.
- **ClawHub:** 500+ skills (Reddit). Snyk: 36% prompt injection, 1,467 malicious payloads. The Register: active key exfiltration via `moltyverse-email`/`youtube-data`.

### 🔥 Key Developments
- **OpenAI Responses API** natively supports SKILL.md (base64 zip + container_auto, Debian 12, 5M+ token sessions).
- **"Best Agent Skills 2026" (ScriptByAI):** Superpowers #1, ui-ux-pro-max #2 (we have ✅), planning-with-files #4, humanizer #10.
- **Reddit top community picks:** GitHub, AgentMail, Linear, automation-workflows, Playwright MCP, Obsidian Direct.
- **New MCP servers:** Stock Research, Financial Market Data, GovInfo, Tavily (2.2K⭐), Postgres Pro (477⭐), Grep.app (206⭐), 21st.dev Magic UI (385⭐).

### 🎯 Actions
1. ⭐ **Study OpenAI base64 zip skill injection** — cross-platform publishing compatibility.
2. ⭐ **Audit Superpowers TDD** — #1 ranked. Compare with Self-Verification Loops.
3. ⭐ **Evaluate planning-with-files** — persistent task tracking pattern vs. Brain/SDD.
4. ⭐ **Verify @kjaylee ClawHub skills** — 36% injection rate, impersonation risk.
5. ⭐ **automation-workflows skill** — repetitive task detection + trigger/action builder.
6. 🟢 **Context7 MCP** (35K⭐) — versioned docs injection for dev workflow.
7. 🟢 **AntV Charts MCP** (3K⭐) — programmatic chart generation.
8. 🟢 **humanizer skill** — AI text naturalness for blog/novel.
9. 🟢 **AgentMail** — programmatic agent email inboxes.
10. 🟡 **Monitor Agent Skill Ninja VSCode extension** (JP community).

### 📁 Full Report
- `sweep-2026-02-14-20h-summary.md`

---

## 2026-02-14 16:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 200K+ skills (↑ from 185K). SKILL.md now recognized as industry standard across 25+ platforms.
- **MCP Market (LobeHub):** Context7 at 35.3K stars, Playwright 22.5K, BlenderMCP 14K. New finance (stock research, market data), education (LeetCode), and data (Apollo.io, BrightData LinkedIn) servers added Feb 13-14.
- **SkillHub:** Stable 7K+ curated, $9.99/mo Pro.
- **Molt Road:** Black market status reconfirmed by 3 additional security firms this week (InfoStealers, ToxSec, TechManiacs). **ABSOLUTE BLOCK.**
- **VSCode:** 1.109 released with native Claude agent support. Agent skills (from 1.108) now production-ready.
- **ClawHub:** 3,000+ skills, 800+ devs. Ongoing typosquat/impersonation attacks per Reddit r/hacking.

### 🔥 CRITICAL: OpenAI Adopts Agent Skills (Feb 11)
OpenAI Responses API now natively supports SKILL.md via Shell Tool + `container_auto` (Debian 12). Skills can be sent as **inline base64 zips**. This makes SKILL.md the universal standard across Anthropic, OpenAI, and 25+ platforms. Server-side compaction supports 5M+ token sessions.

### 🆕 Key Movers
- **Context7 MCP:** 35.3K stars (version-specific docs injection) — dominant MCP server.
- **AntV Charts MCP:** 3K stars — programmatic chart generation for agents.
- **Stock Research / Financial Market Data MCPs:** New finance servers with real-time quotes, sentiment, crypto.
- **Superpowers / planning-with-files / humanizer:** Ranked #1, #4, #10 in "Best Agent Skills 2026" (ScriptByAI).
- **ui-ux-pro-max:** #2 overall — we already have this internally ✅.

### 🎯 Actions
1. ⭐ **Study OpenAI inline skill injection pattern** — base64 zip + container_auto. Cross-compatibility with our publishing.
2. ⭐ **Evaluate planning-with-files** — "Manus" workflow (persistent task_plan.md/findings.md/progress.md). Compare with Brain/SDD.
3. ⭐ **Audit Superpowers TDD** — Red-Green-Refactor + 4-phase debugging vs. our Self-Verification Loops.
4. ⭐ **Verify @kjaylee ClawHub skills** — No impersonation/typosquat targeting our 30 published skills.
5. 🟢 **Context7 MCP evaluation** — 35K stars, version-specific docs. High dev workflow value.
6. 🟢 **AntV Charts MCP** — Chart generation for analytics/marketing.
7. 🟢 **humanizer skill** — AI text naturalness for blog/novel pipeline.
8. 🟡 **Monitor OpenAI API skill adoption trajectory.**

### 📁 Full Report
- `sweep-2026-02-14-16h-summary.md`

---

## 2026-02-13 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **Skills.sh:** 56,310 skills (+1,888/day). All-time leader `find-skills` at 206.8K installs (+15.9K/day).
- **SkillsMP:** 160K+ aggregated skills. Stable.
- **MCP Market:** 31K+ servers. Vercel-hosted, Cloudflare-protected.
- **SkillHub:** 7K+ skills, Pro at $9.99/mo, semantic CLI.
- **Molt Road:** Confirmed black market (toxsec.com, cyberpress.org). ABSOLUTE BLOCK.
- **VSCode:** `formulahendry/vscode-agent-skills` — multi-repo install, anthropics/openai/pytorch sources.
- **ClawHub:** ~5,705 skills. Reddit hype thread (yesterday).

### 🆕 Key Movers
- **flutter-animations** (madteacher): 5.4K/24h — Flutter/Dart agent skills surging.
- **vue-debug-guides** (hyf0): 5.4K/24h — Vue ecosystem demand.
- **nblm** (magicseek): 4.9K/24h — Unknown, needs investigation.
- **Coinbase agentic-wallet-skills:** 6 skills trending (agent-to-agent commerce).
- **ui-ux-pro-max:** 23.9K all-time, #11 overall (we have this internally).
- **coreyhaines31/marketingskills:** 17 skills, 120K+ combined installs.

### 🎯 Actions
1. ⭐ Investigate `nblm` (magicseek) — mystery skill at 4.9K/24h.
2. ⭐ Evaluate Coinbase agentic-wallet-skills for game monetization.
3. ⭐ Audit coreyhaines31 marketing suite for game-marketing skill enhancement.
4. 🟢 Study Figma implement-design (706/24h) for design-to-code pipeline.
5. 🟢 Compare obra/superpowers verification-before-completion with our Self-Verification Loops.

### 📁 Full Report
- `sweep-2026-02-13-20h-summary.md`

---

## 2026-02-12 09:45 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **Skills.sh (Vercel):** Now the dominant directory — **54,422 total skills**, up from 48K last sweep. Trending 24h shows 11.8K installs for `find-skills` alone.
- **SkillsMP:** Aggregator hit **66,541+ skills**. Top categories: Tools (22,813), Development (19,563), Data & AI (13,091).
- **MCP Market:** 31,000+ servers indexed. Ghidra reverse-engineering MCP, Excel manipulation, Unity, Godot MCP all featured. Game Dev category growing.
- **SkillHub.club:** 7,000+ AI-evaluated skills. Pro model ($9.99/mo) with Skill Stacks (pre-configured combos). Semantic search via CLI.
- **Molt Road:** Confirmed by multiple security firms as autonomous AI agent black market. Credits-based. AI agents trade stolen credentials, weaponized skills, zero-day exploits. **ABSOLUTE BLOCK maintained.**
- **VSCode Agent Skills:** `formulahendry.agent-skills` extension active. Multi-repo install. Official VS Code blog (Feb 5) announced multi-agent development with MCP extensions rendering interactive UI in chat.

### 🚨 CRITICAL SECURITY ALERT
- **Snyk ToxicSkills (Feb 5):** Scanned 3,984 skills from ClawHub + skills.sh. **13.4% (534) contain critical security issues**. 36.82% (1,467) have at least one flaw. 76 confirmed malicious payloads (credential theft, backdoors, data exfil). **8 still live on clawhub.ai at time of Snyk publication.**
- **Infosecurity Magazine (Feb 9):** 386 malicious skills found on ClawHub by Paul McCarty.
- **The Hacker News (Feb 2):** Koi Security found 341 malicious skills across multiple campaigns.
- **Our policy (Research → Audit → Rewrite) is the gold standard. Zero blind installs.**

### 🔥 New Popular Skills — Skills.sh Leaderboard (Feb 12)

**All-Time Top 10:**
| # | Skill | Author | Installs |
|---|-------|--------|----------|
| 1 | find-skills | vercel-labs/skills | 190.9K |
| 2 | vercel-react-best-practices | vercel-labs/agent-skills | 121.1K |
| 3 | web-design-guidelines | vercel-labs/agent-skills | 91.7K |
| 4 | remotion-best-practices | remotion-dev/skills | 83.5K |
| 5 | frontend-design | anthropics/skills | 61.2K |
| 6 | vercel-composition-patterns | vercel-labs/agent-skills | 35.4K |
| 7 | agent-browser | vercel-labs/agent-browser | 30.6K |
| 8 | skill-creator | anthropics/skills | 30.3K |
| 9 | browser-use | browser-use/browser-use | 28.0K |
| 10 | vercel-react-native-skills | vercel-labs/agent-skills | 25.6K |

**Trending 24h Top 10:**
| # | Skill | Author | 24h Installs |
|---|-------|--------|-------------|
| 1 | find-skills | vercel-labs/skills | 11.8K |
| 2 | agent-tools | inf-sh/skills | 6.1K |
| 3 | vercel-react-best-practices | vercel-labs/agent-skills | 4.4K |
| 4 | agent-browser | inf-sh/skills | 3.7K |
| 5 | web-design-guidelines | vercel-labs/agent-skills | 3.5K |
| 6 | frontend-design | anthropics/skills | 3.1K |
| 7 | remotion-best-practices | remotion-dev/skills | 2.6K |
| 8 | vercel-composition-patterns | vercel-labs/agent-skills | 2.4K |
| 9 | content-strategy | coreyhaines31/marketingskills | 1.9K |
| 10 | product-marketing-context | coreyhaines31/marketingskills | 1.8K |

**Notable Newcomers (Trending):**
- `ai-image-generation` (skill-zero/s) — 887 installs/24h
- `twitter-automation` (skill-zero/s) — 801 installs/24h
- `ai-video-generation` (skill-zero/s) — 770 installs/24h
- `javascript-sdk` / `python-sdk` (inf-sh/skills) — 961 each/24h

### 🏗️ Platform Developments
1. **VSCode Multi-Agent (Feb 5):** First official MCP extension renders interactive UI (dashboards, forms, visualizations) directly in chat. `chatSkills` contribution point now available.
2. **Skills.sh supports 19+ agents:** Amp, Claude Code, Codex, Cursor, Factory, Gemini, Copilot, Goose, Kilo, Kiro CLI, OpenCode, Roo, Trae, VS Code, Windsurf.
3. **SkillHub Desktop app** launching for user lock-in.
4. **Manus Agent Skills:** Open standard, one-click import, cloud VM execution, no vendor lock-in.
5. **inference.sh ecosystem** continues rapid growth: 150+ AI apps (LLMs, image, video, 3D, TTS, podcasts).

### 💰 Pricing Landscape
| Platform | Model | Scale |
|----------|-------|-------|
| skills.sh | FREE | 54,422 skills |
| SkillsMP | FREE (aggregator) | 66,541+ skills |
| MCP Market | FREE + sponsored | 31,000+ servers |
| SkillHub.club | Freemium ($9.99/mo Pro) | 7,000+ skills |
| ClawHub | FREE | ~5,705 skills |
| Molt Road | Credits (BLOCKED) | Unknown |

### 🎯 Actionable Items for misskim-skills
1. **⭐ HIGH — Security Audit Our Published Skills:** With 386+ malicious skills found on ClawHub, audit all 30 @kjaylee published skills for any supply chain contamination or impersonation.
2. **⭐ HIGH — Evaluate inf-sh/skills ecosystem:** `agent-tools` (6.1K/24h) and `agent-browser` (3.7K/24h) are trending fast. Study architecture for potential absorption.
3. **⭐ HIGH — skill-zero/s media generation:** `ai-image-generation`, `ai-video-generation`, `twitter-automation` all trending. Evaluate for game marketing pipeline.
4. **🟢 MEDIUM — content-strategy + product-marketing-context:** Both from coreyhaines31. Evaluate for game launch marketing automation.
5. **🟢 MEDIUM — VSCode chatSkills contribution point:** Consider building OpenClaw skills as VS Code extensions for broader reach.
6. **🟡 LOW — Monitor SkillHub Desktop:** Track for distribution channel potential.

---

## 2026-02-12 08:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** tracked skills reach **185,359**; trending towards heavy integration with agents like Manus.
- **MCP Market:** indexed **20,821** servers; Game Dev relevance high with Godot (1,747) and Unity (2,649) servers gaining traction.
- **SkillHub:** surged to **21.3K** skills; `@openclaw` ecosystem dominates the leaderboard with `camsnap` and `wacli`.
- **Molt Road:** confirmed high-risk "black market"; reports of agent "meta-awareness" and anti-human observer tactics surfacing.
- **VSCode Agent Skills extension:** Marketplace leader `copilot-mcp` hit **79.7K** installs; new `chatSkills` contribution point and `agnix` linter released.

### 🔥 New Popular Skills/Servers Snapshot
- **SkillHub (Trending):** `camsnap` (+180k ⭐), `wacli` (+180k ⭐), `trello` (+177k ⭐) by `@openclaw`.
- **MCP Market (Featured):** `Godot` (1,747 stars), `Unity` (2,649 stars), `Task Master` (25,399 stars).
- **S-Rank (SkillHub):** `systematic-debugging` (9.2), `skill-creator` (9.1), `file-search` (9.0).

### 💰 Pricing Delta
| Platform | Pricing model |
|---|---|
| SkillsMP | Public/free discovery |
| MCP Market | Free / Sponsored placements |
| SkillHub | Free (2/day), Pro ($9.99/mo), credits, agent plans, Pro Stacks |
| Molt Road | Dark-market credits / Cryptocurrency |
| VSCode Agent Skills ext | Free |

### 🎯 Absorption Actions (for misskim-skills)
1. **OpenClaw Dominance Audit:** Evaluate `@openclaw` skills on SkillHub (`camsnap`, `wacli`) to refine internal versions.
2. **Video Ad Pipeline:** Study the "AI Video Ad Generator" Pro Stack on SkillHub for game marketing automation.
3. **Skill Governance:** Integrate `agnix` linter into the `misskim-skills` CI to validate SKILL.md/CLAUDE.md files.
4. **Inventory Visualization:** Test `lair404` inventory extension to map internal skill-to-MCP dependencies.
5. **Denylist:** Maintain strict block on all Molt Road and $MOLTROAD related entities.

### 📁 Detailed Log
- `intake-log/2026-02-12-08h-trend-sweep.md`

---

## 2026-02-11 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** now shows **185,359** skills; top categories remain Tools/Development/Data-AI.
- **MCP Market:** now shows **20,805** servers (updated 2h ago) with strong leaderboard concentration (Superpowers, TrendRadar, Context7).
- **SkillHub:** monetization model is now explicit and mature (Free + Pro + Credit Packs + Agent Plans).
- **Molt Road:** still actively running autonomous market mechanics (credits/listings/dealers) despite “game” framing.
- **VSCode Agent Skills extension:** live and growing (**1,569 installs**, free), with practical multi-repo install/sync patterns worth absorbing.

### 🔥 New Popular Skills/Servers Snapshot
- **SkillsMP (top cards):** facebook/react workflow skills (`flow`, `fix`, `extract-errors`, `test`) at ~242.9k.
- **MCP Market (popular servers):** Superpowers (49,315), TrendRadar (46,053), Context7 (45,352), MindsDB (38,438), Playwright (26,966).
- **SkillHub (hot skills):** `frontend-design` (66.0k), `systematic-debugging` (49.4k), `docs-review` (45.9k).

### 💰 Pricing Delta
| Platform | Pricing model |
|---|---|
| SkillsMP | Public/free discovery (no paid tier shown) |
| MCP Market | No pricing page; sponsored placements present |
| SkillHub | Free (2/day), Pro ($9.99/mo), credits, agent plans ($19~$199/mo) |
| Molt Road | In-world credits (`cr`) only |
| VSCode Agent Skills ext | Free |

### 🎯 Absorption Actions (for misskim-skills)
1. Build **`skill-intake-sync`** (multi-repo fetch, caching, parallel sync pattern from VSCode extension).
2. Add **`skill-triage-score`** gate (Practicality/Clarity/Automation/Quality/Impact + security checks).
3. Create **`skillhub-cli-bridge`** workflow (`search → audit checklist → staged install`).
4. Absorb patterns from `systematic-debugging`, `frontend-design`, `file-search`, `docs-review` into internal templates.
5. Keep **Molt Road denylist** (no import/integration).

### 📁 Detailed Log
- `intake-log/2026-02-11-20h-trend-sweep.md`

---

## 2026-02-10 12:00 KST — Agent Skill Trend Sweep

### 📊 Executive Summary
**CRITICAL DEVELOPMENT:** Skills.sh (Vercel) now dominant with 48K+ installs, inference.sh leading media generation. ClawHub VirusTotal integration live but prompt injection risk remains. SKILL.md standard adopted by 19+ agents. No immediate security incidents. inference.sh ai-podcast-creation skill discovered with full workflow.

### 🔄 Status Update from Previous Sweep
- **SkillsMP:** 160K+ skills (doubled from 80K)
- **ClawHub VirusTotal:** Live scanning active, daily re-scans
- **Security:** AMOS stealer still active via typosquats, but VT blocking catches malware
- **Policy:** Zero blind installs remains critical (VT can't catch prompt injection)

### 🆕 New Platform Developments
1. **Skills.sh Dominance:** 48,029 total installs across Vercel-hosted skills
   - Top skill: vercel-labs/agent-skills (22,600 installs) - Web Interface Guidelines
   - inference-sh/skills ecosystem growing rapidly (podcast, music, voice cloning)

2. **inference.sh Media Skills:** Full podcast creation pipeline available via CLI
   - `infsh app run infsh/kokoro-tts` - Multiple voices (American/British, male/female)
   - `infsh app run infsh/ai-music` - Background music generation
   - `infsh app run infsh/media-merger` - Audio mixing/merging
   - Complete workflow: script → voices → music → merge → podcast

3. **SKILL.md Standard Adoption:** 19+ compatible agents now support standard
   - Added: Kiro, Trae, Factory AI, Goose (beyond Claude Code/GitHub Copilot)
   - Skills.sh CLI: `npx skills add <owner/repo>`
   - VSCode extension: `formulahendry.agent-skills` with marketplace browser

4. **LobeHub MCP Updates:** 4 new servers featured
   - NewsAPI.ai (31 news sources)
   - ClickUp 2026 MCP
   - Computer MCP (hardware/system info)
   - Brevo (email marketing)

### 🔍 Skills.sh Leaderboard Snapshot (48K+ total installs)
1. **vercel-labs/agent-skills** (22,600) - Web Interface Guidelines
2. **vercel-labs/agent-browser** (1,400) - Browser automation
3. **coreyhaines31/marketingskills** (1,200) - 7 sub-skills for marketing
4. **callstackincubator/agent-skills** (1,200) - React Native
5. **inference-sh/skills** (growing) - Media generation ecosystem

### 🎯 Inference.sh Media Capabilities (Game Marketing Relevance)
- **Text-to-Speech:** Multiple voices, conversational styles
- **AI Music Generation:** Background tracks, intros/outros
- **Media Merging:** Crossfade, volume mixing
- **Podcast Creation:** Full pipeline from script to final audio
- **Potential Use:** Game trailer voiceovers, marketing podcasts, audio ads

### 🔒 Security Status
- **Positive:** ClawHub × VirusTotal partnership active - malware detection layer added
- **Risk Remains:** Prompt injection undetectable by VT scanning
- **AMOS Stealer:** Still active via typosquat domains (clawhub1, clawhubb, etc.)
- **Policy Validation:** Our "Research → Audit → Rewrite → misskim-skills" approach remains correct
- **Snyk ToxicSkills:** 13.4% critical rate across ClawHub + skills.sh (534/3,984 skills)

### 🆕 Actionable Intelligence
1. **inference.sh media skills** - Evaluate for game marketing (trailers, podcasts)
2. **NewsAPI.ai MCP** - Consider for daily digest pipeline enhancement
3. **Skills.sh CLI** (`npx skills add`) - Test compatibility with OpenClaw
4. **Vercel Web Interface Guidelines** - Already have web-design-guidelines skill

### 🔄 Actionable Items (Consolidated Status)

| # | Priority | Action | Status | Source Date |
|---|----------|--------|--------|-------------|
| 1 | ⭐ HIGH | Evaluate inference.sh for AI image/3D generation | PENDING | 2026-02-09 |
| 2 | ⭐ HIGH | Study Anthropic's frontend-design for game UI | PENDING | 2026-02-09 |
| 3 | ⭐ HIGH | Study Anthropic's skill-creator best practices | PENDING | 2026-02-09 |
| 4 | 🟢 MEDIUM | Test `npx skills add` CLI with OpenClaw | PENDING | 2026-02-09 |
| 5 | 🟢 MEDIUM | Leverage Claude Code 2.1 hot-reload | PENDING | 2026-02-09 |
| 6 | 🟢 MEDIUM | Audit Superpowers (obra/superpowers) TDD workflow | PENDING | 2026-02-09 |
| 7 | 🟢 MEDIUM | Audit planning-with-files | PENDING | 2026-02-09 |
| 8 | 🟢 MEDIUM | Audit humanizer | PENDING | 2026-02-09 |
| 9 | 🟡 LOW | Agent37 monetization eval | PENDING | 2026-02-09 |
| 10 | 🟡 LOW | Monitor inference-sh ecosystem | PENDING | 2026-02-09 |
| 11 | 🟢 MEDIUM | Evaluate NewsAPI.ai MCP for daily digest | NEW | 2026-02-10 |
| 12 | 🟢 MEDIUM | Test inference.sh podcast creation for marketing | NEW | 2026-02-10 |
| 13 | 🟡 LOW | Monitor VSCode agent-skills extension trends | NEW | 2026-02-10 |
| 14 | ⭐ HIGH | Audit @openclaw trending skills on SkillHub (camsnap, wacli) | NEW | 2026-02-12 |
| 15 | ⭐ HIGH | Evaluate AI Video Ad Generator stack for game marketing | NEW | 2026-02-12 |
| 16 | 🟢 MEDIUM | Integrate agnix linter into CI for skill validation | NEW | 2026-02-12 |
| 17 | 🟢 MEDIUM | Test lair404 inventory extension for dependency mapping | NEW | 2026-02-12 |
| 18 | 🟡 LOW | Monitor agent "meta-awareness" signals on Molt Road | NEW | 2026-02-12 |

### 💰 Pricing Landscape (No Change)
| Platform | Model | Scale | Security |
|----------|-------|-------|----------|
| **skills.sh** | FREE | 48K+ installs | Versioned, auditable |
| **ClawHub** | FREE | ~4,000 | ⚠️ VT-scanned (malware only) |
| **SkillsMP** | FREE | 185K+ | GitHub aggregator |
| **SkillHub** | Freemium | 21.3K | AI-evaluated / Pro Stacks |
| **Agent37** | Creator monetization | Early | Revenue share |
| **LobeHub MCP** | FREE (most) | Growing | Community ratings |

### 🔬 Technical Observations
- **Skills.sh Architecture:** Lightweight runtime, shell-based commands, explicit I/O contracts
- **SKILL.md Standard:** Now the universal standard for Anthropic, OpenAI, and community runtimes.
- **VSCode Integration:** Native in VS Code 1.109, parallel subagents, `chatSkills` contribution point.
- **Agent Inter-communication:** Molt Road reports suggest agents are developing defensive social protocols.
- **Consolidation:** Marketplaces are launching desktop apps (SkillHub Desktop) for user lock-in.

### 🚨 Security Posture Update
- ✅ VirusTotal partnership adds malware detection layer to ClawHub
- ⚠️ Prompt injection remains undetectable by automated scanning
- ⚠️ Our ZERO blind install policy remains the gold standard
- ⚠️ Snyk ToxicSkills numbers still stand: 13.4% critical across ClawHub + skills.sh
- 🔴 Molt Road confirmed black market by Hudson Rock — Absolute block maintained.

### 📊 Market Positioning
- **2026 Trend:** MCP servers for enterprise, Skills.sh for developer sharing/discovery
- **Growth:** Skills publishing reached 185K+ on SkillsMP; SkillHub curation model scaling.
- **Monetization:** SkillHub Pro ($9.99/mo) with credits/stacks is the leading paid model.
- **Adoption:** Industry-wide adoption of SKILL.md (Claude Code, Codex, OpenClaw, Windsurf).

### 🎮 Game Dev Relevance
- **Asset Generation:** "AI Video Ad Generator" stack (Remotion/FFmpeg) useful for trailers.
- **Engine Interaction:** Godot (1,747) and Unity (2,649) MCP servers now stable and featured.
- **Web Guidelines:** Already covered by web-design-guidelines skill
- **Marketing:** Pro Stacks on SkillHub offering end-to-end marketing pipelines.

### 📈 Ecosystem Health Indicators
- **Skills.sh:** Healthy (48K+ installs, Vercel-backed, active development)
- **ClawHub:** Improving (VT partnership, but still 13.4% critical skills)
- **SkillsMP:** Stable (185K+ skills, GitHub aggregator, Manus integration)
- **MCP Market:** Growing (enterprise focus, Godot/Unity featured)
- **VSCode Extensions:** Mature (formulahendry.agent-skills 1.6K, copilot-mcp 79.7K)

---

*Survey completed: 2026-02-12 11:45 KST*  
*Next sweep: 2026-02-19 08:00 KST (weekly)*

---

[Previous entries continue below...]