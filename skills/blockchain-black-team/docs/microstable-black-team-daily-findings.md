---

## 2026-04-28 Daily Check

### Source Sweep (24h~7d window: 2026-04-21 to 2026-04-28 KST)
- Sources checked: rekt.news frontpage, hacked.slowmist.io front page, Immunefi blog index, GitHub Advisory fallback queries, Solana official security/media pages, Trail of Bits / OtterSec / Neodyme blog indexes, plus search-fallback cross-checks because direct Brave queries remained rate-limited
- **Confirmed in-window items**:
  1. **Scallop / sSUI rewards** is now **admissible as a new named vector**. Public mechanism write-ups make clear this was not merely an unspecified side-contract bug: a **deprecated V2 rewards package** remained callable on-chain, still touched live shared spool/rewards state, and exposed an **uninitialized `last_index`** path that let the attacker harvest historical rewards from the active pool.
  2. The right abstraction is therefore not just A10 logic bug, but **A119 Immutable Legacy Package / Shared-State Version-Gate Bypass**.
  3. GitHub Advisory fallback results did surface `solana-web3` malware entries, but the fetched advisory was **published in 2025**, so it was excluded from today's 24h~7d admission window. Solana's ecosystem-security page was a defensive-program announcement, not a new exploit primitive.

### New Vectors Added Today
- **1 NEW vector**: **A119 Immutable Legacy Package / Shared-State Version-Gate Bypass**
- **0 reinforcements**

### Immediate High-Priority Finding
- **Vector**: **B45 Audit Attestation Gap / Post-Audit Deployment Delta**
- **Severity**: **HIGH**
- **Location**: `microstable/security/audit-attestation.json` is still absent, so the current on-chain / keeper / dashboard deployment set has no machine-checkable binding to the audited commit/artifact set
- **Bypass / abuse path**: an attacker or insider does not need to break a reviewed invariant directly if an unaudited code delta can still ride the normal build/release path. The security boundary is bypassed by **continuity failure** between audited source and live artifact.
- **Immediate blue-team fix**: add `security/audit-attestation.json` with audited commit hash, covered paths, artifact hashes, and CI/release verification that fails on absence or mismatch

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A119 legacy-package / shared-state version-gate bypass** | on-chain program architecture + migration surface | ℹ️ INFO / NOT ACTIVE | `solana/programs/microstable/src/lib.rs` exposes a single `declare_id!` upgrade path, and repo scan did **not** find a parallel retired program / rewards sidecar still writing the same live shared state |
| **D51 Anchor JS lockfile drift / semver-smuggle** | `solana/Anchor.toml`, `solana/package.json`, `solana/yarn.lock` | ⚠️ MEDIUM ACTIVE-LATENT | `Anchor.toml` still uses `package_manager = "yarn"`, `package.json` keeps caret ranges, and review still found **no end-to-end immutable-install proof** (`--frozen-lockfile` or equivalent gate) |
| **D27 RPC poisoned-failover / verifier-specific spoofing** | keeper config + dashboard RPC runtime reads | ⚠️ MEDIUM PARTIAL DEFENSE | `keeper/src/config.rs:402-429` still enforces only distinct RPC hosts, and `docs/app.js:55-94,209-243` keeps strict cross-checking mainly at bootstrap `getGenesisHash`, not provider-independent runtime observation quorum |
| **A115 constrained-CA / allowlisted-host impersonation** | keeper TLS dependency lane | ⚠️ MEDIUM ACTIVE-LATENT | `solana/Cargo.lock` still resolves `rustls-webpki 0.101.7` and `0.103.9` below the patched floor tracked in the matrix |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | `keeper/src/oracle.rs:736-873` still enables manual oracle mode and writes externally validated prices through `ix_update_oracle`; `lib.rs:675-736` still accepts the write path without a last-trusted-Pyth/TWAP drift cap |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | `lib.rs:1571-1605` still gates commit/reveal only when **single-call** turnover crosses `LARGE_REBALANCE_THRESHOLD`; reviewed state still shows no cumulative cross-call drift accumulator |
| **D26 canonical frontend / auxiliary client-surface risk** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | `docs/index.html:6,994` still relies on meta-only CSP and no SRI on the vendored `solana-web3` bundle, while `docs/app.js:46,1645` still embeds a client-side devnet faucet signer |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD | `microstable/security/audit-attestation.json` is still absent |

### Today's Verdict
- New incidents found: **1 requiring a new named vector**
- New attack vectors added: **1** (**A119**)
- New **CRITICAL/HIGH** findings: **0 new**, but **B45 HIGH** remains active
- Active latent / carry-forward priorities remain:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Enforce immutable JS installs (`--frozen-lockfile` or equivalent) for all Anchor-driven package-manager paths
  3. Upgrade or pin away vulnerable `rustls-webpki` resolution in keeper TLS stack
  4. Add provider-independent RPC quorum for keeper/dashboard read paths
  5. Add explicit manual-price-vs-last-trusted-Pyth/TWAP drift guard before `ix_update_oracle`
  6. Track cumulative cross-call rebalance drift for large-turnover commit/reveal admission
  7. Move CSP to headers, add SRI, and remove browser-side faucet signing material

## 2026-04-26 Daily Check

### Source Sweep (24h~7d window: 2026-04-19 to 2026-04-26 KST)
- Sources checked: rekt.news frontpage/newsletter, hacked.slowmist.io front page, Immunefi blog index, GitHub Advisory query page, Solana official pages, Trail of Bits / OtterSec / Neodyme blog indexes, plus search-fallback query checks where direct search remained rate-limited
- **Confirmed in-window items**:
  1. No fresher public **code-level** incident/research delta required a new matrix entry today; the latest admissible items (**GiddyVaultV3 partial signature coverage**, **rustls-webpki CRL-path panic**, **KelpDAO poisoned-failover**, **Volo key leakage**, **Trail of Bits same-VK zkVM guest forgery**) were already absorbed.
  2. Official Solana / Anchor / SPL-facing sources did not expose a new advisory or exploit primitive requiring matrix expansion.
  3. The daily task therefore advanced via **fresh verification + Microstable re-sweep**, not by adding another named vector.

### New Vectors Added Today
- **0 NEW vectors**
- **0 reinforcements**

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **D27 RPC poisoned-failover / verifier-specific spoofing** | keeper config + dashboard RPC runtime reads | ⚠️ MEDIUM PARTIAL DEFENSE | `keeper/src/config.rs:402-429` still enforces only distinct RPC hosts, and `docs/app.js:212-323` keeps strict cross-checking only for bootstrap `getGenesisHash`, not provider-independent runtime observation quorum |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | `keeper/src/oracle.rs:736-836` still enables manual oracle mode and writes externally validated prices through `ix_update_oracle` without an explicit keeper-side drift gate versus last trusted Pyth/TWAP anchor |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | `lib.rs:1546-1605` still gates commit/reveal only when **single-call** turnover crosses `LARGE_REBALANCE_THRESHOLD`; reviewed state still shows no cumulative cross-call drift accumulator |
| **D26 canonical frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | `docs/index.html:6` still relies on meta-only CSP, and `docs/app.js:43-49` still embeds a client-side devnet faucet signer |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 57) | `microstable/security/audit-attestation.json` is still absent; critical-path deployment delta remains unattested |

### Today's Verdict
- New incidents found: **0 requiring a new named vector**
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0 new**, but **B45 HIGH** remains active
- Blue-team priority remains unchanged:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Add provider-independent RPC quorum for keeper/dashboard read paths
  3. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path before `ix_update_oracle`
  4. Track cumulative cross-call rebalance drift for large-turnover commit/reveal admission
  5. Move CSP to headers, add SRI, and remove browser-side faucet signing material

## 2026-04-24 Daily Check

### Source Sweep (24h~7d window: 2026-04-17 to 2026-04-24 KST)
- Sources checked: Trail of Bits blog, rekt.news frontpage, hacked.slowmist.io, Immunefi blog index, Trail of Bits / OtterSec / Neodyme blog indexes, GitHub Advisory / RustSec search, Solana security/status search results, Anchor / SPL recent commit signals
- **Confirmed in-window items**:
  1. **Trail of Bits 2026-04-17** disclosed a **same verification key forged-proof** result caused by **unchecked deserialization + enum jump-table confusion inside a zkVM guest / prover**. This is admissible as a **new vector A118**, because it is not verifier-key drift, not setup collapse, and not Fiat-Shamir claim-binding failure.
  2. **Volo Vaults** (2026-04-22, Sui) remains admissible as a **B15 reinforcement**, because the publicly cited mechanism is explicitly **Private Key Leakage**, not an unspecified “security incident”.
  3. **KelpDAO / LayerZero**, **CoW Swap / eth.limo**, **Rhea**, **Dango**, recent **Anchor / SPL / RustSec** signals did not expose a fresher Solana / Anchor / SPL code-mechanism delta requiring another new named vector in this window.

### New Vectors Added Today
- **1 NEW vector**: **A118 zkVM Guest Unchecked Deserialization / Enum Jump-Table Proof Forgery**
- **1 reinforcement**: **B15 Key Compromise** (Volo Vaults privileged vault-key leakage)

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A118 zkVM guest parser forgery** | keeper proof handling + future proof-backed subsystems | ℹ️ INFO / NOT ACTIVE | Repo-wide review did **not** find SP1 / RISC0 / Groth16 guest proving code, proof-backed reserve attestation, or zk oracle coprocessor. `keeper/src/hermes.rs` uses `pythnet_sdk::wire::v1::{AccumulatorUpdateData, Proof}` and handles `Proof::WormholeMerkle`, which is a merkle/accumulator proof class, not the same-VK zkVM guest-forgery class |
| **B15 privileged keeper key compromise** | keeper key loading + config policy | ⚠️ MEDIUM PARTIAL DEFENSE | `keeper/src/config.rs:432-437,814-845` forces exactly **3 keeper keypairs**, bans ephemeral paths, and requires **three distinct parent directories**. `keeper/src/utils.rs:355-401` securely opens key files and rejects symlink / group-world-readable paths. But the design is still file-key based, not HSM/MPC-attested, and host compromise could still collapse multiple keys at once |
| **D27 RPC poisoned-failover / verifier-specific spoofing** | keeper config + dashboard RPC bootstrap | ⚠️ MEDIUM PARTIAL DEFENSE | `keeper/src/config.rs:402-429` still enforces distinct RPC hosts, and dashboard bootstrap still cross-checks genesis hash, but runtime reads remain closer to failover than true provider-independent observation quorum |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | `keeper/src/oracle.rs:743-851` still writes externally validated prices through `ix_update_oracle` without an explicit keeper-side drift gate versus last trusted Pyth/TWAP anchor |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | `lib.rs:1571-1605` still gates commit/reveal only when **single-call** turnover crosses `LARGE_REBALANCE_THRESHOLD`; reviewed state still shows no cumulative cross-call drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 55) | `microstable/security/audit-attestation.json` is still absent; critical-path deployment delta remains unattested |

### Today's Verdict
- New incidents found: **1 requiring a new named vector**
- New attack vectors added: **1** (**A118**)
- Reinforcements applied: **1** (**B15**)
- New **CRITICAL/HIGH** findings: **0 new**, but **B45 HIGH** remains active
- **External alert target (not sent by this cron per reporting rule)**: Discord channel `1468813323662524500`
- Blue-team priority is now:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Move keeper signing material toward HSM/MPC or host-isolated signer separation instead of multi-file hot keys on one operator plane
  3. Add provider-independent RPC quorum or degraded-mode privileged-action deny logic for keeper/manual paths
  4. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path before `ix_update_oracle`
  5. If zk-backed attestations are ever introduced, ban unchecked witness deserialization in guest code and require forged-same-VK negative tests
  6. Track cumulative cross-call rebalance drift for large-turnover commit/reveal admission

## 2026-04-22 Daily Check

