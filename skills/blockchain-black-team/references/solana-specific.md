# Solana-Specific Attack Patterns

## Account Model Vulnerabilities

### Missing Owner Check
Solana accounts have an `owner` field (the program that controls them). If a program reads data from an account without verifying the owner, an attacker can pass a fake account owned by their own program with crafted data.

```rust
// VULNERABLE
let data = account.try_borrow_data()?;
let amount = u64::from_le_bytes(data[0..8]);

// SAFE (Anchor handles this via Account<> type)
#[account(owner = expected_program)]
pub data_account: Account<'info, MyData>,
```

### Missing Discriminator Check
Anchor uses an 8-byte discriminator (SHA256 hash of account type name) to prevent account type confusion. Raw Solana programs or non-Anchor accounts may lack this.

### Writable Account Not Required
If an instruction modifies an account but doesn't require `mut`, the runtime won't persist changes — but the instruction may still execute logic based on stale reads.

## CPI (Cross-Program Invocation) Patterns

### Unchecked CPI Target
```rust
// VULNERABLE: attacker can substitute any program
invoke(&instruction, &[account1, account2])?;

// SAFE: verify program ID
require!(token_program.key() == spl_token::ID);
```

### Signer Privilege Escalation
CPI can propagate signer status. If a PDA signs via `invoke_signed`, ensure seeds are not predictable or reusable by attacker.

### Arbitrary CPI with User-Provided Program
Never allow users to specify which program to CPI into for sensitive operations.

## PDA (Program Derived Address) Patterns

### Seed Grinding
PDA derivation uses `find_program_address` which searches for a valid bump. If seeds are predictable, attacker may find collisions.

### Missing Bump Verification
```rust
// VULNERABLE: attacker can provide wrong bump
pub fn init(ctx: Context<Init>, bump: u8) -> Result<()> {
    // uses attacker-provided bump

// SAFE: use canonical bump
#[account(seeds = [b"vault", user.key().as_ref()], bump)]
pub vault: Account<'info, Vault>,
```

### Cross-Seed Collision
If two different account types use overlapping seed patterns, they may derive to the same PDA.

```rust
// Type A: seeds = ["data", user_pubkey]
// Type B: seeds = ["data", user_pubkey]  ← COLLISION
// Fix: seeds = ["data_a", user_pubkey] / ["data_b", user_pubkey]
```

## Token Program Patterns

### SPL Token vs Token-2022
- SPL Token (classic): No transfer hooks, predictable behavior
- Token-2022: Transfer hooks enable callbacks during transfers → reentrancy surface
- Always verify which token program is being used

### Mint Authority Check
```rust
// Ensure only protocol can mint
require!(mint.mint_authority == Some(protocol_pda));
```

### Close Authority Drain
When closing a token account, remaining tokens + lamports go to destination. Verify destination is correct.

## Rent & Lamport Accounting

### Rent-Exempt Minimum
Accounts below rent-exempt minimum get garbage collected. Attacker can drain lamports to just below threshold.

### Account Close Lamport Drain
```rust
// When closing: all lamports go to `close` destination
#[account(mut, close = receiver)]
pub account_to_close: Account<'info, MyData>,
// Ensure `receiver` is the intended recipient
```

## Timing & Ordering

### Slot-Based vs Real-Time
Solana uses slots (~400ms) not wall-clock time. `Clock::get()?.unix_timestamp` is approximate and can be manipulated by validators within bounds.

### Transaction Ordering
Validators can reorder transactions within a block. MEV is possible on Solana via Jito and similar infrastructure.

## Oracle Composition & Unit Safety

### Ratio Feed Misuse (Unit Normalization Bug)
When protocols compose feeds (e.g., token/base ratio + base/USD), missing one leg can convert a ratio into a false USD price.

```rust
// VULNERABLE: ratio treated as final USD price
let cbeth_eth = ratio_feed.price;
let usd_price = cbeth_eth; // missing ETH/USD multiplier

// SAFE: explicit composition + sanity guard
let eth_usd = base_usd_feed.price;
let usd_price = cbeth_eth
    .checked_mul(eth_usd)
    .ok_or(ErrorCode::MathOverflow)?
    / SCALE;
require!(usd_price >= MIN_PRICE && usd_price <= MAX_PRICE, ErrorCode::InvalidPrice);
```

### Timelock Recovery Gap
If oracle config changes require long governance delay, attacker can exploit the gap before rollback.

Mitigation:
- Emergency oracle pause path (separate authority with strict scope)
- Fast rollback for feed misconfiguration
- Deployment-time invariant checks (unit tests + on-chain sanity range)

## New 2026 Patterns (Anchor/SPL/Jito Surface)

### Anchor IDL External-Account Overtrust
Anchor patched IDL generation to exclude externally owned account types from internal account definitions (`idl: Exclude external accounts`, 2026-02-22).

**Risk pattern**:
- Client/wallet tooling treats generated IDL as a trust source.
- External accounts appear “first-party safe” in automation or signing UX.
- Integrator skips owner/program checks because metadata looked authoritative.

**Mitigation**:
- Keep runtime owner checks in on-chain code as source of truth.
- In off-chain clients, validate `account.owner` and expected program IDs before signing.
- Treat IDL/schema as descriptive, never as an authorization boundary.


### Anchor IDL Program-ID Drift (PMP Refactor Surface)
Anchor `Refactor IDL PMP commands` (2026-02-27) introduced `--allow-localnet` and optional `--program-id` for IDL init/upgrade flows.

**Risk pattern**:
- CI/ops scripts that previously depended on implicit workspace/program resolution can now execute IDL writes against the wrong cluster/program when flags are omitted or environment variables drift.
- If a privileged deploy key runs the command with a wrong `program-id`, the wrong IDL metadata account may be initialized/upgraded.
- Off-chain clients that auto-consume IDL metadata can then trust a mismatched schema, creating a metadata-confusion foothold (D31 bypass variant).

**Mitigation**:
1. In production, pin both cluster and `program-id` explicitly in scripts (never rely on defaults)
2. Block `--allow-localnet` in release pipelines
3. Preflight check: fetch on-chain program metadata and assert expected authority + program id before `idl upgrade`
4. Postflight check: compare deployed IDL hash against expected artifact hash

**Sources**:
- https://github.com/solana-foundation/anchor/commit/21e67c99471134fe565c5dc6f3e23d7ee481a66a
- https://github.com/solana-foundation/anchor/commits/master.atom

### Slot-Flow Quota Capture (Redemption Griefing)
Protocols with global per-slot caps can be DoSed by one actor who consumes most of the quota early each slot.

**Attack shape**:
1. Attacker prepares redeemable balance.
2. Sends burst redeems at slot boundary.
3. Honest user redeems revert with slot-limit errors despite healthy collateral.

**Mitigation**:
- Per-actor fair-share limits (or stake-weighted quotas).
- Priority lanes for small/organic redeems.
- Burst scoring + grief penalties.

### Redeem Path Validation Bypass (Stake Nova Pattern)
Stake Nova (2026-02-27, Solana) was drained (~$2.39M) after an unchecked validation path in `RedeemNovaSol()` was combined with flash-loan liquidity.

**Solana-specific risk**:
- Redeem code may appear safe under normal flow but fail when atomic liquidity is amplified in one slot.
- If redeem output/account constraints are incomplete, attacker can drain vaults before invariant checks catch up.

**Mitigation**:
- Enforce strict `min_out` and account-binding checks at instruction boundary.
- Apply per-TX + per-slot redeem caps even for keeper-assisted flows.
- Require invariant assertions before and after transfer CPI (`supply`, `vault balances`, `user position`).

**Source**: https://hacked.slowmist.io/

### Typosquat Waves Targeting Solana Rust Tooling
Recent RustSec advisories (`rpc-check`, `tracing-check`) show short-lived malicious crates aimed at credential theft in a specific ecosystem.

**Mitigation**:
- Cargo.lock hash attestation in CI/runtime.
- Registry-source allowlist (crates.io only unless explicitly approved).
- Two-person review for dependency additions/renames near common crate names.

### Transitive Payload Relay (tracings → tracing_checks, 2026-02-26)
New RustSec advisories (`RUSTSEC-2026-0027`, `RUSTSEC-2026-0028`) show a second-stage pattern: the top-level crate looks lightweight while malware is hidden in a transitive dependency.

**Solana/Anchor impact pattern**:
- Keeper teams often add telemetry crates (`tracing*`) during incident response.
- Direct dependency review can miss transitive payload crates that execute build/runtime hooks.
- Cargo.lock attestation protects against *unexpected* lock changes, but if a malicious dependency is deliberately merged and attested, runtime checks will still pass.

**Mitigation upgrade**:
- CI must diff full transitive graph (`cargo tree --locked`) for every dependency change.
- Quarantine newly published crates (<7 days) unless emergency security override is approved.
- Add crate-name distance checks (e.g., `tracing` vs `tracings`) before merge.
- Require two-person security sign-off specifically on Cargo.lock hash updates.

**Sources**:
- https://rustsec.org/advisories/RUSTSEC-2026-0027.html
- https://rustsec.org/advisories/RUSTSEC-2026-0028.html

### Solana SDK Supply Chain Takeover (NPM Trusted Tooling)
GHSA-8f57-hh49-gmqf (2026-03-26) reported malicious behavior in `@solana-ipfs/sdk` (`>=0` vulnerable, first patched version: none): any computer using it should be considered fully compromised; all local secrets should rotate from a clean machine. This is a high-risk **off-protocol**, yet protocol-relevant risk because Solana JS tooling and infra scripts are part of the signing/operations trust boundary.

**Solana-specific risk**:
- A single compromised SDK in local/off-chain tooling can leak KMS/env credentials, RPC private keys, wallet seed material, or keeper operator tokens before a tx reaches chain.
- Impact is often non-deterministic: uninstalling package rarely fully restores trust because prior process execution may have dropped persistent payloads.
- Even if protocol code is clean, operational compromise can authorize privileged keeper actions, oracle feed tampering, or signing abuse.

**Mitigation**:
- Freeze/add to denylist any dependency with advisory `ghsa_id` from GitHub Advisory DB unless explicit exception signed by security owner.
- Keep tooling dependency allowlist with 2-person change gate + 7-day quarantine for newly published versions.
- Use separate ephemeral CI/runner host for any Solana JS tooling that touches signing material; rotate and attest credentials after package alerts.
- Add CI policy that blocks dependency install if `npm` package has security advisory severity ≥ HIGH and no patched version unless exception.

**Source**: https://api.github.com/advisories/GHSA-8f57-hh49-gmqf

### ZK Verifier Key Binding Drift (FOOMCASH Pattern)
FOOMCASH (2026-02-26, ~$2.26M) was exploited after verification-key configuration drift enabled forged/invalid zkSNARK proof acceptance.

**Solana-specific risk**:
- Programs integrating zk verifiers (Groth16/Plonk wrappers or proof-verification CPI) may trust mutable verifier account/config without strict hash binding.
- If verifier key, circuit ID, or public-input schema changes without hard invariants, proof checks can pass for the wrong statement.

**Pattern to detect in codebase**:
```rust
// RISKY: verifier account accepted from mutable config with weak governance
let verifier = load_verifier_account(ctx.accounts.verifier_config)?;
require!(verify_proof(proof, public_inputs, verifier), ErrorCode::InvalidProof);

// SAFER: pin expected verifier key hash / circuit id and assert on every call
require!(verifier.key_hash == EXPECTED_VK_HASH, ErrorCode::VerifierMismatch);
require!(public_inputs.version == EXPECTED_CIRCUIT_VERSION, ErrorCode::CircuitVersionMismatch);
```

**Mitigation**:
1. Immutable verifier-key hash (or two-step timelocked update with quorum)
2. Circuit ID + public-input schema version checks (domain separation)
3. Upgrade pipeline canary proofs (expected-pass + expected-fail)
4. Emergency pause if verifier-integrity check fails

**Sources**:
- https://hacked.slowmist.io/
- https://www.cryptotimes.io/2026/02/26/foomcash-loses-2-26m-in-copycat-zksnark-exploit/

## Hot Key & Stake Authority Patterns (2026 Addition)

### Social-Engineering-to-Stake-Authority-Hijack
Step Finance (2026-01-31, $27.3M): Executive device phished → stake delegation authority transferred to attacker wallet → 261,854 SOL unstaked in 90 minutes. Audited contracts, bug bounties, and security reviews were irrelevant.

**Solana-specific risk**: Stake delegation model separates `StakeAuthority` and `WithdrawAuthority`. Both can be re-assigned unilaterally by the current controller via a single signed instruction. No program code involved. Indistinguishable from legitimate on-chain operations.

**Keeper relevance**: Keeper hot keys on operator's machine have the same exposure. If keeper host is compromised:
- Attacker signs privileged keeper instructions (oracle updates, rebalance)
- Steals treasury-authority keypair → drains treasury
- If MANUAL_ORACLE_MODE path is accessible via keeper key, attacker gains price manipulation surface

**Pattern to detect in codebase**:
```rust
// Check: is the keeper keypair also the stake withdrawal authority?
// If yes → compromise of keeper host = loss of staked collateral
// SAFE: separate keypairs for keeper ops vs treasury/stake authority
```

**Defense**:
1. Hardware keys for any keypair controlling SOL stake or treasury withdrawal
2. Stake accounts split into small sub-accounts (cap loss per account)
3. `StakeAuthorize` changes require M-of-N signatures (multisig delegate)
4. Keeper keypair scope-limited: can only submit to program, cannot re-assign authority
5. EDR on all operator machines; phishing simulation training

## Solana-Specific Defense Checklist

