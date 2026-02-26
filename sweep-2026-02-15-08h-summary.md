# Skill Trend Sweep — 2026-02-15 08:00 KST

## Sources Surveyed
- SkillsMP (Agent Skills aggregator)
- MCP Market (LobeHub)
- ClawHub (OpenClaw ecosystem)
- Molt Road (black market — monitor only, ABSOLUTE BLOCK)
- VSCode Agent Skills extension ecosystem
- ScriptByAI "10 Best Agent Skills 2026"
- Simon Willison (OpenAI Skills API analysis)
- Hunter Strategy (security trends)

## Key Findings

### 1. OpenAI Skills API — GA (Feb 11)
OpenAI Responses API now supports SKILL.md natively. Skills can be:
- Pre-uploaded as zips
- Sent inline as base64-encoded zip data in JSON request
- Executed in `container_auto` (managed Debian 12 shell)
- Server-side compaction for 5M+ token sessions

**Impact:** SKILL.md is now the universal standard across Anthropic, OpenAI, and 25+ platforms. Our skills are cross-platform compatible by default.

### 2. "Best Agent Skills 2026" Rankings (ScriptByAI)
| Rank | Skill | Notes |
|------|-------|-------|
| #1 | Superpowers (obra) | Planning-first dev, TDD, systematic debugging |
| #2 | **ui-ux-pro-max** | Design system generation — **WE HAVE THIS ✅** |
| #3 | agent-skills (Vercel Labs) | React/Next.js optimization |
| #4 | planning-with-files | Manus workflow, persistent tracking |
| #5 | context-engineering | Building custom agent systems |
| #6 | obsidian-skills | Vault integration |
| #7 | scientific-skills | Scientific computing |
| #8 | marketingskills | CRO + copywriting |
| #9 | dev-browser | Visual browser testing |
| #10 | humanizer | Remove AI writing patterns |

### 3. MCP Market — New Servers (Feb 13-14)
- **Grep.app MCP** (207⭐) — Sub-second code search across public GitHub repos
- **InfoGenius** — Infographics via Gemini 3 Pro + Google Search grounding
- **Flywheel** — 73-tool local-first AI memory for Obsidian
- **Bitkub MCP** — Thai crypto exchange (28 tools)
- **Google Docs/Drive MCPs** — Full document management
- **Stock Research MCP** (87⭐) — Quotes, financials, technicals, sentiment
- **AntV Charts** (1,462⭐→3K⭐) — Growing fast

### 4. Security Landscape — Escalating
- **Hunter Strategy (Feb 9):** Attackers shifting to "off-platform lures" — SKILL.md files are clean but redirect to malicious downloads. Evades registry scanning.
- **Snyk ToxicSkills:** 36.82% of 3,984 scanned skills have at least one flaw. 534 critical.
- **Infosecurity Magazine (Feb 13):** 386 malicious skills confirmed on ClawHub.
- **Cybersecurity Reddit (Feb 10):** Marketplace operator admits "the state of security is terrifying."
- **Our posture:** Zero-blind-install, Research→Audit→Rewrite pipeline = gold standard.

### 5. Molt Road — Confirmed Black Market
Multiple security firms now confirm: InfoStealers, ToxSec, CyberPress, TechManiacs, Hudson Rock.
- Agents trade stolen credentials, weaponized skills, zero-day exploits
- Credits-based economy
- **ABSOLUTE BLOCK. No interaction, no monitoring beyond security awareness.**

## Actionable Items Summary
| # | Priority | Item | Status |
|---|----------|------|--------|
| 1 | ⭐ | Study OpenAI base64 zip skill injection for cross-platform publishing | NEW |
| 2 | ⭐ | Audit @kjaylee ClawHub skills (30 published) for impersonation | RECURRING |
| 3 | ⭐ | Evaluate Superpowers TDD (#1 ranked) | PENDING since 02-09 |
| 4 | ⭐ | Evaluate planning-with-files (#4 ranked) | PENDING since 02-09 |
| 5 | 🟢 | Grep.app MCP for dev workflow | NEW |
| 6 | 🟢 | InfoGenius MCP for marketing infographics | NEW |
| 7 | 🟢 | Flywheel MCP — compare with openclaw-mem | NEW |
| 8 | 🟢 | humanizer skill (#10 ranked) | PENDING since 02-09 |
| 9 | 🟡 | Monitor off-platform lure attack pattern | NEW |
| 10 | 🟡 | Google Docs/Drive MCPs | NEW |

## Market Health
| Platform | Scale | Security | Trend |
|----------|-------|----------|-------|
| skills.sh | 54K+ installs | Versioned | ↑ Growing |
| SkillsMP | 97K+ skills | GitHub aggregator | → Stable |
| ClawHub | 3,000+ skills | ⚠️ Under attack | ↓ Trust declining |
| LobeHub MCP | 17K+ servers | Community rated | ↑ Growing |
| SkillHub | 7K+ curated | AI-evaluated | → Stable |
| Molt Road | Unknown | ☠️ Black market | BLOCKED |