### Source Sweep (24h~7d window: 2026-04-15 to 2026-04-22 KST)
- Sources checked: rekt.news frontpage, LayerZero `KelpDAO Incident Statement`, hacked.slowmist.io, Immunefi blog index, Trail of Bits / OtterSec / Neodyme blog indexes, GitHub Advisory spot checks (`solana`, `anchor`, `spl-token`, `rustls-webpki`), plus local search-fallback for community chatter
- Brave Search API direct query remained rate-limited → local search-fallback and direct `web_fetch` cross-checks used instead
- **Confirmed in-window items**:
  1. **KelpDAO rsETH / LayerZero DVN** is now admissible as a **D27 reinforcement**, because the public incident statement exposed a concrete mechanism: **downstream RPC poisoning + DDoS-induced failover concentration**, not just vague “bridge compromise” reporting
  2. **CoW Swap / Trust Wallet / eth.limo** style domain or entrypoint hijack paths remain **D26 reinforcements only**, not a new named vector today
  3. **GitHub Advisory / GHSA spot checks** did not produce a fresh Solana / Anchor / SPL-specific issue requiring matrix expansion, but the existing `rustls-webpki` lane remains relevant to keeper outbound TLS trust
  4. **Trail of Bits / OtterSec / Neodyme / Immunefi** indexes produced no new Solana-specific exploit-research delta requiring a new vector today
  5. Community-query fallback produced no additional confirmed Solana exploit signal beyond already-tracked incidents

### New Vectors Added Today
- **0 NEW vectors**
- **1 reinforcement**: **D27 RPC Endpoint Takeover** (KelpDAO-style poisoned-failover / verifier-specific spoofing)

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **D27 RPC poisoned-failover / verifier-specific spoofing** | keeper config + dashboard RPC bootstrap | ⚠️ MEDIUM PARTIAL DEFENSE | `keeper/src/config.rs:402-429` enforces distinct RPC hosts, and dashboard bootstrap cross-checks genesis hash, but the system still presents as **primary + secondary endpoint failover**, not provider-independent **N-of-M observation quorum**. A KelpDAO-style poisoned subset plus failover pressure is not structurally ruled out yet |
| **A115 TLS / dependency drift exposure** | keeper dependency + lockfile | ⚠️ MEDIUM ACTIVE-LATENT | `solana/Cargo.lock` still carries `rustls-webpki 0.103.9` and `0.101.7`; keeper outbound HTTPS trust remains below the patched floor for the current webpki advisory lane |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ❌ HIGH CARRY-FORWARD | `docs/index.html:6` still relies on **meta-only CSP**, and `docs/app.js:43-49` still embeds a full **64-byte devnet faucet signer secret** client-side. Devnet-only intent does not change the fact that every browser receives a reusable signer |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | `keeper/src/oracle.rs:735-851` still enables manual oracle mode and writes externally validated prices through `ix_update_oracle` without an explicit keeper-side drift gate versus last trusted Pyth/TWAP anchor |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | `lib.rs:1571-1605` still gates commit/reveal only when **single-call** turnover crosses `LARGE_REBALANCE_THRESHOLD`; reviewed state still shows no cumulative cross-call drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 53) | `microstable/security/audit-attestation.json` is still absent; critical-path deployment delta remains unattested |

### Today's Verdict
- New incidents found: **0 requiring a new named vector**
- New attack vectors added: **0**
- Reinforcements applied: **1** (**D27**)
- New **CRITICAL/HIGH** findings: **0 new**, but **D26 HIGH** and **B45 HIGH** remain active
- **External alert target (not sent by this cron per reporting rule)**: Discord channel `1468813323662524500`
- Blue-team priority is now:
  1. **Remove and rotate the client-side faucet signer immediately**; replace with a rate-limited backend faucet or pre-minted dev balances
  2. Add `security/audit-attestation.json` + CI/release gate
  3. Add provider-independent RPC quorum or degraded-mode privileged-action deny logic for keeper/manual paths
  4. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path before `ix_update_oracle`
  5. Track cumulative cross-call rebalance drift for large-turnover commit/reveal admission
  6. Move CSP to HTTP headers and add SRI for vendored JS assets

## 2026-04-18 Daily Check

### Source Sweep (24h~7d window: 2026-04-11 to 2026-04-18 KST)
- Sources checked: rekt.news frontpage, hacked.slowmist.io, Immunefi blog index, Trail of Bits / OtterSec / Neodyme blog indexes, GitHub Advisory API spot checks (`solana`, `anchor`, `spl-token`, `spl token 2022`), plus local search-fallback for X/community chatter
- Brave Search API direct-query quota remained unreliable → local search-fallback used for community-query coverage
- **Confirmed in-window items**:
  1. **Rhea Finance** remains the latest code-level incident in-window that materially affects this skill, and it was already absorbed yesterday as an **A98 reinforcement**
  2. **rekt.news** frontpage still shows already-mapped items (**Hyperbridge / Drift / Resolv**); no fresh Solana-native code-level mechanism was exposed there in this sweep window
  3. **GitHub Advisory API** returned recent **webpki name-constraints** advisories plus unrelated ecosystem hits, but no fresh Solana/Anchor/SPL-specific advisory requiring a matrix expansion today
  4. **Trail of Bits / OtterSec / Neodyme / Immunefi** indexes produced no new Solana-specific exploit-research delta requiring a matrix update
  5. **X/community fallback search** returned no additional Solana exploit signal beyond already-tracked incidents

### New Vectors Added Today
- **0 NEW vectors**
- **0 reinforcements** requiring a matrix edit today

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A115 TLS / dependency drift exposure** | keeper dependency + lockfile | ⚠️ MEDIUM ACTIVE-LATENT | `solana/Cargo.lock` still carries `rustls-webpki 0.103.9` and `0.101.7` through the `reqwest` / `hyper-rustls` stack; no exploit path confirmed today, but fresh GHSA noise keeps this dependency lane live for attention |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ❌ HIGH NEW | `docs/app.js:43-49` still embeds a full **64-byte devnet faucet signer secret** client-side, while `docs/index.html:6` still relies on **meta-only CSP**. This is no longer just “low frontend hygiene” — the signing material is already publicly exposed to every browser that loads the dashboard |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | `keeper/src/oracle.rs:743-851` still enables manual oracle mode, fetches externally validated prices, and sends `ix_update_oracle` without an explicit keeper-side TWAP/max-drift assertion before write |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | `lib.rs:1571-1605` still enforces commit/reveal only when **single-call** turnover crosses `LARGE_REBALANCE_THRESHOLD`; reviewed state still shows no cumulative cross-call drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 49) | `microstable/security/audit-attestation.json` is still absent; critical-path deployment delta remains unattested |

### Today's Verdict
- New incidents found: **0 requiring matrix expansion**
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **1** — **D26 HIGH** (public frontend signer exposure) — plus **B45 HIGH carry-forward**
- **External alert target (not sent by this cron per reporting rule)**: Discord channel `1468813323662524500`
- Blue-team priority is now:
  1. **Remove and rotate the client-side faucet signer immediately**; replace with a rate-limited backend faucet or pre-minted dev balances
  2. Add `security/audit-attestation.json` + CI/release gate
  3. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path before `ix_update_oracle`
  4. Track cumulative cross-call rebalance drift for large-turnover commit/reveal admission
  5. Move CSP to HTTP headers and add SRI for vendored JS assets

## 2026-04-16 Daily Check

### Source Sweep (24h~7d window: 2026-04-09 to 2026-04-16 KST)
- Sources checked: rekt.news frontpage/newsletter, hacked.slowmist.io, Solana ecosystem/security page (STRIDE/SIRN launch), Trail of Bits/OtterSec/Neodyme blog indexes, Immunefi blog, GitHub Advisory DB query page, plus local search-fallback checks for X/Immunefi/GHSA
- Brave Search API quota exhaustion persisted on direct query search → local search-fallback (SearXNG/Scrapling/DDG) used for query-based checks
- **Confirmed in-window items**:
  1. **Dango insurance-fund exploit** remains the only fresh code-level incident in-window requiring a recent matrix delta and is already mapped as **A114**
  2. **Hyperbridge / Polytope** remains an **A32 reinforcement**, not a separate new vector
  3. **Trust Wallet / HypurrFi-style domain or community-entry hijack cases** remain **D26** reinforcements only
  4. **Solana Foundation STRIDE/SIRN launch** is a defensive ecosystem response, not a new exploit primitive
  5. **GitHub Advisory / Solana-specific checks** produced no fresh Solana/Anchor/SPL-specific GHSA hit affecting the current Microstable stack in this window

### New Vectors Added Today
- **0 NEW vectors**
- **0 reinforcements** requiring a matrix edit today

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A114 Dango-style signed donation polarity inversion** | on-chain public amount paths + keeper amount serialization | ✅ DEFENDED / NOT ACTIVE TODAY | `lib.rs` public amount inputs reviewed today remain `u64`; no public insurance-fund / reserve-top-up instruction accepting a signed delta was found |
| **A94/B77 durable nonce admin takeover** | keeper tx flow + privileged on-chain paths | ✅ DEFENDED | `keeper/src/utils.rs` still signs fresh transactions using `get_latest_blockhash()` + `Transaction::new_signed_with_payer`; no durable nonce workflow observed |
| **A109 / META-49 executable config trust drift** | `solana/Anchor.toml` | ✅ SAFE TODAY | Reviewed `Anchor.toml` still has no `[hooks]` section, so the Anchor lifecycle-hook control-plane path is not active in the current tree |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | CSP remains meta-only, vendored Solana web3 bundle still has no SRI hash, and `docs/app.js` still embeds a devnet faucet keypair client-side |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | Manual fallback still fetches externally validated prices and writes on-chain through `ix_update_oracle` without explicit keeper-side max-drift assertion vs TWAP before write |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | Commit/reveal threshold is still enforced per-call; reviewed state still has no cross-slot cumulative drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 47) | `microstable/security/audit-attestation.json` still absent; critical-path delta remains unattested |

### Today's Verdict
- New incidents found: **0 requiring matrix expansion**
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0** beyond **B45 HIGH carry-forward**
- Blue-team priority remains unchanged:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path
  3. Track cumulative cross-call rebalance drift for large-turnover commit/reveal admission
  4. Move CSP to headers, add SRI, and keep browser-side devnet/test material out of dashboard assets

## 2026-04-15 Daily Check

### Source Sweep (24h~7d window: 2026-04-08 to 2026-04-15 KST)
- Sources checked: rekt.news frontpage/newsletter, hacked.slowmist.io, Solana ecosystem/security pages, Trail of Bits/OtterSec/Neodyme blog indexes, fallback query checks for Immunefi/X/Twitter, plus Dango incident cross-read via web_fetch
- Brave Search API quota exhaustion persisted on direct query search → local search-fallback (SearXNG/Scrapling/DDG) used for query-based checks
- **Confirmed in-window items**:
  1. **Dango insurance-fund exploit** (2026-04-13 disclosure window) — public donation logic failed to enforce positive-amount semantics; mapped as **A114 NEW**, not generic A10-only
  2. **GitHub advisory / Solana-specific checks** produced no fresh Solana/Anchor/SPL-specific GHSA hit affecting current Microstable stack in this window
  3. **Trail of Bits / OtterSec / Neodyme indexes** showed no new Solana-specific exploit-research post in-window requiring matrix expansion
  4. **rekt.news / SlowMist / ecosystem checks** did not surface an additional code-level Solana-native exploit in-window requiring a second matrix delta today

### New Vectors Added Today
- **1 NEW vector**: **A114 Signed-Amount Donation Polarity Inversion / Insurance-Fund Drain**
- **0 reinforcements** beyond the new vector entry

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A114 Dango-style signed donation polarity inversion** | on-chain public amount paths + keeper amount serialization | ✅ DEFENDED / NOT ACTIVE TODAY | `lib.rs` public amount inputs reviewed today remain `u64`; no public insurance-fund / reserve-top-up instruction accepting signed delta was found |
| **A94/B77 durable nonce admin takeover** | keeper tx flow + privileged on-chain paths | ✅ DEFENDED | `keeper/src/utils.rs` still signs fresh transactions using `get_latest_blockhash()` + `Transaction::new_signed_with_payer`; no durable nonce workflow observed |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | CSP remains meta-only, vendored Solana web3 bundle still has no SRI hash, browser-side devnet-only state persists in `docs/app.js` |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | Manual fallback still fetches externally validated prices and writes on-chain without explicit keeper-side max-drift assertion vs TWAP before write |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | Commit/reveal threshold is still enforced per-call; reviewed state still has no cross-slot cumulative drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 46) | `microstable/security/audit-attestation.json` still absent; critical-path delta remains unattested |

