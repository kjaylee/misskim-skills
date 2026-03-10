
---

## 2026-03-07 Daily Check

### Source Sweep (24h~7d)
- Reviewed: `rekt.news` (fetched live), `hacked.slowmist.io` (fetched live), DeFiLlama hacks DB, QuillAudits exploit analysis, SlowMist tracker, Chainalysis 2026 report intro, SearXNG fallback.
- **1 new incident-validated exploit pattern** identified: Solv Protocol ERC721 Callback Double-Mint (2026-03-06, $2.7M).
- **1 notable aftermath**: Step Finance officially shut down post-$27.3M hack (B36 confirmed).

### New Patterns Added Today

| Vector | Incident | Amount | Date |
|--------|---------|--------|------|
| **A46 (NEW): ERC721 Callback Reentrancy / Dual-Execution Mint** | Solv Protocol BRO vault | ~$2.7M (38.0474 SolvBTC → 1,211 ETH) | 2026-03-06 |

**A46 Technical Summary**: `BitcoinReserveOffering.mint()` initiates an ERC721 NFT transfer → `onERC721Received()` fires → `_mint()` runs (first time) → callback returns → `mint()` calls `_mint()` AGAIN (second time). Exchange rate constant within TX → each mint call yields double supply for same collateral. 22 iterations: 135 BRO → 567M BRO. Root cause distinct from A1 (no attacker-controlled re-entry loop; the contract's own code paths create the dual execution). Security firm Decurity automated bot detected the attack.

### Full 46-Vector Check Results (Microstable)

**A46 ERC721 Callback Reentrancy / Dual-Execution Mint** — ✅ **N/A (Not Applicable)**
- Microstable uses classic SPL Token, NOT ERC721 or Token-2022
- No NFT transfer mechanism in any mint/redeem instruction path
- SPL Token classic: no `onERC721Received()` equivalent
- Even under Token-2022: Microstable mint path follows CEI (collateral transferred IN first via `transfer_checked`, THEN `mint_mstb_to_user` called once) — no dual-execution path possible
- ✅ Architecture fundamentally immune to this vector

**A1 Reentrancy** — ✅ DEFENDED
- CEI pattern throughout. SPL Token: no reentrancy hooks. Classic program model: not re-entrant.

**A2 Flash Loan + Price Manipulation** — ✅ DEFENDED
- TWAP + Pyth confidence + staleness guards + per-slot flow caps + per-TX limits

**A3 Oracle Manipulation** — ✅ DEFENDED
- Feed-ID binding, staleness checks (20 slots mint, 45 slots redeem), confidence 2% max, TWAP deviation guard 2.5%, unit-invariant feeds (USD-denominated collateral only, no ratio composition)

**A4 Access Control** — ✅ DEFENDED
- 2-of-3 keeper quorum, `TRUSTED_INITIALIZER` constraint, `require_keys_eq!` guards throughout

**A5 Integer Overflow** — ✅ DEFENDED
- `checked_*` operations, u128 intermediates in mul_div

**A6 Account Substitution** — ✅ DEFENDED
- `require_keys_eq!` on all mint/vault/ATA accounts; Pyth feed-ID allowlist; ATA canonicalization verified

**A7–A13** — ✅ DEFENDED (carry-forward from prior checks)

**A33 Audit-Scope-Exclusion Exploitation** — ✅ No known exclusions on oracle composition path

**A40 ERC4626 Donation Attack** — ✅ DEFENDED (accounting field `vault.total_deposits`, not raw balance)

**A41 Burn-Path Fee-Exempt** — ✅ DEFENDED (CEI + uniform fees + per-slot caps)

**A42 Anchor Post-CPI Stale Cache** — ✅ N/A (classic SPL Token, no transfer hooks)

**A43 Commit/Reveal Threshold Circumvention** — ⚠️ PARTIAL (carry-forward)
- Per-call commit/reveal guard at `turnover >= 4%`, no epoch-level cumulative drift tracking
- 5× sub-threshold rebalances bypass intent over 160 slots

**A44/A45 Env-Stealer / Clone-Rotation Campaign** — ⚠️ PARTIAL (carry-forward, D33)
- Runtime Cargo.lock hash attestation in place; build-time provenance pinning to external CI signer not complete

**A46** — ✅ N/A (see above)

**B14–B20** — ✅/⚠️ (carry-forward)
- B17 Checkpoint HMAC: ✅ | B19 Log masking: improved

**B36 Social-Engineering Stake Authority** — ⚠️ OPERATIONAL RISK
- Step Finance shutdown confirmed: audited contracts irrelevant; hot device compromise = protocol death
- Microstable keeper keypairs remain hot. Ledger/HSM for treasury ops still recommended.

**B44 SPL Delegate Drain** — ⚠️ MEDIUM (carry-forward)
- `mint()` does NOT check `user_collateral.delegate` field
- Protocol funds ✅ safe (PDA-owned vault ATAs); user fund launder path ⚠️ remains unpatched

**B45 Post-Audit Deployment Delta** — ❌ HIGH (carry-forward from 2026-03-05)
- Critical-path delta vs audited commit: `adds=3281, dels=324` lines unreviewed
- No `audit-attestation.json` or CI delta gate in place

**B46/B47/B48** — ✅ Addressed operationally / design-time; no new code-level risk since last check

**C21–C30 Economic** — ✅ ALL DEFENDED
**D26–D34 Infra/AI** — ✅/⚠️ (carry-forward D33)

### Today's Verdict
- New vectors added: **1 (A46 ERC721 Callback Reentrancy / Dual-Execution Mint)**
- Findings: **0 CRITICAL / 0 HIGH new (B45 HIGH still open from 2026-03-05) / 0 MEDIUM new**
- Carry-forward: B45 HIGH, B44 MEDIUM, A43 MEDIUM, D33 LOW
- Matrix: 45 → **46 vectors**

---

## 2026-03-05 Daily Check

### Source Sweep (24h~7d)
- Reviewed: `rekt.news`, `hacked.slowmist.io`, GitHub Advisory DB (Solana/Anchor/SPL queries), Solana security channels, Trail of Bits / OtterSec / Neodyme blogs, and X hashtag fallback.
- **No new incident-validated exploit pattern** requiring new vector creation in this cycle.
- OtterSec 2026-03-03 zkVM research is a strong technical signal but not a confirmed loss incident in the requested window, so it was not added as a new matrix vector.

### Full 58-Vector Check Results (Microstable)

**❌ HIGH — B45 Post-Audit Deployment Delta**
- Audit report states audited revision: `f327e7c6df0fae25171f0e00be316f8f7cf4a5c8` (`microstable/docs/audit-report.md`).
- Current critical-path delta vs audited commit:
  - `solana/programs/microstable/src/lib.rs`
  - `solana/keeper/src/*`
  - measured diff: `adds=3281`, `dels=324`.
- No explicit `audit-attestation.json` + CI delta gate found to block critical-path post-audit drift.
- **Risk**: production/security claims can diverge materially from audited scope.
- **Blue-team directive**:
  1. Add `audit-attestation.json` with `audit_commit`, `critical_paths`, `attestor`, `timestamp`.
  2. CI-block any PR touching critical paths unless attestation is refreshed or signed secondary review is attached.
  3. Publish `last_audited_commit` on dashboard/security docs.

**⚠️ MEDIUM — A43 Commit/Reveal Threshold Segmentation**
- `rebalance()` enforces commit/reveal only when per-call `turnover >= LARGE_REBALANCE_THRESHOLD`.
- No epoch/window cumulative drift accumulator was found.
- **Risk**: repeated sub-threshold rebalances can bypass commit/reveal intent over multiple calls.
- **Blue-team directive**: add cumulative drift accounting per epoch/window and force commit/reveal when cumulative drift crosses threshold.

**⚠️ MEDIUM — B44 SPL Delegate Drain Conduit (User-side ATA)**
- `mint()` uses user ATA `transfer_checked` path but no `delegate` rejection check was found in `lib.rs`.
- Vault-side protocol assets remain protected (PDA-owned vault ATAs), but delegated user ATAs can still be abused as a laundering ingress.
- **Blue-team directive**: reject delegated user collateral accounts (`delegate.is_none()` + delegated amount guard) and add explicit event/log for rejected delegated attempts.

**⚠️ LOW — D33/A44 Residual Supply-Chain Trust Gap**
- Keeper now enforces Cargo.lock hash attestation at runtime, but build-time hash is derived from local lockfile (`keeper/build.rs`).
- This mitigates drift-at-runtime but does not fully prevent malicious lock updates introduced before build in compromised developer flows.
- **Blue-team directive**: pin attestation hash from external signed provenance (CI signer / release manifest), not local build context alone.

### Carry-forward Status Improvements
- **B17 Checkpoint Poisoning**: now materially hardened (HMAC integrity tag + 0600 perms + owner UID checks in keeper checkpoint load/save paths).
- **B19 Memory/Log Leak**: improved (redacted pubkey logging and no direct secret material logging path observed in current keeper runtime code).

### Today’s Verdict
- New vectors added: **0**
- Findings: **1 HIGH / 2 MEDIUM / 1 LOW**
- Immediate notification required for HIGH finding (B45).

---

## 2026-03-04 Daily Check

### New Patterns Added Today
| Vector | Incident | Amount | Date |
|--------|---------|--------|------|
| B44: SPL Token Account Persistent Delegate Drain | Ledger/Canissolana (Solana) | ~$30K USDC | 2026-03-02/03 |

### A36 Thin-Liquidity Collateral Cascade — Field Confirmation
Blend/YieldBlox ($10.8M, 2026-02-22): USTRY token on Stellar SDEX had near-zero liquidity. Reflector oracle used single-source "latest price" without TWAP or market-depth gate. Attacker inflated USTRY 100× in one block → borrow $10M+ against <$100K real collateral. Stellar validators froze ~$7.5M XLM. A36 mechanism fully confirmed in production at scale.

### Full 45-Vector Check Results (Microstable)

**B44 SPL Delegate Drain (NEW)**
- Vault ATAs are PDA-owned by `protocol_state` → ✅ external delegate setting IMPOSSIBLE
- User collateral ATAs: `mint()` does NOT check `user_collateral.delegate` field → ⚠️ PARTIAL
  - Attacker with stale delegation can initiate `transfer_checked` to Microstable vault, receiving MSTB in return (launder path). Protocol funds not at risk; user fund attribution is.
  - **Recommendation (MEDIUM)**: Add `require!(ctx.accounts.user_collateral.delegate.is_none(), ErrorCode::DelegateNotAllowed)` to `mint()` instruction.

**A43 Commit/Reveal Threshold Circumvention (carry-forward)**
- `rebalance()` enforces commit/reveal only when `turnover >= LARGE_REBALANCE_THRESHOLD (4%)`
- Per-call enforcement only — no epoch-level cumulative drift tracking
- Attacker (keeper compromise) can run 5× `turnover = 3.9%` rebalances across 160 slots → zero a collateral weight from 10% to 0% with no commit/reveal ever triggered
- ⚠️ PARTIAL — defense exists per-call, not across epoch window
- **Recommendation (MEDIUM)**: Track `epoch_cumulative_drift` per collateral index; require commit/reveal when `sum(epoch_drift) >= LARGE_REBALANCE_THRESHOLD`

**A42 Anchor Post-CPI Stale Account Cache**
- Microstable uses `token::transfer_checked` (classic SPL Token), NOT Token-2022
- No transfer hooks in current collateral mints (USDC, USDT, DAI, USDS)
- Trigger condition for A42 = Token-2022 transfer hooks — not present
- ✅ N/A (for current architecture); watch if Token-2022 collateral ever added

**A40 ERC4626 Share-Price Donation Attack** — ✅ DEFENDED
`vault.total_deposits` accounting field; raw SPL transfers cannot inflate protocol accounting. Already confirmed in yesterday's check.

**A41 Burn-Path Fee-Exempt Flash Loan** — ✅ DEFENDED
No fee-exempt paths. CEI ordering. Per-slot caps. Already confirmed.

**A1–A13 (Smart Contract Core)** — ✅ ALL DEFENDED
CEI, checked math, PDA discriminators, Pyth feed-ID binding, 2-of-3 keeper, flow caps, TWAP/staleness/confidence guards.

**B14–B20 (Keeper/Infra)** — ✅ DEFENDED / ⚠️ PARTIAL
- Multi-RPC: ✅ | 2-of-3 keeper: ✅ | Leader rotation: ✅
- B17 Checkpoint checksums: ⚠️ (carry-forward)
- B19 Log masking: ⚠️ (carry-forward)

**C21–C30 (Economic)** — ✅ ALL DEFENDED
Circuit breaker (3% depeg threshold), per-slot caps, multi-collateral TWAP, progressive fees.

**D26–D34 (Infra/AI)** — ✅ DEFENDED / ⚠️ PARTIAL
- D33 Cargo.lock attestation: ⚠️ (carry-forward)
- All others: ✅

**A32, A38, A39, B44 (protocol-level)** — ✅ N/A or DEFENDED as above

### Today's Verdict
**0 CRITICAL / 0 HIGH / 2 MEDIUM new findings (B44 delegate check, A43 epoch drift).**
Carry-forward operational items: B17, B19, D33.
Matrix: 44 → **45 vectors**. New incident: Ledger/Canissolana SPL delegate drain.

---

## 2026-03-03 Daily Check

### New Patterns Added Today
| Vector | Incident | Amount |
|--------|---------|--------|
| A40: ERC4626 Share-Price Donation Attack | Inverse Finance/LlamaLend (2026-03-02) | $240K |
| A41: Burn-Path Fee-Exempt Flash Loan Amplification | SOF+LAXO/BNB Chain (2026-02-14/22) | $438K |

### Full 44-Vector Check Results (Microstable)

**A40 ERC4626 Donation Attack** — ✅ DEFENDED  
`vault.total_deposits` is accounting field updated only via mint/redeem instructions. Raw SPL transfers to vault ATA do not inflate protocol accounting. No share-price oracle path.

**A41 Burn-Path Fee-Exempt** — ✅ DEFENDED  
No mining reward contract. Redeem fees applied uniformly. Payout computed before any burn. Per-slot caps limit flash-loan amplification.

**A1–A13 (Smart Contract Core)** — ✅ ALL DEFENDED  
CEI, checked math, PDA seed discriminators, Pyth feed-ID binding, 2-of-3 keeper set, per-slot flow caps, commit-reveal for large rebalances, strict account owner checks.

**B14–B20 (Keeper/Infra)** — ✅ DEFENDED / ⚠️ PARTIAL  
- Cross-RPC validation: ✅  
- 2-of-3 keeper set: ✅  
- Leader rotation: ✅  
- B17 Checkpoint Poisoning: ⚠️ keeper state file checksums not verified this cycle  
- B19 Log Scrub: ⚠️ keeper log masking not confirmed this cycle  

**C21–C30 (Economic)** — ✅ ALL DEFENDED  
Progressive fees, circuit breaker (MINT_DEPEG_PAUSE_THRESHOLD 3%), per-slot caps, multi-collateral, TWAP/staleness.

**D26–D34 (Infrastructure/AI)** — ✅ DEFENDED / ⚠️ PARTIAL  
- CSP: `default-src 'self'; script-src 'self'` (no external scripts): ✅  
- D33 Transitive Typosquat: ⚠️ Cargo.lock attestation not checked this cycle  
- D34 WASI: ✅ N/A (no Wasmtime embedding in keeper)

**A32, A38, A39** — ✅ N/A (no cross-chain, no ZK, no upstream fork)

### Today's Verdict
**0 CRITICAL / 0 HIGH / 0 MEDIUM new findings.**  
Existing ⚠️ PARTIAL items (B17, B19, D33) are carried operational items from prior cycles — no regression.  
Matrix: 42 → **44 vectors**. Incidents timeline updated.

---

## 2026-03-10 Daily Check

### Source Sweep (24h~7d window)
- Reviewed: rekt.news, hacked.slowmist.io, Bitget news, Yahoo Finance, SpazioCrypto, PeckShield on-chain data, IDOSLaunchpad, AllCryptocurrencyDaily, InvEzz, Blockchain Magazine, SearXNG fallback.
- **1 new incident-validated exploit pattern** identified: Sillytuna Address Poisoning + Physical Coercion (2026-03-04, $24M).
- **0 new Solana-native smart contract vulnerabilities** in this window (Solv Protocol A46 from 03-06 already added 03-07).
- Step Finance shutdown confirmed (B36 aftermath) — no new vector required.
- B52 (AI Memory Poisoning) from Microsoft Security Blog 2026-03-06 already added in prior run.

### New Patterns Added Today

| Vector | Incident | Amount | Date |
|--------|---------|--------|------|
| **B53 (NEW): Address Poisoning + Physical Coercion Hybrid** | Sillytuna wallet (Ethereum) | ~$24M aEthUSDC | 2026-03-04 |

**B53 Technical Summary**: Two-phase attack. Digital phase: attacker generates vanity look-alike wallet (matching first/last 4-6 chars of victim's regular counterpart), sends dust transactions to poison victim's transaction history, victim copies wrong address when initiating next large transfer → 23.6M aEthUSDC drained in one TX. Physical phase: coercion (violence) confirmed in reporting. All on-chain transactions cryptographically valid — no smart contract vulnerability. Class accounts for >$1.2B losses 2024–2026. PeckShield detected on-chain in real time; funds laundered via Monero.

### Full 53-Vector Check Results (Microstable)

**B53 Address Poisoning + Physical Coercion Hybrid** — ✅ **N/A (On-chain Program)**
- `lib.rs` does not process user wallet transaction history; account resolution is at instruction level via Anchor accounts
- Keeper (automated): N/A — no human copy-paste UX path
- Dashboard (`index.html`):
  - "Live Transaction Feed" shows transaction **signatures** only — not from/to addresses; not a dust-injection surface
  - `walletAddressView` renders connected wallet address in HTML (line 850) — JS rendering in `app.js` not yet audited for truncation-only display
  - ⚠️ LOW risk: if `app.js` renders address truncated in clipboard copy actions, it could create a lookalike confusion surface in future UX
  - No "recent counterparty address" shortcuts found in current dashboard
- **Verdict: ✅ N/A for on-chain + keeper; ⚠️ LOW residual dashboard UX risk**

**A1 Reentrancy** — ✅ DEFENDED (carry-forward)
**A2 Flash Loan + Price Manipulation** — ✅ DEFENDED (carry-forward)
**A3 Oracle Manipulation** — ✅ DEFENDED (carry-forward)
**A4 Access Control** — ✅ DEFENDED (carry-forward)
**A5 Integer Overflow** — ✅ DEFENDED (carry-forward)
**A6–A13** — ✅ DEFENDED (carry-forward)
**A32–A36** — ✅ DEFENDED / carry-forward (no code changes detected)
**A38–A40** — ✅ DEFENDED (carry-forward)
**A41–A43** — ✅/⚠️ A43 partial (carry-forward)
**A44–A52** — ✅/⚠️ N/A or carry-forward
**A46** — ✅ N/A (SPL Token, no ERC721 path)
**B14–B20** — ✅/⚠️ (carry-forward)
**B29** — ✅ DEFENDED (carry-forward)
**B35–B40** — ✅/⚠️ (carry-forward)
**B41–B52** — ✅/⚠️ (carry-forward)

**❌ HIGH (carry-forward) — B45 Post-Audit Deployment Delta**
- Still open from 2026-03-05. Audited commit: `f327e7c6df0fae25171f0e00be316f8f7cf4a5c8`. Current delta vs audited: `adds=3281, dels=324`. No `audit-attestation.json` or CI delta gate found.
- **Blue-team directive** (unchanged): add `audit-attestation.json`, CI-block PRs on critical path without attestation refresh, publish `last_audited_commit` on dashboard.

**⚠️ MEDIUM (carry-forward) — A43 Commit/Reveal Threshold Circumvention**
- No epoch-level cumulative drift accumulator found. Risk: repeated sub-threshold rebalances bypass commit/reveal over 160 slots.

**⚠️ MEDIUM (carry-forward) — B44 SPL Delegate Drain Conduit**
- `mint()` does not check `user_collateral.delegate` field. Protocol PDA vaults ✅ safe; user ATA delegate launder path ⚠️ unpatched.

**⚠️ LOW — B53 Dashboard Residual**
- `walletAddressView` full-address rendering in `app.js` not confirmed. Recommend: verify clipboard copy uses full Base58 address, not truncated display string.

### Today's Verdict
- New vectors added: **1 (B53 Address Poisoning + Physical Coercion Hybrid)**
- Findings: **0 CRITICAL / 0 HIGH new** (B45 HIGH still open from 2026-03-05) / 1 LOW new (B53 dashboard UX)
- Carry-forward: B45 HIGH, B44 MEDIUM, A43 MEDIUM, B53 LOW, D33 LOW
- Matrix: 52 → **53 vectors**

---

## 2026-03-11 Daily Check

### Source Sweep (24h~48h window: 2026-03-10 ~ 2026-03-11)
- Reviewed: rekt.news, hacked.slowmist.io, Bitget news, BTCC, QuillAudits exploit analyses, Brave Search, fallback SearXNG.
- **1 new incident** identified: Gondi NFT platform (2026-03-10, ~$230K).
- No new Solana-native smart contract vulnerabilities this window.
- B54 (Nation-State APT AI Tradecraft) and D36 (HTTP Caching Oracle Poisoning) already documented from prior cycle.
- No new CVEs affecting Solana/Anchor or Microstable's Rust dependency set detected.

### New Patterns Added Today

| Vector | Incident | Amount | Date |
|--------|---------|--------|------|
| **A4 reinforced — NFT Purchase Bundler Missing Asset Owner Verification** | Gondi NFT Platform (Ethereum) | ~$230K (78 NFTs) | 2026-03-10 |

**A4 Reinforcement Technical Summary**: Gondi's `Purchase Bundler` function in the `Sell & Repay` contract (deployed 2026-02-20) verified function-level caller authorization but not asset-level ownership. The function checked "is caller allowed to invoke this bundler?" but omitted "is caller the actual owner or borrower of this specific NFT?" Attacker exploited the gap to drain 78 NFTs (44 Art Blocks, 10 Doodles, 2 Beeple) worth $230K. Key generalization: any bundler/batch function that operates on user assets must independently verify both (a) caller's right to invoke the function AND (b) caller's ownership/authorization for each specific asset. Attack source confirmed: https://hacked.slowmist.io/

### Full 54-Vector Check Results (Microstable)

**A4 Access Control (Gondi sub-pattern: NFT Purchase Bundler Missing Asset Owner Verification)**
- `lib.rs` `mint()`: `token::transfer_checked(authority: ctx.accounts.user.to_account_info())` — SPL Token enforces user signature as transfer authority. No bundler pattern. ✅ DEFENDED
- `lib.rs` `redeem()`: similarly user-signed transfer authority. ✅ DEFENDED
- `lib.rs` `claim_stake()`: triple-verification: `require_keys_eq!(claimant, agent)`, `require_keys_eq!(record.agent, agent)`, `require_keys_eq!(escrow.agent, agent)` — no impersonation path. ✅ DEFENDED
- `lib.rs` `rebalance()`: 2-of-3 keeper quorum required; no user-specific asset targeted. ✅ DEFENDED
- No "Purchase Bundler"-style function that operates on user-owned assets exists in lib.rs. ✅ N/A (structural prevention)
- **Verdict: ✅ DEFENDED — Gondi A4 variant does not apply to Microstable's architecture**

**A1–A3, A5–A13 (carry-forward)** — ✅ DEFENDED (no code changes detected)
**A32–A43, A44–A52 (carry-forward)** — ✅/⚠️ carry-forward from 2026-03-10
**A46** — ✅ N/A (SPL Token, no ERC721 path)
**A49** — ✅ N/A (no ZK verifier)
**A50** — ✅ N/A (no zkVM)
**B14–B20, B29, B35–B40, B41–B54 (carry-forward)** — ✅/⚠️ carry-forward from 2026-03-10
**D26–D36 (carry-forward)** — ✅/⚠️ carry-forward from 2026-03-10

### Carry-Forward Open Items (unchanged)

**❌ HIGH (carry-forward) — B45 Post-Audit Deployment Delta**
- Open since 2026-03-05. Audited commit: `f327e7c6df0fae25171f0e00be316f8f7cf4a5c8`. Current delta vs audited baseline: `adds=3281, dels=324`. No `audit-attestation.json` or CI delta gate exists.
- **Blue-team directive**: add `audit-attestation.json`, CI-block PRs on critical path without attestation refresh, publish `last_audited_commit` on dashboard. URGENT — the B54 (Nation-State APT AI Tradecraft) assessment from 2026-03-10 notes that AI-assisted attackers can scan the unreviewed deployment delta within 24h.

**⚠️ MEDIUM (carry-forward) — A43 Commit/Reveal Threshold Circumvention**
- No epoch-level cumulative drift accumulator found. Risk: repeated sub-threshold rebalances (each <4% turnover) bypass commit/reveal over 160 slots.
- Blue-team directive: add per-epoch cumulative turnover accumulator; trigger commit/reveal when epoch sum crosses LARGE_REBALANCE_THRESHOLD.

**⚠️ MEDIUM (carry-forward) — B44 SPL Delegate Drain Conduit**
- `mint()` does not validate `user_collateral.delegate` field. Protocol PDA vaults are unaffected; however, if a user's collateral ATA has an attacker-controlled delegate set from a prior dApp interaction, the attacker could silently drain collateral from that ATA without the user re-signing. The protocol's `transfer_checked` uses the USER as the authority, so this only applies if the ATA already has a delegate set.
- Blue-team directive: add `require!(ctx.accounts.user_collateral_ata.delegate.is_none(), ErrorCode::DelegatePresent)` in `mint()` to reject ATAs with active delegates.

**⚠️ LOW (carry-forward) — B53 Dashboard Residual**
- `walletAddressView` full-address clipboard rendering not confirmed in `app.js` (file not audited). Low risk.

### Today's Verdict
- New incidents found: **1 (Gondi 2026-03-10, $230K — A4 Access Control reinforcement)**
- New attack vectors added: **0** (Gondi maps to existing A4 sub-pattern)
- Findings: **0 CRITICAL / 0 HIGH new** (B45 HIGH still open since 2026-03-05) / **0 MEDIUM new** / **0 LOW new**
- Carry-forward: B45 HIGH, B44 MEDIUM, A43 MEDIUM, B53 LOW, D33 LOW
- Matrix: **54 vectors** (no new vector added today; A4 reinforced with Gondi sub-pattern)
