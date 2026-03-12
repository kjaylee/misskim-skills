# Project Execution Template

Use this template when dispatching Purple Team to a specific testnet project.

```markdown
# Purple Team Execution — [Project Name]

## 1. Scope
- Project:
- Chain / testnet:
- Repo / contracts / frontend / docs:
- In-scope components:
- Out-of-scope components:

## 2. Intake context
- Public docs reviewed:
- Existing audits:
- Admin / upgrade model:
- Oracle / bridge / keeper dependencies:
- Known constraints:

## 3. Priority review lenses
- [ ] trust-boundary mapping
- [ ] authority overlap
- [ ] stale-state / oracle dependency
- [ ] upgrade / admin safety
- [ ] operational security
- [ ] economic cascade risk

## 4. Working findings
| ID | Tier | Type | Repro status | Short description |
|---|---|---|---|---|
| PT-01 | R0-R5 | Assumption / Ops / Composition / Coverage / Systemic | none / local / testnet | ... |

## 5. Validation queue
List only findings that still need work before they can be externally reported.

## 6. External-report candidates
List only R2+ findings with clear impact.

## 7. Output packet
- Internal memo: [path]
- Disclosure draft: [path]
- Tracker row(s): [path]
```

## Minimum use rule
Do not create an external-report candidate section unless at least one finding is reproducible (R2+).