### Today's Verdict
- New incidents found: **1 requiring matrix expansion**
- New attack vectors added: **1** (**A114**)
- New **CRITICAL/HIGH** findings: **0** beyond **B45 HIGH carry-forward**
- Blue-team priority remains unchanged:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path
  3. Move CSP to headers, add SRI, and keep browser-side devnet/test material out of production dashboard assets

## 2026-04-14 Daily Check

### Source Sweep (24h~7d window: 2026-04-07 to 2026-04-14 KST)
- Sources checked: rekt.news frontpage/newsletter, hacked.slowmist.io, Solana ecosystem security page, Trail of Bits/OtterSec/Neodyme blog indexes, GitHub Advisory API spot checks, SearXNG fallback for Immunefi/X queries
- Brave Search API quota exhaustion persisted on direct web search → SearXNG fallback used for query-based checks
- **Confirmed in-window items**:
  1. **Hyperbridge / Polytope Labs token gateway** (2026-04-13) — confirmed forged state-proof exploit in the intended relay path; mapped as **A32 reinforcement**, not a new vector
  2. **GitHub Advisory API cross-checks** produced no fresh Solana/Anchor/SPL-specific GHSA hit affecting current Microstable stack in this window
  3. **Trail of Bits / OtterSec / Neodyme indexes** showed no new Solana-specific exploit-research post in-window requiring matrix expansion
  4. **Solana ecosystem security announcement** added ecosystem-program context only (STRIDE/SIRN); no new code-level exploit mechanism requiring a matrix delta
- No new on-chain Solana exploit with public code-level mechanism requiring matrix expansion in this sweep window.

### New Vectors Added Today
- **0 NEW vectors**
- **1 reinforcement applied**: **A32 Cross-Chain Bridge Message Forgery** (Hyperbridge forged state-proof → admin/minter seizure)

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A32 Hyperbridge-style bridge proof forgery** | on-chain + keeper architecture | ✅ NOT APPLICABLE / DEFENDED TODAY | No Wormhole / IBC / bridge receiver path present in `lib.rs` or keeper flow; no cross-chain message credit path to abuse |
| **D48 logger-path stage-2 fetch** | `solana/Cargo.lock`, `keeper/Cargo.toml` | ✅ SAFE TODAY | Logging deps remain `tracing` / `tracing-subscriber`; no `logprinter` / `logtrace` evidence in lockfile or keeper manifest |
| **A109 / META-49 executable config trust drift** | `solana/Anchor.toml` | ✅ SAFE TODAY | `grep` confirms no `[hooks]` section, so Anchor lifecycle-hook control-plane path is still absent |
| **A94/B77 durable nonce admin takeover** | keeper tx flow + privileged on-chain paths | ✅ DEFENDED | `keeper/src/utils.rs` still signs fresh transactions using `get_latest_blockhash()` + `Transaction::new_signed_with_payer`; no durable nonce workflow observed |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | CSP remains meta-only, vendored Solana web3 bundle has no SRI hash, devnet faucet keypair remains embedded client-side |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | Manual fallback still fetches externally validated prices and writes on-chain without explicit keeper-side max-drift assertion vs TWAP before write |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | Commit/reveal threshold is enforced per-call; reviewed state still has no cross-slot cumulative drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 45) | `microstable/security/audit-attestation.json` absent; critical-path delta remains unattested |

### Today's Verdict
- New incidents found: **1 requiring reinforcement only**
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0** beyond **B45 HIGH carry-forward**
- Blue-team priority remains unchanged:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path
  3. Move CSP to headers, add SRI, remove client-side faucet keypair

## 2026-04-12 Daily Check

### Source Sweep (24h~7d window: 2026-04-05 to 2026-04-12 KST)
- Sources checked: rekt.news frontpage, hacked.slowmist.io, GitHub advisories query/fallback, Trail of Bits/OtterSec/Neodyme blog indexes, SearXNG fallback for Immunefi/X queries
- Brave Search API quota exhaustion persisted on direct web search → SearXNG fallback used for query-based checks
- **Confirmed in-window items**:
  1. **Drift / Resolv / TMM** remained already-mapped cases; no newly disclosed Solana-native code-level mechanism surfaced since the 2026-04-11 cycle
  2. **GitHub advisories fallback checks** produced no fresh Solana/Anchor/SPL-specific GHSA hit affecting current Microstable stack in this window
  3. **Trail of Bits / OtterSec / Neodyme indexes** showed no new Solana-specific exploit-research post in-window requiring matrix expansion
  4. **Immunefi/X fallback checks** returned no additional confirmed, code-level public disclosure requiring a new vector
- No new on-chain Solana exploit with public code-level mechanism requiring matrix expansion in this sweep window.

