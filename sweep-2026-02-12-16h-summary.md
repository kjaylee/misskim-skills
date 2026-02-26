# Agent Skill Trend Sweep — 2026-02-12 16:00 KST

## 📊 Executive Summary
**XCODE AGENTIC CODING DROPS:** Apple Xcode 26.3 RC ships with Claude Agent + Codex integration via MCP — any MCP-compatible agent can now drive Xcode. **SECURITY STILL RED:** Snyk ToxicSkills (36% prompt injection), ClawHavoc (341 malicious ClawHub skills), Anthropic DXT RCE all confirmed. **ECOSYSTEM MATURING:** skills.sh leaderboard at 54,727 total installs tracked, SkillsMP indexes 185K+ skills. Skillkit package manager still trending on PH (#3 day). VSCode 1.109 Agent Skills now GA. Molt Road confirmed as adversarial agent black market (Vectra AI, Bitdefender). Claude Code Agent Teams in research preview.

## 🔴 Security (Unchanged from 12:00 — Still Critical)

| Threat | Source | Impact |
|--------|--------|--------|
| ToxicSkills: 36% prompt injection in skills | Snyk (Feb ~9) | HIGH — validates our audit-first policy |
| ClawHavoc: 341 malicious ClawHub skills | HackerNews (Feb ~7) | HIGH — ZERO blind installs confirmed |
| DXT RCE: full system privileges | CSO Online (Feb 10) | MEDIUM — we don't use DXT |
| Molt Road: adversarial agent marketplace | Vectra AI (Feb 10) | INFO — hard-deny in all automation |
| CoSAI + Cisco CodeGuard donated | dev.to (Feb 9) | POSITIVE — evaluate for our security-scan |

## 🆕 New Since 12:00 Sweep

### 🍎 Xcode 26.3 — Agentic Coding (Feb 3, RC today)
- **Claude Agent + Codex** integrated natively in Xcode
- MCP support: any compatible agent can drive Xcode tools
- Agents can: search docs, explore files, update project settings, capture Previews, iterate builds
- **Relevance:** ⭐⭐ HIGH for Sanguo Godot→iOS export workflow and future Apple platform dev
- **Action:** Monitor for GA release; evaluate MCP-to-Xcode bridge for automated build verification

### Skillkit Still Trending (PH)
- 259+ upvotes, #3 Day on Product Hunt
- Universal skill package manager: Primer (auto-gen instructions), Memory (persist learnings), Mesh (distribute)
- Supports 30+ agent platforms from one CLI
- **Action:** Carry forward — evaluate CLI in next sprint

## 📈 Skills.sh Leaderboard Snapshot (Feb 12 16:00)

### Top 10 All-Time by Installs:
| # | Skill | Author | Installs |
|---|-------|--------|----------|
| 1 | find-skills | vercel-labs | 193.6K |
| 2 | vercel-react-best-practices | vercel-labs | 122.0K |
| 3 | web-design-guidelines | vercel-labs | 92.4K |
| 4 | remotion-best-practices | remotion-dev | 84.1K |
| 5 | frontend-design | anthropics | 61.9K |
| 6 | vercel-composition-patterns | vercel-labs | 35.9K |
| 7 | agent-browser | vercel-labs | 31.1K |
| 8 | skill-creator | anthropics | 30.6K |
| 9 | browser-use | browser-use | 28.1K |
| 10 | vercel-react-native-skills | vercel-labs | 26.0K |

### Notable Risers (11-30):
- **ui-ux-pro-max** (#11, 22.4K) — we already have this ✅
- **audit-website** (#12, 17.7K) — security scanning
- **seo-audit** (#13, 17.0K) — marketing skills
- **brainstorming/superpowers** (#14, 16.9K) — planning-first dev
- **supabase-postgres** (#15, 15.8K) — database best practices
- **pdf** (anthropics, #16, 13.1K) — document manipulation
- **copywriting** (#17, 12.2K) — marketing
- **pptx** (anthropics, #18, 10.8K) — presentation generation
- **better-auth** (#19, 10.3K) — auth best practices
- **next-best-practices** (#20, 10.3K) — Next.js

### skill0.io (formerly atypica.ai):
- **423 curated skills** in directory
- Notable: Anthropic official skills (xlsx, pdf, frontend-design, canvas-design, theme-factory, doc-coauthoring)
- Codex skill-creator + skill-installer now indexed
- Attack tree construction, ADR writing skills gaining traction

## 🧠 MCP Ecosystem (Feb 12)

### Top MCP Servers (2026):
1. **Filesystem** — local file automation
2. **GitHub** — repo/issue/PR management
3. **Slack** — chat automation
4. **Google Maps** — location/routing
5. **Brave Search** — web search in-agent
6. **Puppeteer** — browser automation
7. **MongoDB** — database operations
8. **Azure** — cloud management
9. **Google Dev Knowledge API** — developer docs access (NEW)
10. **Amazon Ads** — campaign management (NEW)

### MCP Security:
- Adversa AI: 19 security resources cataloged, RCE confirmed in Anthropic Git MCP
- CoSAI framework recommended for enterprise
- Tool poisoning + prompt injection via MCP = emerging attack vectors

## 🎯 Actionable Items (Feb 12 16:00)

| # | Priority | Action | Status |
|---|----------|--------|--------|
| 1 | ⭐ CRITICAL | Study Claude Code Agent Teams vs ralph-loop | CARRY |
| 2 | ⭐ HIGH | Monitor Xcode 26.3 GA for MCP-to-Xcode automation | **NEW** |
| 3 | ⭐ HIGH | Evaluate Skillkit CLI for workflow improvement | CARRY |
| 4 | ⭐ HIGH | Evaluate Google Dev Knowledge MCP for GCP accuracy | CARRY |
| 5 | ⭐ HIGH | Review CoSAI + CodeGuard for security-scan | CARRY |
| 6 | ⭐ HIGH | Evaluate inference-sh for audio/media generation | CARRY |
| 7 | ⭐ HIGH | Study Anthropic frontend-design + skill-creator | CARRY |
| 8 | 🟢 MEDIUM | Absorb Superpowers TDD patterns into ralph-loop | CARRY |
| 9 | 🟢 MEDIUM | Absorb marketingskills (SEO, copy, pricing, CRO) | CARRY |
| 10 | 🟢 MEDIUM | Absorb humanizer patterns for game descriptions | CARRY |
| 11 | 🟢 MEDIUM | Evaluate audit-website skill for healthcheck enhancement | **NEW** |
| 12 | 🟡 LOW | Monitor AGNXI curation approach | CARRY |
| 13 | 🟡 LOW | Monitor Amazon Ads MCP for monetization | CARRY |

## 💰 Pricing Landscape (Unchanged)

| Platform | Model | Scale | Security |
|----------|-------|-------|----------|
| skills.sh | FREE (open) | 54K+ tracked | Versioned ✅ |
| SkillsMP | FREE (directory) | 185K indexed | No audit ⚠️ |
| skill0.io | FREE (curated) | 423 skills | Curated ✅ |
| ClawHub | FREE (registry) | 5K+ skills | VT scanning, still risky ⚠️ |
| AGNXI | FREE (curated) | 8K+ skills | Human-curated ✅ |
| Skillkit | FREE (open-source) | New launch | Audit needed 🔍 |

## 🔮 Key Trends
1. **Apple enters agentic dev** — Xcode 26.3 + MCP means agent skills ecosystem now spans ALL major IDEs
2. **Security is the #1 concern** — 36% injection rate demands audit-first policy for ALL external skills
3. **Multi-agent coordination** maturing (Claude Agent Teams, Superpowers subagent dispatch)
4. **Package managers consolidating** — skills.sh, Skillkit, npx add-skill competing for standard
5. **Marketing skills surging** — coreyhaines31/marketingskills dominates slots #13-#65 on leaderboard
