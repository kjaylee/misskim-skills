---
name: context7-docs
description: Query up-to-date library/framework documentation via Context7 MCP. Use when subagents need latest API docs, code examples, or version-specific references to avoid outdated code generation.
metadata:
  openclaw:
    emoji: 📚
    requires:
      bins: [mcporter]
---

# context7-docs

Fetch latest documentation and code snippets for any library/framework via Context7 MCP (Upstash).

## Prerequisites

- `mcporter` installed (`/opt/homebrew/bin/mcporter`)
- Context7 server configured: `mcporter config add context7 --transport http --url "https://mcp.context7.com/mcp"`
- Verify: `mcporter list context7 --schema`

## Tools Available

| Tool | Purpose |
|------|---------|
| `resolve-library-id` | Find Context7 library ID from a name |
| `query-docs` | Fetch docs/snippets for a library ID |

## Usage

### Step 1: Resolve Library ID

```bash
mcporter call context7.resolve-library-id \
  query="How to set up authentication" \
  libraryName="next.js" \
  --output json
```

Returns matching libraries with:
- **Library ID**: `/org/project` format (e.g. `/vercel/next.js`)
- **Code Snippets**: count of available examples
- **Source Reputation**: High/Medium/Low
- **Benchmark Score**: quality indicator (max 100)
- **Versions**: available version-specific IDs

### Step 2: Query Documentation

```bash
mcporter call context7.query-docs \
  libraryId="/vercel/next.js" \
  query="app router middleware setup" \
  --output json
```

Returns up-to-date documentation and code examples.

## Rules

- Always `resolve-library-id` first, then `query-docs` (unless user provides `/org/project` format directly).
- Max 3 calls per tool per question.
- Pick library with highest Benchmark Score + Source Reputation for ambiguous matches.
- Version-specific queries: use `/org/project/version` format from resolve results.

## Integration Pattern for Subagents

When a subagent needs latest docs for implementation:

```
1. mcporter call context7.resolve-library-id query="<task description>" libraryName="<lib>"
2. Pick best library ID from results
3. mcporter call context7.query-docs libraryId="<id>" query="<specific question>"
4. Use returned docs/snippets in implementation
```

## Common Libraries

| Library | Likely ID |
|---------|-----------|
| Next.js | `/vercel/next.js` or `/websites/nextjs` |
| React | `/facebook/react` |
| Prisma | `/prisma/prisma` |
| Tailwind | `/tailwindlabs/tailwindcss` |
| Stripe | `/stripe/stripe-node` |

Always verify with `resolve-library-id` — IDs may change.
