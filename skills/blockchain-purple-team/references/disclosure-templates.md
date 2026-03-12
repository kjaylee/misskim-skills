# Disclosure Templates

## Template A — short-form initial contact
Use for security email, bug bounty forms, or first DM.

```text
Subject: Reproducible security issue in [Project / Component]

Hello [Team],

I identified a reproducible security issue affecting [scope].

Summary:
- Type: [validation bypass / privilege escalation / oracle issue / etc.]
- Scope: [contract/module/endpoint]
- Reproducibility: [local fork / public testnet]
- Impact: [fund movement / unauthorized action / service disruption / incorrect settlement]

I am sharing this privately first. I can provide detailed reproduction steps, root cause, and remediation suggestions on request or in a follow-up message.

Best,
[Name / handle]
```

## Template B — detailed responsible disclosure
Use once the team acknowledges contact or when the form expects full detail.

```markdown
# Responsible Disclosure — [Project Name]

## 1. Executive summary
- **Issue type**: [type]
- **Severity**: [high/medium/etc.]
- **Reproducibility**: [R2/R3/R4]
- **Affected scope**: [contracts/modules/endpoints]

## 2. Impact
Describe the concrete bad outcome.
Examples:
- unauthorized state transition
- fund loss or mint/burn imbalance
- governance action without required checks
- incorrect oracle-dependent settlement
- denial of service or stuck funds

## 3. Preconditions
List the exact conditions needed:
- attacker permissions
- market state / oracle state
- timing assumptions
- liquidity assumptions
- required addresses or roles

## 4. Reproduction steps
1. [step]
2. [step]
3. [step]
4. observed result: [result]

## 5. Expected vs actual
- **Expected**: [what should happen]
- **Actual**: [what happened instead]

## 6. Root cause
Explain the failure path in plain technical language.
- missing validation
- unsafe trust assumption
- stale dependency chain
- authority overlap
- incomplete invariant enforcement

## 7. Suggested mitigation
Provide the narrowest credible fix first.
Then list any defense-in-depth suggestions.

## 8. Disclosure handling
- private contact date: [date]
- preferred response window: [e.g. 7 or 14 days]
- no public disclosure before coordination
```

## Template C — issue rejected for lack of confidence (internal only)
Do not send externally. Use to park weak findings.

```markdown
# Internal Hold — Not Yet Reportable

## Finding
[short description]

## Why not report yet
- reproduction missing / inconsistent
- impact unclear
- root cause not isolated
- too dependent on unrealistic assumptions

## Next validation move
- build local harness
- fork testnet state
- isolate dependency behavior
- confirm with black/red review
```
