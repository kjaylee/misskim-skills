# Purple Team Pipeline

## Principle
Purple Team can think broadly, but it must report narrowly.
Internal exploration may include R0-R1 observations. External reporting requires R2+ reproducibility.

## Operating flow

### Stage 1 — Intake
Collect:
- project name
- scope (contracts, endpoints, docs, repo, frontend, ops)
- chain / testnet
- known constraints
- disclosure channel availability

### Stage 2 — Internal triage
Classify each lead:
- architectural gap
- operational weakness
- economic/systemic risk
- code/control-flow issue
- dependency / integration trust issue

Assign a provisional tier (R0-R5).

### Stage 3 — Validation gate
For anything below R2, do not prepare an external report.
Promote only when all are true:
- reproduction exists
- impact is understandable
- prerequisites are explicit
- root cause is specific enough to explain

### Stage 4 — Disclosure prep
For R2+ findings:
1. choose the best channel
   - bug bounty / security form
   - security email
   - GitHub private advisory or issue
   - maintainer DM
2. prepare short-form disclosure
3. prepare detailed disclosure
4. set private response window

### Stage 5 — Follow-through
Track:
- date sent
- contact channel
- ack received
- remediation status
- retest status
- whether public disclosure is still prohibited

## Channel priority
1. official security reporting path
2. dedicated security email
3. private maintainer contact
4. public issue only if no safe private route exists and risk is low

## Reporting checklist
Before sending externally, confirm:
- [ ] reproducible
- [ ] impact stated clearly
- [ ] assumptions listed
- [ ] root cause explained
- [ ] mitigation suggested
- [ ] no unnecessary sensitive exploit details beyond what is needed

## Output split
### Internal memo
Include:
- broad hypotheses
- structural concerns
- non-reproducible observations
- future validation ideas

### External packet
Include only:
- verified scope
- reproducible steps
- impact
- root cause
- mitigation

## Escalation rule
If the issue is R4-R5 or affects real-value migration risk, shorten the response window and raise urgency immediately.
