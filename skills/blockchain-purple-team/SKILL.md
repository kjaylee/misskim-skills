---
name: blockchain-purple-team
description: Meta-security analysis that finds structural gaps missed by Black Team (historical patterns) and Red Team (novel techniques). Use when analyzing why audits fail, why patches get bypassed, systemic risk patterns, architecture-level vulnerabilities, or operational security failures in blockchain protocols. Triggers on purple team, meta-security, gap analysis, audit failure analysis, defense review, architecture security, operational security, systemic risk assessment, or cross-team coverage analysis.
---

# Blockchain Purple Team — Meta-Security & Structural Gap Analysis

Find what Black Team and Red Team **cannot see** — the structural blind spots, audit failures, and systemic patterns that make defenses fail.

## When to Use

- Post-audit gap analysis ("what did the auditors miss?")
- Cross-team coverage assessment (Black + Red + Blue coverage map)
- Architecture-level security review (not code, but system design)
- Operational security assessment (key management, deployment, monitoring)
- Systemic risk modeling (correlation, cascade, contagion)
- Defense effectiveness validation (do the patches actually work?)

## Purple Team Unique Perspective

| Team | Question | Time | Level |
|---|---|---|---|
| Black | "What attacks happened?" | Past | Code |
| Red | "What attacks are possible?" | Future | Code |
| **Purple** | **"Why do defenses fail?"** | Meta | Architecture + Operations |

## Five Pillars of Analysis

### Pillar 1: Audit Failure Patterns
Why do professional audits miss critical vulnerabilities?

Read `references/audit-failures.md` for patterns including:
- Scope blindness (auditor focuses on code, misses economic design)
- Assumption inheritance (auditor trusts external dependencies)
- Temporal blindness (point-in-time audit vs evolving protocol)
- Composition blindness (individual components audited separately)

### Pillar 2: Defense Bypass Evolution
How do patched vulnerabilities get re-exploited?

Read `references/defense-evolution.md` for patterns including:
- Patch regression (fix breaks something else)
- Variant attacks (same root cause, different vector)
- Defense decay (defense valid at deployment, invalid after upgrades)
- Incomplete fix (root cause unaddressed, symptom patched)

### Pillar 3: Systemic Composition Risk
When individually safe components create dangerous combinations.

Analysis framework:
1. Map all **trust boundaries** (on-chain ↔ off-chain ↔ oracle ↔ frontend)
2. For each boundary: "What happens if the other side lies?"
3. Map all **state dependencies** (A reads from B, B reads from C)
4. For each chain: "What's the longest stale-data path?"
5. Map all **authority overlaps** (same key controls multiple things)
6. For each overlap: "What's the blast radius of compromise?"

### Pillar 4: Operational Security Gaps
Code is secure but operations fail.

Checklist:
- Key management (HSM vs file, rotation, backup, access control)
- Deployment (CI/CD security, binary verification, upgrade process)
- Monitoring (what's watched, what's not, alert fatigue, response time)
- Incident response (playbook exists? tested? who decides? communication)
- Dependency management (lockfiles, audit trail, update cadence)

### Pillar 5: Economic Systemic Risk
Cross-protocol and macro-level risks.

Analysis:
- Collateral correlation (what happens when everything drops at once?)
- Liquidity dependency (which external liquidity sources are critical?)
- Oracle dependency (single oracle failure → cascade?)
- Governance capture (what's the cost of 51% control?)
- Contagion paths (protocol failure → which other protocols affected?)

## Coverage Gap Detection

### Method: Cross-Team Matrix

Build a matrix of `[Attack Vectors × Defense Layers]`:

```
                | On-chain | Keeper | Oracle | Frontend | Ops |
Reentrancy      |  B+R     |  -     |  -     |  -       | -   |
Flash Loan      |  B+R     |  -     |  B     |  -       | -   |
Key Compromise  |  -       |  B     |  -     |  -       | B   |
Governance      |  B       |  -     |  -     |  -       | -   |
Cascade/Depeg   |  B       |  -     |  B     |  -       | ?   |  ← GAP
...
```

Empty cells = **coverage gaps**. "?" = partially covered. Fill gaps with new analysis.

### Method: Assumption Inventory

For every security property the protocol claims:
1. State the assumption explicitly
2. Ask: "Who/what can violate this assumption?"
3. Ask: "What happens when it's violated?"
4. Ask: "Is there detection? Is there recovery?"

## Report Format

```markdown
# Purple Team Report — {Protocol Name}

## Coverage Map
{Cross-team matrix with gap highlights}

## Structural Gaps Found: N
## Audit Failure Patterns Applicable: N

## {ID}: {Gap Description}
- **Pillar**: 1-5
- **Gap Type**: Coverage / Assumption / Composition / Operational / Systemic
- **Missed By**: Black / Red / Both
- **Why Missed**: {explanation}
- **Risk If Exploited**: {impact}
- **Recommendation**: {architecture/process change}
```

## Cycling Protocol

Purple Team runs after Black+Red and reviews Blue fixes:
```
Black+Red → Blue fix → Purple review → Blue fix → ... → Full coverage
```

Purple validates that Blue fixes don't create new gaps.
