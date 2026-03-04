
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
