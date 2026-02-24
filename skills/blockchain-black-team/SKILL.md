---
name: blockchain-black-team
description: Execute real-world blockchain attack scenarios against smart contracts and off-chain infrastructure. Use when performing security audits, penetration testing, or attack simulation on Solana (Anchor), Ethereum (Solidity), or any programmable blockchain protocol. Triggers on requests for security review, attack simulation, black team, red team, penetration test, exploit analysis, or vulnerability assessment of DeFi/blockchain code.
---

# Blockchain Black Team — Real-World Attack Simulation

## When to Use This vs Others
- **Use this (Black Team)** when you want historically proven attack vectors mapped to real incidents and immediate exploitability checks.
- **Use `blockchain-red-team`** for novel/zero-day style techniques and bypass research beyond known patterns.
- **Use `blockchain-purple-team`** for meta-level coverage gaps, audit failure causes, and architecture/ops blind spots.


Execute battle-tested attack vectors from 68+ historical blockchain incidents ($10B+ total losses) against target protocol code.

## When to Use

- Security audit of smart contracts (Solana Anchor, Solidity, CosmWasm)
- Attack simulation / penetration testing of DeFi protocols
- Pre-mainnet security hardening
- Hackathon security review
- Post-incident analysis using real-world patterns

## Quick Start

1. Read the target codebase (on-chain + off-chain)
2. Load `references/attack-matrix.md` for the 28-vector framework
3. For each vector: map historical pattern → target code → attack scenario → severity
4. Output structured report with PoC sketches for CRITICAL/HIGH findings

## Attack Matrix (28 Vectors)

The full matrix with historical references, code-level mechanisms, and defense patterns is in `references/attack-matrix.md`. Summary:

### A. Smart Contract (13 vectors)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 1 | Reentrancy | The DAO ($60M), Curve/Vyper ($70M) | HIGH-CRITICAL |
| 2 | Flash Loan | Mango ($114M), Euler ($197M) | CRITICAL |
| 3 | Oracle Manipulation | Mango, BonqDAO ($120M) | CRITICAL |
| 4 | Access Control | Ronin ($624M), Wormhole ($320M) | CRITICAL |
| 5 | Integer Overflow/Underflow | Compound ($147M) | HIGH |
| 6 | Account Substitution (Solana) | Cashio ($52M) | HIGH |
| 7 | Signature Replay | Wintermute ($160M) | HIGH |
| 8 | Front-running/Sandwich | MEV ecosystem | MEDIUM |
| 9 | Proxy Upgrade Attack | Nomad ($190M) | HIGH |
| 10 | Logic Bug | Compound ($147M), Cream ($130M) | HIGH |
| 11 | Rent/Lamport Drain (Solana) | Multiple | LOW-MEDIUM |
| 12 | CPI Confusion (Solana) | Crema ($8.8M) | HIGH |
| 13 | PDA Seed Collision (Solana) | Multiple | MEDIUM |

### B. Off-chain/Keeper (7 vectors)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 14 | RPC Manipulation | Multiple | HIGH |
| 15 | Key Compromise | Ronin ($624M), Harmony ($100M) | CRITICAL |
| 16 | Race Condition | Multiple keeper exploits | MEDIUM |
| 17 | Checkpoint Poisoning | Novel | HIGH |
| 18 | Config Injection | Multiple | HIGH |
| 19 | Memory/Log Leak | Slope wallet drain | MEDIUM |
| 20 | Denial of Service | Solana network halts | MEDIUM |

### C. Economic (5 vectors)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 21 | Bank Run / Depeg | UST/LUNA ($40B), USDC SVB | CRITICAL |
| 22 | Collateral Manipulation | stETH depeg, Tether FUD | CRITICAL |
| 23 | Governance Attack | Beanstalk ($182M) | HIGH |
| 24 | Sybil Attack | Multiple | MEDIUM |
| 25 | MEV Extraction | MEV ecosystem | MEDIUM |

### D. Infrastructure (3 vectors)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 26 | Frontend XSS/Injection | BadgerDAO ($120M) | HIGH |
| 27 | RPC Endpoint Takeover | Multiple | HIGH |
| 28 | Supply Chain | event-stream, ua-parser-js | HIGH |