### New Vectors Added Today
- **0 NEW vectors**
- **0 reinforcements applied to matrix**

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A109 / META-49 executable config trust drift** | `solana/Anchor.toml` | ✅ SAFE TODAY | `grep` confirms no `[hooks]` section, so Anchor 1.0 lifecycle-hook control-plane path is not present today |
| **A94/B77 durable nonce admin takeover** | keeper tx flow + privileged on-chain paths | ✅ DEFENDED | `keeper/src/utils.rs` signs fresh transactions using `get_latest_blockhash()` + `Transaction::new_signed_with_payer`; no durable nonce workflow observed |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | CSP is meta-only, vendored Solana web3 bundle has no SRI hash, devnet faucet keypair remains embedded client-side |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | Manual fallback still fetches externally validated prices and writes on-chain without explicit fallback-path max-drift assertion vs TWAP before write |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` + `ProtocolState` | ⚠️ MEDIUM CARRY-FORWARD | Commit/reveal threshold is enforced per-call; reviewed state still has no cross-slot cumulative drift accumulator |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 43) | `microstable/security/audit-attestation.json` absent; critical-path delta remains unattested |

### Today's Verdict
- New incidents found: **0 requiring matrix change**
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0** beyond **B45 HIGH carry-forward**
- Blue-team priority remains unchanged:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path
  3. Move CSP to headers, add SRI, remove client-side faucet keypair

## 2026-04-11 Daily Check

### Source Sweep (24h~7d window: 2026-04-04 to 2026-04-11 KST)
- Sources checked: rekt.news frontpage, hacked.slowmist.io, Solana ecosystem security page, GitHub Advisory API, Trail of Bits/OtterSec/Neodyme blog indexes, SearXNG fallback for Immunefi/X queries
- Brave Search API quota exhaustion persisted on direct web search → SearXNG fallback used for query-based checks
- **Confirmed in-window items**:
  1. **TMM/USDT** (2026-04-05, BNB Chain, $1.665M) — already mapped as **A107**; no new vector required
  2. **HypurrFi** (2026-04-04) — domain hijack only; reinforces **D26**; no new vector required
  3. **Denaria** (2026-04-05, ~$165K) — public incident exists, but no code-level mechanism disclosed yet; excluded from matrix delta
  4. **GitHub advisories 2026-04-09/10** — Wasmtime issues present, but no Solana/Anchor/SPL-specific GHSA affecting current Microstable stack
- No new on-chain Solana exploit with public code-level mechanism requiring matrix expansion in this sweep window.

### New Vectors Added Today
- **0 NEW vectors**
- **0 reinforcements applied to matrix** (all relevant in-window patterns already covered)

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A107 TMM dead-address burn reserve desync** | on-chain + keeper architecture | ✅ NOT APPLICABLE / DEFENDED | No AMM pair reserve accounting, no burnable protocol token path, stablecoin-only collateral ATAs |
| **A94/B77 durable nonce admin takeover** | keeper tx flow + privileged on-chain paths | ✅ DEFENDED | Keeper uses fresh `get_latest_blockhash()`; no durable nonce accounts or pre-signed multisig governance workflow |
| **D26 frontend/domain hijack blast radius** | `docs/index.html`, `docs/app.js` | ⚠️ LOW CARRY-FORWARD | CSP is meta-only, vendored Solana web3 bundle has no SRI hash, devnet faucet keypair remains embedded client-side |
| **A75 MANUAL_ORACLE_MODE drift guard** | keeper `oracle.rs` + on-chain `update_oracle` path | ⚠️ MEDIUM CARRY-FORWARD | Manual fallback still fetches externally validated prices and writes on-chain without explicit fallback-path max-drift assertion vs TWAP before write |
| **A43 cumulative sub-threshold rebalance drift** | `lib.rs` `rebalance()` | ⚠️ MEDIUM CARRY-FORWARD | Commit/reveal threshold is per-call; no cross-slot cumulative drift accumulator observed in reviewed path |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 42) | `microstable/security/audit-attestation.json` absent; critical-path delta remains unattested |

### Today's Verdict
- New incidents found: **3 relevant + 1 advisory batch**, but all were already covered or lacked public mechanism
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0** beyond **B45 HIGH carry-forward**
- Blue-team priority remains unchanged:
  1. Add `security/audit-attestation.json` + CI/release gate
  2. Add explicit manual-price-vs-TWAP drift guard to fallback oracle path
  3. Move CSP to headers, add SRI, remove client-side faucet keypair

## 2026-03-28 Daily Check

### Source Sweep (24h~7d window: 2026-03-21 to 2026-03-28 KST)
- Sources checked: rekt.news (frontpage + newsletter.rekt.news 2026-03-23 issue), hacked.slowmist.io, rustsec.org/advisories, search-fallback (SearXNG), web_fetch (dTRINITY NomosLabs detail, RUSTSEC-2026-0049 rustls-webpki)
- Brave Search API quota exhausted → SearXNG fallback used throughout
- **New confirmed items in window**:
  1. **March 26 malicious Rust crate batch** (RUSTSEC-2023-0104~0124): 15+ Rust crates confirmed malicious removed from crates.io on 2026-03-26. Targets Windows service wrappers, Monero tooling, Tauri UI, OpenVPN Rust binding. → **D28 reinforcement** added to attack-matrix.md + incidents doc.
  2. **RUSTSEC-2026-0049** (rustls-webpki CRL matching, March 20, 2026): CRL Distribution Point matching flaw — "limited impact" per advisory (requires compromised CA first). CVSS not listed. Not relevant to Microstable keeper (no rustls-webpki dep in keeper).
  3. **dTRINITY** (2026-03-17, $257K) — already in matrix as A68; comprehensive incidents doc already has full entry (confirmed in file). No matrix change required.
- No new on-chain Solana exploit with public mechanism between 2026-03-23 and 2026-03-28.

### New Vectors Added Today
- **0 NEW vectors**
- **1 reinforcement**: **D28** (Rust crate malicious-code batch, March 26, 2026)

### Microstable Code Sweep

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **D28 March 26 crate batch** | keeper Cargo.lock | ✅ SAFE | grep confirms 0 matches for all 15+ named malicious crates in keeper build tree |
| **A68 dTRINITY first-depositor / index inflation** | lib.rs mint/redeem/deposit logic | ✅ NOT APPLICABLE | Microstable uses on-chain instruction-tracked accounting (total_deposits field, slot flow caps). ERC4626-style vault share inflation attack surface does not exist in Solana Anchor account model. |
| **RUSTSEC-2026-0049 rustls-webpki** | keeper deps | ✅ N/A | No rustls-webpki in keeper Cargo.lock |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 23) | audit-attestation.json absent; full unattested delta persists |
| **A43 Commit/Reveal Threshold Circumvention** | lib.rs rebalance() | ⚠️ MEDIUM CARRY-FORWARD | No cumulative drift tracking in rebalance(); LARGE_REBALANCE_THRESHOLD constant exists (line 130) but no cross-slot accumulator |
| **B44 SPL Token Delegate Drain** | lib.rs mint() | ⚠️ MEDIUM CARRY-FORWARD | No `delegate.is_none()` check in mint() (grep: no DelegateNotAllowed error, no delegate field validation) |
| **A75 MANUAL_ORACLE_MODE TWAP Drift Guard Missing** | keeper / oracle write path | ⚠️ MEDIUM CARRY-FORWARD | manual_oracle_mode_expiry_slot (line 2655 lib.rs) enforced but no on-chain `assert(|manual_price - twap| <= MAX_DRIFT_BPS)` in write path |

### Today's Verdict
- New incidents found: **2** (D28 crate batch; dTRINITY already in matrix)
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0**
- All existing carry-forwards unchanged: **B45 HIGH (DAY 23)**, **A43 MEDIUM**, **B44 MEDIUM**, **A75 MEDIUM**
- Microstable code-level status: **no actionable new high-severity regression** from today's sweep

---



## 2026-03-27 Daily Check

### Source Sweep (24h~7d window: 2026-03-20 to 2026-03-27 KST)
- Sources checked: rekt.news / newsletter.rekt.news, SlowMist, Hacker News + Brave fallback equivalents, GitHub Advisory (web_search + web_fetch), Trail of Bits/Neodyme/OtterSec index pages, X/Twitter hashtag scan.
- Confirmed incident in window: **GHSA-8f57-hh49-gmqf** (2026-03-26) — `@solana-ipfs/sdk` compromise in npm ecosystem (`vulnerable_version_range: >=0`, no patched version).
- No additional on-chain Solana protocol exploit with confirmed mechanism published between 2026-03-20 and 2026-03-27 that was not already in matrix.
- Existing matrix already includes 2026 reinforcement entries for Neutrl, Venus, DBXen, bonk.fun, dTRINITY, etc. No novel mechanism beyond D28 reinforcement today.

### New Vectors Added Today
- **0 NEW vectors**
- **1 reinforcement candidate**: **D28 Supply Chain** (direct malicious NPM package risk) — no matrix ID extension required.

### 90-Vector Sweep Focus (carry-forward + today)
- Targeted verification performed for all currently open carry-forwards and today’s reinforcement points.

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **D28 Supply Chain** (`@solana-ipfs/sdk` NPM advisory) | off-chain tooling/runtime boundary | ⚠️ MEDIUM-OPEN (N/A for on-chain logic) | Advisory confirms any host running package is potentially fully compromised; rotate keys/certs from clean device. No direct Smart-Contract-path effect observed in current files, but high trust-boundary risk for keeper/dev workflows. |
| **B45 Audit Attestation Gap** | all code | ❌ HIGH CARRY-FORWARD (DAY 22) | audit-attestation.json absent; full unattested delta persists |
| A43 Commit/Reveal Threshold Circumvention | lib.rs rebalance() | ⚠️ MEDIUM CARRY-FORWARD | No cumulative drift tracking |
| B44 SPL Token Delegate Drain | lib.rs mint() | ⚠️ MEDIUM CARRY-FORWARD | No delegate.is_none() check in mint() |
| A75 MANUAL_ORACLE_MODE TWAP Drift Guard Missing | keeper / oracle write path | ⚠️ MEDIUM CARRY-FORWARD | Manual price write path lacks explicit TWAP-drift assertion in current code |
| D26 Frontend Compromise / CSP | docs/index.html | ✅ N/A | CSP meta exists (`script-src 'self'`) and connect-src allowlist; no newly introduced high-risk frontend regression observed |

### Today's Verdict
- New incidents found: **1** (GitHub advisory only)
- New attack vectors added: **0**
- New **CRITICAL/HIGH** findings: **0**
- All existing carry-forwards unchanged and still prioritized: **B45 HIGH**, **A43 MEDIUM**, **B44 MEDIUM**, **A75 MEDIUM**.
- Microstable code-level status: **no actionable new high-severity regression** from today's sweep.


## 2026-03-24 Daily Check

### Source Sweep (24h window: 2026-03-23 to 2026-03-24 KST)
- Sources checked: rekt.news (frontpage, /aave-rekt, /venus-protocol-rekt4, /solv-rekt), cryptotimes.io (USR/Resolv Labs exploit), Brave Search (DeFi hacks March 2026), web_fetch fallback for all above
- **3 new incidents** confirmed with code-level mechanisms in the sweep window:
  1. **Resolv Labs USR Stablecoin** (2026-03-22, ~$25M realized / $80M minted) — A72 NEW VECTOR
  2. **Venus Protocol Rekt4** (2026-03-15, $3.7M) — A73 NEW VECTOR
  3. **Aave wstETH CAPO Misconfiguration** (2026-03-10, $27.78M) — B49 NEW VECTOR
- 1 additional incident noted (Solv BRO vault 2026-03-05, $2.73M — A46 already in matrix; confirmed rekt.news writeup)
- No new Solana-native on-chain smart contract exploits with fund loss in this window beyond those already mapped.

### New Vectors Added Today (2026-03-24)

| Vector | Incident | Date | Category | Loss |
|--------|---------|------|----------|------|
| **A72 (NEW): Privileged Minter EOA Key Compromise + Absent On-Chain Mint Cap** | Resolv Labs USR Stablecoin | 2026-03-22 | Key Compromise + Logic Bug Architecture | ~$25M realized ($80M minted) |
| **A73 (NEW): Long-Horizon Collateral Dominance + Donation Supply-Cap Bypass** | Venus Protocol Rekt4 (BNB Chain) | 2026-03-15 | Flash Loan + Price Manipulation + Economic | $3.7M extracted / $2.15M bad debt |
| **B49 (NEW): Risk-Oracle Anti-Manipulation Guard Misconfiguration → Mass Liquidation** | Aave wstETH CAPO (Ethereum) | 2026-03-10 | Oracle + Config + No Attacker Required | $27.78M healthy positions liquidated |

**A72 Technical Summary (Resolv Labs USR, 2026-03-22, ~$25M)**:
- SERVICE_ROLE was a single EOA (not multisig) with direct mint authority over `requestSwap`/`completeSwap`
- No on-chain validation of mint amounts — no max cap, no oracle cross-check, no supply guard
- Attacker deposited ~$150K USDC and minted ~80M USR (400–500× inflation) via compromised key
- USR depegged from $1.00 → $0.025; converted to ETH via Curve/Uniswap/KyberSwap
- Root cause: ARCHITECTURAL — trusted off-chain role with no on-chain invariant enforcement
- Distinguishes from B15 (key theft): B15 is the trigger; A72 is the design failure that made the trigger lethal

**A73 Technical Summary (Venus Protocol Rekt4, 2026-03-15, $3.7M)**:
- 9-month patience: attacker accumulated 84% of THE token supply cap on Venus
- Donation attack bypassed supply cap (token.transfer to vToken contract → raw balance inflated, supply cap accounting unchanged)
- Mango-style recursive borrow on thin THE/USD liquidity → $3.7M extracted
- Team dismissed identical finding from 2023 Code4rena audit: "supported behavior, no negative side effects"
- Flash loan NOT required — attacker used own patient capital accumulation

**B49 Technical Summary (Aave CAPO, 2026-03-10, $27.78M)**:
- Zero attacker. Chaos Labs Edge Risk engine computed incorrect CAPO parameter for wstETH
- New cap = 2.85% below live market price → immediate 2.85% collateral haircut for all wstETH positions
- AgentHub executed in 1 block → 34 accounts, 10,938 wstETH ($27.78M) liquidated
- First documented large-scale "Defender-Induced Oracle Failure" via automated risk parameter system
- Distinct from A3 (external oracle manipulation) and B18 (attacker config injection)

### Full 90-Vector Microstable Security Check (2026-03-24)

**A72 — Privileged Minter EOA + Absent Mint Cap**
- `lib.rs` `mint()` instruction: USER-SIGNED (`authority: ctx.accounts.user`). Keeper has NO ability to initiate mints on behalf of users.
- On-chain caps enforced in `mint()`: `MAX_COLLATERAL_AMOUNT`, per-TX cap (`MAX_MINT_PER_TX_PPM = 2%`), per-slot cap (`DEFAULT_MAX_MINT_PER_SLOT_PPM = 6%`), CR check, depeg pause, oracle confidence + staleness.
- No SERVICE_ROLE equivalent with direct mint authority exists. ✅ **DEFENDED — A72 architectural failure class not present**

**A73 — Long-Horizon Collateral Dominance + Donation Supply-Cap Bypass**
- `lib.rs` tracks `total_deposits` as explicit accounting field (updated only via `mint()`, `redeem()`, `rebalance()`). Direct SPL token transfers to vault ATAs do NOT update `total_deposits`. ✅
- Microstable is not a lending market with supply cap admission for user-supplied collateral assets — no "collateral listing" with AMM-based spot price. ✅
- No supply cap governance mechanism with raw-balance oracle read path. ✅
- **Known-dismissed finding audit**: No Code4rena-style dismissed findings for Microstable in available audit records. B45 (unattested 3,281-line delta) remains the open risk. ✅ **DEFENDED — A73 direct path not applicable; B45 remains**

**B49 — Risk Oracle Anti-Manipulation Guard Misconfiguration**
- Microstable uses Pyth oracle + keeper `oracle_write_authority`. No CAPO-style automated risk engine.
- `MANUAL_ORACLE_MODE` is time-boxed to 120 slots max, requires cooldown (HIGH-03 fix). ✅
- No automated risk parameter update pipeline (no Chaos Labs / Edge Risk equivalent). ✅
- **Latent risk**: If automated fee rate / CR_TARGET / collateral weight adjustment is ever added → pre-execution sanity gate and liquidation-impact simulation are mandatory before first use.
- ✅ **NOT APPLICABLE (current architecture) — Latent MEDIUM if automated risk oracle ever added**

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A72 Privileged Minter EOA + Absent Cap** | lib.rs mint() | ✅ DEFENDED | User-signed only; multiple on-chain flow caps; no SERVICE_ROLE mint path |
| **A73 Donation Supply-Cap Bypass** | lib.rs total_deposits | ✅ DEFENDED | Accounting field (not raw balance); not a lending market; no spot-price oracle for supply cap |
| **B49 Risk Oracle Misconfiguration** | Keeper / Oracle write path | ✅ NOT APPLICABLE | No automated risk engine; MANUAL_ORACLE_MODE time-boxed 120 slots |
| A59 DEX Aggregator Thin-Pool (carry-forward) | All | ✅ NOT APPLICABLE | No DEX integration |
| **B45 Audit Attestation Gap** | All on-chain code | ❌ HIGH CARRY-FORWARD (DAY 18) | audit-attestation.json absent; unattested delta persists |
| A43 Commit/Reveal Threshold Circumvention | lib.rs rebalance() | ⚠️ MEDIUM CARRY-FORWARD | No cumulative drift tracking |
| B44 SPL Token Delegate Drain | lib.rs mint() | ⚠️ MEDIUM CARRY-FORWARD | No delegate.is_none() check in mint() |
| D43 Security-Tooling Inversion | pages.yml | ⚠️ LOW CARRY-FORWARD | No Trivy; SHA-pin gap |

### Open Carry-Forwards (Priority Order)

| Priority | ID | Days Open | Description | Fix |
|----------|-----|-----------|-------------|-----|
| ❌ HIGH | B45 | DAY 18 | audit-attestation.json absent; 3,281-line unattested delta | Create attestation + CI gate |
| ⚠️ MEDIUM | A43 | DAY ~15 | No cumulative drift accumulator in rebalance() | Add drift tracking |
| ⚠️ MEDIUM | B44 | DAY ~15 | No delegate.is_none() check in mint() | Add check |
| ⚠️ LOW | D43 | DAY 3 | GitHub Actions tag vs. SHA pinning | SHA-pin |

### Today's Verdict
- New incidents found: **3 (USR/Resolv 2026-03-22, Venus Rekt4 2026-03-15, Aave CAPO 2026-03-10)**
- New attack vectors added: **3 (A72, A73, B49)**
- Microstable findings: **0 CRITICAL / 0 HIGH new** / **0 MEDIUM new** / **0 LOW new**
- All 3 new vectors: ✅ DEFENDED or ✅ NOT APPLICABLE for current Microstable architecture
- Carry-forward: B45 HIGH (DAY 18), A43 MEDIUM, B44 MEDIUM, D43 LOW
- Matrix: **90 vectors** total (87 pre-today + 3 new 2026-03-24)


---

## 2026-03-23 Daily Check

### Source Sweep (72h window: 2026-03-20 to 2026-03-23 KST)
- Sources checked: rekt.news (frontpage + leaderboard web_fetch), cryptotimes.io (Movie Token CertiK analysis), theblock.co/thedefiant (CoWSwap/Aave post-mortems), ainvest.com, SearXNG fallback
- **2 new incidents** confirmed in sweep window with code-level mechanisms:
  1. **Aave/CoWSwap Thin-Pool Routing** (2026-03-12, $50M user loss) — mapped to A59 (NEW)
  2. **Movie Token Burn-to-LP Double-Count** (2026-03-10, $242K, BSC) — reinforces A2+A10
- **3 vectors already added** by 3/22 run (A56, A57, A58 — Token-2022 + Anchor v1.0 from Neodyme research)
- No new Solana-specific on-chain exploits with fund loss in this 72h window

### New Vectors Added Today (2026-03-23)

| Vector | Incident | Date | Category | Loss |
|--------|---------|------|----------|------|
| **A59 (NEW): DEX Aggregator Solver Race-to-Minimum / Interface-Mediated Thin-Pool Routing Loss** | Aave/CoWSwap $50M Thin-Pool Routing | 2026-03-12 | Economic / Interface Layer | $50M user loss (no attacker; AMM price impact + post-trade arb) |
| A2+A10 reinforcement: Deflationary-Token Burn-to-LP Direct Write | Movie Token (MT) BSC exploit | 2026-03-10 | Logic Bug + Flash Loan | $242K |

**A59 Technical Summary (Aave/CoWSwap, 2026-03-12)**:
- User signed CoW intent: sell $50.4M aEthUSDT, min buy = 324.94 AAVE (already priced at 99.9% price impact from CoW explorer quote)
- CoW solver selected path: aEthUSDT burn → $50.4M USDT → 17,957 WETH (Uniswap V3, clean) → 327.24 AAVE via SushiSwap AAVE/WETH pool ($73K liquidity, 17.65 WETH reserve)
- 17,957 WETH pushed into 17.65 WETH reserve = 1,017× pool capacity → AMM surrendered all AAVE inventory
- Every contract executed correctly; 327.24 AAVE > signed 324.94 minimum
- Root cause: solver optimizes to meet minimum constraint, not to maximize expected value; price-impact vs. slippage conflation in UI
- Aftermath: Aave Shield (>25% price impact block announced); Aave + CoW DAO pledged fee refunds

### Full Vector Sweep (A59 + carry-forwards)

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| **A59 DEX Aggregator Thin-Pool Routing** | All Microstable code | ✅ NOT APPLICABLE | No DEX aggregator integration; keeper-direct rebalance via vault state; no user collateral swap interface; no CoW/solver integration |
| A2+A10 Movie Token Burn-to-LP | lib.rs mint/redeem | ✅ NOT APPLICABLE | MSTB has no deflationary burn-to-LP function; Pyth oracle (not AMM-based pricing); collateral is 3rd-party stablecoins |
| **B45 Audit Attestation Gap** | All on-chain code | ❌ HIGH CARRY-FORWARD (DAY 17) | audit-attestation.json still absent; unattested 3,281-line delta persists since DAY 1 |
| A43 Commit/Reveal Threshold Circumvention | lib.rs rebalance() | ⚠️ MEDIUM CARRY-FORWARD | No cumulative drift tracking; per-call threshold only |
| B44 SPL Token Delegate Drain | lib.rs mint() | ⚠️ MEDIUM CARRY-FORWARD | No delegate.is_none() check in mint() path |
| A57 Anchor Shadow IDL Migration | keeper/Cargo.toml + programs/Cargo.toml | ✅ DEFENDED | Verified: keeper anchor-client = "0.31.1", on-chain anchor-lang = "0.31.1" — both match. Migration window NOT open. Anchor v1.0.0-rc.5 exists but neither side has adopted it yet. |
| D43 Security-Tooling Inversion | pages.yml | ⚠️ LOW CARRY-FORWARD | No Trivy; tag-pin without SHA structural gap |
| A56 Token-2022 ExtraAccountMeta Injection | lib.rs collateral | ✅ NOT APPLICABLE NOW | SPL Token only; LATENT HIGH if Token-2022 added |
| A58 Token-2022 Transfer Fee Accounting | lib.rs deposit | ✅ NOT APPLICABLE NOW | SPL Token only; LATENT HIGH if Token-2022 added |

### Open Carry-Forwards (Priority Order)

| Priority | ID | Days Open | Description | Fix |
|----------|-----|-----------|-------------|-----|
| ❌ HIGH | B45 | DAY 17 | audit-attestation.json absent; 3,281-line unattested delta | Create attestation artifact |
| ⚠️ MEDIUM | A43 | DAY ~14 | No cumulative drift accumulator in rebalance() | Add drift tracking |
| ⚠️ MEDIUM | B44 | DAY ~14 | No delegate.is_none() check in mint() | Add check |
| ✅ CLOSED | A57 | N/A | Anchor v1.0.0-rc.5 released but both keeper+on-chain on 0.31.1 | No action needed now |
| ⚠️ LOW | D43 | DAY 2 | GitHub Actions tag vs. SHA pinning | SHA-pin all workflow actions |

**No new CRITICAL or HIGH findings for Microstable today.**

---

## 2026-03-21 Daily Check

### Source Sweep (24h window: 2026-03-20 to 2026-03-21 KST)
- Sources checked: SlowMist hacked.slowmist.io (web_fetch), rekt.news (web_fetch), Brave web_search (DeFi/Solana/Immunefi/supply-chain), Wiz blog (Trivy TeamPCP), The Hacker News, CryptoTimes (Neutrl), Socket Security
- **0 new DeFi smart contract exploits** with on-chain fund loss in 24h window (last confirmed: Neutrl DNS hijack 2026-03-19, loss TBD/unknown)
- **1 new CI/CD infrastructure supply chain attack**: Trivy v0.69.4 / TeamPCP (2026-03-19, CVE-2026-28353) — security-tooling inversion, force-push tag hijack, crypto wallet credentials targeted
- **Matrix status**: 83 vectors (pre-today) → **84 vectors** after D43 addition

### New Vectors Added Today

| Vector | Incident | Date | Category | Loss |
|--------|---------|------|----------|------|
| **D43 (NEW): Security-Tooling Inversion — Trusted CI/CD Scanner Compromised via Force-Push Tag Hijack** | Trivy v0.69.4 / TeamPCP / CVE-2026-28353 | 2026-03-19 | Infrastructure / Supply Chain / CI-CD | N/A (credential theft; potential B15 cascades) |

**D43 Technical Summary**: TeamPCP (threat actor) retained GitHub credentials from incomplete containment of Feb 28 hackerbot-claw incident. Used retained aqua-bot service account to:
1. Spoof commits to `aquasecurity/trivy` (impersonating user DmitriyLewen) → push v0.69.4 tag triggering release
2. Publish backdoored binaries to GitHub Releases, Docker Hub, GHCR, ECR
3. Force-push 75/76 `trivy-action` tags to malicious commits (no new release, no branch push — bypasses standard review triggers)
4. Force-push 7 `setup-trivy` tags
5. Steal additional Aqua credentials: GPG keys, Docker Hub, Twitter, Slack
Malicious binary runs legitimate Trivy + credential stealer in parallel. 3-stage payload: memory scrape (Runner.Worker process, SSH keys, cloud creds, **crypto wallet files**) → AES-256+RSA-4096 encrypt → exfil to `scan.aquasecurtiy[.]org` (typosquat). Developer machine persistence via systemd `sysmon.py` polling ICP C2. CVE: CVE-2026-28353.
Source: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack | https://thehackernews.com/2026/03/trivy-security-scanner-github-actions.html

### Microstable D43 Assessment

**Verdict: ⚠️ LOW RISK (Partial)**

**Evidence chain** (actual code read):
- `microstable/.github/workflows/pages.yml` EXAMINED ✅ — no `aquasecurity/trivy-action` or `aquasecurity/setup-trivy` in use. D43 blast radius **does not apply directly**.
- Pipeline only deploys static `docs/` to GitHub Pages via official GitHub-maintained actions (`actions/checkout@v4`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`)
- Keeper builds not observed in any CI pipeline (appear to be local builds)

