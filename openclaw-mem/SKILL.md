---
name: openclaw-mem
description: "Local-first RAG memory system for AI agents. Progressive Disclosure search, Auto-Capture from sessions, Brain directories for per-project context, injection defense."
version: 0.2.0
author: kjaylee
tags: [memory, rag, embeddings, local-first, brain]
---

# openclaw-mem

Local-first RAG memory system for AI agents. No API keys required — runs 100% offline with local embeddings.

## Installation

```bash
pip install openclaw-mem
openclaw-mem init
```

This creates the workspace structure:

```
./memory/
├── core.md           # Key decisions & lessons learned
├── observations.md   # Structured observations
└── projects/         # Brain directories (per-project context)
.env                  # OPENCLAW_MEM_ROOT configuration
```

## Key Commands

| Command | Description |
|---------|-------------|
| `openclaw-mem search "query"` | Semantic search over memory |
| `openclaw-mem index --all` | Index all markdown files |
| `openclaw-mem index --changed` | Incremental index (changed files only) |
| `openclaw-mem observe "text" --tag learning` | Record a structured observation |
| `openclaw-mem auto-capture --since 6h` | Extract observations from session transcripts |
| `openclaw-mem auto-capture --since 6h --route-to-brain` | Auto-route observations to Brain files |
| `openclaw-mem brain-check` | Check Brain files for injection patterns |
| `openclaw-mem brain-check --fix` | Auto-fix injection patterns |
| `openclaw-mem archive --execute` | Archive old memory (3-Layer: Hot/Warm/Cold) |

## Brain Directories

Per-project persistent context stored in `memory/projects/{name}.md`:

```bash
# Create a project Brain
echo "# My Project Brain\n\n## Architecture\n- Stack: Python + FastAPI\n" > memory/projects/my-project.md

# Index it
openclaw-mem index memory/projects/my-project.md

# Search across all Brains
openclaw-mem search "project architecture"

# Verify integrity
openclaw-mem brain-check
```

## Progressive Disclosure (2-Step Search)

Reduces token usage by returning summaries first, then full content on demand:

```bash
# Step 1: Get summaries (index view)
openclaw-mem search "deployment" --index
# Returns: chunk IDs + one-line summaries

# Step 2: Get full content for a specific chunk
openclaw-mem search --detail "chunk:0:abc123"
# Returns: full chunk text
```

## Observation Tags

Tag observations for structured knowledge capture:

```bash
openclaw-mem observe "Redis cache TTL should be 1h" --tag decision
openclaw-mem observe "Always test with --dry-run first" --tag learning
openclaw-mem observe "Forgot to check edge case" --tag mistake
openclaw-mem observe "Service mesh pattern works well" --tag architecture
openclaw-mem observe "User prefers dark mode" --tag preference
openclaw-mem observe "Next: add WebSocket support" --tag next
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_MEM_ROOT` | `.` | Workspace root directory |
| `OPENCLAW_MEM_DB_PATH` | `{root}/lance_db` | LanceDB database path |
| `OPENCLAW_MEM_TABLE` | `memory` | LanceDB table name |
| `OPENCLAW_MEM_BACKEND` | `local` | Embedding backend: `local`, `openai`, `ollama` |
| `OPENCLAW_MEM_MODEL` | `all-MiniLM-L6-v2` | Embedding model name |
| `OPENCLAW_MEM_ARCHIVE_DIR` | `{root}/archive` | Archive directory |
| `OPENCLAW_MEM_ARCHIVE_DAYS` | `30` | Days before auto-archiving |
| `OPENCLAW_MEM_SESSION_DIR` | `{root}/sessions` | Session transcripts directory |

## Security

- **Injection Defense**: Brain files are scanned for prompt injection patterns
- **Sanitizer**: All indexed content passes through the injection sanitizer
- **Local-first**: No data leaves your machine — embeddings run locally
