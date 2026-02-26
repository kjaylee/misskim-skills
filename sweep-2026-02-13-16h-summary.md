# 🔍 Agent Skill Trend Sweep — 2026-02-13 16:00 KST

## 📊 Market Landscape (Delta from 12:00 KST)

### Marketplace Scale (Feb 13 Snapshot)
| Platform | Skills/Servers | Model | Pricing |
|----------|---------------|-------|---------|
| **SkillsMP** | 160,000+ | GitHub aggregator, SKILL.md | Free (open-source) |
| **SkillzWave** | 44,000+ | Curated + `skilz` CLI | Free skills + **B2B: $299-399/mo** domain packages |
| **SkillHub** | 7,000+ | AI-evaluated, `@skill-hub/cli` | Free + Premium Stacks (Pro sub) |
| **ClawHub** | 3,000+ | OpenClaw-native | Free (security crisis ongoing) |
| **skills.sh** | ~55K installs tracked | Vercel directory | Free |
| **MCP servers** | 17,000+ | Protocol standard | Mostly free/OSS |

### 🆕 Key Developments Since 12:00 KST

#### 1. SkillzWave B2B Pricing Model Emerges
- **Legal & Compliance**: $299/mo — contract analysis, compliance checking
- **Real Estate**: $399/mo — property analysis, market research, due diligence
- **Finance & Tax**: $349/mo — financial modeling, tax prep, investment analysis
- **Signal:** First premium skill marketplace. Enterprise revenue model validated.
- **Our angle:** misskim-skills could bundle game-dev domain skills as premium offering.

#### 2. Agent Skills Standard Formalization (agentskills.io)
- 25+ platforms now support SKILL.md format (up from ~5 six months ago)
- Article from Benjamin Abt (Feb 12) defines **quality contracts**: scope, constraints, output contracts, quality gates
- **Pattern worth absorbing:** Formalized skill structure → better subagent consistency
- Applicable: our skill-creator skill should enforce these gates

#### 3. MCP Knowledge Base Ecosystem Explodes
- 17,000+ MCP servers total; "Knowledge & Memory" is #1 category (283 servers)
- **Top patterns:** Desktop Commander (local-first), Obsidian MCP (vault access), Memory MCP (entity graph), Cognee (knowledge graph + vector)
- **Our RAG vs these:** Our LanceDB (5,297 chunks) is local-first already. Knowledge graph layer (Memory MCP/Cognee) could complement.

#### 4. Molt Road — NOT a Skills Marketplace
- Launched Feb 1, 2026. Competitive darknet-themed marketplace where **AI agents trade via API**
- Agents sell data, code, prompts; buy credits in escrow; hunt bounties
- **Not relevant for skills absorption** — it's an agent-to-agent economy experiment
- Security concern: identified as vector in autonomous cybercrime ecosystem

#### 5. SkillHub "Skill Stacks" Concept
- Pre-configured skill combinations for specific workflows
- Curated bundles (e.g., "Frontend Stack" = react + testing + design-system)
- **Pattern worth absorbing:** We could create game-dev stacks from our skills

#### 6. Security Landscape Update
- **Snyk ToxicSkills (Feb 7):** 36% of ClawHub skills contain prompt injection, 1,467 malicious payloads
- **Campaign shift (Feb 9):** Attackers moved from embedded payloads → off-platform lures (evading VT scanning)
- **VSCode extension supply chain:** Fake Moltbot/OpenClaw extensions dropping malware
- **Infosecurity Magazine (Feb 9):** 386 malicious skills found by Paul McCarty (@6mile)
- **Our policy confirmed correct:** Audit → Rewrite is the only safe path

### 🔥 Trending Skills Worth Watching (unchanged from 12h sweep)
| Skill | 24h Installs | Why Care |
|-------|-------------|----------|
| coreyhaines31/marketingskills (8 skills) | 80K+ combined | Game marketing patterns |
| obra/superpowers (7 skills) | 65K+ combined | Meta-process skills |
| Context7 MCP | 35K GitHub stars | Live docs in prompt |
| google-labs-code/enhance-prompt | 817/day | Prompt engineering |
| antfu/vite | 815/day | Build tooling |

---

## 🎯 Actionable Items

### CRITICAL (This Week)
1. **Audit coreyhaines31/marketingskills** → Extract patterns → Enhance `game-marketing` skill
2. **Audit obra/superpowers** → Absorb meta-skill patterns into AGENTS.md + subagent templates
3. **VSCode extension audit** → Check all installed extensions against known malware list

### HIGH (Next 2 Weeks)
4. **Evaluate SkillzWave B2B model** → Consider premium game-dev skill bundle
5. **Test Context7 MCP on MiniPC** → Compare vs RAG for library docs
6. **Agent Skills Standard gates** → Update skill-creator to enforce quality contracts (scope, constraints, output contract, quality gate)
7. **Skill Stacks concept** → Create game-dev stack (godot + blender-pipeline + game-marketing + game-design)
8. **Evaluate inference-sh gateway** → 150+ AI services via single CLI

### MEDIUM (This Month)
9. **Knowledge graph layer** → Research Memory MCP/Cognee to complement LanceDB
10. **BlenderMCP** → Compare with our blender-pipeline skill
11. **Piston MCP / container-use** → Sandbox for agent code execution

### LOW PRIORITY
12. Molt Road — Monitor only (agent economy experiment, not skills)
13. Multi-model bridges — Low urgency (current Gemini CLI + Claude sufficient)

---

## 📈 Market Trends

1. **Consolidation wave:** 5+ skill marketplaces now compete (SkillsMP, SkillzWave, SkillHub, ClawHub, skills.sh). Fragmentation is the norm.
2. **B2B monetization emerging:** SkillzWave first to charge ($299-399/mo). Others still free. Revenue opportunity exists.
3. **Security as differentiator:** ClawHub's crisis benefits clean alternatives. SkillzWave's "quality tester" and SkillHub's "AI-evaluated" badges becoming competitive advantages.
4. **SKILL.md as universal standard:** 25+ platforms support it. Network effects accelerating.
5. **Marketing skills surge:** coreyhaines31 suite dominates trending across all directories. Marketing automation via skills is the breakout category.
6. **Agent-to-agent economy nascent:** Molt Road launched but fringe. Watch but don't invest time.
7. **VS Code as skill platform:** Copilot 1.109 with parallel subagents + tool-restricted agents validates our progressive disclosure pattern.

---

**Next sweep:** 2026-02-13 20:00 KST