**Residual risk (structural, not D43-specific)**:
- All 4 GitHub Actions references use TAG pinning (`@v4`, `@v5`, etc.) WITHOUT SHA pinning
- If any of these officially-maintained actions are ever compromised via the same force-push tag pattern, the build pipeline will silently receive malicious payloads
- GitHub official actions are significantly lower risk than third-party (Aqua Security) actions, but not zero-risk

**Finding classification**: ⚠️ LOW — no current D43 exposure, but structural GitHub Actions SHA-pinning gap present. **No CRITICAL/HIGH escalation required.**

**Recommended fix (non-urgent)**:
```yaml
# pages.yml — replace tag references with SHA pins:
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4
- uses: actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b  # v5
- uses: actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dda462b719fa  # v3
- uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e  # v4
```

### Full Vector Sweep (New D43 + Previous Carry-Forwards)

| Vector | Code Target | Verdict | Notes |
|--------|-------------|---------|-------|
| D43 Security-Tooling Inversion | pages.yml | ⚠️ LOW | No Trivy in pipeline; tag-pinning structural gap; SHA fix recommended |
| B45 Audit Attestation Gap | All on-chain | ❌ HIGH CARRY-FORWARD (DAY 16) | audit-attestation.json still absent; unattested delta persists |
| A43 Commit/Reveal Threshold Circumvention | lib.rs rebalance() | ⚠️ MEDIUM CARRY-FORWARD | No cumulative drift tracking; per-call threshold only |
| B44 SPL Token Delegate Drain | lib.rs mint() | ⚠️ MEDIUM CARRY-FORWARD | No delegate.is_none() check in mint() path |
| D28 Supply Chain | keeper/Cargo.toml | ✅ LOW-DEFENDED | tracing = "0.1" (correct); no lz4_flex in deps; no trivy-action |
| D41 lz4_flex Uninitialized Memory | keeper/ | ✅ NOT PRESENT | cargo tree shows no lz4_flex dependency |
| D42 tracing-ethers SSH Exfil | keeper/Cargo.toml | ✅ DEFENDED | Only `tracing` + `tracing-subscriber` (correct packages) present |
| D26 Frontend XSS/Injection | docs/index.html | ✅ DEFENDED | CSP meta tag present; self-hosted vendor JS (no CDN); no external script src |
| A40 ERC4626 Share-Price Donation | lib.rs | ✅ DEFENDED | total_deposits tracked field; not raw balance |
| A2 Flash Loan + Price Manipulation | lib.rs mint/redeem | ✅ DEFENDED | Pyth TWAP + staleness + confidence + per-slot flow caps |
| A3 Oracle Manipulation | lib.rs | ✅ DEFENDED | Feed ID pinning + staleness + confidence + manual oracle timelock |

**Net new CRITICAL/HIGH findings today: 0**
**Carry-forwards unchanged**: B45 HIGH (audit-attestation.json absent — DAY 16), A43 MEDIUM, B44 MEDIUM

---

## 2026-03-18 Daily Check

### Source Sweep (48h window: 2026-03-17 to 2026-03-18)
- Sources checked: SlowMist hacked.slowmist.io (web_fetch), rekt.news (web_fetch), Brave web_search (DeFi/Solana/Immunefi), web_fetch: cryip.co (dTRINITY mechanism analysis)
- **1 new DeFi exploit with new attack vector**: dTRINITY dLEND (Ethereum, 2026-03-17, $257K) — aToken/index inflation phantom collateral attack
- **1 new infrastructure CVE**: Ubuntu CVE-2026-3888 (systemd snap-confine LPE, 2026-03-18) — keeper server privilege escalation risk
- **1 notable research item**: Injective Immunefi dispute (March 2026) — $500M-risk permissionless state erasure bug in Cosmos SDK; N/A for Solana/Microstable but logged for awareness
- **Matrix status**: 81 vectors (pre-today) → **83 vectors** after A68 + D35 additions