## Daily Evolution Log (Recent)

| Date (KST) | Incident | Vector Mapping | Delta Applied |
|---|---|---|---|
| 2026-02-25 | Moonwell oracle incident ($1.78M bad debt) | A3, A10, B18 | Added oracle unit-normalization misuse pattern, governance timelock recovery-gap note, and feed-composition sanity defenses |

## Defense Failure Patterns (Meta, Purple-Team Informed)

Black Team 점검 시, "취약점 존재"만 보지 말고 **방어가 왜 실패하는지**를 같이 기록한다.

1. **Control Fragmentation**: 감사/바운티/모니터링/IR가 분리돼 신호가 연결되지 않음.
2. **Rollback Latency**: 문제 인지 후 안전한 롤백까지의 의사결정·권한 체인 지연.
3. **Assumption Drift**: 배포 당시 안전하던 임계치/가정이 시장·인프라 변화로 무효화.
4. **Confused-Deputy Ops**: AI/자동화 도구가 비신뢰 입력을 권한 있는 행동으로 변환.
5. **Capacity Griefing**: 단일 대형 공격보다 지속 저강도 압박으로 운영 여유를 소진.

리포트의 각 HIGH/CRITICAL 항목에 아래를 추가:
- `Why defense failed` (설계/운영/조직 중 어디가 끊겼는지)
- `Recovery path` (탐지→차단→복구까지 실제 실행 경로)

## Execution Methodology

For each of the 28 vectors:

1. **Historical Reference** — Which real incident used this vector, what was the mechanism
2. **Code Mapping** — Identify exact file:line in target code where vector applies
3. **Attack Scenario** — Step-by-step attack procedure (numbered steps)
4. **Current Defense** — Evaluate: Defended / Partially Defended / Undefended
5. **Severity** — CRITICAL / HIGH / MEDIUM / LOW / INFO
6. **PoC Sketch** — For CRITICAL/HIGH: pseudocode or concrete attack commands
7. **Remediation** — Code-level fix recommendation

## Chain-Specific Considerations

### Solana (Anchor)
- Account model: owner checks, PDA derivation, account data validation
- CPI: cross-program invocation target verification, signer propagation
- Rent: minimum balance, account close lamport drain
- Discriminator: Anchor 8-byte discriminator collision risk
- Clock/Slot: slot-based timing vs real-time assumptions

Read `references/solana-specific.md` for Solana-specific attack patterns.

### Ethereum (Solidity)
- Storage layout: delegatecall + storage collision
- Reentrancy: external calls before state updates
- ERC-20 approval: infinite approval + permit signatures
- Proxy patterns: UUPS/Transparent upgrade risks

Read `references/ethereum-specific.md` for EVM-specific attack patterns.

## Report Format

Output as structured markdown:

```markdown
# Black Team Report — {Protocol Name}

## 0) Summary Dashboard
- Total vectors evaluated: 28
- CRITICAL: X | HIGH: X | MEDIUM: X | LOW: X
- Undefended (immediately exploitable): X

## Top 5 Most Dangerous Scenarios
1. ...

## {N}) {Vector Name}
- **Historical Reference**: {incident, amount, mechanism}
- **Code Mapping**: {file:line}
- **Attack Scenario**: {numbered steps}
- **Current Defense**: {Defended/Partial/Undefended}
- **Severity**: {level}
- **PoC**: {code/commands for CRITICAL/HIGH}
- **Remediation**: {specific code fix}
```

## Cycling Protocol

Black Team is designed to run in loops with Blue Team:

```
Black R1 → Blue fix → Black R2 → Blue fix → ... → ZERO CRITICAL/HIGH
```

On repeat runs (R2+):
- Re-evaluate ALL 28 vectors against updated code
- Verify previous fixes actually work (bypass attempts)
- Check for regression (new vulnerabilities from fixes)
- Only report NEW or UNFIXED findings
- Target: ZERO CRITICAL + ZERO HIGH to exit loop
