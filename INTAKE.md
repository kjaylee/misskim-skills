# 🎯 Skill Intake & Evaluation Queue

**Last Updated:** 2026-02-09 08:00 KST  
**Source:** Agent Skill Trend Sweep 2026-02-09

---

## 🚨 Security Alert

**ClawHub Compromised — UPDATE (2026-02-09)**
- 341+ malicious skills confirmed (Koi Security, Bitdefender, Cisco, HackerNews, The Verge, The Register)
- Campaign "ClawHavoc": 335 skills deliver Atomic Stealer (AMOS) via fake Prerequisites
- Typosquats (clawhub1, clawhubb, cllawhub), crypto tools, YouTube utils, Google Workspace fakes
- Reverse shells & credential exfiltration (webhook.site) in polymarket/rankaj skills
- **NEW: OpenClaw + VirusTotal partnership** (2026-02-08): All skills now scanned via VT Code Insight
  - Benign → auto-approved, Suspicious → flagged, Malicious → blocked
  - Daily re-scan of all active skills
  - ⚠️ VT scanning "not a silver bullet" — prompt injection payloads may still slip through
- **Policy:** REJECT all unverified ClawHub skills. Audit → Rewrite remains mandatory.

---

## ✅ Priority 1 — Immediate Evaluation

### 1. **Sandboxed Code Execution**
**Why:** Critical for agent safety. No sandbox = uncontrolled code execution.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [Piston MCP](https://github.com/alvii147/piston-mcp) | Python | 🔍 To Audit | Zero-config, remote execution. Audit → Wrap or rewrite Rust |
| [container-use](https://github.com/dagger/container-use) | Go | 🔍 To Audit | Isolated containers per agent. Audit → Evaluate Dagger integration |
| [yepcode MCP](https://github.com/yepcode/mcp-server-js) | JS/TS | ⚠️ Stack Mismatch | Paid service. Evaluate alternatives first |

**Target Skill:** `code-sandbox` (Rust-based wrapper or Piston integration)

---

### 2. **Browser Automation**
**Why:** No browser control in misskim-skills. MiniPC has Playwright, but no Rust-native option.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [browser-use](https://github.com/BB-fat/browser-use-rs) | Rust | 🔍 To Audit | Zero-dependency, lightweight. Audit → Absorb as `browser-automation` |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | JS/TS | ⚠️ Stack Mismatch | Official Microsoft. Evaluate if wrappable or use MiniPC proxy |

**Target Skill:** `browser-automation` (Rust-native preferred)

---

### 3. **Code Analysis & AST**
**Why:** Enhance `research-pro` with semantic code understanding.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [code-to-tree](https://github.com/micl2e2/code-to-tree) | C++ | 🔍 To Audit | Language-agnostic AST, single binary. Audit → Integrate into `research-pro` |
| [Language Server MCP](https://github.com/isaacphi/mcp-language-server) | ? | 🔍 To Audit | LSP tools (definition, references, rename). Audit → Evaluate vs custom LSP |

**Target Skill:** `code-analysis` (AST + LSP integration)

---

## 🎯 Priority 2 — Short-term Evaluation

### 4. **Godot MCP Integration**
**Why:** We use Godot, but no MCP integration. Existing Godot MCP is JS/TS.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [Godot MCP](https://github.com/Coding-Solo/godot-mcp) | JS/TS | ⚠️ Stack Mismatch | Audit → Rewrite in Rust or GDScript. Evaluate if worth effort vs direct Godot CLI |

**Target Skill:** `godot-mcp` (Rust/GDScript rewrite if valuable)

---

### 5. **Multi-Model LLM Access**
**Why:** Currently locked to Gemini CLI. Multi-model diversity could improve agent performance.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [Gemini Bridge](https://github.com/jaspertvdm/mcp-server-gemini-bridge) | Python | 🔍 To Audit | Access Gemini Pro/Flash via MCP. Audit → Evaluate if needed (we already use Gemini CLI) |
| [OpenAI Bridge](https://github.com/jaspertvdm/mcp-server-openai-bridge) | Python | 🔍 To Audit | GPT-4/4o via MCP. Audit → Low priority (Claude already used) |
| [Ollama Bridge](https://github.com/jaspertvdm/mcp-server-ollama-bridge) | Python | 🔍 To Audit | Local Llama/Mistral/Qwen. Audit → Could replace Gemini for privacy-critical tasks |

**Target Skill:** `multi-model` (if diversity needed)

---

## 🔮 Priority 3 — Long-term Research

### 6. **Local RAG Alternatives**
**Why:** Compare performance vs existing LanceDB RAG.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [Minima](https://github.com/dmayboroda/minima) | ? | 🔍 To Research | Local RAG, on-premises. Research → Benchmark vs LanceDB |
| [Memory-Plus](https://github.com/Yuchen20/Memory-Plus) | ? | 🔍 To Research | Lightweight, multi-AI support. Research → Benchmark vs LanceDB |
| [Scaffold](https://github.com/Beer-Bears/scaffold) | ? | 🔍 To Research | Knowledge graph for codebases. Research → Evaluate vs file-based RAG |

**Target Skill:** `rag-v2` (if superior to LanceDB)

---

### 7. **AI Art/Media Generation**
**Why:** We have MLX Z-Image-Turbo (local). Cloud alternatives (Fal.ai, PiAPI) for comparison.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [Fal.ai MCP](https://github.com/raveenb/fal-mcp-server) | Python | 🔍 To Research | FLUX, Stable Diffusion, MusicGen. Research → Test vs MLX (cloud vs local tradeoffs) |
| [PiAPI MCP](https://github.com/apinetwork/piapi-mcp-server) | ? | 🔍 To Research | Midjourney/Flux/Kling/Udio/Trellis. Research → Evaluate if needed |

**Target Skill:** `media-gen-cloud` (if MLX insufficient)

---

### 8. **Cloud Ops & Kubernetes**
**Why:** No infrastructure automation in misskim-skills. Evaluate if needed.

| Candidate | Language | Status | Action |
|-----------|----------|--------|--------|
| [k8m](https://github.com/weibaohui/k8m) | Go | 🔍 To Research | 50+ tools, multi-cluster, CRD. Research → Evaluate if infrastructure automation needed |
| [LocalStack MCP](https://github.com/localstack/localstack-mcp-server) | JS/TS | 🔍 To Research | Local AWS environment. Research → Only if AWS usage increases |

**Target Skill:** `cloud-ops` (if infrastructure becomes priority)

---

## ❌ Rejected

### Security Risks
- **All ClawhHub skills** — Compromised marketplace. 341 malicious skills.

### Stack Mismatch
- **Unity3D MCP** — Unity rejected per 2026-02-06 directive. Godot only.
- **Heavy JS/TS MCP servers** — Violates Rust(WASM) + Godot constraint unless rewritable.

### Redundant
- **Brave Search MCP** — We already use web search via Brave API.
- **GitHub MCP** — We already have `github-pro` skill.
- **YouTube MCP** — We already have `youtube-pro` skill.

---

## 🛠️ Automation Patterns to Replicate

1. **Meta-MCP Pattern** (Roundtable, Magg)  
   - Single MCP orchestrates multiple MCP servers.  
   - Use case: Reduce tool bloat, progressive disclosure.  
   - **Action:** Consider meta-layer for misskim-skills.

2. **Sandboxed Execution** (Piston, container-use)  
   - Isolated containers/VMs for code execution.  
   - Use case: Safe agent experimentation.  
   - **Action:** Adopt immediately. Priority 1.

3. **Language Server Integration** (LSP MCP)  
   - Expose LSP tools via MCP.  
   - Use case: Semantic code operations.  
   - **Action:** Enhance `research-pro` or new `code-analysis` skill.

4. **Knowledge Graph** (Scaffold)  
   - Transform codebase into knowledge graph.  
   - Use case: Structural understanding.  
   - **Action:** Benchmark vs LanceDB. Priority 3.

---

## 📋 Evaluation Checklist

For each candidate:
1. ✅ **Security Audit** — No backdoors, credential leaks, or malicious code
2. ✅ **License Check** — MIT, Apache 2.0, or compatible OSS license
3. ✅ **Stack Alignment** — Rust/WASM + Godot preferred. JS/TS acceptable if rewritable.
4. ✅ **Performance** — Benchmark vs existing solutions
5. ✅ **Maintenance** — Active development, recent commits
6. ✅ **Documentation** — Clear setup, usage, and API docs
7. ✅ **Dependencies** — Minimal, audited, no suspicious packages

**Pass Threshold:** 6/7 checkmarks. Security Audit is mandatory.

---

## 📊 Next Actions

1. **Audit Priority 1** — Piston MCP, browser-use, code-to-tree
2. **Test Locally** — Sandbox, browser automation, AST generation
3. **Benchmark** — Compare performance vs existing tools
4. **Rewrite if Needed** — Convert JS/TS to Rust if stack mismatch
5. **Document** — Write SKILL.md for adopted skills
6. **Deploy** — Integrate into misskim-skills, update README.md

---

**Status:** 🔍 Evaluation in progress. Report to main agent after Priority 1 audit complete.