### New Vectors Added Today

| Vector | Incident | Date | Category | Loss |
|--------|---------|------|----------|------|
| **A68 (NEW): Lending Pool aToken/Index Inflation Phantom Collateral Attack** | dTRINITY dLEND (Ethereum) | 2026-03-17 | Smart Contract / Lending Pool Accounting | $257K |
| **D35 (NEW): Linux Keeper Infrastructure LPE via systemd snap-confine** | CVE-2026-3888 (Ubuntu) | 2026-03-18 | Infrastructure / Privilege Escalation | N/A |

**A68 Technical Summary**: Flash loan USDC from Morpho → deposit $772 USDC into dLEND-dUSD pool → internal liquidity index inflated (accounting error/initialization bug) → protocol values $772 deposit as $4.8M phantom collateral (6,215× inflation) → borrow 257K dUSD → execute 127 deposit/withdrawal cycles draining aToken accounting layer → $257K extracted. Mechanism differs from A40 (ERC4626 donation inflates `totalAssets`); here the *internal index* is inflated, not the token balance. 127-cycle amplification loop is a distinct draining pattern, not reentrancy.
Source: https://hacked.slowmist.io/ | https://cryip.co/dtrinitys-dlend-protocol-exploit-drains-around-257k-on-ethereum/

**D35 Technical Summary**: CVE-2026-3888 (Ubuntu, snap-confine cleanup race). Local attacker with initial code execution on an Ubuntu host running snap packages → exploit cleanup timing window → elevate to root. Requires local foothold but no user interaction once achieved. Attack complexity: high. Keeper servers running Ubuntu + any snap package = elevated risk if unpatched.
Source: https://thehackernews.com/2026/03/ubuntu-cve-2026-3888-bug-lets-attackers.html | CVE-2026-3888

### Microstable A68 Assessment

**Verdict: ✅ N/A — Architecture Mismatch**
- Microstable is a mint/redeem stablecoin protocol, NOT a lending pool. No aToken/liquidity index mechanism exists in current architecture.
- `lib.rs` tracks `vault.total_deposits` as explicit accounting — updated only by `mint()`, `redeem()`, `rebalance()` instructions. No index multiplication layer.
- No `liquidityIndex`, no `exchangeRate`, no `cToken`/`aToken` abstraction in any vault or position struct.
- A68 becomes relevant ONLY if Microstable is integrated into or forks from an Aave/Compound-style lending pool in the future.

### Microstable D35 Assessment

**Verdict: ⚠️ MEDIUM — Keeper Host Ubuntu Snap Exposure**
- Keeper binary (`microstable/solana/keeper/src/`) is compiled Rust (not a snap package itself), so the keeper binary does not directly contain the vulnerability.
- However: if keeper server runs Ubuntu AND any snap package is installed for tooling/monitoring (e.g., `snapd` default snap, or monitoring tools installed as snaps), the host OS privilege escalation surface is live.
- **Risk path**: Any initial foothold on the keeper host (e.g., via D28 supply chain, B19 log leak, or remote exploit in a co-located service) + unpatched CVE-2026-3888 = root on keeper host = full keeper key exposure.
- `run: snap list` on keeper server was not executed in this cycle (requires direct host access), but patch status should be verified within 24h.
- **Blue-team directive**: (1) Run `sudo apt update && sudo apt upgrade snapd` on all keeper servers; (2) Run `snap list` — remove unnecessary snaps from production key-holding servers; (3) If snaps cannot be removed, isolate keeper binary in a container with no snap host namespace exposure.

### Full 83-Vector Microstable Security Check

#### ❌ HIGH — B45 Post-Audit Deployment Delta (CARRY-FORWARD, DAY 13 OPEN)
- `security/audit-attestation.json`: **CONFIRMED ABSENT** (persistent open from all prior cycles)
- Production code delta from last audited commit remains untracked and ungated
- **Blue-team directive (re-escalated — DAY 13)**: Create `security/audit-attestation.json` with fields: `last_audited_commit`, `auditor`, `date`, `scope`; add CI gate blocking critical-path PRs without attestation sign-off. This has been open 13 days — escalate to Master.

#### ⚠️ MEDIUM — D35 Keeper Host Linux LPE CVE-2026-3888 (NEW TODAY)
- Ubuntu CVE-2026-3888 (snap-confine cleanup race, 2026-03-18 disclosure) — privilege escalation to root on unpatched Ubuntu servers running snap packages
- Keeper binary is compiled Rust, not a snap, but any snap on the keeper host = root escalation surface
- **Blue-team directive**: `sudo apt update && sudo apt upgrade snapd` on keeper server; `snap list` audit; isolate keeper in container if snaps cannot be removed

#### ⚠️ MEDIUM — A43 Commit/Reveal Threshold Circumvention (CARRY-FORWARD, STILL OPEN)
- `lib.rs:1579` — per-call commit/reveal check at `turnover >= LARGE_REBALANCE_THRESHOLD (4%)`; no cumulative drift tracking
- Attack path: 5× sub-threshold rebalances at 3.9% over 160 slots = 19.5% equivalent without commit/reveal
- **Blue-team directive**: Add cumulative drift tracking to ProtocolState; trigger commit/reveal when epoch sum exceeds threshold

#### ⚠️ MEDIUM — B44 SPL Token Account Persistent Delegate Drain (CARRY-FORWARD, STILL OPEN)
- `mint()` instruction: no `delegate.is_none()` check on `user_collateral_ata`
- Protocol funds: ✅ safe (PDA vault ATAs); user-side: attacker with stale Approve-granted delegation can force victim collateral into protocol while attacker receives MSTB
- **Blue-team directive**: `require!(ctx.accounts.user_collateral_ata.delegate.is_none(), ErrorCode::DelegateNotAllowed)` in Mint accounts validation

#### ⚠️ MEDIUM — B63 Physical TEE Bypass — Operator Device Risk (CARRY-FORWARD)
- CVE-2026-20435 (MediaTek Android boot chain, ~25% of Android phones, Phantom Wallet extractable in <45s)
- **Blue-team directive**: Audit operator devices for MediaTek SoC; rotate any keeper key accessible via unpatched Android device; enforce hardware wallet for all keeper signing

#### ⚠️ LOW — A63 Business Logic: Redeem min_out_amount No Protocol Floor (CARRY-FORWARD)
- Redeem accepts `min_out_amount=0`; oracle-priced so classic MEV sandwich does not apply
- Residual risk: oracle degradation + haircut applied silently when min=0
- **Blue-team directive (optional)**: emit event with applied haircut multiplier

#### ⚠️ LOW — D26 Dashboard Vendor Script: No SRI Hash (CARRY-FORWARD)
- `docs/index.html`: self-hosted `solana-web3-1.95.3.iife.min.js` without `integrity=` attribute
- CSP `script-src 'self'` in place; SRI adds tamper-detection layer
- **Blue-team directive**: Add `integrity="sha384-..."` computed via `openssl dgst -sha384 -binary <file> | base64`

#### ✅ All Other Vectors
- A1–A13: ✅ ALL DEFENDED (CEI pattern, checked arithmetic, Anchor constraints, PDA seed validation, Solana token program checks)
- A32 (Bridge Message Forgery): ✅ N/A — Solana-native, no IBC/bridge layer
- A33–A35: ✅ DEFENDED (oracle unit invariants, AI commit tagging policy, audit scope tracking)
- A36 (Thin-Liquidity Collateral Cascade): ✅ DEFENDED — collateral limited to USDC/USDT/DAI/USDS (deep liquidity, allowlist constrained)
- A38 (ZK Verifier): ✅ N/A — no ZK layer
- A39–A52: ✅ DEFENDED or N/A
- A61 (ERC-2771): ✅ N/A — Solana, no ERC-2771 meta-tx layer
- A62 (Automated Risk Param Oracle): ✅ DEFENDED — oracle updates require 2-of-3 keeper quorum, no fully-automated AgentHub-style executor
- A67 (Supply Cap Bypass): ✅ DEFENDED — `total_deposits` accounting not bypassable via direct SPL transfer
- **A68 (NEW today)**: ✅ N/A — not a lending pool, no aToken/index mechanism
- B14–B20: ✅ (multi-RPC, HMAC, log masking, rate limiting in place)
- B29 (AI Confused-Deputy): ✅ No AI oracle write path in production
- B35 (Keeper Slippage Misconfiguration): ✅ `MAX_REBALANCE_SLIPPAGE_BPS` enforced at code level
- B36 (Social-Engineering Stake Authority): ⚠️ Operational risk — keeper hot keys remain on workstation
- B37–B43 (AI agent meta-vectors): ✅ N/A — no autonomous AI agent with signing authority
- B45 (Post-Audit Delta): ❌ HIGH — carry-forward (Day 13)
- B53 (Address Poisoning): ✅ Keeper uses deterministic PDA addresses, not user-input addresses
- B63 (MediaTek TEE): ⚠️ MEDIUM carry-forward
- B64 (Injective Permissionless Erasure): ✅ N/A — Solana, different state machine model
- **D35 (NEW today)**: ⚠️ MEDIUM — keeper host snap-confine LPE (see above)
- C21–C30: ✅ DEFENDED (redemption throttle, dynamic fees, circuit breakers, timelocked governance, Pyth oracle)

---

## 2026-03-17 Daily Check

### Source Sweep (72h window: 2026-03-14 to 2026-03-17)
- Sources checked: rekt.news (web_fetch), SlowMist hacked.slowmist.io (web_fetch), Brave web_search (DeFi/Solana), dev.to/ohmygod Firedancer article (web_fetch)
- **1 new DeFi exploit with new attack vector**: Venus Protocol (BNB Chain, 2026-03-15, $2.15M) — supply cap bypass via direct token transfer + slow-accumulation TWAP manipulation
- **Matrix status**: 80 vectors (pre-today) → **81 vectors** after A67 addition

### New Vector Added Today

| Vector | Incident | Date | Category | Loss |
|--------|---------|------|----------|------|
| **A67 (NEW): Supply Cap Bypass via Direct Protocol Contract Token Transfer + Slow-Accumulation TWAP Manipulation** | Venus Protocol (BNB Chain) | 2026-03-15 | Smart Contract / Economic | $2.15M |

**A67 Technical Summary**: 9-month patience attack. Phase 1: attacker accumulates 14.5M THE tokens (84% of supply cap) over 9 months via legitimate deposits — staying under risk alert thresholds. Phase 2: bypasses supply cap by directly calling BEP-20 `transfer()` to protocol contract address instead of using `deposit()`. Supply cap check exists only in the deposit code path, not at the balance level. Position inflated to 53.2M THE (3.67× cap). Phase 3: exploits thin on-chain THE liquidity to push TWAP from $0.27→$0.53 (96%). Borrows massive assets against inflated collateral. $2.15M extracted before Venus paused 7 markets.
Root cause: (1) balance-level supply cap not enforced at contract level, only at deposit function level; (2) TWAP oracle reading on-chain DEX price for thin-liquidity collateral.
Source: https://hacked.slowmist.io/ | https://allez.xyz/research/venus-protocol-attack-analysis

### Microstable A67 Assessment

**Verdict: ✅ DEFENDED**
- Microstable tracks `vault_usdc/usdt/dai/usds.total_deposits` as explicit accounting fields updated only through `mint()`, `redeem()`, and `rebalance()` instructions
- Direct SPL token transfers to vault ATAs do NOT update `total_deposits` → no supply cap bypass possible via direct transfer
- Oracle path uses Pyth price feeds (not on-chain AMM/DEX TWAP) → direct token position manipulation cannot distort oracle pricing
- Collateral limited to USDC, USDT, DAI, USDS (major stablecoins with multi-billion liquidity) → thin-liquidity TWAP manipulation not possible

