# Triad Investigation Template

Use this when Black Team, Red Team, and Purple Team are all involved and you need one synthesis packet.

```markdown
# Triad Investigation — [Project Name]

## 1. Scope summary
- Project:
- Chain / testnet:
- Date:
- Reviewer(s):

## 2. Black Team findings
| ID | Pattern class | Severity | Repro | Summary |
|---|---|---|---|---|
| B-01 | historical exploit pattern | high | yes/no | ... |

## 3. Red Team findings
| ID | Novel attack path | Severity | Repro | Summary |
|---|---|---|---|---|
| R-01 | ... | high | yes/no | ... |

## 4. Purple Team synthesis
| ID | Gap type | Missed by | Repro | Why it matters |
|---|---|---|---|---|
| P-01 | composition / ops / assumption / coverage | black / red / both | yes/no | ... |

## 5. Coverage matrix
| Vector x Layer | On-chain | Oracle | Frontend | Ops | Governance |
|---|---|---|---|---|---|
| Known exploit patterns | covered / gap | ... | ... | ... | ... |
| Novel attack paths | covered / gap | ... | ... | ... | ... |
| Structural/operational gaps | covered / gap | ... | ... | ... | ... |

## 6. Reportable items
Only include reproducible R2+ findings here.

## 7. Hold items
List interesting but non-reportable R0-R1 items here.

## 8. Recommended next move
- validate [finding]
- disclose [finding]
- retest after fix
```

## Use rule
The triad packet is the synthesis layer, not a dump. Keep only the strongest evidence and explicitly separate reportable items from internal holds.