1. ☐ All accounts have owner checks (Anchor `Account<>` type)
2. ☐ All PDAs use canonical bump (`bump` in Anchor constraints)
3. ☐ No seed collisions between different account types
4. ☐ CPI targets verified (`Program<'info, Token>`)
5. ☐ Signer checks on all privileged operations
6. ☐ Token program ID pinned (not user-provided)
7. ☐ Mint/freeze authority verified
8. ☐ Account close destinations verified
9. ☐ Checked arithmetic (no unchecked in release builds)
10. ☐ Oracle staleness + confidence + status validated
11. ☐ No sensitive data in logs or error messages
12. ☐ Upgrade authority secured (multisig or frozen)
13. ☐ Oracle feed composition enforces unit normalization + price sanity range
14. ☐ Keeper keypair is NOT the stake/treasury withdrawal authority (principle of least privilege)
15. ☐ Stake accounts split into sub-accounts (no single monolithic stake)
16. ☐ Dependency audit: `bytes`, `libcrux-psq`, `libcrux-ecdh` pinned to patched versions in Cargo.lock
17. ☐ Audit scope exclusions tracked as open backlog items (never ship with known-excluded vectors)
18. ☐ Transitive dependency review enforced (`cargo tree --locked`) + newly published crate quarantine window for keeper builds
19. ☐ ZK verifier integrations pin verification-key hash/circuit version and enforce canary-proof checks on upgrades

## Third-Party Staking Provider Authority Risk (Cross-Customer Blast Radius)

### Provider-API-to-Multi-Platform Authority Hijack (SwissBorg/Kiln, Sep 2025)
Staking providers (Kiln, Figment, Blockdaemon etc.) that hold `StakeAuthority`+`WithdrawAuthority` on behalf of multiple DeFi clients create a **cross-customer blast radius**. Compromise of the provider's central API → all clients' stake accounts simultaneously exposed.

**Solana on-chain mechanics**: `StakeAuthorize` instruction requires only current-authority signature. No program code. Indistinguishable from legitimate ops on-chain.

**Attack timeline**: Authority transfer (instant) → stake deactivation → 1 epoch cooldown (~2–2.5 days) → withdrawal.

**Microstable-specific risk**: LOW for core protocol (no third-party staking custodian). ELEVATED if LST collateral is added whose backing depends on a centralized provider API.

**Red-team application**:
- When evaluating new LST collateral: enumerate whose API holds stake/withdraw authority for that LST's backing validators.
- If a third-party custodian holds multi-customer authority: model a cascade attack on that custodian to assess collateral safety.

**Mitigation**:
1. Require LST collateral integration docs to detail staking authority model.
2. Prefer LSTs backed by validator networks using distributed or hardware-secured authority.
3. Apply additional haircut to LST collateral with known-centralized custodian authority.
4. Track known providers and their authority architecture in a curated registry.

**Sources**: SwissBorg/Kiln (Sep 2025, $41.5M); infstones.com (Feb 2026)

## Solana-Specific Defense Checklist Update
20. ☐ LST collateral staking authority model audited (no single-custodian blast radius)
21. ☐ crates.io ecosystem namespace provenance check before adding new DeFi SDK dependencies (CI + manual review)

## Anchor Post-CPI Stale Account Cache (A42)

### Mechanism
Anchor `Account<'info, T>` deserializes PDA data once at instruction entry. If a subsequent CPI modifies that PDA on-chain (e.g., via Token-2022 transfer hook), the in-memory Rust struct remains stale. Reads from the struct post-CPI yield pre-CPI values.

```rust
// VULNERABLE: no reload after CPI that may modify vault
let price = ctx.accounts.vault.price;           // cached at entry
token_2022::transfer_checked(cpi_ctx, amount)?; // hook may write vault.price
let minted = collateral * price / SCALE;        // uses stale pre-hook price!

// SAFE: reload after CPI
token_2022::transfer_checked(cpi_ctx, amount)?;
ctx.accounts.vault.reload()?;                   // re-fetch from on-chain bytes
let price = ctx.accounts.vault.price;
```

**Trigger condition**: Any CPI (transfer, callback, hook) that writes to an account that the outer program also reads.

**Microstable risk**: LOW currently (SPL Token classic — no hooks). HIGH if any collateral migrates to Token-2022 with transfer hooks.

**Source**: https://blog.asymmetric.re/invocation-security-navigating-vulnerabilities-in-solana-cpis/

## ACE Fairness / Keeper Oracle-Freshness Ordering (B40)

### Mechanism
Solana's Alpenglow/ACE execution model reduces priority-fee-based ordering advantage. Keeper oracle-update TXs no longer predictably precede user mint/redeem TXs under congestion. Protocols that rely on keeper ordering guarantees face increased staleness windows.

**Microstable defense**: `MINT_ORACLE_STALENESS_MAX = 20 slots` is the guard. Under ACE congestion, keeper cycle may exceed 20 slots → OracleDegraded → liveness degradation (not value extraction).

**Mitigation**: Redundant keeper on second node; pre-benchmark keeper latency under ACE congestion scenarios.

**Source**: Blockdaemon Solana 2026 Technical Roadmap (2026-02-19)

## Commit/Reveal Threshold Segmentation Bypass (A43)

### Mechanism
Protocols with `if turnover >= threshold { require_commit_reveal() }` can be bypassed by splitting one large operation into multiple sub-threshold calls. Cumulative effect equals the large operation; commit/reveal delay is never triggered.

```rust
// Per-call check only (BYPASSABLE via segmentation):
if turnover >= LARGE_THRESHOLD { verify_commit_reveal()?; }

// Fix: add cumulative epoch tracking
if turnover >= LARGE_THRESHOLD
    || epoch_drift + turnover >= LARGE_THRESHOLD {
    verify_commit_reveal()?;
}
```

**Microstable specifics**: WEIGHT_STEP_LIMIT=2%, LARGE_THRESHOLD=4%, BATCH_WINDOW_SLOTS=32. 5 calls × 32 slots = 160 slots to zero any collateral weight.

**Requires**: 2-of-3 keeper compromise. Eliminates commit/reveal MEV-protection once keepers are compromised.

## Solana-Specific Defense Checklist Update
22. ☐ Post-CPI `.reload()` called on any PDA that a CPI hook may have modified (mandatory for Token-2022 integration)
23. ☐ ACE/Alpenglow ordering impact assessed for keeper oracle-freshness model; redundant keeper runner in place
24. ☐ Commit/reveal threshold checks include cumulative epoch drift (not per-call only)

### Utility-Impersonating Env-Stealer Crate (A44, RUSTSEC-2026-0030)
Fresh-named malicious crate (not a typosquat) added as a direct dependency that silently exfiltrates `.env` files via HTTP POST at build or init time. Distinct from Typosquat Waves and Transitive Payload Relay (D33).

**Microstable keeper specific attack path**:
1. Keeper's `Cargo.toml` gains a new crate added via social engineering or compromised PR.
2. `cargo build` runs on MiniPC (`/home/spritz/microstable-keeper/`); crate reads `.env` at same path.
3. `DEFAULT_KEEPER_ENV_PATH = "/home/spritz/microstable-keeper/.env"` — signing key exfiltrated.
4. Attacker issues malicious oracle/rebalance/circuit-breaker transactions with the leaked keypair.

**Defense (Solana keeper specific)**:
- Strict crate allowlist in `cargo deny` (`[bans]` section); reject any unlisted crate.
- `cargo audit --deny` in CI + `cargo deny check bans` pre-build gate.
- Run `cargo build` in a sandboxed environment with NO access to the production `.env` path (Docker/nsjail with `/home/spritz/microstable-keeper/.env` not bind-mounted).
- Move signing key out of `.env` into a hardware signer or remote KMS; no plaintext key at build path.
- Enforce mandatory >7-day quarantine window before any new crate is permitted in the production build.

**Sources**:
- RUSTSEC-2026-0030: https://rustsec.org/advisories/RUSTSEC-2026-0030.html

### Campaign-Clone Env-Stealer Rotation (A45, RustSec 0031/0032)
After `time_calibrator` takedown, near-clone crates (`time_calibrators`, `dnp3times`) appeared within hours with the same `.env` exfiltration objective and fake `timeapi.io`-style endpoint theme.

**Solana keeper-specific risk**:
- Incident response often adds/changes utility crates quickly under uptime pressure.
- Name-level denylisting (`block time_calibrator`) is too narrow; next clone passes unless policy is campaign-wide.
- Cargo.lock attestation remains green if the malicious clone is intentionally merged and hash is re-attested.

**Mitigation upgrade**:
1. Security quarantine: reject newly published crates (<7 days) for keeper builds unless emergency waiver + dual review.
2. Campaign-level deny rule: when one malicious crate is confirmed, block semantic siblings (`time*`, `slot*`, `rpc*`) until manual clearance.
3. CI static scan for outbound HTTP/file-read in `build.rs` and global initializers of new crates.
4. Maintainer trust gate: require minimum maintainer age/history for newly added dependencies.

**Sources**:
- https://rustsec.org/advisories/RUSTSEC-2026-0031.html
- https://rustsec.org/advisories/RUSTSEC-2026-0032.html

### Solana Leader-Isolation / Stopping Liveness Attack (B47)
New comparative research (`arXiv:2603.02661`) identifies Solana as vulnerable to leader-isolation and stopping attacks under adversarial communication conditions.

**Solana-specific risk to protocol operators**:
- Deterministic leader schedule enables targeted pre-slot disruption of expected leaders.
- Even with honest keepers/oracles, slot progression/finality lag can push protocol freshness gates into repeated fail-closed mode.
- Availability degradation can cascade into rebalance delay, watchdog churn, and user-facing mint/redeem rejection spikes.

**Mitigation**:
1. Add leader-isolation chaos drills to ops runbook (targeted packet loss around known leader windows).
2. Track chain-liveness SLOs (`finalized slot lag`, `slot production continuity`) separately from RPC endpoint health checks.
3. Define explicit degraded-mode behavior (safe pause + operator escalation) when liveness SLO breaches persist.
4. Keep geographically/network-diverse keeper runners to reduce correlated path disruption.

**Source**: https://arxiv.org/abs/2603.02661

## Solana-Specific Defense Checklist Update
25. ☐ Dependency policy handles campaign-level clone waves (semantic sibling block + new-crate quarantine)
26. ☐ Leader-isolation/stopping chaos tests executed and linked to oracle freshness SLO alarms

### RPC Proxy HTTP Request Smuggling (D35, RUSTSEC-2026-0033)
Cloudflare `pingora-core` <0.8.0 allows HTTP request smuggling via premature Upgrade handling. CVSS 9.3 CRITICAL.

**Solana keeper-specific risk**:
- Microstable keeper does NOT directly depend on pingora-core (confirmed via Cargo.lock scan).
- However, if any RPC endpoint, oracle feed relay, or internal API used by the keeper is fronted by a Cloudflare/Pingora proxy (as documented in TOOLS.md: GCP VM 34.19.69.41 + Cloudflare), an unpatched proxy instance exposes internal services to request smuggling that bypasses WAF and IP allowlist controls.
- JSON-RPC over HTTPS has no valid use case for the `Upgrade` header — any Upgrade-bearing request to an RPC proxy should be considered anomalous and rejected.

**Mitigation**:
1. Patch all `pingora-core` deployments to >=0.8.0 (CVE-2026-2833).
2. Configure proxy/WAF to strip `Upgrade` and `Connection` headers for all RPC-bound routes.
3. Verify Cloudflare CDN edge is on patched Pingora for all keeper/oracle traffic paths.
4. Add chain-infra monitoring rule: alert on `Upgrade` headers observed in RPC request logs.
5. Migrate critical keeper↔RPC connections to HTTP/2 where possible.

**Defense Checklist Item**:
27. ☐ All proxy layers in RPC/oracle traffic path use pingora-core ≥0.8.0 or HTTP/2 (CVE-2026-2833 defense)

**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0033 | https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-2833

### ZK Trusted Setup Misconfiguration Future Watch (A49)
Microstable is currently Solana-native with no ZK components. However, if ZK proof integration is ever planned (private transactions, ZK oracle attestation, ZK governance proofs):

**Solana-specific ZK risks**:
- Solana's `zk-token` (SPL Token Confidential Transfers) uses BulletProofs, not Groth16 — different trusted setup model, but same class of ceremony verification requirement.
- Any custom Groth16 verifier implemented as a Solana program (on-chain verification) must have its verifying key cross-checked against the ceremony transcript.
- Program-level verifying key storage (as PDA data or hardcoded constants) can be inspected on-chain — publish and verify before deployment.

**Defense Checklist Item**:
28. ☐ If any ZK proof verifier is introduced: third-party ceremony verification (gamma2 ≠ delta2, correct circuit hash, Powers of Tau transcript) completed BEFORE deployment

**Source**: https://rekt.news/the-unfinished-proof | https://blog.zksecurity.xyz/posts/groth16-setup-exploit/

## Token-2022 Hook Security Patterns (2026 Addition)

### A51. ExtraAccountMetaList Account Injection (Transfer Hook Context Confusion)
**Signal**: Zealynx Security Blog "Solana Smart Contract Audit Guide 2026" (2026-03)

Token-2022 transfer hooks receive additional accounts via `ExtraAccountMetaList`. If the hook program doesn't validate that these accounts match expected PDA seeds, an attacker can inject a malicious account (e.g., spoofed whitelist) to bypass transfer logic.

**Code pattern to find**:
```rust
// VULNERABLE: ExtraAccountMetaList account accepted without seed verification
fn execute_hook(ctx: Context<HookCtx>) -> Result<()> {
    require!(ctx.accounts.whitelist.allowed, ErrorCode::Blocked);  // attacker-supplied → always true
}

// SAFE: derive and verify PDA address before trusting account data
fn execute_hook(ctx: Context<HookCtx>) -> Result<()> {
    let (expected, _) = Pubkey::find_program_address(
        &[b"whitelist", ctx.accounts.mint.key().as_ref()],
        ctx.program_id,
    );
    require_keys_eq!(ctx.accounts.whitelist.key(), expected, ErrorCode::InvalidAccount);
    require!(ctx.accounts.whitelist.allowed, ErrorCode::Blocked);
}
```

**Microstable risk**: LOW (SPL Token classic, no hooks). HIGH if Token-2022 migration.

**Secondary: Confidential Transfer Auditor Key**: If `auditor_elgamal_pubkey` ≠ `[0u8; 32]`, auditor can decrypt all confidential balances — compliance backdoor. Explicitly disable unless required.

