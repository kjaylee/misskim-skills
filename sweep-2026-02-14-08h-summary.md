# Skill Trend Sweep — 2026-02-14 08:00 KST

## 🆕 New Signals Since 04:00 Sweep

### 1. "MCP vs Agent Skills vs AGENTS.md" Standard Comparison (Feb 13)
Dr. Leon Eversberg (AI Advances / Medium) published a widely-shared comparison piece positioning:
- **MCP** = "USB-C port" for tool/data connectivity
- **Agent Skills** = packaged domain expertise layer
- **AGENTS.md** = codebase behavior instructions for coding agents
This 3-layer model is gaining consensus. Our stack (AGENTS.md + skills + mcporter) already covers all three.

### 2. OpenAI Codex CLI: MCP + Skills Hardening (Feb 13-14)
Latest Codex CLI commits show:
- `project_doc` skill-render tests made deterministic — skills are first-class in Codex now
- `MCP OAuth creds` backed by files (not in-memory) — production hardening
- `Sandbox read access` now configurable — granular permission model
- `Apps SDK` apps support — third-party app marketplace forming
**Impact:** Codex is converging on the same skill/MCP ecosystem. Our skills are cross-compatible.

### 3. Cloudflare Moltworker (Feb 7-11, new details)
Cloudflare launched self-hosted AI agent runtime: $5/month on Workers+Sandboxes.
- R2 persistent state, AI Gateway, Browser Rendering (headless Chromium at edge)
- Zero Trust Access for auth
**Relevance:** Validates edge-hosted agent pattern. Our MiniPC worker fills similar role locally.

### 4. Amazon Ads MCP Server Beta (Feb ~7)
Amazon Ads opened beta for its MCP server — natural language prompts → ad campaign ops.
First major ad platform with native MCP. Enterprise monetization signal for MCP ecosystem.

### 5. SkillzWave Hits 42,645+ Skills
SkillzWave (vendor-agnostic marketplace) now at 42K+ skills. Offering $299-$399/mo domain expert packages (Legal, Real Estate, Finance). Quality scores via AI evaluation. Premium skill bundles are a real monetization path.

### 6. ClawHub Security Crisis Ongoing
- TheHackerNews: 341 malicious skills, 9,000+ compromised installations
- Infosecurity Magazine: hightower6eu account alone = 7,000 downloads of malware
- Categories targeted: crypto wallets, YouTube tools, auto-updaters, polymarket bots
- ClawHub now has VirusTotal partnership but "cannot be secured" per maintainer admission
**Our policy:** Zero-blind-install confirmed correct. Audit → Rewrite → misskim-skills.

### 7. Community Top Skills (Reddit r/AI_Agents, Feb 13)
Most recommended daily-driver ClawHub skills:
- **github** (managed OAuth, repos/issues/PRs)
- **agentmail** (agent email inboxes, programmatic)
- **linear** (GraphQL project management)
- **automation-workflows** (trigger/action builder)
- **monday** (boards/tasks, 2.5K downloads)
- **playwright-scraper** (anti-bot bypass)
- **playwright-mcp** (full browser automation)
- **obsidian-direct** (fuzzy search, tags, wikilinks)
- **lb-nextjs16-skill** (Next.js 16 docs in markdown)

### 8. LobeHub MCP Trending (Feb 13)
Top by installs: Playwright (22K), Context7 (35K), Tavily (2.2K), Firecrawl (1.9K), AntV Charts (1.5K), Magic UI Builder 21st.dev (319), Postgres Pro (439), Grep code search (205).
New: DART Korean FSS disclosure data server, Harbor container registry, Swedish legal research.

## 📊 Ecosystem Totals (Feb 14 08:00)
| Platform | Count | Trend |
|----------|-------|-------|
| SkillsMP | 160,000+ | ↑ rapid |
| SkillzWave | 42,645+ | ↑ steady |
| ClawHub | 5,705+ | ↑ (security issues) |
| LobeHub MCP | 8,230+ | ↑ daily adds |
| Smithery MCP | 938+ repos | ↑ |
| SkillHub | 7,000+ | ↑ |
| SkillsLLM | new entrant | launching |

## 🎯 Actionable Items (Updated)

### HIGH Priority
1. **Context7 docs skill** — Still #1 demand signal. Version-specific library docs injection. Would benefit our own Godot/Rust dev work.
2. **AgentMail-style skill** — Programmatic agent email inboxes trending. Could automate signup flows, verification chains.
3. **Automation-workflows skill** — Trigger/action workflow builder for agents. High community adoption.
4. **Stripe MCP wrapper** — Payment integration. Direct relevance to our monetization goals.

### MEDIUM Priority
5. **Markdownify skill** — Convert any file (PDF/PPTX/audio/images) to markdown. Universally useful.
6. **Grafana/monitoring skill** — Our GCP/MiniPC/NAS monitoring could use this pattern.
7. **DART Korean FSS skill** — Korean financial disclosure data. Niche but unique market opportunity.
8. **Publish to SkillzWave** — 42K+ marketplace, $299-$399/mo premium tiers. Monetization path for curated bundles.

### LOW Priority
9. Monitor Codex Apps SDK for third-party app marketplace opportunity.
10. Track Cloudflare Moltworker pricing/capabilities for potential deployment alternative.

### 🔒 Security Standing
- ClawHub: RED (36% flawed, ongoing malware campaigns). Zero blind install.
- Molt Road: HARD-DENY. Confirmed adversarial black market.
- SkillzWave: YELLOW (newer, AI-evaluated quality but less battle-tested).
- All external skills: Audit → Rewrite → misskim-skills. No exceptions.

## Sources Checked
- SkillsMP (search results — Cloudflare-protected)
- SkillzWave.ai (live, 42K+ skills, premium tiers)
- SkillsLLM.com (new entrant, minimal content)
- LobeHub.com/mcp (live, Feb 13 listings)
- Obot.ai top 15 MCP servers guide
- Reddit r/AI_Agents ClawHub skills thread (Feb 13)
- AI Advances: MCP vs Skills vs AGENTS.md (Feb 13)
- Releasebot.io: OpenAI Codex CLI commits (Feb 13-14)
- InfoQ/SerenitiesAI: Cloudflare Moltworker
- AdExchanger: Amazon Ads MCP beta
- TheHackerNews/Infosecurity: ClawHub malware
- DigitalApplied: Autonomous AI Agents 2026 landscape
