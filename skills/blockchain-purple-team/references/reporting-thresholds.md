# Reporting Thresholds

## Core rule
**External disclosure requires reproducibility.**
If an issue cannot be reproduced, keep it internal as an observation or hypothesis.

## Tier table

| Tier | Label | Reproducibility | External reporting | Meaning |
|---|---|---:|---:|---|
| R0 | Observation | None | No | A structural concern or oddity with no confirmed exploit path |
| R1 | Hypothesis | Partial / weak | No | A plausible exploit idea that still lacks repeatable proof |
| R2 | Local reproduction | Yes | Yes, conditional | Reproduced on a local fork, harness, or isolated test setup |
| R3 | Public testnet reproduction | Strong | Yes | Safely reproduced against the public testnet scope |
| R4 | Practical exploitability | Strong | Yes, high priority | Exploit path and impact are both clear and realistic |
| R5 | Confirmed live exploitation | Confirmed | Yes, immediate | Attack evidence or successful abuse already exists |

## External disclosure minimum bar
Only disclose externally when all of the following are available:
1. reproducible steps
2. impact statement
3. prerequisites / attack conditions
4. root-cause explanation
5. exploitability or concrete impact demonstrated beyond mere exposure

## Important clarification
Exposure-only findings are usually **internal observations**, not external vulnerability reports, unless they already imply clear demonstrated impact.

## Internal-only queue
Keep these internal until promoted:
- architecture discomfort with no exploit path
- risky assumptions without working break
- operational weakness with no demonstrated impact
- economic/systemic concern without a concrete scenario

## Conditional cases
### Send only after local reproduction (R2)
- privilege escalation
- oracle manipulation path
- validation bypass
- unsafe upgrade or admin control path
- insolvency / liquidation edge case

### Prefer public testnet reproduction (R3)
- issues affecting user funds, minting, redemption, bridge flows, or governance execution
- any case where the team is likely to challenge realism

## Do not send as a vulnerability
Do not externally label these as vulnerabilities without reproduction:
- "looks unsafe"
- "probably exploitable"
- "code smells"
- "single point of failure" without a concrete failure path

## Purple-team role in this model
Purple Team may generate R0-R1 findings internally, but only R2+ findings should enter the disclosure queue.