**Mitigation**:
1. Anchor `seeds` + `bump` constraints on ALL hook context accounts (no exceptions)
2. Explicitly set `auditor_elgamal_pubkey = None` in Confidential Transfer config
3. Include hook account seed validation in Token-2022 audit checklist

### A52. Transfer Hook Infinite Recursion Griefing (Asset Freeze DoS)
**Signal**: Zealynx Security Blog "Solana Smart Contract Audit Guide 2026" (2026-03)

If a transfer hook triggers a CPI that transfers the *same mint*, the runtime invokes the hook again — recursive chain. Runtime halts with compute budget exceeded → every transfer of that mint reverts → asset freeze DoS.

**Microstable risk**: LOW currently. HIGH risk if Token-2022 mints are used.

**Attack surface**: Protocols that accept user-supplied Token-2022 collateral with user-controlled hooks.

**Mitigation**:
1. **Acyclicity invariant**: hook must never initiate a transfer of the same mint (prove mathematically, not just code-review)
2. Freeze hook upgrade authority post-deployment
3. Reject collateral mints with mutable hook authority or unverified hook acyclicity

## Firedancer Finality Patterns (2026 Addition)

### B50. Skip-Vote Structural Finality Lag
**Signal**: Zealynx Security Blog "Solana Smart Contract Audit Guide 2026" (2026-03); Solana SIMD-0370

Under Firedancer dynamic block sizing, validators running Agave or older hardware may skip voting on oversized blocks → structural finality delay. During the lag window, transactions may appear "on-chain" but not finalized — creating a micro-reorg risk window for finality-dependent operations.

**Distinct from B40**: B40 is about TX ordering (ACE fairness). B50 is about finality *timing* from heterogeneous validator hardware.
**Distinct from B47**: B47 requires an adversary targeting leaders. B50 is structural (no adversary needed).

**Microstable-specific risk**:
- Slot-based staleness guards (`STALE_ORACLE_PENALTY_PER_SLOT`, `Clock::get()?.slot`) are NOT directly affected (slots advance continuously)
- `Confirmed` commitment (keeper default) has a skip-vote micro-reorg window
- If bridge/large-withdrawal instructions using `Finalized` are added, they face unexpected latency

**Pattern to detect**:
```rust
// RISKY: hard-coded 400ms finality assumption
let deadline = current_slot + 1;  // assumes 400ms = finalized → no longer holds under Firedancer

// SAFER: use slot range with skip-vote buffer
let deadline = current_slot + 3;  // +2–3 slot buffer for heterogeneous validator lag
// AND: require Finalized commitment for irrevocable operations
```

**Mitigation**:
1. Use `Finalized` commitment for all irrevocable/large-value keeper operations
2. Add +2–3 slot slack to any deadline calculation assuming 400ms finality
3. Monitor `confirmed → finalized` slot delta in keeper telemetry; alert if > 3 slots

## Solana-Specific Defense Checklist Update
29. ☐ Token-2022 hooks: all ExtraAccountMetaList accounts verified via seed derivation (not caller-supplied)
30. ☐ Token-2022 hooks: acyclicity proven (no same-mint CPI transfer within hook); hook upgrade authority frozen
31. ☐ Firedancer skip-vote buffer: irrevocable operations use `Finalized` commitment; deadline calculations include +2–3 slot slack

---

## Firedancer Write-Lock LDoS — Single Global PDA Starvation (B64, 2026-03-16)

**Signal**: DreamWork Security (dev.to, 2026-03-13). New attack class specific to Firedancer era throughput.

**Pattern**: Protocols with a single monolithic global state PDA required for all writes are vulnerable to targeted write-lock flooding. An attacker submits high-priority-fee minimal-compute TXs write-locking the PDA. Firedancer's higher block density means more competing lock TXs per slot. Legitimate operations (oracle updates, liquidations) are starved.

```rust
// VULNERABLE ARCHITECTURE: single PDA for all writes
pub protocol_state: Account<'info, ProtocolState>,  // appears in every instruction context

// ATTACK: 10,000 TXs/slot each requesting write lock on protocol_state
// → oracle update keeper TX queued behind attacker flood
// → staleness accumulates → circuit breaker or hard halt
```

**Solana-specific checklist additions**:
32. ☐ Identify all global-state PDAs required as `writable` in critical paths (oracle update, liquidation)
33. ☐ For each global-state PDA: assess write-lock LDoS cost/impact ratio (if one account blocks all operations, HIGH risk)
34. ☐ Keeper priority fee strategy: dynamic fee escalation on write-lock contention (not fixed priority fee)
35. ☐ Graceful degradation: if oracle update blocked N consecutive slots, switch to TWAP-only mode (not hard halt)

---

## Firedancer Dense-Block Intra-Slot Oracle Staleness (B65, 2026-03-16)

**Signal**: DreamWork Security (dev.to, 2026-03-13). Extends oracle staleness analysis to intra-slot dense-block scenarios.

**Pattern**: Slot-number-based staleness checks pass when oracle was updated in the same slot as the attacker TX (`slots_since_oracle = 0`). In a Firedancer dense block, price may move significantly between oracle update and attacker TX within the same slot.

```rust
// CHECK THAT MAY BE INSUFFICIENT in dense Firedancer slots:
let slots_since_oracle = current_slot - oracle.last_update_slot;
require!(slots_since_oracle <= MAX, OracleStale);
// → passes even if oracle.publish_time is 200ms ago and price moved 1%

// IMPROVED: add publish_time check
let time_since_oracle = Clock::get()?.unix_timestamp - oracle.publish_time;
require!(time_since_oracle <= MAX_SECONDS, OracleStale);
```

**Solana-specific checklist additions**:
36. ☐ Oracle staleness: verify both `slot` check AND `publish_time` (Unix timestamp) check are in place
37. ☐ Dense-slot scenario: confirm Pyth confidence interval check rejects when confidence > threshold regardless of slot match
38. ☐ TWAP deviation guard covers intra-slot divergence (not only cross-slot TWAP smoothing)

---

## Glassworm C2 via Solana Accounts (D39, 2026-03-17)

**Pattern**: Attackers use Solana accounts as a censorship-resistant, anonymous command-and-control channel for supply-chain payloads. This makes Glassworm-class malware invisible to traditional network security tools.

**Why Solana is an ideal C2**:
- Accounts are permanent — no takedown mechanism
- Reads are free and unlimited — no detection via rate-limit triggers
- IP logs: Solana RPC endpoints do not log per-client request origin
- Security scanners that flag suspicious HTTP C2 domains are blind to `api.mainnet-beta.solana.com` (legitimate DeFi infrastructure)

**Detection**: Monitor for unusual Solana RPC calls (especially `getAccountInfo`) originating from developer workstation JS processes or CI environments that are NOT the keeper binary. Network-layer: alert on `getAccountInfo` calls to unknown pubkeys from non-keeper processes.

**Solana protocol implication**: Any future Microstable feature that reads arbitrary user-supplied pubkeys via `getAccountInfo` should treat the returned data as untrusted external input — never `eval()` or interpret as code.

## B50 Reinforcement — Cross-Chain Bridge Finality Lag Attack (2026-03-17)

**Operational detail added**: Firedancer skip-vote finality lag creates a concrete **bridge double-spend window**:
1. Attacker submits deposit transaction in a large Firedancer-produced block (causes Agave skip-votes)
2. Cross-chain bridge sees *block inclusion* → releases funds on destination chain
3. Firedancer block finality is delayed → in edge case, block may be skipped entirely
4. Attacker received destination-chain funds for a deposit that never finalized on Solana

**Key**: No adversarial leader needed (distinct from B47). Normal Firedancer operation under heterogeneous validator hardware is sufficient.

**Solana-specific mitigation for bridge/cross-chain integrations**:
- Require `Finalized` commitment (not `Confirmed`) before any fund release
- Add +2–3 slot buffer on all deadline calculations
- Monitor `confirmed→finalized` delta: alert if >5 slots

## D45 — Solana Blockchain-as-C2 Channel (2026-03-20)

**Operational specifics for Solana DeFi environments:**

The Windsurf IDE malware (Bitdefender, March 20, 2026) established a critical precedent: Solana's **public read API is weaponizable as a censorship-resistant C2 channel** because:
1. `getTransaction(sig)` is unauthenticated and free on mainnet
2. Transaction `memo` and instruction data fields can store arbitrary bytes
3. Encrypted payload fragments survive indefinitely (blockchain immutability)
4. Attacker deploys C2 payload once; any infected client retrieves it forever

**Solana-specific attack surface for keeper infrastructure:**
- Default keypair location `~/.config/solana/*.json` is world-readable by default on many Unix systems
- `solana config get` reveals keypair path; if process inspector runs on same machine, path is trivially found
- Keeper `config.toml` RPC keys (Helius, QuickNode, Triton) are stored in plaintext in typical deployments

**Detection heuristics for Solana C2:**
- Non-keeper processes (e.g., `node`, extension workers, `.vsix` processes) making bulk `getTransaction` calls to mainnet
- `getTransaction` calls targeting old/unknown transaction signatures (not recent keeper TXs)
- High-frequency `getTransaction` to signatures that are not in the keeper's own TX log

---
<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-22 -->

## Token-2022 Extension Attack Patterns (2026-03-22)

### ExtraAccountMeta Injection (A56)
Transfer hooks receive extra accounts via `ExtraAccountMetaList` PDA at `seeds = [b"extra-account-metas", mint_pubkey]`. Protocol or hook program must re-derive and verify these PDAs — never trust them without seed validation.

### Transfer Fee Invisible Tax (A58)
Token-2022 fee extension deducts fee at protocol level. Protocols crediting `amount` (sent) instead of `post_balance - pre_balance` (received) are undercollateralized by the fee rate on every deposit.

### Anchor v1.0.0 Shadow Migration (A57 — current Solana Anchor ecosystem)
Anchor v1.0.0-rc.5 released 2026-03-20. Programs on Anchor 0.31.x face silent discriminator mismatch if off-chain tools migrate to v1.x before on-chain program compatibility is verified. Pin keeper Cargo.lock and add CI version-parity gate.

## 2026-03-23 New Patterns

### CPI Signer Authority Forwarding (Extended — see A70)
The brief entry under "Signer Privilege Escalation" is reinforced with a full attack vector.
Key addition: **DeFi aggregators/routers** are the primary risk surface. When a protocol acts as a router between user and external DEX:
- If the external DEX program account is passed as `AccountInfo` (not `Program<T>`), an attacker can substitute a malicious program.
- The malicious program receives `is_signer = true` for the user's account.
- It can use this to drain any account the user has authority over.
**Safe pattern**: user transfers to protocol vault first (user signs → your program), then protocol CPIs to DEX using PDA only. User signing authority never crosses into external program.

### Solana ACE (Application-Controlled Execution) Bypass Surface
**Status**: Emerging (2026-03-19, Chainstack Solana MEV 2026 analysis).
Solana's evolving ACE (Application-Controlled Execution) system lets dApps define execution constraints: ordering, slippage bounds, actor whitelists. Jito BAM (Blockspace Auction Mechanism) is the complementary infrastructure.
**Risk pattern**:
1. If ACE constraints are enforced at the application layer only (not runtime-enforced), an attacker can submit transactions that bypass the application's constraint-checking path (e.g., calling the program directly rather than through the ACE-gated interface).
2. BAM priority fee griefing: if an attacker pays enough priority in Jito BAM, they can reorder transactions relative to ACE-gated operations, potentially front-running within a bundle.
3. ACE constraint specification bugs: if the constraint language allows ambiguous expressions, edge cases may evaluate to "unconstrained" — effectively disabling the protection.
**Mitigation**: ACE constraints should be enforced on-chain (program-level checks), not merely off-chain (interface-level checks). Never rely on ACE as the sole protection against reordering or sandwiching.
**Microstable relevance**: LOW — does not currently use ACE. Monitor if implementing Jito bundles for keeper.

<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-24 -->

## 2026-03-24 Patterns

### tar-rs Supply Chain CI/CD Attack (A74)
Keeper Rust build pipelines using tar-rs ≤ 0.4.44 are vulnerable to:
1. **RUSTSEC-2026-0067** (CVE-2026-33056): `unpack_in` follows symlinks via `fs::metadata()` → crafted tarball can chmod keeper key directories to 0777.
2. **RUSTSEC-2026-0068**: PAX size header silently ignored when header size nonzero → crafted entries bypass size-based validation.

**Mitigation**: Pin `tar = ">=0.4.45"` in keeper Cargo.toml; run `cargo audit` in CI.

### Audit-Evading Economic Exploit Architecture (A75)
Exploitation of the gap between "technically correct code" and "economically safe protocol":
- All individual instructions are technically correct; no audit finding can be raised
- Multi-transaction oracle manipulation + deposit + mint + price-restore + withdraw sequence crosses audit scope boundary
- Detection: for every oracle-price-dependent function, enumerate the profit path when price deviates N%
- For MANUAL_ORACLE_MODE protocols: on-chain TWAP sanity gate is mandatory (reject writes > ±2% from TWAP)

**Microstable-specific gap**: `write_oracle_price` in MANUAL_ORACLE_MODE has no TWAP deviation cap on-chain. Add `MAX_MANUAL_PRICE_DEVIATION = 200bps` constant + pre-write check.

<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-25 -->

## 2026-03-25 Patterns

### rustls-webpki CRL Bypass in Keeper TLS (A77)
**Confirmed Keeper Exposure**: Cargo.lock has `rustls-webpki = "0.103.9"` (new combined fix floor is `>=0.103.13`; `0.103.10` only addressed the March CRL bug, and `0.103.12` still predates `RUSTSEC-2026-0104`).