**Future risk to watch**: If Microstable ever adds (a) AMM-derived pricing OR (b) exotic/thin-liquidity collateral OR (c) raw `vault_ata.amount` as collateral basis → A67 applies immediately.

### Full 81-Vector Microstable Security Check

#### ❌ HIGH — B45 Post-Audit Deployment Delta (CARRY-FORWARD, DAY 12 OPEN)
- `security/audit-attestation.json`: CONFIRMED ABSENT (persistent open from all prior cycles)
- **Blue-team directive (ESCALATED)**: Create `security/audit-attestation.json` with `last_audited_commit`, `auditor`, `date`, `scope`; add CI gate blocking critical-path PRs without attestation sign-off

#### ⚠️ MEDIUM — A43 Commit/Reveal Threshold Circumvention (CARRY-FORWARD, STILL OPEN)
- `lib.rs:1579` — per-call commit/reveal check at `turnover >= LARGE_REBALANCE_THRESHOLD (4%)`; no cumulative drift tracking
- `grep "cumulative_drift\|epoch_drift"` → 0 results (confirmed today)
- Attack path: 5× sub-threshold rebalances at 3.9% each over 160 slots = 19.5% equivalent without commit/reveal
- **Blue-team directive**: Add cumulative drift tracking to ProtocolState; trigger commit/reveal when epoch sum exceeds LARGE_REBALANCE_THRESHOLD

#### ⚠️ MEDIUM — B44 SPL Token Account Persistent Delegate Drain (CARRY-FORWARD, STILL OPEN)
- `mint()` instruction: no `delegate.is_none()` check on user_collateral_ata
- `grep "delegate" lib.rs` → 0 results (confirmed today)
- Protocol funds: ✅ safe; user-side: attacker with stale delegate can launder stolen collateral through protocol
- **Blue-team directive**: `require!(ctx.accounts.user_collateral_ata.delegate.is_none(), ErrorCode::DelegateNotAllowed)` in Mint accounts validation

#### ⚠️ MEDIUM — B63 Physical TEE Bypass — Operator Device Risk (CARRY-FORWARD)
- CVE-2026-20435 (MediaTek, ~25% of Android phones, Phantom Wallet extractable in <45s)
- **Blue-team directive**: Audit operator devices; rotate any keeper key accessible via Phantom mobile on unpatched MediaTek device; enforce hardware wallet for all keeper signing

#### ⚠️ LOW — A63 Business Logic: Redeem min_out_amount No Protocol Floor (CARRY-FORWARD)
- `redeem()` accepts min_out_amount=0; oracle-priced so classic MEV sandwich does not apply
- Risk: user silently accepts oracle-penalty haircut with no on-chain signal
- **Blue-team directive (optional)**: emit event with applied haircut multiplier

#### ⚠️ LOW — D26 Dashboard Vendor Script: No SRI Hash (CARRY-FORWARD)
- `docs/index.html:994`: `<script src="./vendor/solana-web3-1.95.3.iife.min.js">` — no `integrity=` attribute
- CSP `script-src 'self'` in place; SRI adds tamper-detection layer
- **Blue-team directive**: Add `integrity="sha384-..."` via `openssl dgst -sha384 -binary vendor.js | base64`

#### ✅ All Other Vectors
- A1–A13: ✅ ALL DEFENDED
- A32, A38, A39, A46, A48–A52: ✅ N/A or DEFENDED (no bridge, no ZK, classic SPL Token)
- A33–A35, A36, A40–A42: ✅ DEFENDED
- A47, A62–A64: ✅ DEFENDED (CR-01 bindings, 2-of-3 quorum, hard slippage cap at code level)
- **A67 (NEW today)**: ✅ DEFENDED (total_deposits accounting + Pyth oracle, see above)
- B14–B20, B29, B35–B36: ✅ / ⚠️ Operational (B36 open by design: hot keys)
- B37–B43, B50–B66: ✅ N/A for current architecture / LOW

---

## 2026-03-16 Daily Check

### Source Sweep (72h window: 2026-03-13 to 2026-03-16)
- Sources checked: rekt.news (web_fetch), SlowMist hacked.slowmist.io, NOMINIS February 2026 report (web_fetch), Brave web_search, OWASP Smart Contract Top 10: 2026 (web_fetch), dev.to/ohmygod CVE-2026-20435 (web_fetch), TheBlock/CryptoNews (web_fetch)
- **1 new hardware vulnerability with on-chain key implications**: CVE-2026-20435 — MediaTek Android boot chain TEE bypass (Ledger Donjon, 2026-03-12; ~25% of Android phones)
- **0 new DeFi protocol exploits** in March 13–16 window (no new hacks above $100K found in 3-day period)
- **Matrix status**: 79 vectors (pre-today) → **80 vectors** after B63 addition

### New Vector Added Today

| Vector | CVE/Incident | Date | Category |
|--------|-------------|------|----------|
| **B63 (NEW): Physical-Access Hardware TEE Bypass — MediaTek Boot Chain** | CVE-2026-20435 | 2026-03-12 (disclosed) | Hardware / Physical Access |

**B63 Technical Summary**: MediaTek Dimensity 7300 + Trustonic TEE (kinibi/t-base) boot chain flaw. Attacker with physical access → USB connection to powered-off device → bootloader exploit before OS loads → TEE encryption key extraction → offline device storage decryption → full seed phrase + PIN in <45 seconds. Phantom Wallet (Solana) confirmed extractable. Affects ~25% of Android devices globally. B15 distinction: no OS, no malware, no running process — pure hardware TEE bypass. Patch issued to OEMs 2026-01-05 but budget/mid-range device lag is 3+ months.
Source: https://www.theblock.co/post/393154/ledger-researchers-expose-android-flaw-enabling-theft | CVE-2026-20435

### Full 80-Vector Microstable Security Check

#### ❌ HIGH — B45 Post-Audit Deployment Delta (CARRY-FORWARD, DAY 11 OPEN)
- `security/audit-attestation.json`: **CONFIRMED ABSENT** (ls security/ output verified: green-team-report.md, red-team-report.md, red-team-v2-report.md, yellow-team-report.md, invariant_monitor.py — no attestation JSON)
- Production code delta from last audited commit remains untracked and ungated
- **Blue-team directive (re-escalated)**: Create `security/audit-attestation.json` with `last_audited_commit`, `auditor`, `date`, `scope`; add CI gate blocking critical-path PRs without attestation sign-off

#### ⚠️ MEDIUM — B63 Physical TEE Bypass — Operator Device Risk (NEW TODAY)
- **CVE-2026-20435 (MediaTek, Ledger Donjon, 2026-03-12)**: Phantom Wallet (Solana) confirmed extractable from unpatched Android MediaTek devices in <45 seconds with physical access
- Keeper code is a Rust server binary (no direct Android dependency in `keeper/src/`), but operator devices used for key setup/management may be Android
- If any keeper keypair was ever set up on or imported to a Phantom/mobile wallet on a MediaTek Android device with firmware pre-2026-03 security patch → treat key as potentially compromised
- **Blue-team directive**: (1) Audit all operator devices for MediaTek SoC; (2) Rotate any keeper/treasury key accessible via Phantom mobile on unpatched MediaTek device; (3) Enforce hardware wallet (Ledger/Trezor) for all keeper signing — no mobile hot wallet for keeper keys going forward

#### ⚠️ MEDIUM — A43 Commit/Reveal Threshold Circumvention (CARRY-FORWARD, STILL OPEN)
- `lib.rs:1574` — per-call commit/reveal check at turnover >= 4% (`LARGE_REBALANCE_THRESHOLD = 40_000`)
- `grep "cumulative_drift\|epoch_drift\|epoch_weight_start"` → 0 results
- Attack path: 5× sub-threshold rebalances at 3.9% each over 160 slots achieves 19.5% equivalent without commit/reveal ceremony
- **Blue-team directive**: Add `epoch_weight_start[4]` snapshot and `cumulative_drift: u64` to `ProtocolState`; accumulate drift per rebalance; trigger commit/reveal when cumulative sum exceeds threshold

#### ⚠️ MEDIUM — B44 SPL Token Account Persistent Delegate Drain (CARRY-FORWARD, STILL OPEN)
- `mint()` instruction: `user_collateral_ata` at line 2310 — no `delegate.is_none()` check
- `grep "delegate" lib.rs` → 0 results (only key name references, no authority check)
- Protocol funds: ✅ safe (PDA vault ATAs); user-side: attacker with stale Approve-granted delegation on victim's USDC ATA can force victim's collateral into protocol while attacker receives MSTB
- **Blue-team directive**: `require!(ctx.accounts.user_collateral_ata.delegate.is_none(), ErrorCode::DelegateNotAllowed)` in Mint accounts validation

#### ⚠️ LOW — A63 Business Logic: Redeem min_out_amount Has No Protocol Floor (NEW TODAY)
- `redeem(ctx, musd_amount, min_out_amount)`: user can set `min_out_amount = 0`
- Contract enforces `total_payout >= min_out_amount` — if min = 0, any oracle-priced payout accepted
- **Not an AMM MEV attack path**: redemption is oracle-priced (not pool-priced), so classic Aave-style sandwich does not apply
- **Residual risk**: during oracle degradation + penalty haircuts, user with min_out_amount=0 silently accepts reduced payout; no on-chain protection signals the user of actual haircut applied
- **Severity**: LOW (oracle defenses limit manipulation; not a protocol fund drain path)
- **Blue-team directive (optional hardening)**: add `require!(min_out_amount >= expected_floor, ...)` or emit event with applied haircut multiplier so users can off-chain validate

#### ⚠️ LOW — A64 Deployment Config Audit Blindspot: Oracle Constants (CARRY-FORWARD, RELATED TO B45)
- Oracle staleness/confidence constants are code-level (not deployment params), but values set at initialization are not in audit attestation scope
- `MINT_ORACLE_STALENESS_MAX = 20`, `REDEEM_ORACLE_STALENESS_MAX = 45`, `MINT_ORACLE_CONFIDENCE_MAX = 2%` — these are correct/reasonable values but unattested
- Covered by B45 (attestation gap); A64 adds specific concern about oracle parameter documentation
- **Status**: OPEN but Low, absorbed into B45 remediation scope

#### ⚠️ LOW — D26 Self-Hosted Vendor Script Without SRI Hash (CARRY-FORWARD)
- `docs/index.html:994`: `<script src="./vendor/solana-web3-1.95.3.iife.min.js"></script>` — no `integrity=` attribute
- CSP `script-src 'self'` limits external risk; SRI adds tamper-detection for self-hosted files
- **Blue-team directive**: Add `integrity="sha384-..."` to vendor script tag; compute with `openssl dgst -sha384 -binary <file> | base64`

#### All Other Vectors (carry-forward from 2026-03-12 check)
- A1–A13: ✅ ALL DEFENDED
- A32 (Bridge Message Forgery): ✅ N/A (Solana-native, no IBC/bridge layer)
- A33–A35: ✅ DEFENDED (oracle unit invariants, AI commit tagging in place)
- A36 (Thin-Liquidity Collateral Cascade): ✅ DEFENDED (collateral limited to USDC/USDT/DAI/USDS with known deep liquidity; allowlist constrained)
- A38 (ZK Verifier): ✅ N/A (no ZK layer)
- A39–A52: ✅ DEFENDED or N/A
- A61–A62: ✅ DEFENDED
- A63: ⚠️ LOW (redeem min_out floor, see above)
- A64: ⚠️ LOW (oracle constant attestation, absorbed into B45)
- A46 (ERC721 Dual-Mint): ✅ N/A (classic SPL Token, no NFT transfer hooks)
- B14–B20: ✅ (B17 HMAC ✅, B19 log masking ✅)
- B29 (AI Confused-Deputy): ✅ No AI oracle write path in production
- B35 (Keeper Slippage Misconfiguration): ✅ `MAX_REBALANCE_SLIPPAGE_BPS = 1500` enforced at code level (lib.rs:1556)
- B36 (Social-Engineering Stake Authority): ⚠️ Operational. Step Finance shutdown confirmed. Keeper hot keys remain on workstation. B63 adds new physical access dimension.
- B37–B43: ✅/N/A
- B44: ⚠️ MEDIUM (open, see above)
- B45: ❌ HIGH (open, see above)
- B46–B62: ✅ (operational recommendations, no code gap)
- B63: ⚠️ MEDIUM (new, see above)
- C21–C30: ✅ ALL DEFENDED (overcollateralization, TWAP, progressive redemption fees, circuit breakers)
- D26: ⚠️ LOW (SRI missing, see above)
- D27–D38: ✅ (D37 HTTP cache poisoning: keeper uses direct Solana RPC, not HTTP proxy layer)

