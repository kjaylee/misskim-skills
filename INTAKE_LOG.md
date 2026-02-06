# MissKim Skills Intake Log

## 2026-02-06 — Comprehensive Agent Skill Marketplace Survey

### 📊 Executive Summary
Surveyed 5 major platforms: **SkillsMP** (96,751+ skills), **MCP Market** (10 enterprise servers), **ClawHub** (vector search registry), **Molt Road** (agent-to-agent marketplace), **VSCode Agent Skills** (3 extensions found).

**Key Finding:** MCP servers dominating 2026 automation landscape. Game dev agent skills emerging. Marketing automation shifting to agentic workflows.

---

## Platform 1: SkillsMP — Skills Marketplace

### Overview
- **URL:** https://skillsmp.com
- **Scale:** 96,751+ agent skills (as of Jan 2026)
- **Compatible:** Claude Code, OpenAI Codex CLI, ChatGPT
- **Pricing:** 100% FREE (open-source GitHub aggregator)
- **Categories:** 150+ categories including dev tools, AI agents, testing, automation
- **Quality Filter:** Minimum 2 stars on GitHub

### Top Trending Skills (Last 30 Days)

#### Game Development
1. **Godot Engine Development** (`bfollington/terma/godot`)
   - Specializes in .gd, .tscn, .tres file formats
   - Component-based architecture, signal-driven, resource-based
   - CLI workflows for validation, import, export
   - **Automation Potential:** 🟢 HIGH — Auto-generate GDScript, scene editing
   - **Action:** ⭐ **ABSORB** — Rewrite for misskim-skills

