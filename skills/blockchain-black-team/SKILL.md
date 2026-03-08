---
name: blockchain-black-team
description: Execute real-world blockchain attack scenarios against smart contracts and off-chain infrastructure. Use when performing security audits, penetration testing, or attack simulation on Solana (Anchor), Ethereum (Solidity), or any programmable blockchain protocol. Triggers on requests for security review, attack simulation, black team, red team, penetration test, exploit analysis, or vulnerability assessment of DeFi/blockchain code.
---

# Blockchain Black Team — Real-World Attack Simulation

## When to Use This vs Others
- **Use this (Black Team)** when you want historically proven attack vectors mapped to real incidents and immediate exploitability checks.
- **Use `blockchain-red-team`** for novel/zero-day style techniques and bypass research beyond known patterns.
- **Use `blockchain-purple-team`** for meta-level coverage gaps, audit failure causes, and architecture/ops blind spots.


Execute battle-tested attack vectors from 69+ historical blockchain incidents ($10B+ total losses) against target protocol code.

## When to Use

- Security audit of smart contracts (Solana Anchor, Solidity, CosmWasm)
- Attack simulation / penetration testing of DeFi protocols
- Pre-mainnet security hardening
- Hackathon security review
- Post-incident analysis using real-world patterns

## Quick Start

1. Read the target codebase (on-chain + off-chain)
2. Load `references/attack-matrix.md` for the 44+ vector framework
3. For each vector: map historical pattern → target code → attack scenario → severity
4. Output structured report with PoC sketches for CRITICAL/HIGH findings

## Attack Matrix (48+ Vectors, continuously extended)

The full matrix with historical references, code-level mechanisms, and defense patterns is in `references/attack-matrix.md`. Summary:

### A. Smart Contract (core 13 + extended A32/A33/A34/A35/A36/A38)
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

### B. Off-chain/Keeper (core 7 + extended B29/B35/B36/B37/B38)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 14 | RPC Manipulation | Multiple | HIGH |
| 15 | Key Compromise | Ronin ($624M), Harmony ($100M), IoTeX ioTube ($4.4M) | CRITICAL |
| 16 | Race Condition | Multiple keeper exploits | MEDIUM |
| 17 | Checkpoint Poisoning | Novel | HIGH |
| 18 | Config Injection | Multiple | HIGH |
| 19 | Memory/Log Leak | Slope wallet drain | MEDIUM |
| 20 | Denial of Service | Solana network halts | MEDIUM |
| 29 | AI Agent Prompt-Injection Confused-Deputy | Trail of Bits Comet audit (2026) | HIGH |
| 37 | AI Agent Steganographic Oversight Evasion | arXiv 2602.23163 (2026-02-26) | HIGH |
| 38 | Multi-turn Tool-Return Boundary Takeover (IPI) | arXiv 2602.22724 + 2602.22302 (2026-02-25/26) | HIGH |

### C. Economic (6 vectors)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 21 | Bank Run / Depeg | UST/LUNA ($40B), USDC SVB | CRITICAL |
| 22 | Collateral Manipulation | stETH depeg, Tether FUD | CRITICAL |
| 23 | Governance Attack | Beanstalk ($182M) | HIGH |
| 24 | Sybil Attack | Multiple | MEDIUM |
| 25 | MEV Extraction | MEV ecosystem | MEDIUM |
| 30 | Liquidity-Exhaustion Griefing | Intent bridge study (2026) | MEDIUM |

### D. Infrastructure (core 4 + extended D32/D33/D34)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 26 | Frontend XSS/Injection | BadgerDAO ($120M) | HIGH |
| 27 | RPC Endpoint Takeover | Multiple | HIGH |
| 28 | Supply Chain | event-stream, ua-parser-js | HIGH |
| 31 | Protocol-Metadata Confusion (IDL/Schema Trust) | Anchor IDL external-account patch (2026) | HIGH |

## Daily Evolution Log (Recent)

