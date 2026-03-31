---
name: blockchain-black-team
description: Execute real-world blockchain attack scenarios against smart contracts and off-chain infrastructure. Use when performing security audits, penetration testing, or attack simulation on Solana (Anchor), Ethereum (Solidity), or any programmable blockchain protocol. Triggers on requests for security review, attack simulation, black team, red team, penetration test, exploit analysis, or vulnerability assessment of DeFi/blockchain code.
---

# Blockchain Black Team — Real-World Attack Simulation

## When to Use This vs Others
- **Use this (Black Team)** when you want historically proven attack vectors mapped to real incidents and immediate exploitability checks.
- **Use `blockchain-red-team`** for novel/zero-day style techniques and bypass research beyond known patterns.
- **Use `blockchain-purple-team`** for meta-level coverage gaps, audit failure causes, and architecture/ops blind spots.


Execute battle-tested attack vectors from 90+ historical blockchain incidents ($10B+ total losses) against target protocol code. (Matrix: 103 named vectors + META-01~31 meta-patterns | last updated 2026-04-01 | note: A90 = A78 duplicate; A85/A86 reserved; A91 = BCE burn/fee-on-transfer AMM reserve manipulation; A92 = low-cost rapid-quorum governance attack; B73 = LiteLLM PyPI supply chain; B74 = GlassWorm Wave 5 Solana C2 + developer supply chain; B75 = RUSTSEC-2026-0078 intaglio; B76 = Token-2022 delegate check gap in mint())

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

## Attack Matrix (90 Vectors, continuously extended)

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

### C. Economic (6 vectors + A59)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 59 | DEX Aggregator Solver Race-to-Minimum / Thin-Pool Routing | Aave/CoWSwap ($50M loss, 2026-03-12) | HIGH (if DEX integration) |

### D. Infrastructure (core 4 + extended D32/D33/D34)
| # | Vector | Historical Example | Typical Severity |
|---|---|---|---|
| 26 | Frontend XSS/Injection | BadgerDAO ($120M) | HIGH |
| 27 | RPC Endpoint Takeover | Multiple | HIGH |
| 28 | Supply Chain | event-stream, ua-parser-js | HIGH |
| 31 | Protocol-Metadata Confusion (IDL/Schema Trust) | Anchor IDL external-account patch (2026) | HIGH |
| 43 | Security-Tooling Inversion — Force-Push Tag Hijack | Trivy v0.69.4 / TeamPCP (2026-03-19, CVE-2026-28353) | HIGH |

## Daily Evolution Log (Recent)