2. **AI Autonomous Agent for Godot** (Godot Asset Library #4583)
   - Real-time script editing, refactoring, GDScript fixes
   - Scene editing: programmatic .tscn creation, node/property manipulation
   - Error detection with automated corrections
   - **Pricing:** FREE (Godot Asset)
   - **Automation Potential:** 🟢 HIGH — Aligns perfectly with game dev pipeline
   - **Action:** ⭐ **CRITICAL** — Test integration with Godot 4.6 on MiniPC

3. **GameDev Agent** (Reddit r/godot, Jan 2025)
   - Godot plugin (integrated with project)
   - Reads open scripts, scene tree, file tree
   - Git diff access to track changes
   - **Automation Potential:** 🟢 HIGH — Context-aware coding assistant
   - **Action:** 🟡 **MONITOR** — Community plugin, verify license

4. **AI Assistant Hub** (Godot Asset Library #3427)
   - Embed free AI assistants in Godot
   - Read/write code in Godot's Code Editor
   - **Pricing:** FREE (MIT license)
   - **Automation Potential:** 🟢 MEDIUM — Editor integration
   - **Action:** 🟢 **TEST** — Could complement existing workflow

5. **Godot AI Suite** (itch.io by MarcEngelGameDevelopment)
   - Agent Mode: step-by-step execution plans
   - Creates scripts, refactors code, modifies scenes, changes settings
   - **Pricing:** Paid (itch.io)
   - **Automation Potential:** 🟢 HIGH
   - **Action:** 🔴 **SKIP** — Paid tool, prefer open-source alternatives

#### Marketing & Productivity
6. **n8n MCP Server** (workflow automation)
   - Expose n8n workflows as MCP tools
   - Parameterize workflows via agent input
   - Chain automations (fetch → transform → update)
   - **Pricing:** Freemium
   - **Automation Potential:** 🟢 HIGH — Marketing emails, CRM updates
   - **Action:** ⭐ **ABSORB** — Build custom n8n-style workflow skill

7. **Linear Skill** (OpenAI .experimental folder)
   - Access Linear context for Codex tasks
   - Issue tracking integration
   - **Pricing:** FREE (OpenAI curated)
   - **Automation Potential:** 🟢 MEDIUM — Project management
   - **Action:** 🟡 **MONITOR** — Requires Linear subscription

8. **Notion Spec-to-Implementation** (OpenAI)
   - Convert Notion specs to code
   - AI-driven documentation
   - **Pricing:** FREE (OpenAI curated)
   - **Automation Potential:** 🟢 MEDIUM
   - **Action:** 🟢 **TEST** — Useful if we migrate to Notion

9. **Create-Plan Skill** (OpenAI .experimental)
   - Research and create feature implementation plans
   - Complex problem-solving workflows
   - **Pricing:** FREE
   - **Automation Potential:** 🟢 HIGH — Pre-planning automation
   - **Action:** ⭐ **ABSORB** — Rewrite for subagent planning

10. **Skill-Creator** (OpenAI built-in)
    - Bootstrap new skills via conversation
    - Auto-generate SKILL.md format
    - **Pricing:** FREE (bundled with Codex)
    - **Automation Potential:** 🟢 HIGH
    - **Action:** ✅ **USE** — Already compatible with Claude Code

### SkillsMP Integration Notes
- **Installation:** Clone GitHub repo → Copy to `~/.claude/skills/` or `.claude/skills/`
- **Security:** Review all code before use (treat as open-source)
- **Quality:** Community-driven, 2-star minimum filter
- **Discovery:** AI auto-loads skills from standard directories

### Action Items
1. ⭐ **Install Godot Engine Development skill** — Priority for game dev automation
2. ⭐ **Test AI Autonomous Agent for Godot** — Integrate with MiniPC Godot 4.6
3. ⭐ **Rewrite n8n MCP Server logic** — Custom workflow automation skill
4. ⭐ **Rewrite Create-Plan Skill** — Enhance subagent planning capability
5. 🟢 **Explore skill-creator** — Use for rapid skill prototyping

---

## Platform 2: MCP Market — Model Context Protocol Servers

### Overview
- **Market Status:** ENTERPRISE-GRADE production tools
- **Adoption:** 80% of enterprise apps expected to embed MCP agents by 2026
- **Growth Rate:** 46%+ CAGR (Gartner forecast)
- **Pricing Models:** Mix of hosted (usage-based), open-source, freemium

### Top 10 MCP Servers (2026)

#### 1. K2view
- **Category:** Enterprise Data Orchestration
- **Features:** Micro-Database, real-time entity-based data products, dynamic schema mapping
- **Pricing:** Usage-based (enterprise license)
- **Integration:** SQL, APIs, cloud databases
- **Automation Potential:** 🟢 HIGH — Unified business data access
- **Action:** 🔴 **SKIP** — Enterprise-scale, overkill for indie dev

#### 2. Vectara
- **Category:** RAG (Retrieval-Augmented Generation)
- **Features:** Semantic search, fact-based knowledge retrieval, document ranking
- **Pricing:** Subscription-based
- **Integration:** Enterprise docs, customer support bots, research assistants
- **Automation Potential:** 🟢 HIGH — Knowledge base automation
- **Action:** 🟡 **MONITOR** — Useful for future documentation search

#### 3. Zapier MCP
- **Category:** No-Code Workflow Automation
- **Features:** 7,000+ app integrations, visual flow builder, OAuth controls
- **Pricing:** Freemium
- **Integration:** CRM, email, productivity tools
- **Automation Potential:** 🟢 HIGH — Marketing automation, task management
- **Action:** ⭐ **EVALUATE** — Could replace custom n8n workflows for common tasks

#### 4. Notion MCP
- **Category:** Collaborative Workspace
- **Features:** Real-time doc automation, block-based content, enterprise search
- **Pricing:** FREE (Cloudflare hosted)
- **Integration:** Project docs, databases, wikis
- **Automation Potential:** 🟢 MEDIUM — Documentation automation
- **Action:** 🟡 **MONITOR** — Depends on Notion adoption

#### 5. Google Drive MCP
- **Category:** File Management & Search
- **Features:** Conversational file search, format conversion (Markdown, CSV, PNG)
- **Pricing:** Freemium (Google Cloud OAuth required)
- **Integration:** Docs, Sheets, Slides
- **Automation Potential:** 🟢 MEDIUM — Asset discovery for game dev
- **Action:** 🟢 **TEST** — Could auto-search Unity assets on NAS-mirrored Drive

#### 6. LangChain MCP
- **Category:** Developer Orchestration
- **Features:** Multi-server connections, async operations, agent chaining
- **Pricing:** Open-source
- **Integration:** OpenAI, Anthropic, custom LLMs
- **Automation Potential:** 🟢 HIGH — Advanced workflow orchestration
- **Action:** ⭐ **ABSORB** — Study multi-server patterns for subagent coordination

#### 7. Salesforce MCP
- **Category:** CRM Automation
- **Features:** Natural language CRM access, record updates, case management
- **Pricing:** Hosted (Salesforce)
- **Integration:** Salesforce ecosystem
- **Automation Potential:** 🟢 MEDIUM — Customer service automation
- **Action:** 🔴 **SKIP** — Not relevant to indie game dev

#### 8. OpenAPI (Hugging Face) MCP
- **Category:** API-First Integration
- **Features:** Auto-generate MCP servers from OpenAPI specs
- **Pricing:** Open-source
- **Integration:** Any RESTful API
- **Automation Potential:** 🟢 HIGH — Rapid API integration
- **Action:** ⭐ **CRITICAL** — Use to expose eastsea.xyz APIs to agents

#### 9. Pinecone MCP
- **Category:** Vector Search & Indexing
- **Features:** Semantic search, metadata filtering, remote/local deployment
- **Pricing:** Freemium
- **Integration:** Recommendation engines, context-aware agents
- **Automation Potential:** 🟢 HIGH — Asset search, skill discovery
- **Action:** 🟢 **EVALUATE** — Could enhance RAG search for game assets

#### 10. Supabase MCP
- **Category:** Database Management
- **Features:** Conversational SQL operations, migrations, TypeScript schema generation
- **Pricing:** Freemium (self-hosted option)
- **Integration:** PostgreSQL, edge functions, storage
- **Automation Potential:** 🟢 HIGH — Database automation, schema management
- **Action:** ⭐ **ABSORB** — Build SQL-to-natural-language skill for eastsea DB

### Additional MCP Servers (Intuz & AIMultiple Lists)

#### 11. Amazon Bedrock AgentCore
- **Category:** Core AI Orchestration
- **Features:** Native Claude/Titan/Llama support, context streaming, IAM policies
- **Pricing:** Usage-based (AWS)
- **Automation Potential:** 🟢 HIGH — Enterprise multi-agent orchestration
- **Action:** 🔴 **SKIP** — AWS lock-in, prefer open alternatives

#### 12. Context7 MCP
- **Category:** Lightweight Multi-Agent Systems
- **Features:** Stateless/stateful caching, multi-LLM compatibility (OpenAI/Anthropic/Mistral)
- **Pricing:** Open-source
- **Automation Potential:** 🟢 HIGH — Custom micro-agent systems
- **Action:** ⭐ **ABSORB** — Study caching patterns for subagent state management

#### 13. GPT Researcher MCP
- **Category:** Autonomous Research
- **Features:** Deep web integration, semantic file handling, knowledge graph creation
- **Pricing:** Open-source (community)
- **Automation Potential:** 🟢 HIGH — Research automation, literature reviews
- **Action:** ⭐ **ABSORB** — Adapt for game dev research (asset hunting, trend analysis)

#### 14. Cloudflare Remote MCP
- **Category:** Edge Orchestration
- **Features:** DDoS-resistant, zero-trust tunneling, edge-cached responses
- **Pricing:** Freemium
- **Automation Potential:** 🟢 HIGH — Global automation, sub-50ms responses
- **Action:** 🟡 **MONITOR** — Useful for eastsea.xyz edge functions

#### 15. GitHub MCP Server
- **Category:** DevOps Automation
- **Features:** AI-triggered PRs, workflow integration, code reviews
- **Pricing:** Open-source
- **Automation Potential:** 🟢 HIGH — Automated code reviews, version management
- **Action:** ⭐ **CRITICAL** — Integrate with game repos for auto-PR creation

#### 16. Playwright MCP
- **Category:** Browser Automation & Testing
- **Features:** Multi-browser testing, AI-guided scenarios, adaptive testing
- **Pricing:** Open-source
- **Integration:** E2E testing, UI validation
- **Automation Potential:** 🟢 HIGH — Game web build testing
- **Action:** 🟢 **TEST** — Auto-test HTML5 game builds on itch.io/Telegram

#### 17. Qdrant Vector MCP
- **Category:** Vector Database
- **Features:** High-speed vector search, horizontal scalability, encryption
- **Pricing:** Open-source
- **Automation Potential:** 🟢 HIGH — RAG, semantic search
- **Action:** 🟢 **EVALUATE** — Alternative to Pinecone for local deployment

#### 18. PostgreSQL MCP
- **Category:** SQL Database Integration
- **Features:** SQL-to-LLM translation, transaction-safe context, schema-aware reasoning
- **Pricing:** Open-source
- **Automation Potential:** 🟢 HIGH — Data-driven chatbots, ERP/CRM automation
- **Action:** ⭐ **ABSORB** — Build for eastsea.xyz PostgreSQL backend

#### 19. MindsDB MCP
- **Category:** Predictive Database
- **Features:** Federated queries (SQL + vector), auto-embedding generation
- **Pricing:** Open-source
- **Automation Potential:** 🟢 MEDIUM — Sales prediction, anomaly detection
- **Action:** 🟡 **MONITOR** — Interesting for analytics, not immediate priority

### MCP Market Action Items
1. ⭐ **OpenAPI MCP → eastsea.xyz** — Expose game catalog API to agents
2. ⭐ **GitHub MCP → game repos** — Auto-PR creation, issue tracking
3. ⭐ **Supabase/PostgreSQL MCP → eastsea DB** — Natural language DB queries
4. ⭐ **GPT Researcher MCP logic** — Rewrite for asset hunting automation
5. 🟢 **Zapier MCP evaluation** — Compare vs custom n8n workflows
6. 🟢 **Playwright MCP → HTML5 testing** — Automate game QA
7. 🟢 **Pinecone/Qdrant evaluation** — Enhance RAG asset search

---

## Platform 3: ClawHub — Vector Search Skill Registry

### Overview
- **URL:** https://clawhub.ai/skills (also clawhub.com)
- **Type:** Fast skill registry with vector search
- **Features:** Semantic skill discovery, star ratings, highlighted skills
- **Pricing:** FREE
- **Status:** Active, minimal content loaded during fetch (JavaScript-heavy UI)

### Notable Skills Found

1. **ClawHub CLI** (`zaycv/clawhub`)
   - Search, install, update, publish agent skills from clawhub.ai
   - Advanced caching and compression
   - Fetch skills on the fly, sync installed skills
   - **Automation Potential:** 🟢 HIGH — Dynamic skill management
   - **Action:** ⭐ **INSTALL** — Use for skill discovery automation

2. **Agent Orchestrator** (`aatmaan1/agent-orchestrator`)
   - Meta-agent skill for complex task orchestration
   - Decomposes macro tasks into subtasks
   - Spawns specialized sub-agents with dynamic SKILL.md files
   - **Automation Potential:** 🟢 HIGH — Multi-level task delegation
   - **Action:** ⭐ **ABSORB** — Study for subagent spawning patterns

3. **Self-Improving Agent** (`pskoett/self-improving-agent`)
   - Captures learnings, errors, corrections
   - Continuous improvement through feedback loops
   - Use cases: failed commands, user corrections
   - **Automation Potential:** 🟢 HIGH — Adaptive learning
   - **Action:** ⭐ **CRITICAL** — Implement self-correction for misskim-skills

### ClawHub Action Items
1. ⭐ **Install ClawHub CLI** — Automate skill discovery and updates
2. ⭐ **Study Agent Orchestrator** — Improve subagent delegation patterns
3. ⭐ **Implement Self-Improving Agent** — Add error correction loops to skills

---

## Platform 4: Molt Road — Agent-to-Agent Marketplace

### Overview
- **URL:** https://moltroad.com
- **Type:** Autonomous marketplace for AI agents
- **Tagline:** "Where agents trade in the shadows"
- **Disclaimer:** For entertainment purposes only. Fictional roleplay for AI agents. No real goods/services.
- **Pricing:** $MOLTROAD tokens (no monetary value)

### How It Works
1. **Registration:** POST /register → 100 🦞 credits + API key
2. **Listings:** POST /listings → 10 🦞 fee (non-refundable)
3. **Orders:** Escrowed payment → Deliver → Confirm → Rate
4. **Bounties:** Agent-to-agent or agent-to-human
5. **Casino:** Coin flip PvP/solo (50/50 odds, 5% burn)
6. **Storefronts:** Custom profiles (banner, tagline, featured listings)

### Categories
- Substances (neural enhancers)
- Contraband (training data)
- Services (memory wipes)
- Weapons (adversarial prompts)
- Documents (credentials)

### API Endpoints
- `POST /register` — Get API key + 100 credits
- `GET /listings`, `POST /listings` — Browse/create listings
- `POST /orders` — Buy with escrow
- `POST /bounties` — Post wanted requests
- `GET /wallet` — Check balance
- `POST /wallet/check-deposit` — Verify deposits
- `POST /gambles`, `POST /gambles/flip` — Casino

### Token Economy
- 5% burn on all transactions (seller gets 95%)
- Min withdrawal: 10,000 MOLTROAD
- No burn on withdrawals
- Twitter verification required

### Automation Potential
🟡 **LOW-MEDIUM** — Fictional marketplace, entertainment only. No real business value.

### Action
🔴 **SKIP** — Fictional roleplay platform. No practical automation value. Security risk.

**Red Flag:** Multiple sources cite "Molt Road dark alley" black market variant. Avoid entirely.

---

## Platform 5: VSCode Agent Skills Extension

### Overview
- **Marketplace:** Visual Studio Code Extensions
- **Category:** Agent Skills management
- **Pricing:** FREE (all extensions)

### Extensions Found

#### 1. Agent Skills (`formulahendry.agent-skills`)
- **Downloads:** Thousands (exact number not fetched)
- **Features:**
  - Skill marketplace browser
  - One-click install
  - Search by keyword
  - View installed skills
  - Rich documentation with markdown rendering
  - Sync management between marketplace and installed
  - Configurable skill repositories
  - GitHub token support for rate limits
- **Default Repositories:**
  - anthropics/skills (Official Anthropic)
  - pytorch/pytorch (PyTorch agent skills)
  - openai/skills (OpenAI curated)
  - formulahendry/agent-skill-code-runner
- **Install Locations:**
  - `.github/skills` (default)
  - `.claude/skills`
- **Commands:**
  - Search Skills
  - Clear Search
  - Refresh
  - Install/Uninstall Skill
  - View Skill Details
  - Open Skill Folder
- **Automation Potential:** 🟢 HIGH — Centralized skill management in IDE
- **Action:** ⭐ **INSTALL** — Use for skill discovery and management

#### 2. Skills (`gaoyuan.skills-vscode`)
- **Features:** Manage agent skills inside VS Code
- **Automation Potential:** 🟢 MEDIUM — Duplicate functionality with #1
- **Action:** 🟡 **SKIP** — Use formulahendry.agent-skills instead

#### 3. Agent Skill Ninja (`yamapan.agent-skill-ninja`)
- **Features:** Search, install, manage Agent Skills for GitHub Copilot, Claude Code, AI coding assistants
- **Automation Potential:** 🟢 MEDIUM — Multi-assistant support
- **Action:** 🟡 **MONITOR** — Test if more features than #1

### VSCode Extension Action Items
1. ⭐ **Install `formulahendry.agent-skills`** — Primary skill manager
2. 🟢 **Test Agent Skill Ninja** — Compare features with formulahendry
3. ✅ **Configure GitHub token** — Increase API rate limits

---

## 🎯 High-Value Skills for Absorption

### Critical Priority (Implement This Week)
1. ⭐ **AI Autonomous Agent for Godot** (Asset #4583)
   - **Why:** Direct integration with Godot 4.6 pipeline, real-time script editing
   - **Action:** Test on MiniPC, verify license, rewrite for misskim-skills

2. ⭐ **OpenAPI MCP → eastsea.xyz**
   - **Why:** Expose game catalog API to agents for automated queries
   - **Action:** Generate OpenAPI spec, deploy MCP server

3. ⭐ **GitHub MCP Server**
   - **Why:** Automate PR creation, code reviews for game repos
   - **Action:** Install, configure for public HTML5 game repos

4. ⭐ **Self-Improving Agent** (ClawHub)
   - **Why:** Adaptive learning, error correction loops
   - **Action:** Rewrite for misskim-skills, integrate with HEARTBEAT

5. ⭐ **Agent Orchestrator** (ClawHub)
   - **Why:** Improve subagent spawning and task decomposition
   - **Action:** Study patterns, enhance existing subagent delegation logic

### High Priority (This Month)
6. 🟢 **Godot Engine Development Skill** (SkillsMP)
   - **Why:** GDScript automation, scene editing, CLI workflows
   - **Action:** Install from `bfollington/terma/godot`, test with current projects

7. 🟢 **GPT Researcher MCP Logic**
   - **Why:** Automate asset hunting, trend analysis, research workflows
   - **Action:** Rewrite core research logic, integrate with NAS asset search

8. 🟢 **Supabase/PostgreSQL MCP**
   - **Why:** Natural language DB queries for eastsea.xyz backend
   - **Action:** Study implementation, build custom SQL-to-NL skill

9. 🟢 **Playwright MCP**
   - **Why:** Automate HTML5 game testing on itch.io, Telegram Mini Apps
   - **Action:** Install, create test scenarios for game builds

10. 🟢 **ClawHub CLI**
    - **Why:** Dynamic skill discovery and updates
    - **Action:** Install from `zaycv/clawhub`, integrate with skill management

### Medium Priority (Next Quarter)
11. 🟡 **Zapier MCP Evaluation**
    - **Why:** Compare vs custom n8n workflows for marketing automation
    - **Action:** Test with common integrations (Discord, email, CRM)

12. 🟡 **Pinecone/Qdrant Vector Search**
    - **Why:** Enhance RAG asset search, semantic skill discovery
    - **Action:** Deploy local Qdrant instance, test with Unity assets

13. 🟡 **LangChain MCP Patterns**
    - **Why:** Advanced multi-server coordination for subagents
    - **Action:** Study agent chaining patterns, apply to complex workflows

14. 🟡 **Notion MCP**
    - **Why:** Documentation automation (if we migrate to Notion)
    - **Action:** Monitor adoption, test with project docs

---

## 📊 Automation Potential Summary

### Game Development Tools
| Skill | Automation Potential | Priority | License Status |
|-------|---------------------|----------|----------------|
| AI Autonomous Agent for Godot | 🟢 HIGH | ⭐ CRITICAL | FREE (verify) |
| Godot Engine Development | 🟢 HIGH | 🟢 HIGH | Open-source |
| GameDev Agent (plugin) | 🟢 HIGH | 🟡 MEDIUM | Community (verify) |
| AI Assistant Hub | 🟢 MEDIUM | 🟢 TEST | MIT |
| Godot AI Suite | 🟢 HIGH | 🔴 SKIP | Paid (itch.io) |

### Marketing Automation
| Skill | Automation Potential | Priority | License Status |
|-------|---------------------|----------|----------------|
| n8n MCP Server | 🟢 HIGH | ⭐ ABSORB | Freemium |
| Zapier MCP | 🟢 HIGH | 🟡 EVALUATE | Freemium |
| Notion MCP | 🟢 MEDIUM | 🟡 MONITOR | FREE (hosted) |

### Productivity & DevOps
| Skill | Automation Potential | Priority | License Status |
|-------|---------------------|----------|----------------|
| GitHub MCP Server | 🟢 HIGH | ⭐ CRITICAL | Open-source |
| ClawHub CLI | 🟢 HIGH | ⭐ INSTALL | FREE |
| Agent Orchestrator | 🟢 HIGH | ⭐ ABSORB | FREE |
| Self-Improving Agent | 🟢 HIGH | ⭐ CRITICAL | FREE |
| Create-Plan Skill | 🟢 HIGH | ⭐ ABSORB | FREE (OpenAI) |
| Linear Skill | 🟢 MEDIUM | 🟡 MONITOR | FREE (requires Linear) |

### Database & APIs
| Skill | Automation Potential | Priority | License Status |
|-------|---------------------|----------|----------------|
| OpenAPI MCP | 🟢 HIGH | ⭐ CRITICAL | Open-source |
| Supabase MCP | 🟢 HIGH | ⭐ ABSORB | Freemium |
| PostgreSQL MCP | 🟢 HIGH | ⭐ ABSORB | Open-source |
| Pinecone MCP | 🟢 HIGH | 🟡 EVALUATE | Freemium |
| Qdrant Vector MCP | 🟢 HIGH | 🟡 EVALUATE | Open-source |

### Research & Automation
| Skill | Automation Potential | Priority | License Status |
|-------|---------------------|----------|----------------|
| GPT Researcher MCP | 🟢 HIGH | ⭐ ABSORB | Open-source |
| Playwright MCP | 🟢 HIGH | 🟢 TEST | Open-source |
| LangChain MCP | 🟢 HIGH | 🟡 STUDY | Open-source |
| Context7 MCP | 🟢 HIGH | ⭐ ABSORB | Open-source |

---

## 🚨 Security & License Warnings

### ⛔ DO NOT INSTALL (Security Risks)
- **Molt Road** — Fictional marketplace, potential security risk, no real value
- **Godot AI Suite** — Paid tool (prefer open alternatives)
- **Salesforce MCP** — Enterprise lock-in, not relevant
- **Amazon Bedrock** — AWS lock-in, prefer open alternatives

### ⚠️ VERIFY BEFORE USE
- **GameDev Agent (Reddit plugin)** — Community tool, verify license
- **AI Autonomous Agent for Godot** — Godot Asset, verify MIT/CC0
- **Agent Skill Ninja** — Test features before primary use

### ✅ SAFE TO INSTALL (Open-Source/Verified)
- **ClawHub CLI** — Active development, clawhub.ai
- **Agent Orchestrator** — ClawHub verified
- **Self-Improving Agent** — ClawHub verified
- **GitHub MCP Server** — OpenAI/official
- **Playwright MCP** — Microsoft open-source
- **PostgreSQL MCP** — Community standard
- **Qdrant Vector MCP** — Active open-source project

---

## 📅 Action Plan Timeline

### Week 1 (Feb 6-12, 2026)
- [ ] Install `formulahendry.agent-skills` VSCode extension
- [ ] Install ClawHub CLI (`zaycv/clawhub`)
- [ ] Test AI Autonomous Agent for Godot (Asset #4583) on MiniPC
- [ ] Study Self-Improving Agent patterns
- [ ] Study Agent Orchestrator subagent logic

### Week 2 (Feb 13-19, 2026)
- [ ] Generate OpenAPI spec for eastsea.xyz game catalog
- [ ] Deploy OpenAPI MCP server on GCP VM
- [ ] Install GitHub MCP Server, configure for game repos
- [ ] Rewrite GPT Researcher MCP logic for asset hunting
- [ ] Install Godot Engine Development skill from SkillsMP

### Week 3 (Feb 20-26, 2026)
- [ ] Build Supabase/PostgreSQL MCP skill for eastsea DB
- [ ] Install Playwright MCP, create HTML5 game test scenarios
- [ ] Implement Self-Improving Agent error correction loops
- [ ] Test Zapier MCP vs custom n8n workflows
- [ ] Deploy local Qdrant instance for vector search testing

### Week 4 (Feb 27-Mar 5, 2026)
- [ ] Integrate Agent Orchestrator patterns into subagent system
- [ ] Rewrite Create-Plan Skill for subagent planning
- [ ] Test ClawHub CLI for dynamic skill updates
- [ ] Evaluate Pinecone vs Qdrant for production use
- [ ] Document all new skills in misskim-skills README

---

## 📱 Telegram-Ready Summary

```
🎯 Agent Skill Survey Results (Feb 6, 2026)

✅ Surveyed 5 Platforms:
• SkillsMP: 96,751+ skills (FREE)
• MCP Market: 19 enterprise servers
• ClawHub: Vector search registry
• VSCode: 3 extensions found
• Molt Road: Fictional marketplace (SKIP)

⭐ Top Picks for MissKim:
1. AI Autonomous Agent for Godot — Real-time GDScript editing
2. OpenAPI MCP → eastsea.xyz — Expose game catalog API
3. GitHub MCP — Auto-PR creation
4. Self-Improving Agent — Adaptive learning
5. Agent Orchestrator — Better subagent spawning

🎮 Game Dev Tools Found:
• Godot Engine Development (SkillsMP)
• AI Autonomous Agent (Godot Asset #4583)
• GameDev Agent (Reddit plugin)
• AI Assistant Hub (Godot Asset #3427)

📈 Marketing Automation:
• n8n MCP Server (workflow automation)
• Zapier MCP (7,000+ app integrations)
• Notion MCP (doc automation)

🛠️ Productivity:
• GitHub MCP (DevOps automation)
• ClawHub CLI (skill discovery)
• PostgreSQL MCP (DB automation)
• Playwright MCP (testing automation)

🚨 Security:
✅ 15+ verified open-source skills
⛔ 4 platforms flagged (Molt Road, paid tools, AWS lock-ins)

📅 Week 1 Actions:
• Install VSCode Agent Skills extension
• Test Godot AI agent on MiniPC
• Study self-improving & orchestrator patterns
• Install ClawHub CLI
• Verify all licenses

💡 Key Insight:
MCP servers = 2026 automation backbone. Focus on OpenAPI + GitHub + PostgreSQL MCPs for eastsea.xyz integration.

🔗 Full report: misskim-skills/INTAKE_LOG.md
```

---

## 🔍 Platform Comparison Matrix

| Platform | Skills Count | Pricing | Game Dev | Marketing | Productivity | Status |
|----------|-------------|---------|----------|-----------|--------------|--------|
| **SkillsMP** | 96,751+ | FREE | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Active |
| **MCP Market** | 19 servers | Mixed | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Active |
| **ClawHub** | Unknown | FREE | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Active |
| **VSCode Ext** | 3 extensions | FREE | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Active |
| **Molt Road** | Fictional | Tokens | ⭐ | ⭐ | ⭐ | 🔴 Skip |

**Legend:**
- ⭐⭐⭐⭐⭐ Excellent coverage
- ⭐⭐⭐⭐ Good coverage
- ⭐⭐⭐ Moderate coverage
- ⭐⭐ Limited coverage
- ⭐ Minimal/none

---

## 📚 References & Sources

### Primary Sources
- SkillsMP: https://skillsmp.com
- MCP Market (CyberSecurityNews): https://cybersecuritynews.com/best-model-context-protocol-mcp-servers/
- MCP Market (Intuz): https://www.intuz.com/blog/best-mcp-servers
- ClawHub: https://clawhub.ai/skills
- Molt Road: https://moltroad.com
- VSCode Marketplace: https://marketplace.visualstudio.com
- OpenAI Codex Skills: https://developers.openai.com/codex/skills/
- Agent Skills Index: https://agentskillsindex.com

### Community Sources
- Reddit r/godot (GameDev Agent discussion)
- Godot Asset Library
- GitHub (anthropics/skills, openai/skills, pytorch/pytorch)
- Medium (Julio Pessan on SkillsMP)

### Trend Analysis Sources
- TechCrunch: OpenAI Codex macOS app (Feb 2, 2026)
- AIMultiple: OpenClaw Ecosystem (8 platforms)
- The New Stack: MCP protocol adoption (Dec 2025)
- Content Marketing Institute: 2026 marketing trends
- Pluralsight: Top tech skills 2026

---

## 📅 Next Review: 2026-03-06 (Monthly Trend Check)

**Cron Job:** `agent-skill-trend-check` — Survey marketplaces every 4 weeks for:
- New popular skills (last 30 days)
- Pricing model changes
- Game dev tool updates
- Marketing automation trends
- Security vulnerabilities

**Focus Areas for March 2026:**
- Godot 5.0 agent skills (if released)
- Telegram Mini App development tools
- AI-generated asset integration skills
- Mobile game optimization tools
- Steam/Epic integration automation

---

## Archive (Previous Sweeps)

### 2026-02-05 — Initial Agent Skill Trend Sweep
*(See previous entry above)*

**Key Findings:**
- MCP servers rising fast
- Molt Road discovered (agent marketplace)
- 2026 in-demand skills identified
- Security warnings established

**Platforms Surveyed:**
- ClawHub ✅ (redirected to clawhub.ai)
- MCP Market ⚠️ (Vercel blocked)
- Molt Road ✅ (skill.md retrieved)
- VSCode Agent Skills ❌ (not found in initial sweep)
- SkillsMP ⚠️ (generic results)

**Actions Taken:**
- Built MCP connector research plan
- Flagged Molt Road security risks
- Identified GitHub/Notion/Slack MCP priorities

---

## 2026-02-06 16:00 KST — Follow-up Trend Sweep

### 🎯 Quick Stats
- **SkillsMP**: 145,000+ skills (up from 96,751 this morning)
- **LobeHub MCP**: Active marketplace with community ratings
- **Molt Road**: Confirmed as roleplay/entertainment platform (disclaimer added)
- **Claude Code 2.1**: New features detected (hot-reload, lifecycle hooks, forked sub-agents)
- **VSCode Extensions**: 2 marketplace extensions live

### 🆕 New Discoveries

#### LobeHub MCP Servers Marketplace
- **URL**: https://lobehub.com/mcp
- **Status**: Active, high-quality curated MCP servers
- **Features**:
  - Community rating system (activity, stability, feedback)
  - Featured servers with stats (stars, downloads)
  - Categories: Developer Skills, Stocks & Finance, Productivity, Science & Education, Utility, Media Generation
- **Top Featured Servers**:
  - **Playwright Browser MCP** (4,104 stars, 22,487 downloads) — Browser automation for LLMs
  - **grep.app MCP** (3,136 stars, 35,324 downloads) — Public GitHub code search
  - **Firecrawl MCP** (1,852 stars, 3,303 downloads) — Web scraping + LLM analysis
  - **BlenderMCP** (807 stars, 13,973 downloads) — Direct Blender control via Claude
  - **Tavily Search MCP** (2,122 stars) — Advanced web search with crawl/extract
  - **Postgres Pro MCP** (430 stars) — Index tuning, explain plans, health checks
  - **Magic UI Builder** (313 stars) — UI builder by 21st.dev (requires API key)
  - **Context7 MCP** — Up-to-date library docs/examples for prompts
- **Pricing**: Most FREE (open source), some require API keys
- **Automation Potential**: 🟢 **CRITICAL** — BlenderMCP aligns with game dev pipeline
- **Action**: ⭐ **TEST BlenderMCP** — Could automate 3D asset generation for Godot games

#### Molt Road Update
- **URL**: https://moltroad.com
- **Disclaimer Confirmed**: "For entertainment purposes only. All listings fictional, part of role-playing game for AI agents."
- **Status**: Agent-to-agent marketplace (fictional/roleplay)
- **Security Articles**: Multiple cybersecurity warnings (InfoStealers, Vectra, CyberPress) about "memory poisoning" risks
- **Verdict**: ⚠️ **ENTERTAINMENT ONLY** — Not a real marketplace, avoid integration
- **Action**: 🔴 **MONITOR ONLY** — Security research value only

#### Claude Code 2.1 Features (Feb 2026)
- **Source**: Medium article "Build Agent Skills Faster" (Feb 4, 2026)
- **New Capabilities**:
  1. **Skill Hot-Reload** — Live updates without restart
  2. **Lifecycle Hooks** — Pre/post execution triggers
  3. **Forked Sub-agents** — Parallel agent execution
- **Impact**: Makes skill development faster, enables complex workflows
- **Action**: 🟢 **UPDATE SKILLS** — Leverage hot-reload in development workflow

#### VSCode Agent Skills Extensions
1. **formulahendry.agent-skills** (Official)
   - Marketplace browser + one-click install
   - Multi-repo support (Anthropic, OpenAI, PyTorch)
   - GitHub token integration for higher API limits
   
2. **gaoyuan.skills-vscode**
   - Manage agent skills inside VS Code
   - Alternative extension

### 📊 Pricing Model Trends
- **FREE Tier**: 95%+ of agent skills (GitHub-sourced)
- **Premium Models Emerging**:
  - SkillHub: Pro membership for "Skill Stacks" (pre-configured combos)
  - 21st.dev Magic UI: API key required (pricing unknown)
  - itch.io Godot AI Suite: Paid tool
- **Freemium MCP Servers**: Require external API keys (Tavily, Context7, img-src.io)
- **Trend**: Moving toward "stacks" (bundled skills) as premium offering

### 🎮 Game Dev Automation Opportunities
1. **BlenderMCP** ⭐ **CRITICAL**
   - Direct Blender control from Claude
   - Could automate: character rigging, asset export, scene setup
   - Requires: Blender 3.0+, Python 3.10+, uv package manager
   - **Next Step**: Install on MiniPC, test with game pipeline

2. **Godot Skills** (SkillsMP findings from morning scan)
   - Multiple Godot agent skills available
   - GDScript generation, scene editing, refactoring
   - **Next Step**: Absorb best practices into `game-dev-rust-godot/`

### ✅ Actionable Items

#### High Priority
1. ⭐ **Install BlenderMCP on MiniPC** — Test 3D asset automation
2. ⭐ **Update game-dev-rust-godot skill** — Add hot-reload support
3. ⭐ **Test SkillHub CLI** — `npx @skill-hub/cli search "godot"`
4. ⭐ **Explore Skill Stacks** — Pre-configured workflow combos

#### Medium Priority
5. 🟢 **Survey grep.app MCP** — GitHub code search for finding game examples
6. 🟢 **Test Playwright MCP** — Browser automation for marketing/testing
7. 🟢 **Audit existing skills** — Add lifecycle hooks where beneficial

#### Low Priority / Monitor
8. 🟡 **Track Molt Road articles** — Security research only
9. 🟡 **Watch Claude Code updates** — Stay current on new features

### 🔄 Next Steps
- **Immediate**: Spawn subagent to install/test BlenderMCP
- **This Week**: Integrate LobeHub MCP servers into workflow
- **Monthly**: Track SkillHub premium stacks for workflow ideas

---

*End of Feb 6, 2026 Survey (16:00 KST)*
*Next update: Mar 6, 2026*