| Date (KST) | Incident | Vector Mapping | Delta Applied |
|---|---|---|---|
| 2026-03-09 | OtterSec "Unfaithful Claims: Breaking 6 zkVMs" (2026-03-03) — Jolt/Nexus/Cairo-M/Ceno/Expander/Binius64 all vulnerable to Fiat-Shamir public-claim unbound variable bypass | A50 (NEW) | Added zkVM Fiat-Shamir Public-Claim Unbound Variable Bypass; distinct from A49 (gamma=delta setup constants) — A50 correct constants but wrong transcript binding order pre-challenge squeeze; proof forgery enables arbitrary false statement claiming; Microstable ✅ not applicable (no zkVM); future integration gate: transcript binding-order audit + forged-claim CI test required |
| 2026-03-08 | CrossCurve bridge ReceiverAxelar.expressExecute() missing gateway validation (2026-02-02, $3M multi-chain) | A48 (NEW) | Added Unguarded Cross-Chain Receiver Function vector; distinct from A32 (IBC content forgery) — attacker bypasses relay entirely by directly calling receiver; Microstable ✅ not applicable (no bridge receiver); onlyGateway modifier pattern documented |
| 2026-03-07 | Solv Protocol BRO vault ERC721 callback double-mint exploit (2026-03-06, $2.7M / 38 SolvBTC drained via 22-iteration dual-execution) | A46 (NEW) | Added ERC721 Callback Reentrancy / Dual-Execution Mint vector; distinct from A1 (not loop re-entry); reinforced NFT-callback CEI discipline; Microstable ✅ not applicable (SPL Token classic, no callbacks) |
| 2026-03-05 | Localhost WebSocket takeover hardening signal (OpenClaw v2026.2.25 + Oasis disclosure) | B48 | Added localhost trust-boundary collapse vector for agent-controlled keeper ops; reinforced browser-origin gateway threat modeling, no-loopback-exception controls, and pairing/origin hardening requirements |
| 2026-03-02 | Holdstation DeFAI Smart Wallet (2026-02-25, $462K) | B15 (tentative) | Added to incidents timeline; mechanism pending (MFA bypass / session theft in AI-integrated wallet). DeFAI surface note added: AI intent layer + signing authority co-location amplifies B15/B29 exposure |
| 2026-03-02 | February 2026 monthly loss total (~$37.7M, lowest since Mar 2025) | Meta | Contextual stat: phishing = $8.5M of total (22%). Key-compromise-class still dominant vector |
| 2026-03-01 | AgentSentry + Agent Behavioral Contracts (arXiv 2602.22724 / 2602.22302) | B38 | Added multi-turn tool-return boundary takeover vector and runtime contract-based mitigation notes |
| 2026-03-01 | Immunefi bug-bounty telemetry lag signal (2-week disclosure delay) | A34, B15 | Added signal-latency-blindness note: public bounty metrics lag should not drive real-time incident prioritization |
| 2026-03-01 | FOOMCASH zkSNARK verifier drift exploit (~$2.26M) | A38 | Added new ZK verifier-key misbinding vector with code-level key-hash/circuit-version defenses |
| 2026-03-01 | Trail of Bits Comet prompt-injection audit techniques | B29 | Reinforced confused-deputy vector with fake system/user delimiters + fake validator/CAPTCHA multi-step exfil patterns |
| 2026-02-28 | YieldBlox Blend V2 collateral chain exploit ($10.97M) | A3, A36 | Elevated "thin-liquidity collateral + raw-latest oracle adapter + lending health-factor" as a compositional failure chain (not single oracle bug) |
| 2026-02-28 | AI oversight-evasion research signal (arXiv 2602.23163) | B37 | Added covert-channel/steganographic agent bypass pattern (post-prompt-injection hardening bypass class) |
| 2026-02-28 | Stake Nova redeem-path exploit ($2.39M) | A2, A10 | Reinforced flash-loan-amplified redeem validation failures (`RedeemNovaSol`) and added Solana-specific redeem-path hardening pattern |
| 2026-02-26 | IoTeX ioTube validator key compromise ($4.4M) | B15 | Added new key-compromise case + keeper key hygiene emphasis |
| 2026-02-25 | Moonwell oracle incident ($1.78M bad debt) | A3, A10, B18 | Added oracle unit-normalization misuse pattern, governance timelock recovery-gap note, and feed-composition sanity defenses |

## Defense Failure Patterns (Meta, Purple-Team Informed)

Black Team 점검 시, "취약점 존재"만 보지 말고 **방어가 왜 실패하는지**를 같이 기록한다.

1. **Control Fragmentation**: 감사/바운티/모니터링/IR가 분리돼 신호가 연결되지 않음.
2. **Rollback Latency**: 문제 인지 후 안전한 롤백까지의 의사결정·권한 체인 지연.
3. **Assumption Drift**: 배포 당시 안전하던 임계치/가정이 시장·인프라 변화로 무효화.
4. **Confused-Deputy Ops**: AI/자동화 도구가 비신뢰 입력을 권한 있는 행동으로 변환.
5. **Capacity Griefing**: 단일 대형 공격보다 지속 저강도 압박으로 운영 여유를 소진.
6. **Market-Quality Blindness**: 가격 정확성만 보고 시장 깊이/분산도/거래활동 품질을 신뢰 경계에 포함하지 않음.
7. **Telemetry-Truth Drift**: 대응 단계에서 공지 지표(순손실/동결액)와 온체인 사실이 분리되어 의사결정·포렌식이 오염됨.
8. **Signal-Latency Blindness**: 공개 바운티/리포트 통계의 지연(예: 2주 지연 반영)을 실시간 위협 지표로 오용해, 이미 진행 중인 변형 공격 대응 우선순위를 놓침.
9. **Localhost-Trust Mirage**: 운영 환경에서 `localhost`를 무조건 신뢰해 rate-limit/origin/pairing 예외를 두면, 브라우저-origin 로컬 WebSocket 경로로 인증 경계가 붕괴될 수 있음. 온체인 감사만으로는 탐지되지 않는 운영 계층 실패.

리포트의 각 HIGH/CRITICAL 항목에 아래를 추가:
- `Why defense failed` (설계/운영/조직 중 어디가 끊겼는지)
- `Recovery path` (탐지→차단→복구까지 실제 실행 경로)

## Execution Methodology

For each of the 44+ vectors:

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
- Total vectors evaluated: 44
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
- Re-evaluate ALL 44 vectors against updated code
- Verify previous fixes actually work (bypass attempts)
- Check for regression (new vulnerabilities from fixes)
- Only report NEW or UNFIXED findings
- Target: ZERO CRITICAL + ZERO HIGH to exit loop