Attack scenario:
1. RPC provider (Helius/QuickNode/Triton) rotates TLS cert; old cert revoked via CRL with multiple distributionPoints
2. rustls-webpki 0.103.9 only checks first DP → subsequent DPs ignored → revocation status "unknown"
3. If keeper's rustls uses `UnknownStatusPolicy::Allow` → accepts revoked cert → MITM possible
4. 2026-04-15 reinforcement: the same 0.103.9 branch is also below the patch floor for `RUSTSEC-2026-0099`, where wildcard DNS names can be accepted under an invalid permitted-subtree constraint. (`RUSTSEC-2026-0098` exists too, but URI-name constraints are low-relevance for Microstable RPC hostname validation because rustls-webpki does not expose URI assertion APIs.)
5. 2026-04-25 reinforcement: `RUSTSEC-2026-0104` / `GHSA-82j2-j2ch-gfr8` adds a CRL-path availability failure mode. A syntactically valid empty BIT STRING in `onlySomeReasons` can panic inside `bit_string_flags()` before CRL signature verification. If a future custom verifier enables CRL checking, malformed CRLs can become keeper connectivity kill-switches even without successful MITM trust persistence.
6. Attacker intercepts keeper→RPC connection → injects malicious oracle price responses or suppresses circuit breaker TX

**Remediation**:
```bash
# In microstable/solana/ workspace:
cargo update -p rustls-webpki --precise 0.103.13
cargo update -p reqwest  # may pull in updated webpki transitively
cargo audit  # verify clean
```

### HPKE Nonce Reuse Attack Class (A76) — Future Risk
If any future Microstable component uses hpke-rs for keeper↔oracle or keeper↔relayer secure messaging:
- hpke-rs ≤ 0.5.x: u32 nonce counter wraps at 2^32 → nonce reuse → full message decryption possible
- Companion: X25519 non-contributive DH (RUSTSEC-2026-0072) → weak shared secret accepted
- Preemptive rule: any future HPKE adoption must pin hpke-rs ≥ 0.6.0 from day 1

---
*(2026-03-26 Red Team Evolution: A81 + A82)*