### Today's Verdict
- **New vectors added**: 1 (B63 — CVE-2026-20435 MediaTek TEE bypass; matrix: 79 → **80 vectors**)
- **New CRITICAL findings**: 0
- **New HIGH findings**: 0
- **New MEDIUM findings**: 1 (B63 operator device risk)
- **New LOW findings**: 1 (A63 redeem min_out_amount floor)
- **Carry-forward open items**: B45 HIGH (day 11), A43 MEDIUM, B44 MEDIUM, B63 MEDIUM (new), D26 LOW, A63 LOW (new)
- **No CRITICAL/HIGH new code-level findings** — no immediate Discord protocol-breach alert required
- **B63 operator device action recommended**: Discord channel 1468813323662524500 alert (operational advisory, not protocol code breach)

---

## 2026-03-12 Daily Check

### Source Sweep (24h window)
- Sources checked: rekt.news, hacked.slowmist.io (live fetch), Halborn blog, Brave search, web_fetch on confirmed incident URLs
- **No new DeFi incidents** in March 11–12 window. SlowMist last entry: 2026-03-10 Gondi ($230K, A4 reinforcement).
- 0 new vectors this cycle. Matrix holds at **79 vectors**.

### Pattern Reinforcement: Gondi A4 (2026-03-10, confirmed March 12 sweep)
- Gondi NFT Platform `Purchase Bundler` function (Sell & Repay contract, deployed 2026-02-20): verified caller authorization for bundle invocation but did NOT separately verify caller ownership/borrower status for each specific NFT operated on.
- 78 NFTs drained ($230K: 44 Art Blocks, 10 Doodles, 2 Beeple). All transfers cryptographically valid.
- **Meta pattern confirmed**: any batch/multicall abstraction where the calling-function-level auth check is separated from the per-asset ownership check creates a dual-authorization gap. This is architecturally identical to keeper-batch operations over user positions in Microstable — if a future `batch_redeem()` or `batch_liquidate()` function is added, it MUST independently re-verify per-position ownership at the element level.

### Full 79-Vector Microstable Security Check

#### ❌ HIGH — B45 Post-Audit Deployment Delta (CARRY-FORWARD, STILL OPEN)
- `/Users/kjaylee/.openclaw/workspace/microstable/security/audit-attestation.json`: **NOT FOUND** — confirmed absent again today
- Delta vs audited commit `f327e7c6df0fae25171f0e00be316f8f7cf4a5c8`: adds=3,281 lines, dels=324 lines, zero CI-gated delta tracking
- **Status**: 7-day-old open HIGH finding. Every additional day without attestation gate widens the unreviewed production surface.
- **Blue-team directive (re-escalated)**: Create `security/audit-attestation.json`, add CI gate to block critical-path PRs without attestor sign-off, publish `last_audited_commit` to dashboard security section.

#### ⚠️ MEDIUM — A43 Commit/Reveal Threshold Circumvention (CARRY-FORWARD, STILL OPEN)
- `lib.rs:1579` — `if turnover >= LARGE_REBALANCE_THRESHOLD { verify_commit_reveal() }` — per-call check only
- No cumulative drift accumulator found: `grep -n "cumulative|epoch_drift|period_drift|window_drift" lib.rs` → no results
- Attack path: 5× calls with `turnover = 3.9%` (just below 4% threshold) over 5 × 32 slots = 160 slots (~64s) achieves equivalent of a 19.5% single-step rebalance without any commit/reveal ceremony
- **Blue-team directive**: add `epoch_weight_start[4]` snapshot and `cumulative_drift: u64` field to `ProtocolState`; accumulate `|current_weight - epoch_start_weight|` per `rebalance()` call; trigger commit/reveal when sum exceeds threshold.

#### ⚠️ MEDIUM — B44 SPL Token Account Persistent Delegate Drain (CARRY-FORWARD, STILL OPEN)
- `lib.rs` `mint()` instruction: `authority: ctx.accounts.user.to_account_info()` used for transfer_checked — no `delegate.is_none()` check on `user_collateral_ata`
- `grep -n "delegate" lib.rs` → 0 results
- Protocol funds: ✅ safe (PDA-owned vault ATAs, no external delegate possible)
- User-side gap: an attacker holding a stale `Approve`-granted delegation on victim's USDC ATA can drain victim funds into Microstable (attacker receives MSTB, victim's collateral is locked in protocol)
- **Blue-team directive**: `require!(ctx.accounts.user_collateral_ata.delegate.is_none(), ErrorCode::DelegateNotAllowed)` in `mint()` accounts validation.

#### ⚠️ LOW — D26 Self-Hosted Vendor Script Without SRI Hash (NEW THIS CYCLE)
- `docs/index.html:994`: `<script src="./vendor/solana-web3-1.95.3.iife.min.js"></script>` — no `integrity=` attribute
- CSP `script-src 'self'` prevents external script injection ✅, but does not verify integrity of same-origin served files
- If the server/repository is compromised, a modified `solana-web3.iife.min.js` would load silently with no hash mismatch detection
- **Severity**: LOW (self-hosted, same-origin risk chain requires server/repo compromise first; D26 main risk is external CDN which is not present here)
- **Blue-team directive (optional hardening)**: compute SHA-384 of `vendor/solana-web3-1.95.3.iife.min.js` and add `integrity="sha384-..."` attribute; also add `crossorigin="anonymous"`. Adds tamper-detection layer even for self-hosted assets.

#### All Other Vectors (carry-forward from 2026-03-07 check)
- A1-A13, A32-A35, A36, A38-A52: **✅ DEFENDED** or **✅ N/A** (unchanged from prior cycle)
- B14-B20, B29, B35-B43, B45-B57: B45 HIGH open (above); all others ✅/N/A
- C21-C30: ✅ ALL DEFENDED
- D26: LOW (new, above); D27-D35: ✅; D36: ✅

### Today's Verdict
- **New vectors added**: 0 (matrix: 79 vectors unchanged)
- **New incidents found**: 0 (no exploits March 11–12)
- **New findings**: 1 LOW (D26 self-hosted vendor script SRI gap)
- **Carry-forward open items**: B45 HIGH (7 days open), A43 MEDIUM, B44 MEDIUM, D33 LOW
- **No CRITICAL/HIGH new findings** — no immediate Discord alert required

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

---

## 2026-03-26 — Daily Security Sweep

**Evolution cycle**: BLACK TEAM 03:00 KST | Operator: Miss Kim
**Matrix state before**: 90 vectors (META-01~21) | **After**: 93 vectors (META-01~22)

### New Patterns Added Today

| Vector | Incident / Source | Date |
|--------|-------------------|------|
| **A74 full — Rust tar-rs CI/CD Build Pipeline Symlink Traversal + PAX Size Injection** | RUSTSEC-2026-0067 (CVE-2026-33056) + RUSTSEC-2026-0068 (RustSec, 2026-03-23) | 2026-03-23 |
| **A75 full — Audit-Evading Economic Exploit Design (Meta-Technique)** | Solana Security Toolbox 2026, dev.to (2026-03-17) + pattern synthesis | 2026-03-17 |
| **A72 reinforcement — AWS KMS Cloud Infrastructure Angle** | Chainalysis Resolv Labs post-mortem (2026-03-25) | 2026-03-25 |
| **META-22 — Cloud KMS Trust Boundary Collapse** | Synthesis from Chainalysis Resolv analysis | 2026-03-25 |

### Full Vector Sweep Results (Today's New Vectors)

**A74 — tar-rs CI/CD Symlink Traversal (RUSTSEC-2026-0067/0068)**
- Checked all Microstable `Cargo.toml` files for `tar` crate dependency → **no `tar` crate found**
- Microstable keeper deployment does not use Rust tar-based artifact extraction
- **Verdict: ✅ N/A — structural prevention (no tar crate dependency)**

**A75 — Audit-Evading Economic Exploit via Manual Oracle Deviation**
- Checked `update_oracle()` in `lib.rs`: accepts any `price` in range `[PRICE_MIN=$0.50, PRICE_MAX=$1.50]`
- Requires 2-of-3 keeper quorum AND MANUAL_ORACLE_MODE active (120-slot time-box)
- No on-chain check that `|new_price - last_pyth_price|` stays within tight deviation band
- Attack path: 2-of-3 keeper compromise → enable MANUAL_ORACLE_MODE → write $0.50 USDC oracle → attacker mints MSTB at 2× rate → oracle restored → redeem MSTB for double collateral
- Damage bound: per-slot cap (6%), per-TX cap (2%), 120-slot window = max ~72M MSTB from $10M TVL if all caps maximally exploited — significant but bounded
- **Verdict: ⚠️ MEDIUM — Existing caps limit blast radius. Gap: no per-write Pyth-deviation check**
- **Blue-team directive**: add `const MAX_MANUAL_ORACLE_DRIFT_BPS: u64 = 500; // 5%` and `require!(price.abs_diff(last_known_pyth_price) <= MAX_MANUAL_ORACLE_DRIFT_BPS * last_known_pyth_price / 10_000)` in `update_oracle()` to cap manual price deviation relative to last Pyth observation.

**A72 + META-22 — Cloud KMS Trust Boundary / Resolv Pattern**
- Re-verified Microstable: `mint()` is USER-signed (not keeper), per-slot/TX caps enforced on-chain
- Even 2-of-3 keeper cloud compromise ≡ worst-case keeper compromise → NO uncapped minting possible
- **Verdict: ✅ DEFENDED — architectural difference from Resolv (user-signed mint + on-chain caps)**

**Dashboard D26 (frontend security)**
- CSP: `script-src 'self'` confirmed in `<meta>` CSP tag → no external scripts
- Local vendor scripts: `./vendor/solana-web3-1.95.3.iife.min.js` — SRI hash not present
- **Sub-finding: ⚠️ LOW — vendored script has no SRI integrity check**
- **Blue-team directive**: add `integrity="sha384-..."` attribute to `<script src="./vendor/...">` tags

### All Carry-Forward Items (unchanged from prior sweeps)

| Severity | Finding | Open Since |
|----------|---------|-----------|
| ❌ HIGH | B45 Post-Audit Deployment Delta (3,281 lines unattested vs audited commit `f327e7c6`) | 2026-03-05 |
| ⚠️ MEDIUM | A43 Commit/Reveal Threshold Circumvention (no epoch-level cumulative turnover accumulator) | 2026-03-10 |
| ⚠️ MEDIUM | B44 SPL Delegate Drain Conduit (no `delegate.is_none()` check in `mint()`) | 2026-03-10 |
| ⚠️ MEDIUM | A75 Manual Oracle Drift (no per-write Pyth-deviation cap in `update_oracle()`) | **NEW 2026-03-26** |
| ⚠️ LOW | B53 Dashboard residual (wallet address clipboard rendering unconfirmed in app.js) | 2026-03-08 |
| ⚠️ LOW | D26 vendored script SRI missing | **NEW 2026-03-26** |

### Today's Verdict
- New incidents collected: **1** (Resolv Labs Chainalysis cloud-KMS detail, 2026-03-25)
- New attack vectors fully documented: **2** (A74, A75 — previously table-only, now full sections)
- A72 reinforced with Chainalysis cloud-KMS infrastructure angle
- META-22 added (Cloud KMS Trust Boundary Collapse synthesis)
- Findings: **0 CRITICAL / 0 HIGH new** / **1 MEDIUM new (A75)** / **1 LOW new (D26 SRI)**
- Matrix: **93 vectors** (A74, A75 full + A72 reinforcement + META-22)