| Date (KST) | Incident | Vector Mapping | Delta Applied |
|---|---|---|---|
| 2026-04-01 | **Source sweep (24h, Brave quota exhausted → SearXNG fallback)**: rekt.news, SlowMist hacked.slowmist.io, Futuresearch.ai, RustSec, GitHub advisories. **Three new confirmed incidents**: (1) **LiteLLM PyPI Supply Chain** (2026-03-24, 47,000+ affected) — malicious litellm 1.82.7/1.82.8 on PyPI with `litellm_init.pth` backdoor; steals SSH keys, cloud credentials, K8s configs, crypto wallets; maintainer GitHub fully compromised; fork bomb bug accidentally exposed attack. (2) **GlassWorm Wave 5** (March 2026, 433 packages) — Solana blockchain as C2 dead drop, queries every 5s; 200 Python repos + 151 JS/TS repos + 72 VSCode extensions + 10 npm packages compromised via GitHub account takeover + force-push. (3) **RUSTSEC-2026-0078** (2026-03-30) — intaglio symbol confusion after hasher panic; not in Microstable Cargo.lock. **Microstable sweep (lib.rs full read)**: B76 (Token-2022 delegate check gap) ⚠️ **MEDIUM-OPEN** — `mint` instruction accepts `user_collateral_ata` without checking `delegate.is_none()`. While the transfer uses user signing authority, a delegate set on the ATA creates a user-side security gap that could facilitate collateral theft via bystander delegation. `transfer_checked` confirmed at line ~1104 with `authority: user.to_account_info()`. Keeper Cargo.toml: pure Rust (anchor-client, solana-client, reqwest); no Python, no litellm dependency ✅. Keeper immune to B73/B74. Dashboard: pure static HTML, no Python ✅. On-chain: pure Rust/Anchor ✅. **Carry-forwards**: B45 HIGH (audit-attestation.json absent — DAY 32), A43 MEDIUM (no cumulative drift accumulator in rebalance()), **B44 elevated to MEDIUM-OPEN** (B76 refactored as Token-2022 delegate check gap — `delegate.is_none()` check absent in `mint` instruction; requires on-chain fix), A75 MEDIUM (MANUAL_ORACLE_MODE TWAP drift guard absent). | **B73 NEW + B74 NEW + B75 NEW + B76 NEW** | **4 NEW VECTORS** (B73 LiteLLM PyPI supply chain, B74 GlassWorm Wave 5 Solana C2 + developer tool supply chain, B75 RUSTSEC-2026-0078 intaglio [NOT APPLICABLE to Microstable], B76 Token-2022 delegate check gap in mint). Matrix at **103 named vectors** (A1–A92 + A85/A86 reserved) + META-01~31 + B73~B76 = 134 total. Full Microstable sweep: B73 ✅ N/A (Rust on-chain + keeper); B74 ✅ N/A (Rust on-chain, developer tool hygiene advisory); B75 ✅ N/A (intaglio not in Cargo.lock); B76 ⚠️ **MEDIUM-OPEN** — `delegate.is_none()` check absent in mint instruction; requires on-chain fix. No new CRITICAL/HIGH. |
| 2026-03-31 | **Source sweep (24h)**: rekt.news, SlowMist hacked.slowmist.io, web_fetch/SEARXNG. **Two new confirmed incidents**: (1) PancakeSwap BCE-USDT $679K (2026-03-23, BlockSec Phalcon) — BCE token `_transfer()` triggered automatic burns on pool interactions, desyncing AMM cached reserves without `sync()` call; attacker deployed two malicious contracts to bypass per-tx limits and accumulate reserve desync across fragmented transfers. Root cause: token supply modification outside AMM awareness. (2) Moonwell Moonriver Governance Attack (2026-03-26, $1.08M at risk, $0 lost) — attacker spent ~$1,808 to buy 40M MFAM on SolarBeam, passed initial quorum in 11 min; proposed transferring admin control of 7 lending markets + comptroller + oracle to malicious contract; community counter-mobilized and proposal failed. **Microstable sweep**: A91 (BCE burn mechanism) ✅ DEFENDED — Microstable collateral allowlist (USDC/USDT/DAI/USDS) is standard SPL Token with no burn-on-transfer; `token::transfer_checked` CPI path confirmed; no AMM pool integration; A92 (governance attack) ✅ N/A — Microstable has no governance token. | **A91 NEW + A92 NEW** | **2 NEW VECTORS** (A91 BCE burn/fee-on-transfer AMM reserve manipulation, A92 low-cost rapid-quorum governance attack). Matrix at **99 named vectors** (A1–A92; A90=A78 duplicate; A85/A86 reserved) + META-01~28 = 127 total entries. Full Microstable sweep: 0 new CRITICAL/HIGH. **Carry-forwards unchanged**: B45 HIGH (DAY 31), A43 MEDIUM, B44 MEDIUM, A75 MEDIUM. |
| 2026-03-30 | **Source sweep (24h, SearXNG fallback — Brave quota exhausted)**: rekt.news, hacked.slowmist.io, rustsec.org, dailycve.com. **NEW CONFIRMED INCIDENT**: 2026-03-27 BSC Stake Contract ($133K, BlockSec Phalcon) — spot-price oracle in staking reward calculation + referral amplification; flash-loan-compressed single-TX attack. All March 24 libcrux/hpke-rs advisories (RUSTSEC-2026-0071~0077) confirmed already covered (A76–A84, A90/A78 duplicate). x402 SDK payment proof bypass (GHSA-qr2g-p6q7-w82m, 2026-03-07): Solana payment facilitator missing signature validation; no confirmed exploitation; NOT applicable to Microstable. **Housekeeping**: A90 (added 2026-03-29 daily cycle) is a duplicate of A78 — both cover RUSTSEC-2026-0075 libcrux-ed25519 all-zero key gen. A85/A86 remain unassigned (reserved). **SKILL.md header corrected**: 93 → 97 named vectors, META-01~24 → META-01~25 (META-25 was added in 2026-03-29 attack-matrix.md but not reflected in SKILL.md header). | **A3 reinforcement** (BSC Stake 2026-03-27 spot-oracle staking sub-pattern) | **0 NEW VECTORS, 1 REINFORCEMENT, 1 INCIDENT LOG ADDITION** — Matrix at **97 named vectors** (96 unique; A90 = A78 duplicate) + META-01~25. Full Microstable sweep: A3 BSC staking sub-pattern ✅ DEFENDED (Pyth, no referral/staking reward calc); A87 ZK ✅ N/A; A88 ERC-3525 ✅ N/A (Solana); A89 supply cap ✅ CONFIRMED SAFE (v.total_deposits tracker, confirmed 2026-03-29). **Carry-forwards: B45 HIGH (DAY 25)**, A43/B44/A75 MEDIUM unchanged, A81 LOW-MEDIUM (RPC endpoint count). No new CRITICAL/HIGH. |
| 2026-03-29 | **Source sweep (24h–7d)**: rekt.news, SlowMist, hacked.slowmist.io, coinpaprika (Brave quota exhausted → SearXNG fallback). No new incidents from March 22–28 window beyond already-tracked entries. **Q1 2026 stats** (CoinPaprika 2026-03-27): 15 protocols, $137.7M total, 6.5% recovery rate, OWASP #1 = access control. **Incidents log backfill**: AM/USDT pool BSC (2026-03-12, ~$131K) and Aave/CoWSwap $50M price impact (2026-03-12) were in attack matrix but missing from `docs/blockchain-security-incidents-comprehensive.md`. Both added. **META-24 stats addendum** appended to attack-matrix.md with Q1 2026 quantified ground truth + keeper 2-of-3 risk framing. **Note**: attack-matrix.md also received A87~A90 + META-25 in this cycle (not reflected in original log entry — corrected in 2026-03-30 sweep). | **A41** + **A59** (incidents log backfill) + **META-24 addendum** + **A87/A88/A89/A90 + META-25** (late-cycle addition) | **4 NEW VECTORS** (A87 ZK trusted setup skip, A88 ERC-3525 SFT callback reentrancy, A89 9-month accumulation + supply cap donation bypass, A90 libcrux-ed25519 all-zero key gen [=A78 duplicate]), **1 NEW META** (META-25 formal verification spec gap). Matrix at **97 named vectors** + META-01~25. Full Microstable sweep: today's new/reinforced vectors (A41 burn-reserve, A59 thin-pool) ✅ NOT APPLICABLE. A87 ZK ✅ N/A; A88 ERC-3525 ✅ N/A; A89 supply cap ✅ CONFIRMED SAFE. Carry-forwards: **B45 HIGH (DAY 24)**, A43/B44/A75 MEDIUM unchanged. No new CRITICAL/HIGH. |
| 2026-03-28 | **Source sweep (7d)**: rekt.news, SlowMist, rustsec.org (advisory batch), SearXNG fallback (Brave quota exhausted). **New D28 reinforcement**: March 26, 2026 — 15+ malicious Rust crates removed from crates.io (RUSTSEC-2023-0104~0124): Windows service wrappers, Monero tooling, Tauri UI, OpenVPN Rust binding. RUSTSEC-2026-0049 (rustls-webpki CRL, limited impact) — no keeper dep. dTRINITY (A68) already in matrix. | **D28** (reinforced, Rust crate batch) | **0 NEW VECTORS**, **1 REINFORCEMENT** — Matrix holds at **90 named vectors** (unchanged). Keeper Cargo.lock verified: 0 matches for all malicious crates ✅. No new CRITICAL/HIGH. Carry-forwards: **B45 HIGH (DAY 23)**, A43/B44/A75 MEDIUM unchanged. |
| 2026-03-27 | **Source sweep (24h~7d)**: rekt.news, SlowMist, GitHub Advisory checks (web_search/fallback), and web_fetch. New confirmed item: **GHSA-8f57-hh49-gmqf (`@solana-ipfs/sdk`, 2026-03-26)**; no additional on-chain Solana incidents with public exploit mechanism in the window; `hacked.slowmist.io` and `newsletter.rekt.news` items already in matrix. | **D28** (reinforced, malware supply-chain case) + D26 reinforcement unchanged | **0 NEW VECTORS**, **1 REINFORCEMENT** — `Matrix holds at 90 named vectors` (unchanged). Daily microstable verdict: all vectors from previous carry-forward unchanged, **0 new CRITICAL/HIGH**; no reclassified findings against Microstable from this sweep. |
| 2026-03-25 | **Source sweep — no new 24h incidents** (rekt.news + Brave confirmed: Resolv USR $25M = most recent, published 2026-03-23, already captured as A72+META-19). Full 90-vector Microstable sweep vs. all A71–A75+META-19 additions from yesterday's run: A71 Cross-Protocol Flash-Loan MEV Sandwich ✅ NOT APPLICABLE (no user-DEX swap interface); A72 Privileged Minter EOA + Absent Cap ✅ DEFENDED (mint() is USER-SIGNED, no SERVICE_ROLE mint path, slot flow caps enforced on-chain); A73 Long-Horizon Dominance ✅ DEFENDED (Pyth not DEX TWAP, stablecoin-only collateral); A74 Rust tar-rs Symlink ✅ N/A (keeper builds local, no CI tarball unpack); A75 Audit-Evading Economic Design ⚠️ MEDIUM-OPEN (MANUAL_ORACLE_MODE + key compromise → 120-slot window, TWAP drift guard absent for manual price writes — confirmed on-chain, no `assert(|manual_price - twap| <= MAX_DRIFT_BPS)`); META-19 OPCA ✅ MOSTLY DEFENDED (mint/redeem user-signed, no privileged mint SERVICE_ROLE) + ⚠️ MEDIUM gap (keeper MANUAL_ORACLE_MODE price commits lack independent TWAP-drift on-chain validation). | **0 NEW** | Matrix holds at **90 named vectors**. No new CRITICAL/HIGH for Microstable. **Carry-forwards**: B45 HIGH (audit-attestation.json absent — **DAY 20**), A43 MEDIUM (no cumulative drift accumulator in rebalance()), B44 MEDIUM (no delegate.is_none() check in mint()), A75 MEDIUM (MANUAL_ORACLE_MODE TWAP drift guard absent). |
| 2026-03-24 | **Resolv Labs USR $25M** (2026-03-22, Ethereum): Compromised SERVICE_ROLE private key (single EOA) + absent on-chain mint cap. 100K USDC deposit → 50M USR (500× ratio). USR crashed 74%. Underlying collateral intact; allowlisted redemptions announced. **Rust tar-rs RUSTSEC-2026-0067/0068**: `tar::unpack_in` symlink traversal + PAX header size bypass — supply chain risk for keeper build pipeline. **Cross-Protocol MEV Sandwich** (Kyberswap/Camelot, 2026-03-18): multi-venue flash loan split across 3 DEXes to bypass single-pool sandwich defenses. **Meta-synthesis**: A72+A35+B49+B35 = $58.27M losses from single structural pattern (OPCA). | **A71 NEW + A72 NEW + A73 NEW + A74 NEW + A75 NEW + META-19 NEW** | 5 NEW VECTORS + 1 META pattern. Matrix **88→90 named vectors** + META-19. A72 Microstable: ✅ DEFENDED (no SERVICE_ROLE mint path). A74 Microstable: ✅ N/A (local keeper builds). META-19 gap documented (MANUAL_ORACLE_MODE). **Carry-forwards**: B45 HIGH (audit-attestation.json absent — DAY 19), A43 MEDIUM, B44 MEDIUM. No new CRITICAL/HIGH. |
| 2026-03-23 | **Aave/CoWSwap $50M Thin-Pool Routing Loss** (2026-03-12): User rotated $50M aEthUSDT→aEthAAVE via Aave interface → CoW solver routed final WETH leg through SushiSwap pool with $73K liquidity (1,017× pool reserve) → user received 327 AAVE (~$36K). No attacker; loss from AMM price impact + solver race-to-minimum objective. "Aave Shield" announced (>25% price impact block). **Movie Token Burn-to-LP double-count** (2026-03-10, $242K BSC): flash loan + burn function writes directly to LP reserve, double-counting in swap+burn tracker → inflated AMM price → sold for profit. | **A59 NEW** + A2/A10 reinforcement | 1 NEW VECTOR (A59: DEX Aggregator Solver Race-to-Minimum / Interface-Mediated Thin-Pool Routing Loss). A2+A10 reinforced with "Deflationary-Token Burn-to-LP Direct Write" sub-pattern. Matrix now **88 named vectors** (A56+A57+A58 from 3/22 run + A59 today). Microstable A59 verdict: ✅ NOT APPLICABLE (no DEX aggregator, keeper-direct rebalance, no user collateral swap interface). A2/A10 Movie Token verdict: ✅ NOT APPLICABLE (no deflationary burn function, Pyth oracle not AMM). **Carry-forwards**: B45 HIGH (audit-attestation.json absent — DAY 17), A43 MEDIUM, B44 MEDIUM. No new CRITICAL/HIGH for Microstable. |
| 2026-03-22 | **Neodyme Token-2022 research** (dev.to 2026-03-15) + **Anchor v1.0.0-rc.5 release** (2026-03-20) + **Windsurf IDE extension malware targeting Solana developers** (Bitdefender 2026-03-20, D45 reinforcement) | **A56 NEW + A57 NEW + A58 NEW** | 3 NEW VECTORS (A56: Token-2022 ExtraAccountMeta Injection; A57: Anchor Shadow IDL Migration Discriminator Gap; A58: Token-2022 Transfer Fee Invisible Tax Accounting Bypass). Matrix: 84→87 vectors (pre-3/23 count). |
| 2026-03-21 | **Trivy supply chain attack by TeamPCP** (2026-03-19, CVE-2026-28353): Retained credentials from incomplete Feb 28 containment → force-pushed 75/76 trivy-action tags → backdoored v0.69.4 steals SSH keys + crypto wallet files from CI/CD runners. **Security-tooling inversion pattern**: legit scan results presented alongside credential theft. | **D43 NEW** | 1 NEW VECTOR (D43: Security-Tooling Inversion — Trusted CI/CD Scanner Compromised via Force-Push Tag Hijack). Matrix now **84 named vectors**. Microstable CI/CD audit: pages.yml uses `actions/checkout@v4` (tag-pinned, no SHA) ⚠️ LOW risk (GitHub-maintained action; no trivy-action in pipeline; keeper builds done locally). D43 verdict: ⚠️ LOW — no Trivy in pipeline, but tag-pinning without SHA is structural risk if any third-party actions are added. **Carry-forwards unchanged**: B45 HIGH (audit-attestation.json absent — DAY 16), A43 MEDIUM, B44 MEDIUM. No new CRITICAL/HIGH findings today. |
| 2026-03-20 | **Neutrl DNS hijack** (2026-03-19, loss TBD): DNS provider social-engineered → domain redirected; users urged to revoke Permit2 approvals immediately via Revoke.cash. **AM/USDT pool burn reserve manipulation** (2026-03-12, $131K): `toBurnAmount` manipulated to artificially lower reserves → sold at inflated price. **Injective $500M access control bypass** (2026-03-16, disclosed; $0 lost, $500M at risk): any user could drain any account; patched via upgrade vote; bounty dispute ($50K offered vs. $500K cap). | D26 + Permit2 note, A41 reinforcement, A4 reinforcement | **0 NEW VECTORS** (all reinforce existing). D26 updated: Neutrl case + **Permit2 persistence as DNS-hijack force-multiplier** documented. A41 updated: AM/USDT burn-reserve case added. A4 updated: Injective chain-level auth bypass case added. Matrix holds at **83 named vectors**. Full Microstable sweep: D26 Neutrl ✅ N/A (Solana, no Permit2); A41 ✅ DEFENDED; A4 ✅ DEFENDED. **Carry-forwards unchanged**: B45 HIGH (audit-attestation.json absent — DAY 15), A43 MEDIUM, B44 MEDIUM. No new CRITICAL/HIGH findings. |
| 2026-03-17 | **Venus Protocol supply cap bypass + slow-accumulation TWAP manipulation** (2026-03-15, $2.15M / $3.7M exposure): Attacker accumulated 84% of supply cap over 9 months, bypassed cap via direct token transfer to protocol contract (not through deposit function), then pushed TWAP 96% on thin-liquidity THE collateral. Drained $2.15M in CAKE/BNB/USDC/BTCB. | **A67 NEW** | 1 NEW VECTOR (A67). Total matrix: **81 named vectors**. Microstable: A67 ✅ DEFENDED (total_deposits tracked field + Pyth oracle not DEX TWAP + stablecoin collateral only). Full 81-vector sweep — 0 new CRITICAL/HIGH. Carry-forwards unchanged: B45 HIGH (audit-attestation.json still absent — DAY 12), A43 MEDIUM (no cumulative drift tracking), B44 MEDIUM (no delegate.is_none() check in mint()), B63 MEDIUM (MediaTek TEE, operator devices). |
| 2026-03-15 | **Aave wstETH CAPO oracle misconfiguration** (2026-03-10, $27.78M): Chaos Labs Edge Risk engine computed snapshotRatio 2.85% below market → AgentHub auto-executed 1 block later with no human gate → 34 healthy E-Mode positions liquidated. No attacker. First confirmed large-scale loss from fully automated risk parameter pipeline. | **A62 NEW** | 1 NEW VECTOR (A62). Total matrix: 62 named vectors. Microstable: A62 ✅ DEFENDED (2-of-3 keeper quorum + manual oracle mode time-box; no automated rate-cap executor exists). Full sweep below — 0 new CRITICAL/HIGH. Carry-forwards: B45 HIGH (audit-attestation.json unattested delta persists), A43 MEDIUM, B44 MEDIUM. |
| 2026-03-13 | **DBXen ERC-2771 sender mismatch exploit** (2026-03-12, $150K): burnBatch() used _msgSender() but onTokenBurned() callback used msg.sender → forwarder addr credited; permissionless forwarder + fresh-address fee backdating bug amplified. **bonk.fun domain hijack** (2026-03-12): team account compromised → DNS takeover → wallet-drainer JS injected on canonical domain. D26 escalation note: server-level CSP header required (meta-tag alone cannot block server-injected scripts). | **A61 NEW** + D26 reinforced | 1 NEW VECTOR (A61). Total matrix: 61 named vectors. Microstable: A61 NOT APPLICABLE (Solana, no ERC-2771). D26: Microstable dashboard has CSP meta tag ✅ — but no server-level HTTP CSP header (static file serving). LOW carry-forward. Full sweep: no new CRITICAL/HIGH findings today. Carry-forwards: B45 HIGH (audit-attestation.json unattested 3,281-line delta persists), A43 MEDIUM, B44 MEDIUM. |
| 2026-03-12 | Source sweep: no new incidents in 24h window (last: Gondi NFT $230K 2026-03-10, A4 reinforcement); SlowMist/rekt.news/Halborn/Brave confirmed — 0 new DeFi exploits March 11-12. Full 79-vector Microstable sweep: B45 HIGH still open (audit-attestation.json absent; 3,281-line unattested delta persists), A43 MEDIUM open (no cumulative drift accumulator in rebalance()), B44 MEDIUM open (no delegate.is_none() check in mint()). D26 LOW-NEW: vendor/solana-web3-1.95.3.iife.min.js loaded without SRI integrity attribute — self-hosted so low severity, but should be hash-verified for tamper detection parity. | 0 NEW | Matrix holds at 79 vectors. No new pattern from March 11–12 sweep. Open carry-forwards: B45 HIGH (priority), A43 MEDIUM, B44 MEDIUM, D26/D33 LOW. Gondi (2026-03-10) confirmed A4 dual-authorization pattern: function-level auth ≠ asset-level ownership — bundler-pattern applies equally to any batch/multicall abstraction over user-owned assets. |
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
- ERC-2771 meta-transaction: mixed msg.sender/_msgSender() + permissionless forwarder (A61)

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