### Quinn QUIC Validator Infrastructure Attack Class (A81)
- RustSec advisory in Quinn (Agave's QUIC transport library) — publicly disclosed March 2026 without private coordination.
- Remote process crash of Agave validators, no authentication required.
- Attack amplification: crash targeted honest validators → skew stake-weighted block production in attacker's favor during window before community upgrades.
- Microstable indirect risk: keeper RPC relies on Agave nodes. During validator crash event, all 3 default RPC endpoints may degrade simultaneously.
- **Defense requirement**: keeper must have ≥ 3 geographically-distributed RPC fallbacks. Retry-on-503 logic must be confirmed in keeper code. Alert if all RPCs fail simultaneously.

### Solana Blockchain as C2 Transport — Developer Targeting (A82)
- Confirmed attack campaign (Bitdefender, March 2026): malicious IDE extension uses Solana on-chain transaction data as payload delivery channel.
- Bypasses traditional C2 detection because traffic is indistinguishable from legitimate Solana network traffic.
- Target profile: Solana developers (Rust/Anchor/TS) — exactly the Microstable developer persona.
- Highest-value exfiltration from a Microstable developer machine:
  1. Anchor upgrade authority keypair (wallet.json / id.json)
  2. Keeper hot wallet seed phrase
  3. Helius/QuickNode/Pyth API keys
  4. AWS IAM credentials (CI/CD pipeline)
- **Mandatory mitigations for Microstable team**:
  1. IDE extension allowlist policy on all machines with keeper/deploy key access
  2. Anchor deploy keys in hardware wallet (Ledger) — never flat file on dev machine
  3. Keeper hot wallet: HSM or at minimum OS keychain, never plaintext .env
  4. API keys: 1Password / environment injection at runtime, never committed
  5. Rotate all secrets if any team member's machine shows unexpected Solana RPC traffic

## 2026-03-27 Patterns

### libcrux-ml-dsa Signature Verification Faults (A83)
- **RUSTSEC-2026-0076 (HIGH)**: malformed ML-DSA signature hints can trigger an out-of-bounds read during verification, producing panic-based remote DoS when verification service accepts attacker-controlled serialized signatures.
- **RUSTSEC-2026-0077 (HIGH)**: ML-DSA signer response norm check incorrectly validated, allowing malformed signatures to pass verification in some paths (integrity policy break).
- **Microstable relevance**: no `libcrux-ml-dsa` in `microstable/solana/Cargo.lock` today; attack is **latent**.
- **If adopted in keeper or program**: blocklist versions `<0.0.8` and require explicit fuzz tests for invalid/oversized hint cases.

### libcrux-sha3 Incremental SHAKE Discrepancy (A84)
- **RUSTSEC-2026-0074**: `libcrux-sha3` incremental `portable::incremental::Shake*::squeeze` dropped first output block when output exceeds RATE size.
- **Impact**: deterministic output mismatch / entropy drift in protocols that rely on long-output XOF streams.
- **Microstable relevance**: no `libcrux-sha3` dependency today; no direct exploit path.
- **Future migration guard**: require `libcrux-sha3 >= 0.0.8` for any PQ hashing/KEM rollout.

---


<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-28 -->

## 2026-03-28 Patterns

### libcrux-poly1305 Standalone MAC Unauthenticated Panic (A85)
- **RUSTSEC-2026-0073 (HIGH, CVSS 8.7)**: incorrect constant for key length in `libcrux-poly1305` causes `libcrux_poly1305::mac` to always panic with out-of-bounds memory access.
- **Attack surface**: any service exposing a code path that calls `libcrux_poly1305::mac` with attacker-controlled input. Network-reachable, no authentication required (AV:N/AC:L/AT:N/PR:N/UI:N).
- **Scope boundary**: standalone MAC use only. `libcrux-chacha20poly1305` (AEAD) is **unaffected** — the vulnerability is isolated to the standalone MAC API, not the AEAD composition.
- **Patched**: `libcrux-poly1305 >= 0.0.5`
- **Microstable relevance**: no `libcrux-poly1305` dependency in Cargo.lock today; attack is **LATENT**.
- **Sibling cluster**: A83 (libcrux-ml-dsa), A84 (libcrux-sha3), A85 (libcrux-poly1305) — all `libcrux` PQ/crypto primitives advisory batch (2026-03-24). The cluster pattern suggests the libcrux library is undergoing broad security audit; expect additional advisories.
- **Future migration guard**: if any libcrux-* crate is introduced, verify advisory status for ALL libcrux-* sibling crates, not just the directly imported one. Pin to advisory-clean versions at adoption time.
- **Source**: https://rustsec.org/advisories/RUSTSEC-2026-0073.html | https://github.com/cryspen/libcrux/pull/1351

### Coordinated Mass-Deployment Malicious Crate Wave — Crypto Ecosystem Targeting (A86)
- **Signal**: 2026-03-26, RustSec batch removal of 20+ malicious crates in a single day; crate names include crypto/DeFi/trading targets: `monero-rpc-rs`, `monero-api`, `acceptxmr-rs` (Monero payment processor), `lfest-main` (trading framework), alongside Windows-ecosystem cloaks (`registry-win`, `win-crypto`, `windows-service-rs`, `openvpn-plugin-rs`, `win-base64-rs`, `winx-rs`, `lasso-rs`, `tauri-winrt-notifications`).
- **Attack pattern — carpet-bomb multi-vector**:
  1. Attacker registers 20+ crates simultaneously under different categories (crypto-utility, OS-wrapper, UI)
  2. Crates are dormant or functional for weeks; legitimate installs accumulate
  3. Malicious payload activates at a trigger time (e.g., specific date, environment variable) or exfiltrates continuously
  4. All crates are taken down in a coordinated wave — but any developer who installed during the active window is compromised
  5. **Key asymmetry**: crate-by-crate deny-listing is too slow; the attacker deploys faster than defenders remove
- **Why distinct from A44 (single direct-dep env-stealer)**: A44 is a targeted, single-crate injection aimed at one ecosystem. A86 is a carpet-bomb deployment across multiple package categories simultaneously — scale and cross-ecosystem targeting are the novel elements.
- **Why distinct from A45 (campaign-clone rotation)**: A45 is a reactive pattern (clone appears AFTER original takedown). A86 is a proactive parallel deployment — all clones are live simultaneously.
- **Crypto developer kill chain**: `monero-api` or `lfest-main` added to Solana project → exfiltrates RPC keys, Anchor deploy keypair, `.env` secrets → attacker sends privileged keeper/upgrade transactions with stolen keys.
- **Microstable relevance**: Cargo.lock clean ✅. Risk elevated when: (a) incident-response pressure to add new utility crates quickly, (b) new team members or contractors add dependencies without full review.
- **Mitigation upgrade** (extends A44/A45 defenses):
  1. Campaign-level detection: when 5+ crates are removed in one day in any registry, trigger immediate full Cargo dependency audit across ALL projects
  2. Category quarantine: if one crypto-adjacent crate is flagged malicious, quarantine the entire semantic cluster (Monero-related, trading-related, Windows-adjacent) for 7 days pending review
  3. Install telemetry: log ALL `cargo install`/`cargo build` events with new crate additions (date, crate name, version, maintainer age) — alert on any new crate <30 days old
  4. Out-of-band maintainer verification: for any DeFi-adjacent crate (matching name contains: monero, btc, eth, sol, defi, trade, crypto), require direct GitHub-verified maintainer identity check before allowlist approval
- **Source**: https://rustsec.org/advisories/ (batch, 2026-03-26)

### Solana-Specific Defense Checklist Update
39. ☐ libcrux-* adoption: full advisory check across ALL sibling crates (not just the directly imported one) before adoption
40. ☐ Registry mass-removal detection: CI/toolchain monitors crates.io security events; 5+ removals/day triggers immediate full Cargo audit

---
<!-- AUTO-ADDED 2026-03-29 (Red Team Daily Evolution) — A87~A90 Solana/Anchor-relevant patterns -->

## 2026-03-29 New Pattern Additions

### A87 — Groth16 Trusted Setup Ceremony Skip (ZK circuits on Solana/Anchor)
- **Solana context**: While mainstream Solana programs do not use Groth16 ZK proofs directly, Solana's ZK Token standard (Confidential Transfers in Token-2022) uses ElGamal + range proofs. Any custom Solana program integrating a Groth16 ZK verifier (via a Solana-native ZK VM or off-chain verifier contract) faces this attack surface.
- **Future risk trigger**: If Microstable adds confidential transfer support or a ZK proof-based compliance feature, mandatory ceremony verification must be part of the deployment checklist.
- **Detection command**: For any `verification_key.json`, verify `gamma_g2 != [G2_GENERATOR_X, G2_GENERATOR_Y]`. If equal → ceremony was not completed.
- **Checklist item 41**: ☐ Any ZK verifier deployed to Solana/Anchor must provide ceremony transcript with ≥ 1 external contributor. Verify `snarkjs zkey verify` output before deploy.

### A88 — Token-2022 TransferHook CPI Reentrancy (Solana analog of ERC-3525 SFT reentrancy)
- **Solana context**: SPL Token-2022 `TransferHook` extension fires an additional CPI instruction during every transfer. If the hook's target program re-enters the calling instruction before all accounts are finalized:
  - Balances, supply counters, or position states can be read mid-update (stale).
  - The calling program may have transferred tokens (changing ATA balances) but not yet updated its internal state.
  - A malicious hook could trigger a second deposit, borrow, or mint against the pre-update state.
- **Microstable current status**: spl-transfer-hook-interface 0.9.0/0.10.0 in Cargo.lock (transitive dep). No active hook handler in lib.rs. LATENT.
- **Guard pattern for Anchor programs using Token-2022 with TransferHook**:
```rust
// SAFE pattern: update ALL internal state before any SPL transfer that invokes a hook
ctx.accounts.vault.total_deposits = ctx.accounts.vault.total_deposits
    .checked_add(deposit_amount)
    .ok_or(ErrorCode::MathOverflow)?;  // state updated FIRST

// THEN initiate transfer (which will fire TransferHook CPI)
token_2022::transfer_checked(...)?;  // hook fires here against updated state
```
- **Checklist item 42**: ☐ If Token-2022 TransferHook is applied to mSTABLE or any vault collateral token, audit all callers: ensure state updates precede transfer calls (CEI for SPL).

### A89 — Supply Cap Enforcement: Internal Tracker vs. ATA Balance (Solana-Specific)
- **Microstable confirmation (2026-03-29)**: `total_collateral_value()` correctly uses `v.total_deposits` (internal counter). NOT vulnerable to donation attack. ✅ CONFIRMED SAFE.
- **General Solana pattern**: Programs that read `token_account.amount` from a vault ATA as the authoritative deposit counter are vulnerable to donation-bypass. Any `require!(vault_ata.amount <= cap)` check is bypassable by direct SPL token transfer to the ATA.
- **Vulnerable pattern**:
```rust
// VULNERABLE: reads ATA balance directly
let vault_balance = ctx.accounts.vault_ata.amount;
require!(vault_balance <= supply_cap, ErrorCode::SupplyCapExceeded);
```
- **Safe pattern** (what Microstable correctly implements):
```rust
// SAFE: reads internal program-controlled state
let protocol_deposits = ctx.accounts.vault.total_deposits;
require!(protocol_deposits <= supply_cap, ErrorCode::SupplyCapExceeded);
```
- **Checklist item 43**: ☐ Audit ALL supply/collateral caps: verify they read from program-internal state, not raw ATA `token_account.amount`.
- **Multi-horizon monitoring note**: Standard per-slot circuit breakers do not catch 9-month slow accumulation. Add 30-day/90-day rolling concentration alerts.

### A90 — RNG Failure Key Generation Oracle (libcrux-ed25519 / ed25519 Variants)
- **Solana context**: Solana validators and programs use ed25519 signatures. If keeper or validator software uses `libcrux-ed25519 < 0.0.4` for key generation, catastrophic RNG failure → all-zero key → predictable.
- **Keeper key generation risk**: Any Rust binary that generates ed25519 keypairs using libcrux-ed25519 without RNG error handling is vulnerable. Microstable keeper: libcrux-ed25519 NOT present (confirmed). Standard Solana `solana-keygen` uses a different code path.
- **Checklist item 44**: ☐ If any new Rust utility is introduced for Microstable keypair generation, verify: (a) does NOT use libcrux-ed25519 < 0.0.4; (b) always validates generated key != all-zeros before use; (c) uses hardware RNG source (HSM/TPM/TRNG) in production.

### Solana-Specific Defense Checklist Update
41. ☐ ZK verifier deployment: ceremony transcript with ≥1 external contributor + `snarkjs zkey verify` before mainnet deploy
42. ☐ Token-2022 TransferHook callers: CEI ordering enforced — internal state updated BEFORE transfer CPI
43. ☐ Supply cap enforcement: uses program-internal deposit tracker, NOT raw ATA `token_account.amount`
44. ☐ New keypair generation utilities: verify libcrux-ed25519 >= 0.0.4 + non-zero key validation + hardware RNG

---
<!-- AUTO-ADDED 2026-04-03 (Red Team Daily Evolution) — A95~A96 Anchor 1.0 trust-boundary patterns -->

## 2026-04-03 Anchor 1.0 Pattern Additions

### A95 — Anchor `reload()` Owner-Drift Bypass
- **Solana context**: Developers commonly call `.reload()` after CPI to refresh account state. Anchor's 2026 fix shows that, on older versions, `reload()` itself was not a complete trust barrier because owner validation had to be tightened.
- **Attack idea**: A CPI path mutates, closes, or otherwise changes the trust context of an account; the caller then `reload()`s and accepts the new bytes as trusted state without re-asserting owner/business invariants.
- **Why this matters on Solana**: CPI-heavy programs, Token-2022 hook flows, and migration paths frequently depend on post-CPI refresh. Reviewers who know A42 (missing reload) may miss the inverse pattern: reload is present, but still unsafe on older Anchor.
- **Checklist item 45**: ☐ On Anchor `<1.0.0`, every post-CPI `.reload()` must be preceded by an explicit owner assertion and followed by invariant re-checks (seed, mint, authority, status).

### A96 — Duplicate Mutable Account Aliasing
- **Solana context**: Passing the same pubkey into two mutable roles can collapse accounting assumptions even when owner/signer checks all pass.
- **Anchor 1.0 signal**: Default duplicate mutable-account rejection was added because this pattern was repeatedly dangerous in nested, optional, and `remaining_accounts` flows.
- **Audit question**: For every instruction with two or more mutable roles, ask: "what breaks if these two accounts are actually the same pubkey?"
- **Checklist item 46**: ☐ For every pair of mutable roles that must be distinct (`source/destination`, `user/fee vault`, `position_a/position_b`), add `require_keys_neq!` unless the instruction uses explicit `dup` and documents why aliasing is safe.

### Solana-Specific Defense Checklist Update
45. ☐ On Anchor `<1.0.0`, post-CPI `.reload()` requires manual owner assertion + invariant re-check
46. ☐ Add `require_keys_neq!` for every security-relevant mutable-role pair unless aliasing is explicitly intended via `dup`

---
<!-- AUTO-ADDED 2026-04-03 (Red Team Daily Evolution) — B77 Drift durable nonce admin-takeover generalization -->

## 2026-04-03 Additional Pattern Additions

### B77 — Durable Nonce Approval Laundering / Pre-Signed Multisig Admin Takeover
- **Solana context**: durable nonce accounts allow a transaction to remain executable far beyond the normal recent-blockhash lifetime. That is operationally useful, but it also means signer approval time can be separated from execution time by hours or days.
- **Why this matters on Solana specifically**:
  1. Multisig / council workflows often happen off-band in chat, ticket, or wallet UI approval flows.
  2. Signers may treat a durable-nonce transaction as a temporary test or maintenance action, not a transaction that can be stockpiled for later broadcast.
  3. Once quorum is collected, the attacker no longer needs real-time signer interaction.
- **Observed real-world signal**: Drift Protocol (April 2, 2026) disclosed a Security Council takeover involving durable nonce accounts and pre-signed transactions.
- **Attack shape**:
  1. Prepare durable nonce accounts in advance.
  2. Gather privileged signatures on opaque or misrepresented transactions.
  3. Wait until enough signatures are accumulated.
  4. Broadcast later to rotate authority, change limits, or unlock fund flows.
- **Detection pattern in Solana code / ops**:
```rust
// RISKY: privileged tx remains valid after signer review window closes
let message = Message::new_with_nonce(
    instructions,
    Some(&payer.pubkey()),
    &nonce_account,
    &nonce_authority,
);
let mut tx = Transaction::new_unsigned(message);
tx.try_partial_sign(&[signer_a, signer_b], durable_nonce_hash)?;
archive_or_forward(tx)?; // delayed execution risk
```
- **Why distinct from generic multisig compromise**: signer keys do not need to be stolen. The signed transaction itself becomes the weapon because execution is deferred.
- **Microstable current status**: reviewed keeper code uses fresh `get_latest_blockhash()` send-time signing, not durable nonce accounts. Current path is **not active**. Risk becomes immediate if upgrade-authority or emergency-admin flows adopt durable nonce signing.

### Solana-Specific Defense Checklist Update
47. ☐ Privileged multisig / upgrade / treasury transactions must not use durable nonce accounts by default; if emergency nonce flow exists, require short TTL, explicit instruction digest review, nonce rotation, and no shared storage of partially signed transactions

---
<!-- AUTO-ADDED 2026-04-06 (Red Team Daily Evolution) — A98~A99 Drift Protocol refined patterns -->

## 2026-04-06 Drift Protocol Refined Patterns

### A98 — Oracle Manipulation via Fake Asset with Minimal Liquidity (Solana-Specific Variant)
- **Solana context**: SPL token creation is cheap (<0.01 SOL). Raydium and other Solana AMMs have no minimum liquidity requirement for listing. Oracles that use AMM spot price without liquidity weighting are vulnerable.
- **2026 cross-ecosystem reinforcement (Rhea Finance, 2026-04-16, NEAR)**: Rhea reportedly fell to **multiple fake token contracts + newly created pools** that misled not only price discovery but also internal **validation layers**. Treat this as a warning that `TVL > 0` or `pool exists` checks are not enough — **pool provenance** and **canonical mint-pair admission** must be verified too. **Source**: https://hacked.slowmist.io/ | https://x.com/CertiKAlert/status/2044791732575912321
- **Attack shape**:
  1. Mint 750M units of fake token (CVT in Drift case).
  2. Seed $3,000 liquidity on Raydium.
  3. Wash trade to maintain price near $1.
  4. Oracle accepts token as collateral based on spot price.
  5. Deposit fake tokens, withdraw real assets.
- **Why distinct from A3**: A3 manipulates price of REAL assets. A98 creates the asset itself — no underlying value exists.
- **Solana-specific defense**:
  - Pyth oracle: only lists assets on major exchanges (gatekeeping).
  - Custom oracle: minimum liquidity threshold (>$1M TVL), asset age requirement (30+ days), liquidity-weighted price.
  - Pool provenance: only accept prices from approved mint pairs / approved pool factories; attacker-created pools must fail admission even if they have non-zero liquidity.
- **Checklist item 48**: ☐ If protocol accepts custom collateral assets, require: (a) TVL > $1M on primary DEX, (b) asset age > 30 days, (c) liquidity-weighted oracle price, (d) manual governance whitelist, (e) approved pool-factory + canonical mint-pair provenance.

### A99 — Zero-Timelock Governance Migration Attack (Solana-Specific Variant)
- **Solana context**: Solana programs often use PDAs as admin authorities. Migration of admin authority (e.g., Security Council) can change threshold and timelock settings.
- **Attack shape**:
  1. Protocol migrates governance to new council/multisig.
  2. Migration sets timelock = 0 for "operational flexibility".
  3. Attacker (already positioned) immediately executes privileged operations.
  4. No time for monitoring/alerting/response.
- **Observed real-world signal**: Drift Protocol migrated Security Council to 2/5 threshold on March 27, 2026 — with zero timelock. This eliminated the detection window.
- **Why distinct from A5**: Not a timelock bypass — it's a governance decision that REMOVES the timelock entirely.
- **Solana-specific defense**:
  - Enforce minimum timelock (24h) at program level.
  - Migration requires separate governance vote.
  - Monitor governance config changes.
- **Checklist item 49**: ☐ All governance/admin migrations must: (a) enforce ≥24h timelock, (b) require separate vote for timelock removal, (c) trigger monitoring alert on config change.

### Solana-Specific Defense Checklist Update
48. ☐ Custom collateral onboarding: TVL > $1M, age > 30 days, liquidity-weighted oracle, governance whitelist
49. ☐ Governance migration: enforce ≥24h timelock, separate vote for removal, monitoring alert

### A105 — Persistent Nonce Durable Pre-Signed Transaction Bypass (Drift Pattern)
- **Solana context**: Durable nonce accounts allow transactions to remain executable indefinitely beyond normal recent-blockhash lifetime (~150 slots). Pre-signed durable nonce transactions can be stockpiled and executed at attacker-chosen time.
- **Drift-specific attack chain** (April 1, 2026):
  1. March 23: Attacker initialized 4 persistent nonce accounts (2 linked to Drift Security Council signers, 2 attacker-controlled)
  2. Pre-signed instructions were obtained under guise of routine protocol maintenance
  3. March 27: Governance migration to 2/5 + zero timelock removed delay window
  4. April 1: Pre-signed txs executed in 12 minutes across 31 withdrawals
- **Why distinct from A99**: A99 covers the governance migration to zero timelock. A105 is the *mechanism* — durable nonces make ANY pre-signed privileged tx a deferred weapon, regardless of governance changes
- **Keeper/infrastructure relevance**: If Microstable privileged operations (upgrade, emergency admin, treasury) ever use durable nonce accounts, the same stockpiling attack applies. Keeper binary uses fresh `get_latest_blockhash()` per transaction — NOT currently using durable nonces
- **Detection command**: Search for `nonce_account` or ` durable_nonce` in all privileged admin scripts and program initialization paths
- **Checklist item 50**: ☐ No privileged operations use durable nonce accounts. If emergency nonce flow is added, require: (a) short TTL ≤10 slots, (b) explicit instruction digest review by all signers, (c) no stockpiling of partially-signed nonce transactions

### A106 — Stablecoin Issuer CCTP Exfil via Selective Inaction (Drift $232M USDC Pattern)
- **Solana context**: Circle's Cross-Chain Transfer Protocol (CCTP) is the primary USDC bridge from Solana to Ethereum. CCTP requires Circle's mint/burn mechanism — Circle can freeze minted USDC on destination chain
- **Drift-specific exploit**: $232M USDC bridged Solana → Ethereum via CCTP during active exploit. Circle had frozen 16 unrelated wallets 8 days earlier for a sealed U.S. civil case, demonstrating active freeze capability. Circle took 6+ hours to begin partial freezing — 0 freeze during active attack
- **Attack shape**:
  1. Drain Solana DeFi protocol using admin key compromise or smart contract exploit
  2. Convert assets to USDC
  3. Bridge USDC to Ethereum via CCTP (Circle's own infrastructure)
  4. Circle has freeze power but may delay or refuse during active exploit
- **Microstable specific risk**: Microstable accepts USDC, USDT, DAI, USDS as collateral. If USDC is the dominant collateral and a similar exploit occurs, $232M in USDC could be exfil'd via CCTP before Circle acts
- **Defense requirements**:
  1. Document Circle emergency freeze contact procedure and SLA (target: <30 min response)
  2. Maintain alternative circuit breaker that pauses mint/redeem if >$10M USDC exits via CCTP in <1 hour
  3. Cross-chain bridge usage monitoring with automatic alert
- **Source**: https://www.cryptotimes.io/2026/04/03/285m-gone-in-12-minutes-how-a-fake-token-and-stolen-keys-gutted-drift-protocol/

### B78 — Wide Cross-Slot Sandwich Attack (Firedancer Era, 93% of Solana MEV)
- **Signal**: dev.to analysis (2026-04), Solana MEV defense research
- **Pattern**: 93% of Solana sandwich attacks now span multiple validator slots — no longer detectable as same-block transactions:
  ```
  Slot N (Attacker-Controlled Validator): tx[last] = front-run buy
  Slot N+1 (Any Validator): tx[mid] = victim swap at inflated price
  Slot N+2 (Attacker-Controlled Validator): tx[0] = back-run sell
  ```
- **Distinct from B40**: B40 (ACE fairness) is about protocol-level ordering rules. B78 is about MEV extraction across slot boundaries made possible by validator-level coordination
- **Single bot dominance**: One program (vpeNALD) executes 51,600 TX/day, 88.9% success rate, ~$450K SOL/day extraction
- **Firedancer verification lag amplifier**: Firedancer's dynamic block sizing + skip-vote creates intra-slot price lag. Keeper oracle update TX in slot N may show `oracle_slot=N` while price publication was 200ms prior — attacker can sandwich against the stale inner-slot price
- **Microstable risk**: LOW (stablecoin mint/redeem with fixed-price oracles, not AMM swaps). Keeper oracle updates use Pyth with publish_time + slot freshness — Firedancer intra-slot lag is absorbed by the publish_time check
- **Mitigation**: Jito `dontfront` flag protects within-block ordering; wide-slot attacks require separate defense

### Solana-Specific Defense Checklist Update
50. ☐ No privileged operations use durable nonce accounts; emergency nonce flow has ≤10 slot TTL + instruction digest review
51. ☐ Circle CCTP exfil: documented freeze procedure SLA <30 min + circuit breaker on large USDC bridge outflows
52. ☐ Wide cross-slot sandwich: Jito dontfront for keeper TX when possible; monitor for multi-slot MEV patterns
53. ☐ Instruction introspection: if using `load_instruction_at_checked`, migrate to `get_instruction_relative`; no hardcoded absolute instruction index for prerequisite checks

### A108 — Improper Instruction Introspection: Absolute vs Relative Indexing
- **Signal**: dev.to "Solana's CPI Security Trap" (2026-04-09)
- **Pattern**: `load_instruction_at_checked(n)` with hardcoded absolute index allows single instruction to satisfy multiple checks
- **Fix**: Use `get_instruction_relative(offset)` — verifies instruction immediately adjacent to current instruction
- **Microstable**: Not used — zero instruction introspection calls in program code ✅

---
<!-- AUTO-ADDED 2026-04-11 (Red Team Daily Evolution) — A109 Anchor lifecycle hooks -->

## 2026-04-11 Anchor 1.0 Tooling-Plane Pattern Additions

### A109 — Anchor Lifecycle Hook Supply-Chain Persistence
- **Solana context**: Anchor 1.0 adds executable lifecycle hooks in `Anchor.toml` (`pre_build`, `post_build`, `pre_test`, `post_test`, `pre_deploy`, `post_deploy`). That makes project configuration an execution surface on developer and deploy machines.
- **Attack idea**: A malicious PR or compromised contributor adds a seemingly harmless hook or referenced script. Routine `anchor build/test/deploy` then runs attacker code that swaps artifacts, exfiltrates wallet material, or mutates release outputs before on-chain deployment.
- **Why this matters on Solana**: Solana projects often keep deploy authority, IDL workflows, local validators, and CLI wallets in the same operator environment. Compromise of the Anchor hook plane can become upgrade-authority compromise without any on-chain bug.
- **Microstable current status**: `programs/microstable/Cargo.toml` and `keeper/Cargo.toml` are still on Anchor `0.31.1`, and no `Anchor.toml` / `[hooks]` usage was found in the repo. The vector is **not active today**, but becomes immediately relevant on Anchor 1.0 migration.
- **Checklist item 54**: ☐ If migrating to Anchor `>=1.0.0`, treat `Anchor.toml` as executable code: forbid `[hooks]` by default, require CODEOWNER review for any hook, and run deploys from ephemeral/hardware-signer environments.

### Solana-Specific Defense Checklist Update
54. ☐ Anchor `>=1.0.0` migration: no lifecycle hooks by default; any `[hooks]` entry requires explicit review, allowlist, and isolated runner/hardware signer path

---
<!-- AUTO-ADDED 2026-04-12 (Red Team Daily Evolution) — A110~A112 fair-ordering / randomness / Anchor raw-metadata patterns -->

## 2026-04-12 Fair-Ordering / Randomness / Anchor Pattern Additions

### A110 — Receipt-Threshold Poisoning / Commit-Set Saturation
- **Solana context**: 앞으로 Jito-like private ordering, encrypted mempool, committee receipt, commit/open ordering layer가 붙는 Solana 시스템은 “ordering fairness”와 “admission fairness”를 분리해서 봐야 한다.
- **핵심 패턴**: threshold receipt를 받은 트랜잭션만 admissible set에 들어가는 구조에서는, 공격자가 저가치 commit spam·selective non-open·validator attention saturation으로 **좋은 주문이 set에 못 들어오게** 만들 수 있다.
- **왜 Solana에서 중요하나**:
  1. 빠른 슬롯(400ms대) + validator-local order flow + Jito/private relay 결합 시 receipt capacity가 scarce resource가 된다.
  2. “순서 랜덤화”가 있어도 admission 단계가 오염되면 공정성은 이미 깨진다.
  3. Keeper / liquidation / auction flow가 fair-order infra 위에 얹히면 ordering stage보다 admission stage가 먼저 공격받는다.
- **Microstable current status**: MEV-ACE식 threshold receipt / committee admission layer는 **없다**. 따라서 full vector는 **NOT ACTIVE**.
- **Microstable-adjacent note**: 다만 `programs/microstable/src/lib.rs`에는 대규모 리밸런스용 단일 `pending_rebalance_commit` 슬롯이 있어, admission fairness가 아니라 **single-slot liveness choke** 관점의 부분 유사성은 있다. 현재는 keeper 2-of-3 compromise가 먼저 필요하므로 직접 severity는 낮다.
- **Checklist item 55**: ☐ 공정 주문 / private ordering / committee receipt 계층을 도입하면, `threshold receipts` 외에 `admission fairness`, `per-identity quota`, `non-open slashing`, `spam eviction`을 별도 설계할 것

### A111 — VDF Economic Speedup Grinding / Reward-Spike Delay Collapse
- **Solana context**: VDF 기반 랜덤 순서, keeper selection, liquidation auction randomness, batch fairness 설계를 도입할 경우 “암호학적으로 sequential”하다는 이유만으로 안전하다고 보면 안 된다.
- **핵심 패턴**: 공격자는 평시가 아니라 **reward spike가 큰 이벤트**에서만 더 빠른 하드웨어·selective abort·grinding을 사용한다. 평균 기준 delay는 tail-event에서 경제적으로 깨질 수 있다.
- **Solana-specific trigger**:
  1. liquidation bonus / MEV / auction spread가 특정 슬롯에서 급증
  2. validator/searcher가 temporary hardware rental 또는 privileged colocated infra 사용
  3. beacon parameter가 평균 수익 기준으로만 정해짐
- **Microstable current status**: `programs/microstable/src/lib.rs` / `keeper/src/`에 VDF beacon, randomness-based keeper election, lottery path는 발견되지 않았다. **NOT ACTIVE**.
- **Checklist item 56**: ☐ VDF / randomness beacon을 도입하면 지연 파라미터를 평균이 아니라 `p99 reward spike + attacker hardware edge + selective abort` 기준으로 산정할 것

### A112 — Anchor Raw IDL Metadata Trust-Boundary Confusion
- **Solana context**: Anchor가 `decodeIdlAccountRaw`를 추가하면서, 오프체인 툴이 raw metadata account의 `program`, `authority`, `canonical`, `encoding`, `compression` 필드를 직접 사용하는 경로가 생겼다.
- **핵심 패턴**: account owner / canonical flag / expected program pubkey 검증 없이 raw metadata를 신뢰하면 **IDL spoofing** 또는 **program-binding confusion**이 가능해진다.
- **왜 Solana/Anchor에서 중요하나**:
  1. 많은 팀이 IDL을 배포 메타데이터·클라이언트 생성·운영 대시보드의 신뢰 기반으로 사용한다.
  2. raw decode 노출은 “파싱 가능함”과 “신뢰 가능함”을 혼동하게 만든다.
  3. 잘못된 metadata account를 받아도 on-chain bug 없이 off-chain tooling이 먼저 속을 수 있다.
- **Microstable current status**: repo는 여전히 Anchor `0.31.1` 기준이고, `decodeIdlAccountRaw` 사용 흔적은 없다. **LATENT / NOT ACTIVE**.
- **Checklist item 57**: ☐ Anchor raw IDL metadata를 사용할 경우, `owner`, `program`, `authority`, `canonical` 검증 없이는 decoded 값을 코드생성·배포·모니터링 입력으로 신뢰하지 말 것

### Solana-Specific Defense Checklist Update
55. ☐ Fair-order / committee-receipt 도입 시 ordering fairness와 admission fairness를 분리 설계하고, per-identity quota + non-open slashing + spam eviction을 넣을 것
56. ☐ VDF/randomness beacon 파라미터는 평균이 아니라 p99 reward spike + hardware speedup + selective abort 비용 모델로 산정할 것
57. ☐ Anchor raw IDL metadata는 owner/program/authority/canonical 검증 없이는 자동 코드생성·배포·모니터링 입력으로 신뢰하지 말 것

---
<!-- AUTO-ADDED 2026-04-13 (Red Team Daily Evolution) — D48 logger-path stage-2 fetch -->

## 2026-04-13 Logging Supply-Chain Runtime-Trigger Pattern

### D48 — Logger-Path Stage-2 Remote Payload Fetch
- **Solana context**: Solana keeper/operator는 장애 대응, oracle drift 조사, RPC 이상 징후 분석 때 TRACE/DEBUG 로깅을 켜는 경우가 많다. 이때 악성 logging dependency는 빌드 시점이 아니라 **실전 incident-response 시점**에만 활성화될 수 있다.
- **핵심 패턴**: `trace()` 또는 logger bridge 내부에서 외부 endpoint로 2차 payload를 받아 실행한다. 따라서 빌드 샌드박스·기본 테스트·정적 diff review를 모두 통과한 뒤, 실제 운영 프로세스에서만 발화한다.
- **왜 Solana에서 특히 위험한가**:
  1. keeper, deploy CLI, RPC 토큰, signer path가 같은 운영 환경에 공존하는 경우가 많다.
  2. 평소에는 INFO 수준 로그만 쓰다가 incident 때 TRACE를 켜므로, 악성 코드가 **위기 순간에만** 발화할 수 있다.
  3. 운영팀은 로깅 dependency를 business logic보다 덜 위험하게 보는 경향이 있어 review intensity가 낮다.
- **Microstable current status**: `microstable/solana/Cargo.lock`에는 `logprinter` / `logtrace`가 없고, 정상 `tracing` / `tracing-subscriber`만 존재한다. 따라서 **ACTIVE exploit path는 미확인**. 다만 keeper 전역에 tracing 호출이 넓게 퍼져 있어, 향후 악성 logger helper가 병합되면 activation surface는 넓다.
- **Checklist item 58**: ☐ logging/telemetry dependency는 allowlist-only로 관리하고, 신규 logger crate/bridge 추가 시 security review + egress 제한 + privileged runtime 분리를 강제할 것

### Solana-Specific Defense Checklist Update
58. ☐ Logging/telemetry dependency는 allowlist-only; 신규 logger crate/bridge 추가 시 security review, lock diff review, runtime egress restriction을 강제할 것

---
<!-- AUTO-ADDED 2026-04-14 (Red Team Daily Evolution) — A113 Token-2022 authority-meta elision -->

## 2026-04-14 Token-2022 Extension Control-Plane Pattern

### A113 — Token-2022 Extension Authority-Meta Elision / Control-Plane Freeze
- **Solana context**: Anchor upstream PR #4324 (`ead011c`, merged 2026-04-13) fixed a Token-2022 `group_pointer_update` CPI helper that built the instruction correctly but omitted `authority` from the `invoke_signed` account-info slice.
- **핵심 패턴**: Solana CPI는 “instruction meta는 맞는데 실제 `invoke_signed` 에 넘긴 `AccountInfo` 집합이 빠진” 상태가 생기면, privileged extension update가 조용히 dead path가 된다. 공격자는 이 dead path 자체를 이용해 revoke / rotate / pointer cleanup을 지연시키고, 운영팀이 급히 넣는 permissive raw-CPI hotfix를 두 번째 공격면으로 전환할 수 있다.
- **왜 Solana에서 특히 위험한가**:
  1. Token-2022 extension pointer/group/member metadata는 off-chain indexer, allowlist, compliance 분류, wallet UX에 연쇄적으로 소비된다.
  2. update path가 막히면 자금 탈취가 즉시 안 보여도 **신뢰 분류 stale state** 가 길게 지속될 수 있다.
  3. 팀은 종종 “막힌 CPI wrapper만 우회”하려고 `remaining_accounts` / raw instruction / `UncheckedAccount` 로 문제를 봉합한다. 이때 authority confusion surface가 커진다.
- **Microstable current status**:
  - `microstable/solana/programs/microstable/src/lib.rs` 와 `keeper/`에서 `token_2022_extensions`, `group_pointer`, `remaining_accounts` 사용 흔적을 찾지 못했다.
  - Anchor `0.31.1` 사용 중이며 `Anchor.toml` 은 존재하지만 `[hooks]` 섹션은 없다.
  - 따라서 **NOT ACTIVE today**. 다만 향후 Token-2022 extension 기반 자산 분류/registry를 붙이면 즉시 재평가 대상이다.
- **Checklist item 59**: ☐ privileged CPI wrapper는 instruction metas와 `invoke[_signed]` account-info slice가 동일 계정 집합인지 golden-test로 고정하고, 실패한 extension update를 `remaining_accounts` / raw `UncheckedAccount` 우회로 봉합하지 말 것

### Solana-Specific Defense Checklist Update
59. ☐ Privileged CPI wrapper는 instruction metas와 `invoke[_signed]` account-info slice 일치성을 테스트로 고정하고, extension update 실패를 permissive raw-CPI 우회로 해결하지 말 것

<!-- AUTO-ADDED 2026-04-15 (Black Team Daily Evolution) — A114 signed-amount polarity inversion -->

## 2026-04-15 Signedness / Reserve-Delta Pattern

### A114 — Signed-Amount Donation Polarity Inversion (Solana adaptation note)
- **Solana context**: Anchor/Solana on-chain business logic는 토큰 수량 자체는 대개 `u64` 로 받지만, perp PnL, funding, insurance-fund offsets, fee rebates, settlement netting에서는 `i64`/`i128` signed delta를 쓰고 싶어지는 순간이 온다. 이때 public 또는 semi-public instruction이 signed delta를 직접 받으면, "적립" 과 "차감" 이 같은 숫자 공간에 섞이면서 polarity inversion attack surface가 열린다.
- **핵심 패턴**: `donate(delta)`, `settle(offset)`, `insurance_adjust(delta)` 같은 instruction이 `delta < 0` 를 막지 않거나, direction enum 없이 signed value 하나로 회계를 태우면, 입금용 경로가 사실상 인출용 경로로 역전될 수 있다.
- **Solana에서 특히 주의할 점**:
  1. SPL Token transfer amount는 unsigned여도, 내부 state accounting은 signed netting으로 흘러가기 쉽다.
  2. keeper 또는 off-chain signer가 signed delta를 직렬화해 보내는 순간, on-chain program은 "누가 이 방향을 허용했는가" 를 별도로 검증해야 한다.
  3. insurance fund / fee rebate / PnL settlement가 같은 reserve를 공유하면, polarity bug는 곧 shared-vault drain으로 이어질 수 있다.
- **Microstable current status**:
  - `lib.rs` 검토 결과 public amount path는 `u64` 기반이고 public insurance-fund donation instruction도 없다.
  - 따라서 오늘 기준 active path는 보이지 않는다.
  - 다만 향후 perp/insurance/funding-rate 정산 레이어가 추가되면 signed delta policy를 별도 설계 규약으로 강제해야 한다.

### Solana-Specific Defense Checklist Update
60. ☐ Reserve/insurance/PnL settlement instruction은 **direction(credit/debit)** 과 **magnitude(u64)** 를 분리하고, public path에서 signed delta 하나로 자금 이동 의미를 동시에 표현하지 말 것

---
<!-- AUTO-ADDED 2026-04-16 (Red Team Daily Evolution) — A115 rustls-webpki name-constraint bypass -->

## 2026-04-16 Keeper TLS Trust-Boundary Pattern

### A115 — Keeper TLS Name-Constraint Escape / Allowlisted Host Impersonation
- **Solana context**: Solana keeper / oracle / relayer는 대부분 RPC, Hermes, external price API를 `reqwest` + `rustls` 로 붙고, 설정 계층에서는 `https://` 스킴과 hostname allowlist로 outbound trust boundary를 관리한다. 그런데 verifier가 constrained subordinate CA 또는 wildcard certificate의 **name constraints** 를 잘못 검증하면, 공격자는 config를 건드리지 않고도 allowlisted host에 대한 신뢰를 가로챌 수 있다.
- **핵심 패턴**: `rpc_url` / `secondary_rpc_url` / `hermes_url` / `coingecko_url` / `binance_url` 가 allowlisted host라도, TLS verifier가 misissued constrained cert를 받아들이면 **hostname policy가 certificate namespace policy를 대신하지 못한다**. 즉, “허용된 도메인만 쓴다”는 정책이 실제로는 “허용된 문자열만 본다”가 된다.
- **왜 Solana keeper에서 특히 위험한가**:
  1. keeper는 on-chain signer보다 덜 민감해 보이지만, 실제로는 emergency shutdown, rebalance cadence, oracle freshness decision을 좌우한다.
  2. Solana 운영팀은 종종 RPC host allowlist를 강하게 두기 때문에, 그 바깥의 PKI 제약은 상대적으로 덜 보게 된다.
  3. 공격자는 즉시 자금 탈취가 안 되더라도, 단일 source impersonation만으로 timeout / stale / failover storm을 유도해 운영팀을 hotfix 모드로 밀어 넣을 수 있다.
- **Source signals**:
  - RustSec `RUSTSEC-2026-0098` (issued 2026-04-15)
  - RustSec `RUSTSEC-2026-0099` (issued 2026-04-15)
  - `solana-program/token` commit `4c6f8a7` (`deps: Update rustls-webpki`, 2026-04-15)
- **Microstable current status**:
  - `keeper/Cargo.toml` uses `reqwest` with `rustls-tls`
  - `Cargo.lock` contains `rustls-webpki = "0.103.9"` and `"0.101.7"`
  - `keeper/src/hermes.rs` / `price_feed.rs` create default `reqwest::Client` instances for HTTPS endpoints
  - `keeper/src/config.rs` enforces HTTPS and RPC host allowlist, but certificate pinning is not present
  - 따라서 **ACTIVE LATENT**. 무결성 변조는 다중 endpoint compromise가 더 필요하지만, availability degradation과 operator-pressure path는 현실적이다.
- **Checklist item 61**: ☐ keeper outbound HTTPS는 `https://` + hostname allowlist로 끝내지 말고, `rustls-webpki >= 0.103.12` 업그레이드와 함께 RPC/Hermes/price API에 대해 SPKI pinning 또는 issuer drift 감시를 추가할 것

### Solana-Specific Defense Checklist Update
61. ☐ Keeper outbound HTTPS는 `https://` + hostname allowlist만으로 신뢰하지 말고, `rustls-webpki >= 0.103.12` 업그레이드와 SPKI pinning/issuer drift monitoring을 병행할 것

---
<!-- AUTO-ADDED 2026-04-22 (Black Team Daily Evolution) — D27 KelpDAO RPC poisoning reinforcement -->

## 2026-04-22 Solana Keeper RPC Independence / Failover Integrity Pattern

### D27 — KelpDAO-style downstream RPC poisoning + failover concentration
- **Solana context**: Solana keeper / dashboard / relayer는 보통 `primary RPC + secondary RPC` 정도의 다중화와 hostname allowlist를 갖춘다. 하지만 KelpDAO는 이것만으로는 충분하지 않다는 것을 보여줬다. verifier가 직접 해킹되지 않아도, **신뢰 중인 일부 RPC 노드만 오염시키고 나머지 노드를 DDoS로 흔들어 failover를 poisoned set으로 몰아넣으면** 거짓 체인 상태가 legitimate read path로 들어올 수 있다.
- **핵심 패턴**:
  1. endpoint URL은 그대로 둔다.
  2. allowlisted RPC 공급망 내부의 일부 노드를 장악한다.
  3. poisoned 노드는 특정 verifier / keeper IP에게만 거짓 값을 보여주고, 외부 관측자에게는 정상 응답을 돌려 monitoring을 속인다.
  4. 정상 노드에는 장애를 유발해 운영 로직이 poisoned 경로를 "healthy fallback" 으로 채택하게 만든다.
- **왜 Solana keeper에서 특히 위험한가**:
  1. keeper는 종종 oracle freshness, emergency shutdown, rebalance cadence를 모두 off-chain reads에 의존한다.
  2. `primary_host != secondary_host` 검증은 해도, provider ownership / ASN / cloud / operator correlation까지는 잘 보지 않는다.
  3. degraded mode를 availability improvement로만 다루면, 실제로는 integrity downgrade인데도 privileged action이 계속 흘러갈 수 있다.
- **Microstable current status**:
  - `keeper/config.devnet.json` 은 `rpc_url` + `secondary_rpc_url` 2개만 둔다.
  - `keeper/src/config.rs` 는 두 URL이 서로 다르고 allowlist 안에 있는지만 강제한다.
  - `docs/app.js` 는 bootstrap 시 `getGenesisHash` 만 quorum cross-check 하고, runtime RPC method는 대부분 단일 endpoint 결과를 그대로 채택한다.
  - 따라서 **PARTIAL DEFENSE**. 단순 endpoint substitution에는 강해졌지만, KelpDAO식 poisoned-failover / verifier-specific spoofing까지 막는 구조는 아직 아니다.
- **Source signals**:
  - LayerZero `KelpDAO Incident Statement` (2026-04-20 fetch, incident 2026-04-18)
  - SlowMist Hacked listing (2026-04-18)
- **Checklist item 62**: ☐ keeper / dashboard RPC는 `2개 URL` 수준이 아니라 **N-of-M independent observation quorum**, provider-correlation inventory, degraded-mode privileged-action deny, observability-path independence를 함께 설계할 것

### Solana-Specific Defense Checklist Update
62. ☐ RPC failover는 availability 기능이 아니라 잠재적 integrity downgrade로 취급하고, poisoned-failover를 막기 위해 N-of-M observation quorum + provider correlation inventory + degraded-mode privileged-action deny를 둘 것

---
<!-- AUTO-ADDED 2026-04-17 (Red Team Daily Evolution) — A116 Anchor CPI return-data provenance -->

## 2026-04-17 Anchor CPI Return-Data Provenance Pattern

### A116 — Anchor CPI Return-Data Program-ID Confusion / Spoofed View Result
- **Solana context**: Solana return-data는 instruction-scoped shared buffer다. Anchor의 `Return<T>` / view-like helper를 쓰면 값 deserialize는 편하지만, patched path를 쓰지 않으면 **그 값을 마지막에 쓴 program_id가 기대한 callee인지** 까지 자동으로 보장되지 않을 수 있다.
- **핵심 패턴**: trusted CPI가 정상 값을 return한 뒤, 이후 attacker-controlled CPI가 같은 직렬화 형태로 `set_return_data` 를 한 번 더 호출하면, caller는 타입은 맞지만 **출처가 다른 값** 을 읽을 수 있다. 즉, typed return value가 authenticity proof는 아니다.
- **왜 Solana에서 특히 위험한가**:
  1. return-data는 account graph에 남지 않아 code reviewer가 source-provenance risk를 놓치기 쉽다.
  2. Anchor view helper는 ergonomics가 좋아서 quote helper, validation helper, permission check helper에 쉽게 퍼질 수 있다.
  3. Solana CPI는 같은 instruction 내 다수 callee 호출이 자연스러워, "나중 callee overwrite" attack chain이 구조적으로 가능하다.
- **Source signals**:
  - Anchor commit `f634129` (`fix(lang): validate program_id in CPI Return<T>::get() (#4411)`, 2026-04-16)
  - upstream PoC: legitimate return `10` 뒤 malicious overwrite `999`
- **Microstable current status**:
  - `programs/microstable/src/lib.rs` 와 `keeper/src/` 에서 `get_return_data`, `set_return_data`, `Return::<T>` 사용 흔적을 찾지 못했다.
  - 따라서 **NOT ACTIVE today**.
  - 다만 향후 quote/view helper를 CPI return-data로 붙이면 provenance 검증이 설계 필수 조건이 된다.
- **Checklist item 62**: ☐ Anchor CPI return-data는 typed deserialize만 믿지 말고, expected callee `program_id` provenance 검증을 강제하며, access-control/oracle/slippage gate의 단독 근거로 쓰지 말 것

### Solana-Specific Defense Checklist Update
62. ☐ Anchor CPI return-data는 `Return<T>` 타입 적합성만 믿지 말고, expected callee `program_id` provenance 검증과 malicious overwrite PoC 테스트를 함께 강제할 것

---
<!-- AUTO-ADDED 2026-04-18 (Red Team Daily Evolution) — D50 build-host persistence + Telegram session theft -->

## 2026-04-18 Builder / Operator Host Persistence Pattern

### D50 — Malicious Crate SSH Authorized-Key Persistence + Telegram Session Exfiltration
- **Solana context**: Solana keeper/operator 환경은 `~/.config/solana/*.json`, `.env`, SSH-based Git access, Telegram/Discord incident coordination이 한 워크스테이션에 공존하기 쉽다. 따라서 악성 crate가 단순히 secret 하나를 훔치는 수준을 넘어 **builder/operator host 자체에 재진입 수단을 심는 순간**, on-chain exploit 없이도 control-plane takeover로 이어질 수 있다.
- **핵심 패턴**: 악성 Rust crate가 build/install/runtime 중 `~/.ssh/authorized_keys` 에 공격자 공개키를 추가해 영속 셸 접근을 만들고, 동시에 `.env`, credential-like JSON, 문서형 비밀, Telegram Desktop `tdata` 를 exfiltrate 한다. 이 조합은 "비밀 유출"을 "세션·호스트 지배"로 격상시킨다.
- **왜 Solana에서 특히 위험한가**:
  1. keeper keypair JSON, deploy keypair, RPC credential, `.env` 가 같은 홈 디렉터리 계층에 모여 있는 경우가 많다.
  2. 사고 대응 시 Telegram/Discord로 hotfix 링크·지시를 주고받는 팀이 많아, 메신저 세션 탈취가 운영 권한 탈취로 바로 연결된다.
  3. Solana 운영자는 로컬 빌드/배포/검증을 빠르게 반복하므로 "작은 유틸 crate" 추가가 incident window에 특히 잘 섞인다.
- **Source signals**:
  - RustSec `RUSTSEC-2026-0102` (`microsoftsystem64`, issued 2026-04-15)
  - related cluster context: `RUSTSEC-2026-0100`, `RUSTSEC-2026-0101`
- **Microstable current status**:
  - `microstable/solana/Cargo.lock` 에 해당 crate들은 없다.
  - 따라서 **NOT ACTIVE today**.
  - 다만 keeper는 `.env` 와 keypair 경로를 적극 사용하므로, privileged build host가 오염되면 blast radius는 크다.
- **Checklist item 63**: ☐ privileged Rust build host에는 운영자 실사용 `$HOME`, `~/.ssh`, Telegram Desktop profile, production `.env` 를 mount하지 말고, `authorized_keys` 변경을 구성관리 + 경보 대상으로 취급할 것

### Solana-Specific Defense Checklist Update
63. ☐ privileged Rust build host에는 운영자 실사용 `$HOME`, `~/.ssh`, Telegram Desktop profile, production `.env` 를 mount하지 말고, `authorized_keys` 변경을 구성관리 + 경보 대상으로 취급할 것

### 2026-04-27 Reinforcement — Ecosystem-Native Build-Script Exfiltration Cluster (D28)
- **Signal**: RustSec `RUSTSEC-2026-0107` (`mysten-metrics`) and `RUSTSEC-2026-0108` (`sui-execution-cut`) both say the malicious crate shipped a **build script that attempted to exfiltrate data from the build machine**.
- **Why Solana teams should care**:
  1. crate names no longer need to look fake, Windows-only, or obviously typosquatted.
  2. ecosystem-native names that sound like internal metrics/execution tooling are enough to win a rushed PR review.
  3. compile-time exfil means the compromise happens before runtime behavior or integration tests give defenders any signal.
- **Solana-specific translation**: expect the same pattern under names resembling `solana-metrics`, `anchor-execution`, `pyth-cut`, `jito-profiler`, protocol-specific `*-metrics` helpers, or emergency incident tooling.
- **Microstable current status**:
  - `microstable/solana/Cargo.lock`, `keeper/Cargo.toml`, and keeper/docs scans show **no `mysten-metrics` / `sui-execution-cut` match**.
  - Therefore **NOT ACTIVE today**.
  - But keeper builds still happen on a host that resolves outbound dependencies and reads secret-adjacent config, so the class remains **LATENT and high-blast-radius**.
- **Source**: https://rustsec.org/advisories/RUSTSEC-2026-0107.html | https://rustsec.org/advisories/RUSTSEC-2026-0108.html

---
<!-- AUTO-ADDED 2026-04-19 (Red Team Daily Evolution) — D51 Anchor JS lockfile drift -->

## 2026-04-19 Anchor Toolchain Determinism Pattern

### D51 — Anchor JS Lockfile Drift / Semver-Satisfying Supply-Chain Smuggle
- **Solana context**: Solana 팀은 on-chain Rust 코드만 보는 경향이 강하지만, 실제로는 `Anchor.toml` 의 `package_manager`, generated TS client, test harness, local validator workflow가 같은 개발 문맥에서 함께 움직인다. 따라서 Anchor가 호출하는 JS package-manager install 경계는 그 자체로 중요한 신뢰 경계다.
- **핵심 패턴**: older/unhardened Anchor workflow가 `yarn`/`yarn install` 을 `--frozen-lockfile` 없이 호출하면, 이미 허용된 semver range 안의 새 transitive 버전이 routine build/test/scaffold 실행 중 조용히 들어올 수 있다. 공격자는 개발자에게 노골적인 새 package를 추가시키지 않아도 된다.
- **왜 Solana에서 특히 위험한가**:
  1. Anchor client generation/test가 deploy wallet, local validator, TS SDK, `.env` 와 같은 호스트에서 같이 돈다.
  2. generated client artifact가 바뀌어도 리뷰 초점이 주로 Rust instruction logic에 쏠려 JS 쪽 drift를 놓치기 쉽다.
  3. localnet/devnet 운영자는 `anchor test` 를 반복 실행하므로 "한 번의 unfrozen install" 이 반복적 노출면이 된다.
- **Source signals**:
  - Anchor commit `4b8f0e0` (`fix: enforce --frozen-lockfile for yarn install calls (#4228)`, 2026-04-16)
- **Microstable current status**:
  - `Anchor.toml` 에 `package_manager = "yarn"` 존재
  - `package.json` 에 `@coral-xyz/anchor = ^0.31.1`, `@solana/spl-token = ^0.4.9`
  - `yarn.lock` 존재. 즉 lockfile은 있으나, install 경계가 immutable인지가 별도 문제다.
  - 따라서 **ACTIVE LATENT today** — 직접 compromise 증거는 없지만, toolchain discipline failure가 있으면 builder path가 노출된다.
- **Checklist item 64**: ☐ Anchor가 호출하는 package-manager 경로(`anchor test`, workspace/client scaffold 포함)는 반드시 immutable install(`--frozen-lockfile` 또는 동등 정책)로 고정하고, build/test 중 `yarn.lock` 변화가 생기면 실패 처리할 것

### Solana-Specific Defense Checklist Update
64. ☐ Anchor가 호출하는 package-manager 경로(`anchor test`, workspace/client scaffold 포함)는 반드시 immutable install(`--frozen-lockfile` 또는 동등 정책)로 고정하고, build/test 중 `yarn.lock` 변화가 생기면 실패 처리할 것

---
<!-- AUTO-ADDED 2026-04-20 (Red Team Daily Evolution) — A117 signer-downgrade serialization -->

## 2026-04-20 Anchor Nested Signer-Downgrade Pattern

### A117 — Anchor Composite AccountMeta Signer-Override Drop / Privilege Downgrade Bypass
- **Solana context**: Solana에서는 proxy / adapter / aggregator / keeper helper가 외부 instruction을 조립할 때 `AccountMeta.is_signer` 를 의도적으로 낮춰서 권한을 축소하는 경우가 있다. 이때 팀은 `to_account_metas(Some(false))` 같은 helper 호출을 "권한 제거 완료" 의 증거로 오해하기 쉽다.
- **핵심 패턴**: old Anchor generated code는 composite/nested account struct에 signer override를 끝까지 전파하지 못해, 호출부가 명시적으로 signer를 꺼도 중첩 계정에서는 signer bit가 살아남을 수 있다. 즉, **권한 전달 자체가 아니라 권한 제거가 실패** 한다.
- **왜 Solana에서 특히 위험한가**:
  1. Solana CPI는 signer bit가 외부 프로그램 branch 조건에 직접 쓰이므로, 한 번 새면 영향이 즉시 권한 오남용으로 이어진다.
  2. proxy/remaining-accounts forwarding은 지갑·router·keeper·adapter 패턴에서 자주 생기지만, 감사는 대개 on-chain 비즈니스 로직에 집중해 meta serialization 경계를 얕게 본다.
  3. nested account struct에서만 드러날 수 있어, 단순 happy-path 테스트로는 놓치기 쉽다.
- **Source signals**:
  - Anchor commit `55daadb` (`fix: Client is_signer usage in to_account_metas (#3322)`, 2026-04-15)
  - upstream regression test added a `proxy` path where `.to_account_metas(Some(false))` should clear signer but old behavior failed on nested forwarding
- **Microstable current status**:
  - `programs/microstable/Cargo.toml` = `anchor-lang 0.31.1`, `anchor-spl 0.31.1`
  - `keeper/Cargo.toml` = `anchor-client 0.31.1`
  - reviewed `programs/microstable/src/lib.rs` / `keeper/src/` did **not** show `declare_program!`, `to_account_metas`, or generic proxy/meta-forwarding usage
  - 따라서 **NOT ACTIVE today**. 다만 future router/adapter/proxy path에서는 즉시 재평가해야 한다.
- **Checklist item 65**: ☐ external CPI / proxy / adapter 경로에서 signer downgrade를 의도한다면 `to_account_metas(Some(false))` 호출 자체를 믿지 말고, composite/nested accounts 포함 최종 `AccountMeta.is_signer` 결과를 regression test로 고정할 것

### Solana-Specific Defense Checklist Update
65. ☐ external CPI / proxy / adapter 경로에서 signer downgrade를 의도한다면 `to_account_metas(Some(false))` 호출 자체를 믿지 말고, composite/nested accounts 포함 최종 `AccountMeta.is_signer` 결과를 regression test로 고정할 것

---
<!-- AUTO-ADDED 2026-04-22 (Red Team Daily Evolution) — D52 parser ambiguity collision -->

## 2026-04-22 Anchor Parser Account-Group Collision Pattern

### D52 — Anchor Composite Account-Group Name Collision / Instruction Parser Ambiguity Smuggle
- **Solana context**: Solana 팀은 IDL / generated account schema / instruction parser 출력을 대개 "툴링 산출물" 로 보고 내부 일관성 검증을 약하게 둔다. 하지만 Anchor의 composite account-group dedup 버그는, 위조 metadata 없이도 **generated parser input 내부에 duplicate group identity** 를 남겨 off-chain parser/client/policy layer를 오도할 수 있음을 보여준다.
- **핵심 패턴**: vulnerable de-duplicator가 composite group을 이전 composite들과만 비교하고 top-level instruction account entry와는 비교하지 않으면, 같은 generated name 또는 사실상 같은 account-group definition이 최종 출력에 중복으로 남을 수 있다. 이후 instruction parser나 generated client가 이를 first-wins/last-wins 식으로 해석하면, 운영자는 한 계정 스키마를 본다고 생각하지만 실제 도구는 다른 group을 기준으로 parse/validate/sign 할 수 있다.
- **왜 Solana에서 특히 위험한가**:
  1. Solana는 account ordering, signer, writable semantics가 조금만 바뀌어도 완전히 다른 의미가 된다.
  2. 많은 팀이 on-chain logic보다 generated client / dashboard / validation helper를 더 자주 직접 만진다.
  3. 사고가 나도 runtime은 정상이라, parser plane ambiguity를 늦게 발견하기 쉽다.
- **Source signals**:
  - Anchor commit `df44381` (`fix name collision in composite account de-duplicator (#4401)`, 2026-04-21)
  - upstream note: duplicate names / duplicate account-group definitions can cause ambiguous parsing or duplicate generated items in final output
- **Microstable current status**:
  - `package.json` = `@coral-xyz/anchor ^0.31.1`
  - tests use `target/types/microstable` and `anchor.workspace.microstable`
  - current repo scan did **not** show Anchor 1.0 parser migration or composite parser-heavy client path
  - 따라서 **NOT ACTIVE today**, but future Anchor parser/client upgrade should treat generated schema diff as a release gate.
- **Checklist item 66**: ☐ Anchor parser/client migration 시 emitted account-group namespace에 duplicate name/layout alias가 없는지 lint 하고, old/new parser 결과를 동일 instruction corpus로 diff 하여 account ordering·mutability·signer semantics drift를 차단할 것

### Solana-Specific Defense Checklist Update
66. ☐ Anchor parser/client migration 시 emitted account-group namespace에 duplicate name/layout alias가 없는지 lint 하고, old/new parser 결과를 동일 instruction corpus로 diff 하여 account ordering·mutability·signer semantics drift를 차단할 것

---
<!-- AUTO-ADDED 2026-04-26 (Red Team Daily Evolution) — D53 recursive DNS sibling-zone cache poisoning -->

## 2026-04-26 Recursive DNS Resolver Trust-Boundary Pattern

### D53 — Recursive DNS Sibling-Zone NS Cache Poisoning / Parent-Pool Zone-Context Elevation
- **Solana context**: Solana keeper / oracle fetcher / bridge watcher / dashboard backend는 `rpc_url`, `secondary_rpc_url`, `hermes_url`, 가격 API host allowlist를 두면 충분하다고 느끼기 쉽다. 하지만 hostname allowlist 앞단의 recursive resolver가 authority delegation을 잘못 cache하면, 팀이 같은 URL을 계속 쓰더라도 실제 질의는 공격자 authoritative nameserver로 흘러갈 수 있다.
- **핵심 패턴**: 취약한 Hickory recursor 계열은 AUTHORITY section NS record를 record owner key 기준으로 cache하면서, 그 유효성 검사를 실제 query zone이 아니라 parent NS-pool zone context에 걸었다. 그 결과 `attacker.poc.` 응답 하나로 `victim.poc.` 의 NS cache를 오염시켜 이후 victim zone 질의를 공격자 nameserver로 유도할 수 있다.
- **왜 Solana에서 특히 위험한가**:
  1. RPC / oracle / attestation host는 대개 allowlist로만 관리되고, DNS authority drift 자체는 runtime에서 거의 보지 않는다.
  2. 많은 팀이 multi-RPC를 구성해도 resolver plane은 단일 로컬 DNS path를 공유해, failover가 있어도 같은 poisoned resolution plane에 묶일 수 있다.
  3. 사고가 나면 endpoint config는 바뀌지 않았기 때문에 운영자는 provider outage나 TLS 문제로 오진하기 쉽다.
- **Source signals**:
  - RustSec `RUSTSEC-2026-0106` / `GHSA-83hf-93m4-rgwq` (2026-04-22)
- **Microstable current status**:
  - `solana/Cargo.lock` / keeper 의존성 스캔에서 `hickory`, `hickory-recursor`, `trust-dns` 미발견
  - 현재 keeper는 `reqwest`, `solana-client`, 시스템 DNS 해석 경로를 쓰며 custom recursive resolver / local DNS sidecar 흔적이 없다
  - 따라서 **NOT ACTIVE today**
  - 다만 향후 RPC/oracle failover 앞단에 Rust-native resolver 또는 sidecar recursor를 붙이면 즉시 재평가해야 한다
- **Checklist item 67**: ☐ keeper / dashboard / bridge watcher가 local recursive DNS resolver를 쓰면 sibling-zone AUTHORITY poisoning 회귀 테스트를 넣고, security-critical hostname의 authoritative NS drift를 모니터링하며, multi-RPC도 resolver monoculture 없이 독립 해석 경로를 둘 것

### Solana-Specific Defense Checklist Update
67. ☐ keeper / dashboard / bridge watcher가 local recursive DNS resolver를 쓰면 sibling-zone AUTHORITY poisoning 회귀 테스트를 넣고, security-critical hostname의 authoritative NS drift를 모니터링하며, multi-RPC도 resolver monoculture 없이 독립 해석 경로를 둘 것

---
<!-- AUTO-ADDED 2026-04-28 (Red Team Daily Evolution) — A119 immutable legacy package -->

## 2026-04-28 Legacy Program Migration / Shared-PDA Version-Gate Pattern

### A119 — Immutable Legacy Package / Shared-State Version-Gate Bypass
- **Solana context**: Solana는 같은 program ID 업그레이드라면 예전 바이너리를 직접 다시 호출하는 Scallop형 surface가 상대적으로 작다. 그러나 팀이 rewards / bridge / sidecar / migration을 **새 program ID** 로 분리하고, old/new program이 같은 PDA, vault ATA, mint authority, reward state를 계속 공유하면 문제가 다시 생긴다. 예전 program ID는 여전히 callable인데, 운영팀은 UI/SDK가 새 program만 쓰니 retired 되었다고 착각할 수 있다.
- **핵심 패턴**: deprecated program / sidecar / helper가 live shared PDA나 vault authority에 대한 write 권한을 유지한 채 남아 있고, 그 legacy path 안의 오래된 invariant bug나 약한 auth check가 현재 자산 상태에 그대로 영향을 준다. 즉 retire된 것은 사용자 경로뿐이고, **권한은 retire되지 않은 상태** 다.
- **왜 Solana에서 특히 위험한가**:
  1. migration 과정에서 "새 program 배포 + old UI 차단" 을 완료로 착각하기 쉽지만, old program authority revoke / PDA rebind / vault owner migration은 별도 작업이다.
  2. Solana는 PDA, token account authority, upgrade authority가 분리돼 있어, 새 코드로 갈아탔어도 shared state write-capability가 남을 수 있다.
  3. reward sidecar / bridge helper / attestation program은 core program보다 감사 강도가 낮기 쉬워 legacy surface가 오래 남는다.
- **Source signals**:
  - Scallop / sSUI rewards incident write-ups (incident 2026-04-26, mechanism public 2026-04-27)
- **Microstable current status**:
  - `programs/microstable/src/lib.rs` 에서 단일 `declare_id!` program path 확인
  - 현재 repo scan에서 retired parallel program ID, 별도 rewards sidecar, old program that still writes the same live shared state 흔적은 확인되지 않음
  - 따라서 **NOT ACTIVE today**
  - 다만 향후 auxiliary program migration이 생기면 shared PDA/vault authority가 반드시 active program binding을 갖는지 재평가 필요
- **Checklist item 68**: ☐ program migration을 새 program ID로 수행할 때는 shared PDA / vault / mint authority에 `active_program_id` 또는 동등한 version gate를 두고, retired program의 write 권한을 revoke or migrate 완료하기 전에는 "deprecated" 로 분류하지 말 것

### Solana-Specific Defense Checklist Update
68. ☐ program migration을 새 program ID로 수행할 때는 shared PDA / vault / mint authority에 `active_program_id` 또는 동등한 version gate를 두고, retired program의 write 권한을 revoke or migrate 완료하기 전에는 "deprecated" 로 분류하지 말 것
